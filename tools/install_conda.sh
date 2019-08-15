#!/bin/bash

# Using on travis
# wget http://home.zcu.cz/~mjirik/lisa/install/install_conda.sh && source install_conda.sh

if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
elif [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O miniconda.sh;
elif [[ "$TRAVIS_OS_NAME" == "windows" ]]; then
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -O miniconda.exe;
else
    echo "Error: Just for use on travis"
fi
bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
conda config --set always_yes yes --set changeps1 no