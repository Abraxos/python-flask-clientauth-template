from pathlib import Path
from multiprocessing import cpu_count
from python_flask_clientauth_template.utils import package_path, number_of_workers


MY_PATH = Path(__file__)


def test_basics():
    print("Hello, world!")
    assert True


def test_num_workers():
    assert number_of_workers() == (cpu_count() * 2) + 1


def test_file_path():
    assert str(MY_PATH).endswith('python-flask-clientauth-template/'
                                 'python_flask_clientauth_template/test/test_basics.py')


def test_package_path():
    package = package_path(MY_PATH)
    print(package)
    assert str(package).endswith('/python_flask_clientauth_template')