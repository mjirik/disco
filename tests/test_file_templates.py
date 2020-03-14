# /usr/bin/env python
# -*- coding: utf-8 -*-
from loguru import logger

import pytest
import discon.file_content


def test_check_template():
    meta_yml = discon.file_content.get_str_from_template_file("meta.yml.template")
    meta_yml2 = discon.file_content._META_YML_OLD
    assert meta_yml.find("python") > 0
    assert meta_yml2.find("python") > 0
    # assert meta_yml == meta_yml2

