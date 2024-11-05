from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import os
import json
from api.utils import Utils

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

Utils = Utils()  # Instantiate the Utils class

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/api/benford_test/")
def benford_test():
    data = request.args.get('data')

    if not data:
        return jsonify({'error': 'Missing data parameter', 'details': 'The data parameter is required and must be a JSON array'}), 400

    try:
        # Parse the data as a JSON array
        data = json.loads(data)
        if not isinstance(data, list):
            raise ValueError("Data is not a list")

        # Use the data directly
        values = data  # No need to use get_number_pool

        # Use the existing count_digits method for analysis
        observed_counts = Utils.count_digits(values)
        total_observed = sum(observed_counts.values())
        actual_percentages = {digit: count / total_observed for digit, count in observed_counts.items()}
        expected_percentages = Utils.get_expected_percentages()
        p_value, chi2_stat = Utils.get_p_value(values)

        # Compute KS Statistic and MAD using existing methods
        ks_statistic, ks_p_value = Utils.get_ks_test(values)
        mad = Utils.get_mad(values)

        return jsonify({
            'actual_percentages': actual_percentages,
            'expected_percentages': expected_percentages,
            'p-value': p_value,
            'chi2_stat': chi2_stat,
            'ks_statistic': ks_statistic,
            'ks_p_value': ks_p_value,
            'mad': mad
        })
    except Exception as e:
        return jsonify({'error': 'Invalid parameter or format', 'details': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
