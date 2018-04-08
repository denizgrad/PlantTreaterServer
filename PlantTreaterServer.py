from flask import Flask
from flask import jsonify


app = Flask(__name__)


@app.route("/")
def hello():
    return jsonify({'text':'Hello World!'})

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
