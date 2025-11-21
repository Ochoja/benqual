from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from api.utils import Utils
from api.validators import DataValidator

app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:5173",
            "https://benqual.netlify.app"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

utils = Utils()
validator = DataValidator()


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/api/validate_dataset/", methods=['GET', 'POST'])
def validate_dataset():
    """Validate dataset and detect missing values"""
    if request.method == 'GET':
        data = request.args.get('data')
    else:
        data = request.form.get('data') or (
            request.get_json() or {}).get('data')

    if not data:
        return jsonify({'error': 'Missing data parameter', 'details': 'The data parameter is required and must be a JSON array'}), 400

    try:
        data = json.loads(data)
        if not isinstance(data, list):
            raise ValueError("Data is not a list")

        quality_report = DataValidator.generate_quality_report(data)

        return jsonify({
            'status': 'success',
            'data_quality': quality_report['summary'],
            'missing_values': quality_report['missing_values'],
            'invalid_values': quality_report['invalid_values'],
            'issues': quality_report['issues'],
            'ready_for_analysis': quality_report['summary']['ready_for_analysis']
        })
    except Exception as e:
        return jsonify({'error': 'Validation failed', 'details': str(e)}), 400


@app.route("/api/benford_test/", methods=['GET'])
def benford_test():
    """Perform Benford's Law analysis with automatic missing value handling"""
    data = request.args.get('data')
    skip_validation = request.args.get(
        'skip_validation', 'false').lower() == 'true'

    if not data:
        return jsonify({'error': 'Missing data parameter', 'details': 'The data parameter is required and must be a JSON array'}), 400

    try:
        data = json.loads(data)
        if not isinstance(data, list):
            raise ValueError("Data is not a list")

        if not skip_validation:
            cleaned_data, quality_report = DataValidator.preprocess_for_analysis(
                data)

            if not quality_report['summary']['ready_for_analysis']:
                return jsonify({
                    'error': 'Insufficient valid data',
                    'details': 'Dataset contains no valid numeric records for analysis',
                    'data_quality': quality_report
                }), 400
        else:
            cleaned_data = data
            quality_report = None

        observed_counts = utils.count_digits(cleaned_data)
        total_observed = sum(observed_counts.values())
        actual_percentages = {
            digit: count / total_observed for digit, count in observed_counts.items()}
        expected_percentages = utils.get_expected_percentages()
        p_value, chi2_stat = utils.get_p_value(cleaned_data)

        ks_statistic, ks_p_value = utils.get_ks_test(cleaned_data)
        mad = utils.get_mad(cleaned_data)

        response = {
            'actual_percentages': actual_percentages,
            'expected_percentages': expected_percentages,
            'p-value': p_value,
            'chi2_stat': chi2_stat,
            'ks_statistic': ks_statistic,
            'ks_p_value': ks_p_value,
            'mad': mad,
            'records_analyzed': total_observed
        }

        if quality_report:
            response['data_quality'] = quality_report['summary']
            response['issues'] = quality_report['issues']

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': 'Invalid parameter or format', 'details': str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
