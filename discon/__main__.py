#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © %YEAR%  <>
#
# Distributed under terms of the %LICENSE% license.

"""
Tool for easy push project to pypi and binstar (Anaconda).
Git pull, bumpversion, pip build and upload, conda build and upload and git push is performed.
There is also option to init new project directory.

"""

from loguru import logger
import argparse
import subprocess
import os
import os.path as op
import shutil
import glob
from pathlib import Path
from . import file_content
from . import discon_tools
from .main_app import make_init, pypi_build_and_upload, init

__version__ = "2.7.11"


def mycall(command, ignore_error=True):
    if type(command) is list:
        try:
            # subprocess.call(command)
            subprocess.check_call(command)
        except subprocess.CalledProcessError as e:
            if ignore_error:
                logger.warning("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
            else:
                raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    else:
        try:
            # subprocess.call(command, shell=True)
            subprocess.check_call(command, shell=True)
        except subprocess.CalledProcessError as e:
            if ignore_error:
                logger.warning("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
            else:
                raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))


def check_git():
    try:
        import git
        import git.exc
    except:
        logger.info("GitPython is not installed")
        return

    try:
        repo = git.Repo(".")
    except git.exc.InvalidGitRepositoryError as e:
        logger.info("It is not Git repo")


    if repo.is_dirty():
        logger.error("Git working directory is dirty. Clean it.")
        exit()


def get_recipe_prefix():
    if op.exists("meta.yaml"):
        # old position of recipe
        prefix = ""
    else:
        prefix = "conda-recipe/"
    return prefix

def make(args):
    prefix = get_recipe_prefix()

    logger.debug(f"prefix: {prefix}")
    if not op.exists("conda-recipe"):
        import os
        os.makedirs("conda-recipe")
    if not op.exists(prefix + "build.sh"):
        with open(prefix + 'build.sh', 'a') as the_file:
            the_file.write('#!/bin/bash\n\n$PYTHON setup.py install\n')
    if not op.exists(prefix + "bld.bat"):
        with open(prefix + 'bld.bat', 'a') as the_file:
            the_file.write('"%PYTHON%" setup.py install\nif errorlevel 1 exit 1')

    check_git()
    if (args.action == "init"):
        init(args) #, author=args.author, email=args.email, githubuser=args.gihubuser)
        return
    elif (args.action == "stable"):
        mycall("git push --tags")
        mycall("git checkout stable")
        mycall("git pull origin master")
        mycall("git push")
        mycall("git checkout master")
        return
    elif args.action in ["minor", "major", "patch"]:
        if not args.skip_git:
            logger.debug("pull, patch, push, push --tags")
            mycall("git pull")
        if args.skip_bumpversion:
            logger.info("skip bumpversion")
        else:
            mycall("bumpversion " + args.action)
            if not args.skip_git:
                mycall("git push")
                mycall("git push --tags")
        # if args.init_project_name is "pypi":
        #     upload_conda = False
    elif args.action in ["stay"]:
        logger.debug("stay on version")
    # elif args.action in ["build_conda"]:
    #     logger.debug("build conda based on meta.yaml")
    #     process_pypi = False
    elif args.action in ["skeleton"]:
        logger.debug("building skeleton")
        package_name = args.project_name
        mycall(["conda", "skeleton", "pypi", package_name], ignore_error=False)
        return
    else:
        logger.error("Unkown command '"+ args.action + "'")
        return

# fi
    # upload to pypi
    if not args.skip_pypi:
        pypi_build_and_upload(args)


from discon import main_app

def main():
    # logger = logging.getLogger()

    # logger.setLevel(logging.DEBUG)
    # ch = logging.StreamHandler()
    # logger.addHandler(ch)

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
        "action",
        help="Available values are: 'init', 'stay', 'patch', 'minor', 'major' or 'stable'. "
            "Git pull is performed in the beginning. "
            "If 'init' is used the project directory with all necessary files is prepared and app quits. "
            "Version number will be increased with bumpversion if option 'patch', 'minor' and 'major' is used. "
            "Command 'stay' causes skipping of the bumpversion. Comands 'stay', 'patch', 'minor' and 'major' "
            "build PyPi and conda package and upload it to the server. The changes are then pushed to git."
        ,
        default=None)
    parser.add_argument(
        "project_name",
        nargs='?',
        help="project directory (with setup.py) or new project name if 'init' action is used",
        default="default_project")
    parser.add_argument("--py",
            # default="2.7",
            # default="both",
            action="append",
            default=[],
            # default="all",
            help="specify python version. '--py 2.7' or '--py both' for python 3.6 and 2.7. "
                 "Parameter can be used multiple times.")
    parser.add_argument("--arch",
                        # default="2.7",
                        # default="both",
                        default="check",
                        # default="all",
                        help="'check' (default) or 'noarch' or 'convert' or 'noconvert' ")
    parser.add_argument(
        "-c", "--channel",
        nargs=1,
        action="append",
        help="Add conda channel. Can be used multiple times.",
        default=[])
    parser.add_argument(
        "-V", "--version", action='store_true',
        help="Print version number",
        default=False)
    # parser.add_argument(
    #     "arg2",
    #     required=False,
    #     default=None)
    # parser.add_argument(
    #     '-i', '--inputfile',
    #     default=None,
    #     # required=True,
    #     help='input file'
    # )
    parser.add_argument(
        '-ll', '--loglevel', type=int, default=None,
        help='Debug level 0 to 100')

    parser.add_argument(
        '-d', '--debug', action='store_true',
        help='Debug mode')
    parser.add_argument(
        '-sg', '--skip-git', action='store_true',
        help='Skip git pull on beginning and git push after bumpversion.')
    parser.add_argument(
        '-sp', '--skip-pypi', action='store_true',
        help='Do not upload to pypi')
    parser.add_argument(
        '-sc', '--skip-conda', action='store_true',
        help='Do not process conda package')
    parser.add_argument(
        '-sb', '--skip-bumpversion', action='store_true',
        help='Do not build and upload pypi package')
    parser.add_argument(
        '-su', '--skip-upload', action='store_true',
        help='Do not upload to pypi and conda')
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Do not create any files in init')

    args = parser.parse_args()


    if args.loglevel is not None:
        logger.add(level=args.loglevel)
        logger.remove(0)

    if args.debug:
        logger.add(level="DEBUG")
        logger.remove(0)
        # ch.setLevel(logging.DEBUG)

    if args.version:
        print(__version__)

    # print(dir(args))
    make(args)


if __name__ == "__main__":
    main()

