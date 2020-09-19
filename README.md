# gametime

## overview

all of the server is contained within the app folder. the flask server is created and configured in `app/__init__.py`. `app/config.py` contains the environment variables and other configuration options for prod, dev, and testing. `.env` contains the actual environment variables that are imported into the config file and is not included in version control. the `api` folder contains blueprints of each the api functionalities. the `db` folder contains blueprints for all of the database interactions.

## dev setup

1. clone the repo
2. download the python extension for vs code
3. create python virtual environment and activate
4. `pip install -r requirements.txt`
5. create `.env` in `app`
6. set `FLASK_APP=app` and `FLASK_ENV=dev` outside of `.env`

## issues

- importing api in `app/__init_.py` doesn't work
- importing config in `app/__init__.py` doesn't work
