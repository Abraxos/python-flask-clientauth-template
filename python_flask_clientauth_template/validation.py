from os import access, R_OK
from functools import partial
from pathlib import Path
from voluptuous import Schema, Invalid, Required, Optional, Any


class InvalidInput(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code if status_code is not None else self.status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def existing_readable_file(path: str, relative_to: Path=None) -> bool:
    path = (Path('/') / path) if not relative_to else (relative_to / path)
    if not path.exists():
        raise Invalid('Path does not exist: {}'.format(path))
    if not path.is_file():
        raise Invalid('Not a file: {}'.format(path))
    if not access(str(path), R_OK):
        raise Invalid('No read access to: {}'.format(path))
    return True


def config_schema(relative_to: Path=None):
    if relative_to is not None:
        exists = partial(existing_readable_file, relative_to)
    else:
        exists = existing_readable_file
    return Schema({
        Required('server'): {
            Required('ca-cert'): exists,
            Required('cert'): exists,
            Required('key'): exists,
            Optional('hostname'): str,
            Optional('timeout'): int,
            Optional('num-workers'): int
        },
        Required('database'): {
            Required('host'): str,
            Required('port'): int,
            Required('username'): str,
            Required('password'): str
        },
        Optional('webapp'): {
            Optional('log-level'): Any('CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG')
        }
    })
