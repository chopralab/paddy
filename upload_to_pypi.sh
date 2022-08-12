#!/bin/bash

echo -e "[pypi]" > ~/.pypirc
echo -e "username = __token__" >> ~/.pypirc
#echo -e "password = ${{ secrets.PYPI_API_TOKEN }}" >> ~/.pypirc
echo -e "password = $$PYPI_PASSWORD" >> ~/.pypirc

python setup.py install --user

pip install twine
twine upload --verbose dist/*
#twine upload --verbose -u __token__ -p $PYPI_PASSWORD dist dist/*

