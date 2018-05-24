import RPi.GPIO as GPIO
import Adafruit_DHT
import time
from flask import Flask, render_template, redirect, url_for, request

import water_module as water

app = Flask(__name__)

actions = {}
sensors = {}
app.logger.info('actions, sensors instantiated')
GPIO.setmode(GPIO.BOARD)

def actionsInit():
    # Create a dictionary called pins to store the pin number, name, and pin state:
    actions = {
        32: {'name': 'Red Top', 'state': GPIO.LOW},
        33: {'name': 'Green Top', 'state': GPIO.LOW},
        35: {'name': 'Red Down', 'state': GPIO.LOW},
        37: {'name': 'Green Down', 'state': GPIO.LOW}
    }
    app.logger.info('%s sized actions created', len(actions))
    # Set each pin as an output and make it low:
    for action in actions:
        GPIO.setup(action, GPIO.OUT)
        GPIO.output(action, GPIO.LOW)
        # For each pin, read the pin state and store it in the pins dictionary:    for action in actions:
        actions[action]['state'] = GPIO.input(action)

    app.logger.info('action gpios are setup and low')
    return actions


def sensorsInit():
    sensors = {
        17: {'name': 'DHT 22', 'humidity': '', 'temperature': ''},
        18: {'name': 'DHT 11', 'humidity': '', 'temperature': ''},
    }

    sensor = Adafruit_DHT.DHT22
    sensor2 = Adafruit_DHT.DHT11

    pin = 17
    pin2 = 27

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    humidity2, temperature2 = Adafruit_DHT.read_retry(sensor2, pin2)

    sensors = {
        1: {'humidity': humidity, 'temperature': temperature},
        2: {'humidity': humidity2, 'temperature': temperature2},
    }
    return sensors


@app.route("/")
def root():
    return redirect(url_for('led'))


@app.route("/led")
def led():
    app.logger.info('-> led page')
    actions = actionsInit()

    print('½s actions gotten', actions)
    # Put the pin dictionary into the template data dictionary:
    templateData = {
        'actions': actions
    }
    # Pass the template data into the template led.html and return it to the user
    return render_template('led.html', **templateData)


# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
    app.logger.info('change pin')
    # Convert the pin from the URL into an integer:
    changePin = int(changePin)
    # Get the device name for the pin being changed:
    deviceName = actions[changePin]['name']
    # If the action part of the URL is "on," execute the code indented below:
    if action == "on":
        # Set the pin high:
        GPIO.output(changePin, GPIO.HIGH)
        # Save the status message to be passed into the template:
        message = "Turned " + deviceName + " on."
    if action == "off":
        GPIO.output(changePin, GPIO.LOW)
        message = "Turned " + deviceName + " off."
    if action == "toggle":
        # Read the pin and set it to whatever it isn't (that is, toggle it):
        GPIO.output(changePin, not GPIO.input(changePin))
        message = "Toggled " + deviceName + "."

    time.sleep(1)
    # For each pin, read the pin state and store it in the pins dictionary:
    for actionPin in actions:
        actions[actionPin]['state'] = GPIO.input(actionPin)

    # Along with the pin dictionary, put the message into the template data dictionary:
    templateData = {
        'message': message,
        'pins': actions
    }

    return render_template('led.html', **templateData)


@app.route("/water/<second>", methods=['post', 'get'])
def water(second):
    app.logger.info('water plants')
    # Convert the pin from the URL into an integer:
    if request.method == 'POST':
        second = request.form.get('second')  # access the data inside
        second = int(second)
        app.logger.info('-> water request second %s', second)


    # Get the device name for the pin being changed:
    app.logger.info('watering')
    response = water.openInterval(second)
    app.logger.info('watering done')

    sensorsInit()
    templateData = {
        'sensors': sensors
    }
    return render_template('soil.html', **templateData)


@app.route("/soil")
def soil():
    sensors = sensorsInit()
    print('½s actions gotten', sensors)
    templateData = {
        'sensors': sensors
    }
    return render_template('soil.html', **templateData)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'