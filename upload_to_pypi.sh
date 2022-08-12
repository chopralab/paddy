#!/bin/bash

echo -e "[pypi]" >> ~/.pypirc
echo -e "username = chopralab" >> ~/.pypirc
echo -e "password = ${{PYPI.TEST}}" >> ~/.pypirc
echo ${{PYPI.TEST}}

python setup.py install --user

pip install twine
twine upload dist/*

