from flask import Flask
from flask import jsonify
import RPi.GPIO as GPIO

app = Flask(__name__)

LedPin = 32    # pin11

def setup():
        GPIO.setmode(GPIO.BOARD)       # Set the board mode to numbers pins by physical location
        GPIO.setup(LedPin, GPIO.OUT)   # Set pin mode as output
        GPIO.output(LedPin, GPIO.HIGH) # Set pin to high(+3.3V) to off the led

@app.route("/")
def hello():
    return jsonify({'text':'Hello World!'})


@app.route("/led", methods=['GET'])
def ledGet():
    return jsonify({'data': 'read req'})


@app.route("/led", methods=['POST'])
def ledPost():
    print("gpios are setting")
    GPIO.output(LedPin, GPIO.LOW)  # led on
    return jsonify({'data': 'open req!'})


@app.route("/led", methods=['DELETE'])
def ledDelete():
    GPIO.output(LedPin, GPIO.HIGH)  # led off
    GPIO.cleanup()
    return jsonify({'data': 'open req!'})


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)  # Set the board mode to numbers pins by physical location
    GPIO.setup(LedPin, GPIO.OUT)  # Set pin mode as output
    app.debug = True
    app.run(host='0.0.0.0', port=80)
