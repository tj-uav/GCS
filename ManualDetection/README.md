# IMU + GUI Demonstration

A basic demonstration on how a device would read from an IMU (inertial measurement unit) and have that data displayed on a user interface.

## Structure

Run _server.py_ on the device which hosts the web server, and _imu.py_ on the device that has the IMU.

## Technologies

-   Python 3.7
    -   [Flask](http://flask.pocoo.org/)
-   JavaScript
    -   [three.js](https://threejs.org/)

## Development

Use `pipenv` to manage the development environment.
More information on `pipenv` available in the [documentation](https://pipenv.readthedocs.io/en/latest/).
If you already have `pipenv` installed, run:

```
pipenv install  # Install dependencies
```

On the device that runs the web server:

```
pipenv run python3 server.py
```

On the device with the IMU:

```
pipenv run python3 imu.py
```
