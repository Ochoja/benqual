from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/api/check_probability", methods=['GET', 'POST'])
def check_probability():
    """Get expected and actual values"""
    expected_values = {1: 0.301, 2: 0.176, 3: 0.125, 4: 0.097,
                       5: 0.079, 6: 0.067, 7: 0.058, 8: 0.051, 9: 0.046}
    return jsonify(expected_values)
