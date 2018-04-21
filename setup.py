"""Setup file for a template python client-authenticated webapp."""
from setuptools import setup, find_packages

with open('README.md') as f:
    README = f.read()

with open('requirements.txt') as f:
    REQUIREMENTS = f.readlines()

setup(
    name='passwords',
    version='0.1.0',
    description="A python template for a flask webapp with client certificate authentication",
    long_description=README,
    author='Eugene Kovalev',
    author_email='euge.kovalev@gmail.com',
    url='https://github.com/Abraxos/python-flask-clientauth-template',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=REQUIREMENTS,
    entry_points={'console_scripts': ['python-flask-clientauth-webapp='
                                      'python_flask_clientauth_template.webapp:run_app_server']},
)
