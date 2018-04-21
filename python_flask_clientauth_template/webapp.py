import click
from flask import Flask, jsonify, request
from pathlib import Path
import logging as log
from voluptuous import MultipleInvalid
import arrow
import yaml
import psycopg2
from psycopg2.sql import SQL, Literal
from psycopg2.extras import NamedTupleCursor

from .utils import package_path
from .client_auth_app import ClientAuthApplication
from .validation import config_schema, InvalidInput

MY_PATH = Path(__file__)
PACKAGE_PATH = package_path(MY_PATH)


# Global logging configuration
LOG_LEVEL = {'CRITICAL': log.CRITICAL, 'ERROR': log.ERROR, 'WARNING': log.WARNING, 'INFO': log.INFO,
             'DEBUG': log.DEBUG, 'NOTSET': log.NOTSET}
log.basicConfig(format='%(levelname)s - %(module)s.%(funcName)s - [%(asctime)s]: %(message)s')


def configure_logging(log_level: str):
    log.getLogger().setLevel(LOG_LEVEL[log_level])


def load_configuration_or_die(config_path: Path):
    """Loads configuration and validates it or exits the application."""
    log.info("Loading configuration: %s", str(config_path))
    config_data = yaml.load(config_path.open('r'))
    try:
        config_schema(config_path)(config_data)
    except MultipleInvalid as exc:
        log.critical("Cannot load config from %s: %s", str(config_path), str(exc))
        exit(2)
    log.debug("Configuration loaded successfully: %s", str(config_path))
    return config_data


def configure_app(app, config):
    app.config.update(
        DB_HOSTNAME=config['database']['hostname'],
        DB_USERNAME=config['database']['username'],
        DB_PASSWORD=config['database']['password'],
        DB_PORT=config['database']['port'],
        DB_NAME='example' if 'db-name' not in config['database'] else config['database']['db-name']
    )
    return app


# Queries
SHA_512_EXISTS = SQL("SELECT EXISTS(SELECT 1 FROM passwords.account_passwords WHERE passwd_hash={0})")


APP = Flask(__name__)


@APP.errorhandler(InvalidInput)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def api_v0_1(route):
    return '/api/v0.1/{}'.format(route)


def with_metadata(data):
    return {'metadata': {'timestamp': arrow.utcnow().timestamp},
            'data': data}


@APP.route(api_v0_1('hello'), methods=['GET', 'POST'])
def hello():
    """Hello world endpoint"""
    return jsonify(with_metadata("Hello, world!"))


@APP.route(api_v0_1('headers'))
def headers():
    """Basic function"""
    return jsonify(with_metadata({'X-USER': request.headers['X-USER'],
                                  'X-ISSUER': request.headers['X-ISSUER'],
                                  'X-NOT_BEFORE': request.headers['X-NOT_BEFORE'],
                                  'X-NOT_AFTER': request.headers['X-NOT_AFTER']}))


# @APP.route(api_v0_1('is_password_known/<sha512>'), methods=['GET'])
# def is_password_known(sha512: str):
#     """Look up the SHA512 in the database and return True if it exists"""
#     try:
#         SHA512_SCHEMA(sha512)
#     except MultipleInvalid as e:
#         raise InvalidInput(e.msg)
#
#     with psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'"
#                           .format(APP.config['DB_NAME'],
#                                   APP.config['DB_USERNAME'],
#                                   APP.config['DB_HOSTNAME'],
#                                   APP.config['DB_PASSWORD'])) as conn:
#         with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
#             cursor.execute(SHA_512_EXISTS.format(Literal(sha512)))
#             result = cursor.fetchone()
#             return jsonify(known_password_reply(sha512, result.exists))


# @APP.route(api_v0_1('search/account/<account_name>'))
# def search_account_name(account_name: str):
#     """Look up a specific account substring in the database and return all entries. WARNING: This function is dangerous.
#        Can be used to search for people's passwords. Control access to it very tightly."""
#     pass


# @APP.route(api_v0_1('search/password/<password>'))
# def search_password_name(password: str):
#     """Look up a specific password substring in the database and return all entries. WARNING: This function is dangerous.
#        Can be used to search for people's passwords. Control access to it very tightly."""
#     pass


@click.command()
@click.option('-c', '--config-path', default=Path.cwd() / 'config.yaml', help='Path to the configuration file')
@click.option('-l', '--log-level', default=None, type=click.Choice(LOG_LEVEL.keys()),
              help='Logging level for the application, overrides the configuration.')
def run_app_server(config_path, log_level):
    """Launches REST API (without client authentication) in a gunicorn server"""
    # Set logging if its given on the commandline
    if log_level is not None:
        configure_logging(log_level=log_level)
    # Load the configuration
    config = load_configuration_or_die(Path(config_path))
    # Otherwise use the logging configuration from the config file once its loaded
    if log_level is None:
        configure_logging(config['webapp']['log-level'])

    ca_path = Path(config['server']['ca-cert'])
    cert_path = Path(config['server']['cert'])
    key_path = Path(config['server']['key'])
    port = config['webapp']['port']
    hostname = None if 'hostname' not in config['server'] else config['webapp']['hostname']
    timeout= None if 'timeout' not in config['server'] else config['webapp']['timeout']
    num_workers = None if 'hostname' not in config['server'] else config['webapp']['hostname']

    configure_app(APP, config)
    ClientAuthApplication(APP, ca_path, cert_path, key_path, port=port,
                          hostname=hostname, timeout=timeout, num_workers=num_workers).run()


if __name__ == '__main__':
    run_app_server()
