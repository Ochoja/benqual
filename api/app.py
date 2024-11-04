from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import os
import json
from api.utils import Utils  # Ensure that utils.py is in the api folder

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

Utils = Utils()  # Instantiate the Utils class

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(file):
    """Uploads file to the uploads folder"""
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 200  # File saved successfully
    else:
        return 400  # Invalid file type

@app.route("/api/benford_test/upload/", methods=['POST'])
def benford_test_file():
    """Get expected and actual values"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    status = upload_file(file)  # Upload file and return status

    if status == 200:
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        column = request.form.get('column')

        try:
            if filename.endswith('.csv'):
                data = Utils.extract_csv_values(filename, column)
            else:
                data = Utils.extract_excel_values(filename, column)

            values = Utils.get_number_pool(data)
            actual_percentages = Utils.get_digit_percentages(values)
            expected_percentages = Utils.get_expected_percentages()
            p_value, chi2_stat = Utils.get_p_value(values)
            
            # Compute KS Statistic and MAD
            ks_statistic, ks_p_value = Utils.get_ks_test(values)
            mad = Utils.get_mad(values)

            os.remove(filename)  # Delete the file
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
            os.remove(filename)  # Delete the file in case of error
            return jsonify({'error': 'Invalid column name or values', 'details': str(e)}), 400

@app.route("/api/benford_test/")
def benford_test():
    data = request.args.get('data')

    try:
        data = json.loads(data)
        if not isinstance(data, list):
            raise ValueError("Data is not a list")
        
        values = Utils.get_number_pool(data)
        actual_percentages = Utils.get_digit_percentages(values)
        expected_percentages = Utils.get_expected_percentages()
        p_value, chi2_stat = Utils.get_p_value(values)
        
        # Compute KS Statistic and MAD
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
    app.run(debug=True)  # Make sure to have this to run the app
