#!/bin/bash

echo -e "[pypi]" > ~/.pypirc
echo -e "username = __token__" >> ~/.pypirc
#echo -e "password = ${{ secrets.PYPI_API_TOKEN }}" >> ~/.pypirc
echo -e "password = $API_TOKEN" >> ~/.pypirc

echo -e "[testpypi]" >> ~/.pypirc
echo -e "username = __token__" >> ~/.pypirc
echo -e "password = $TEST_TOKEN" >> ~/.pypirc

python setup.py install --user
pip install build
pip install twine
python -m build
rm dist/*.egg
twine upload --repository testpypi dist/*
twine upload dist/*
