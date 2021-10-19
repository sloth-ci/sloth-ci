# Welcome to Sloth CI!

[![image](https://img.shields.io/pypi/v/sloth-ci.svg)](https://pypi.org/project/sloth-ci)
[![Build Status](https://travis-ci.com/Sloth-CI/sloth-ci.svg?branch=develop)](https://travis-ci.com/Sloth-CI/sloth-ci)


**Sloth CI** is a lightweight, standalone CI server.

Via extensions, Sloth CI offers detailed logs, build status badges, email notifications, and webhooks. 


## Run Locally

Deploy the project with Poetry:

    $ poetry install

Run locally with:

    $ poetry run sci start

Check that the instance is running:

    $ poetry run sci status

Build the docs:

    $ poetry run foliant make site -p docs

