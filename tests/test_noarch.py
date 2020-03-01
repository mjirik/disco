# /usr/bin/env python
# -*- coding: utf-8 -*-
from loguru import logger

import pytest
import os.path as op
import discon
import discon.discon_tools

path_to_script = op.dirname(op.abspath(__file__))

def test_noarch_from_text():
    assert discon.discon_tools.check_meta_yaml_for_noarch(None, "adfadf\n   noarch: python   \n") == True, "Check noarch in meta.yaml"
    assert discon.discon_tools.check_meta_yaml_for_noarch(None, "adfadf\n # noarch: python   \n") == False, "Check noarch in meta.yaml"


def test_noarch_from_file():
    # pth = op.join(path_to_script, "../conda-recipe/meta.yaml")
    pth = op.join(path_to_script, "../../io3d/conda-recipe/meta.yaml")
    assert discon.discon_tools.check_meta_yaml_for_noarch(pth) == False, "Check noarch in meta.yaml"


