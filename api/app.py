from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import pandas as pd
import tempfile
from werkzeug.utils import secure_filename

from api.utils import Utils
from api.validators import DataValidator

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "./"
ALLOWED_EXTENSIONS = {"csv", "xls", "xlsx"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

utils = Utils()
validator = DataValidator()


# ----------------------------
# Helpers
# ----------------------------
def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# ----------------------------
# Validate dataset only
# ----------------------------
@app.route("/api/validate_dataset/", methods=["GET", "POST"])
def validate_dataset():
    if request.method == "GET":
        data = request.args.get("data")
    else:
        data = request.form.get("data") or (
            request.get_json() or {}).get("data")

    if not data:
        return jsonify({
            "error": "Missing data parameter",
            "details": "The data parameter must be a JSON array"
        }), 400

    try:
        data = json.loads(data)
        if not isinstance(data, list):
            raise ValueError("Data is not a list")

        quality_report = DataValidator.generate_quality_report(data)

        return jsonify({
            "status": "success",
            "data_quality": quality_report["summary"],
            "missing_values": quality_report["missing_values"],
            "invalid_values": quality_report["invalid_values"],
            "issues": quality_report["issues"],
            "ready_for_analysis": quality_report["summary"]["ready_for_analysis"]
        })
    except Exception as e:
        return jsonify({
            "error": "Validation failed",
            "details": str(e)
        }), 400


# ----------------------------
# Manual Benford test
# ----------------------------
@app.route("/api/benford_test/", methods=["GET", "POST"])
def benford_test():
    if request.method == "GET":
        data = request.args.get("data")
        skip_validation = request.args.get(
            "skip_validation", "false").lower() == "true"

        if not data:
            return jsonify({
                "error": "Missing data parameter",
                "details": "The data parameter must be a JSON array"
            }), 400

        try:
            data = json.loads(data)
        except Exception as e:
            return jsonify({
                "error": "Invalid JSON",
                "details": str(e)
            }), 400
    else:
        json_data = request.get_json()
        if not json_data:
            return jsonify({
                "error": "Missing JSON body"
            }), 400

        data = json_data.get("data")
        skip_validation = json_data.get("skip_validation", False)

        if not data:
            return jsonify({
                "error": "Missing data parameter"
            }), 400

    try:
        if not isinstance(data, list):
            raise ValueError("Data is not a list")

        if not skip_validation:
            cleaned_data, quality_report = DataValidator.preprocess_for_analysis(
                data)

            if not quality_report["summary"]["ready_for_analysis"]:
                return jsonify({
                    "status": "insufficient_data",
                    "data_quality": quality_report["summary"],
                    "missing_values": quality_report["missing_values"],
                    "invalid_values": quality_report["invalid_values"],
                    "issues": quality_report["issues"],
                    "ready_for_analysis": False
                }), 200
        else:
            cleaned_data = data
            quality_report = None

        if len(cleaned_data) == 0:
            return jsonify({
                "status": "no_data",
                "message": "No valid data to analyze",
                "records_analyzed": 0
            }), 200

        # Benford calculations (ALL DIGITS)
        observed_counts = utils.count_digits(cleaned_data)
        total_digits = sum(observed_counts.values())

        actual_percentages = {
            d: c / total_digits for d, c in observed_counts.items()
        }

        expected_percentages = utils.get_expected_percentages()
        p_value, chi2_stat = utils.get_p_value(cleaned_data)
        ks_statistic, ks_p_value = utils.get_ks_test(cleaned_data)
        mad = utils.get_mad(cleaned_data)

        response = {
            "status": "success",
            "actual_percentages": actual_percentages,
            "expected_percentages": expected_percentages,
            "p-value": p_value,
            "chi2_stat": chi2_stat,
            "ks_statistic": ks_statistic,
            "ks_p_value": ks_p_value,
            "mad": mad,
            "records_analyzed": total_digits
        }

        if quality_report:
            response["data_quality"] = quality_report["summary"]
            response["issues"] = quality_report["issues"]

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "error": "Invalid parameter or format",
            "details": str(e)
        }), 400


# ----------------------------
# File upload Benford test
# ----------------------------
@app.route("/api/benford_test/upload/", methods=["POST"])
def benford_test_upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    column = request.form.get("column")

    if not column:
        return jsonify({"error": "Column name is required"}), 400

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(file.filename)
    ext = filename.rsplit(".", 1)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({"error": "Unsupported file type"}), 400

    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            file.save(tmp.name)
            temp_path = tmp.name

        if ext == "csv":
            df = pd.read_csv(temp_path)
        else:
            df = pd.read_excel(temp_path)

        if column not in df.columns:
            return jsonify({
                "error": "Invalid column",
                "details": f"Column '{column}' not found"
            }), 400

        raw_data = df[column].tolist()

        cleaned_data, quality_report = DataValidator.preprocess_for_analysis(
            raw_data)

        if not quality_report["summary"]["ready_for_analysis"]:
            return jsonify({
                "status": "insufficient_data",
                "data_quality": quality_report["summary"],
                "missing_values": quality_report["missing_values"],
                "invalid_values": quality_report["invalid_values"],
                "issues": quality_report["issues"],
                "ready_for_analysis": False
            }), 200

        observed_counts = utils.count_digits(cleaned_data)
        total_digits = sum(observed_counts.values())

        actual_percentages = {
            d: c / total_digits for d, c in observed_counts.items()
        }

        expected_percentages = utils.get_expected_percentages()
        p_value, chi2_stat = utils.get_p_value(cleaned_data)
        ks_statistic, ks_p_value = utils.get_ks_test(cleaned_data)
        mad = utils.get_mad(cleaned_data)

        return jsonify({
            "status": "success",
            "actual_percentages": actual_percentages,
            "expected_percentages": expected_percentages,
            "p-value": p_value,
            "chi2_stat": chi2_stat,
            "ks_statistic": ks_statistic,
            "ks_p_value": ks_p_value,
            "mad": mad,
            "records_analyzed": total_digits,
            "data_quality": quality_report["summary"],
            "issues": quality_report["issues"]
        })

    except Exception as e:
        return jsonify({
            "error": "File processing failed",
            "details": str(e)
        }), 400


# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
