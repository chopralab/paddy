#!/bin/bash

echo -e "[pypi]" > ~/.pypirc
echo -e "username = chopralab" >> ~/.pypirc
echo -e "password = ${{PYPI.TEST}}" >> ~/.pypirc
echo "${{ PYPI.TEST }}"
echo "$PYPI.TEST"
echo "${{ secrets.TEST }}"
echo "$TEST"
echo "$secrets.TEST"
