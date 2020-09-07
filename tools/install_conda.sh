#!/bin/bash

# Using on travis
# wget https://raw.githubusercontent.com/mjirik/discon/master/tools/install_conda.sh && source install_conda.sh
# or
# wget http://home.zcu.cz/~mjirik/lisa/install/install_conda.sh && source install_conda.sh

if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    if [[ "$CONDA_PYTHON_VERSION" == "2.7" ]]; then
        wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O miniconda.sh;
    else
        wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
    fi
#    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
elif [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O miniconda.sh;
elif [[ "$TRAVIS_OS_NAME" == "windows" ]]; then
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -O miniconda.exe;
else
#    echo "Error: Just for use on travis"
    if [ "$(uname)" == "Darwin" ]; then
        # Do something under Mac OS X platform
        wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O miniconda.sh;
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        # Do something under GNU/Linux platform
        wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
    elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
        # Do something under 32 bits Windows NT platform
        wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -O miniconda.exe;
    elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
        # Do something under 64 bits Windows NT platform
        wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -O miniconda.exe;
    fi
fi
bash miniconda.sh -b -p $HOME/miniconda3
export PATH="$HOME/miniconda3/bin:$PATH"
conda config --set always_yes yes --set changeps1 no