import RPi.GPIO as GPIO
import Adafruit_DHT
import time
from flask import Flask, render_template, request

app = Flask(__name__)

GPIO.setmode(GPIO.BOARD)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
    21: {'name': 'WATER', 'state': GPIO.LOW},
    33: {'name': 'Green Top', 'state': GPIO.LOW},
    35: {'name': 'Red Down', 'state': GPIO.LOW},
    37: {'name': 'Green Down', 'state': GPIO.LOW}
}

# Set each pin as an output and make it low:
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

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


@app.route("/")
def led():
    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
    # Put the pin dictionary into the template data dictionary:
    templateData = {
        'pins': pins
    }
    # Pass the template data into the template led.html and return it to the user
    return render_template('led.html', **templateData)


# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
    # Convert the pin from the URL into an integer:
    changePin = int(changePin)
    # Get the device name for the pin being changed:
    deviceName = pins[changePin]['name']
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

    time.delay(1)
    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

    # Along with the pin dictionary, put the message into the template data dictionary:
    templateData = {
        'message': message,
        'pins': pins
    }

    return render_template('led.html', **templateData)


@app.route("/soil")
def soil():
    templateData = {
        'sensors': sensors
    }
    return render_template('soil.html', **templateData)

@app.route("/water")
def water():
    if GPIO.input(21) == GPIO.LOW:
        GPIO.output(21, GPIO.HIGH)
    else:
        GPIO.output(21, GPIO.LOW)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
