#!/bin/bash

echo -e "[pypi]" >> ~/.pypirc
echo -e "username = chopralab" >> ~/.pypirc
echo -e "password = $PYPI_PASSWORD" >> ~/.pypirc

python setup.py install --user

pip install twine
twine upload dist/*

