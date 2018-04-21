import pytest
import json

from python_flask_clientauth_template.webapp import APP, api_v0_1


APP.testing = True


def test_hello():
    app = APP.test_client()
    r = json.loads(app.get(api_v0_1('hello')).data, encoding='utf-8')
    assert r['data'] == 'Hello, world!'
