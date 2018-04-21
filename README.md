# Python Client-Cert Authenticated Flask Template

A template that I use to create new Flask-based web APIs with client cert authentication. Has examples of how to do basic logging, configuration/input validation, testing, and database access.

## Setup

Since this is a template, my assumption is that it will be used for development only, so this only includes the development setup:

**Setting up the virtualenv**

Install a virtualenv and virtualenvwrapper according to the instructions here:

+ https://virtualenv.pypa.io/en/stable/
+ https://virtualenvwrapper.readthedocs.io/en/latest/

Then execute:

```
mkvirtualenv --python=$(which python3) python-flask-clientauth-template
```

**Installing the Package For Development**

```
(python-flask-clientauth-template) pip install -e /path/to/repo
```

The `-e` installs the package in place for development.

## Configuration

For configuration examples, see the `examples/valid-config.yaml` file, as well as the `load_configuration_or_die()` function in `python_flask_clientauth_template/webapp.py` which uses Voluptuous schema validation to verify that the configuration is valid.

## Database

Coming soon...

## Testing

Testing is done with `pytest`. Here are some useful commands:

Run all tests

```
(python-flask-clientauth-template)$ pytest -s -vv python_flask_clientauth_template/test
```

Run all tests with coverage

```
(python-flask-clientauth-template)$ pytest -s -vv --cov-report=html --cov=python_flask_clientauth_template python_flask_clientauth_template/test
```

Run all the unit tests Right now all the tests are unit tests, but eventually there may be integration tests.

```
(python-flask-clientauth-template)$ pytest -s -vv --cov-report html --cov=python_flask_clientauth_template python_flask_clientauth_template/test/unit
```

Run a specific test

```
(python-flask-clientauth-template)$ pytest -s -vv --cov=python_flask_clientauth_template --cov-report=html python_flask_clientauth_template/test/test_client_cert_auth.py::test_client_auth_with_same_credentials
```