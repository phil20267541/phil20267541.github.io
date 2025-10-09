from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Backend is running!"})

@app.route('/api/data')
def data():
    return jsonify({"data": [1, 2, 3, 4, 5]})

if __name__ == '__main__':
    app.run()
