# Approach
Tecnical test I have made back in the days applying ddd + hexagonal/clean architecture. It's build with Flask (python) and Angular.

# Spec
This application retrieves measurement data of an electric device from a file. It then queries an electricity cost API to determine the cost associated with the device over time. Finally, the application plots this data on the client side.

## Install it and run it
### Backend
Python version
> 3.10.6

Python virutal env
> cd backend && python -m venv env && source env/bin/activate

Install libs
> env/bin/pip3 install -r requirements.txt

Run app
> PYTHONPATH=`pwd`/src env/bin/python3 src/consume/infrastructure/entrypoints/app_flask.py

Config file
> backend/src/config.py

<i>POWER_MEASUREMENTS_FILE the path of measurements json</i>

Test 
>PYTHONPATH=`pwd`/src pytest

### Frontend
Node version
> v19.8.1

Install deps
> cd frontend && npm i 

Run it
> npm start
