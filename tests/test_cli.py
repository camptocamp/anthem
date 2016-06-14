# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import subprocess
import pytest


def test_no_params_prints_usage():
    with pytest.raises(subprocess.CalledProcessError) as e:
        subprocess.check_output(['anthem'], stderr=subprocess.STDOUT)
    assert "usage" in e.value.output
    assert e.value.returncode == 2
