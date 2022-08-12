#!/bin/bash

echo -e "[pypi]" >> ~/.pypirc
echo -e "username = armenbeck" >> ~/.pypirc
echo -e "password = $PYPI_PASSWORD" >> ~/.pypirc

python setup.py install --user

pip install twine
twine upload -u armenbeck -p $PYPI_PASSWORD dist dist/*

