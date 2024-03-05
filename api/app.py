from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import os
import json
from api.utils import Utils

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

Utils = Utils()


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/api/benford_test/upload/", methods=['GET', 'POST'])
def benford_test_file():
    """Get expected and actual values"""
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        filename = file.filename
        print(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully'
    else:
        return jsonify({'error': 'Invalid file type'}), 400


@app.route("/api/benford_test/")
def benford_test():
    data = request.args.get('data')

    try:
        data = json.loads(data)
        if type(data) is not list:
            raise Exception
        else:
            values = Utils.extract_first_digits(data)
            actual_percentages = Utils.get_digit_percentages(values)
            expected_percentages = Utils.get_expected_percentages()
            p_value = Utils.get_p_value(values)
    except Exception:
        return jsonify({'error': 'Invalid parameter or format'}), 400

    return jsonify({'actual_percentages': actual_percentages, 'expected_percentages': expected_percentages, 'p-value': p_value})
