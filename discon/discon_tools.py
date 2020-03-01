#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
from loguru import logger
from pathlib import Path


def check_meta_yaml_for_noarch(fn:Path, text=None):
    import re
    logger.debug("Checking for noarch")
    if text is None:
        with open(fn, "rt") as fl:
            text = fl.read()

    mo = re.search(r"\n\s*noarch_python:\s*True", text)
    if mo:
        logger.info("Detected conda noarch python")
        return True
    mo = re.search(r"\n\s*noarch:\s*python", text)
    if mo:
        logger.info("Detected conda noarch python")
        return True
    return False

