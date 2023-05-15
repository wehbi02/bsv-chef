# bsv-chef

A simple toy system for the course PA1417 Basic System Verification

## Summary

## Structure

This repository is structured as follows:

* *documentation*: Markdown-files containing the context, requirements and system specification.
  * *context-specification.md*: The context of the system, describing *why* the system needs to be achieved.
  * *requirements-specification.md*: The requirements of the system, describing *what* needs to be achieved.
  * *system-specification.md*: The system specification, describing *how* the system will be achieved.

## Setup

To set up the full system, ensure that you have Python, MongoDB, and NodeJS available on you system. 

1. Make sure that the data base path *data\db* exists in the root folder of this repository.
2. Install the requirementens in the *backend* folder by running `python -m pip install -r requirements.txt`

## Starting the system
 
You can either get the system running by starting all three components individually

### Local 

In three distinct consoles, execute the following commands:

1. In a console **with admin rights** run `mongod --port 27017 --dbpath data\db` from the root folder to start the data base (make sure that the direction of the slashes matches your operating system).
2. In another console, run `python -m main` from the *backend* folder to start the server

### Dockerized

