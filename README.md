# Tiny Chef

A simple toy system for the 2023 exam of the course PA1417 Basic System Verification at BTH. It currently consists of a backend implemented in Flask and is connected to a MongoDB database. A frontend is anticipated according to the requirements, but not yet implemented.

## Structure

This repository is structured as follows:

* [backend](./backend/): Directory containing the backend
  * [src](./backend/src/): Source code of the backend
  * [test](./backend/test/): Location for all test files
  * .env: Environment variables
  * [Dockerfile](./backend/Dockerfile): Definition of a docker image
  * [main.py](./backend/main.py): Main starting point of the backend, to be started with `python -m main`
  * [pytest.ini](./backend/pytest.ini): Pytest configuration
  * [requirements.txt](./backend/requirements.txt): Libraries required by the backend, to be installed via `pip install -r requirements.txt`
* [documentation](./documentation/): Markdown-files containing the context and requirements specification.
  * [context-specification.md](./documentation/context-specification.md): The context of the system, describing *why* the system needs to be achieved.
  * [requirements-specification.md](./documentation/requirements-specification.md): The requirements of the system, describing *what* needs to be achieved.

## Using the System

While not essential for the PA1417 exam, you can [setup](#setup) and [run](#accessing-the-system) the system to familiarize yourself with its functionality.

### Setup

To set up the system, you have two choices: you can either [run the system locally](#local-setup) or run the dockerized version.

#### Local Setup

Make sure that [Python 3.10](https://www.python.org/downloads/release/python-3100/) and [MongoDB](https://www.mongodb.com/try/download/community) are available on your system. Then, perform the following steps for preparation:

1. Make sure that the data base path *data\db* exists in the root folder of this repository.
2. Install the requirementens in the *backend* folder by running `python -m pip install -r requirements.txt`. 

Finally, get the system running with the following commands (each executed in its own shell):

1. To start the data base, run `mongod --port 27017 --dbpath data\db` from the root folder in a console **with admin rights** (make sure that the direction of the slashes matches your operating system).
2. To start the the server, run `python -m main` from the *backend* folder.

#### Dockerized Setup

Make sure that [Docker](https://docs.docker.com/get-docker/) is available on your system. Then, perform the following steps:

1. With Docker Desktop running, execute `docker-compose up` from the root folder in a console **with admin rights**.

### Accessing the System

Once the system is running, you can interact with it for example using [Postman](https://www.postman.com/downloads/). Verify that the system is running by executing `GET http://localhost:5000/` which should return a heartbeat in the form of a version string `{ "version" : "v0.5.0" }`.

The database stores **pantry items**, which you can view via `GET http://localhost:5000/items/all`. At the beginning, the database is empty and this REST call should return an empty array `[]`. Populate the database by running `POST http://localhost:5000/populate`, which will take [the dummy data](./backend/src/static/dummy_items/) and adds them to the database. Now, `GET http://localhost:5000/items/all` should list several items. You can create further items via `POST http://localhost:5000/items/create`, where the *body must contain the name, quantity, and unit field*.

Finally, you can explore the main functionality of the system by running `GET http://localhost:5000/receipes` (containing the *diet* and *usage_mode* fields in the body as specified in [the method description](./backend/src/blueprints/receipeblueprint.py)), which generates a random receipe. For example, calling the aforementioned request with `diet = normal` and `usage_mode = optimal` should - if the populate function had been run - return a receipe for *banana bread*, while changing `diet = vegan` should return a receipe for *whole grain bread*.

You can retrace the database by connecting to it using [MongoDB Compass](https://www.mongodb.com/try/download/compass). Connect on the url `mongodb://localhost:27017/` (if you are using a [local setup](#local-setup)) or `mongodb://root:root@localhost:27017/` (if you are using a [dockerized setup](#dockerized-setup)). In the *tinychef* database, you will find the *item* collection, where all the items are stored.
