# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html)
import subprocess
import pytest


def test_no_params_prints_usage():
    with pytest.raises(subprocess.CalledProcessError) as e:
        subprocess.check_output(['anthem'], stderr=subprocess.STDOUT)
    assert "usage" in e.value.output.decode()
    assert e.value.returncode == 2


def test_one_param_calls_song():
    result = subprocess.check_output(['anthem', 'anthem.sample_songs::empty'])
    assert result.decode() == "I am empty\n"
