#!/bin/bash

echo -e "[pypi]" >> ~/.pypirc
echo -e "username = armenbeck" >> ~/.pypirc
echo -e "password = $PYPI_PASSWORD" >> ~/.pypirc

python setup.py install --user

pip install twine
twine --verbose upload dist/*
#twine upload --verbose -u __token__ -p $PYPI_PASSWORD dist dist/*

