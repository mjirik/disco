#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © %YEAR%  <>
#
# Distributed under terms of the %LICENSE% license.

"""

"""

import logging

logger = logging.getLogger(__name__)
import argparse
import subprocess

def make(args):
    # upload to pypi
    subprocess.call(["python", "setup.py", "register", "sdist", "upload"])

    # build conda and upload

    subprocess.call(["rm ", "-rf ", "win-*"])
    subprocess.call(["rm ", "-rf ", "linux-*"])
    subprocess.call(["rm ", "-rf ", "osx-*"])

    subprocess.call("conda build -c mjirik -c SimpleITK .", shell=True)
    subprocess.call("conda convert -p all `conda build --output .`", shell=True)

    subprocess.call("binstar upload */*.tar.bz2", shell=True)

    subprocess.call(["rm", "-rf", "win-*"])
    subprocess.call(["rm", "-rf", "linux-*"])
    subprocess.call(["rm", "-rf", "osx-*"])


def main():
    logger = logging.getLogger()

    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    # create file handler which logs even debug messages
    # fh = logging.FileHandler('log.txt')
    # fh.setLevel(logging.DEBUG)
    # formatter = logging.Formatter(
    #     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)
    # logger.debug('start')

    # input parser
    parser = argparse.ArgumentParser(
        description=__doc__
    )
    parser.add_argument(
        "bumptype",
        default=None)
    parser.add_argument(
        '-i', '--inputfile',
        default=None,
        # required=True,
        help='input file'
    )
    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='Debug mode')
    args = parser.parse_args()

    if args.debug:
        ch.setLevel(logging.DEBUG)

    make(args)


if __name__ == "__main__":
    main()