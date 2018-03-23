from flask import Flask
from flask import request
from flask import render_template
from flask import redirect, url_for
import datetime

app = Flask(__name__)



@app.route('/')
def index():
    return datetime.datetime.now()



if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=80)
