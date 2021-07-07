# Welcome to Sloth CI!

[![image](https://img.shields.io/pypi/v/sloth-ci.svg)](https://pypi.org/project/sloth-ci)


![Logo](sloth.png)


**Sloth CI** is a lightweight, standalone CI server.

Via extensions, Sloth CI offers detailed logs, build status badges, email notifications, and webhooks. 


## Run Locally

Deploy the project with [Poetry](https://python-poetry.org/):
```
$ poetry install
```

Run locally with:
```
$ poetry run sci start
```

Check that the instance is running:
```
$ poetry run sci status
Starting Sloth CI on http://localhost:8080
```

Visit ``http://localhost:8080`` and enter the default username (``admin``) and password (``password``), see: ``sloth.yml``.

Build the docs:
```
$ poetry run sphinx-build sdocs docs/_build/html
```

And open ``docs/_build/html/index.html``.

