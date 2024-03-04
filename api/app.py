from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/api/check_probability", methods=['GET', 'POST'])
def check_probability():
    """Get expected and actual values"""
    return jsonify()
