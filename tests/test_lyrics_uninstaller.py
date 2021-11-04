# Copyright 2016 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html)

import pytest

import anthem.cli
from anthem.exceptions import AnthemError
from anthem.lyrics.modules import uninstall


def test_uninstall_1():
    with anthem.cli.Context(None, anthem.cli.Options(test_mode=True)) as ctx:
        with pytest.raises(AnthemError) as excinfo:
            uninstall(ctx, [])
        excinfo.match(r"You have to provide a list of module.*")


def test_uninstall_2():
    with anthem.cli.Context(None, anthem.cli.Options(test_mode=True)) as ctx:
        ctx.env["ir.module.module"].search(
            [("name", "=", "lunch")]
        ).button_immediate_install()

    # In later version `button_immediate_install` returns an action
    # to open base.module.upgrade wizard which will make a reload.
    # By separating contexts we simulate this reload and get a context
    # where the module lunch is already installed.
    with anthem.cli.Context(None, anthem.cli.Options(test_mode=True)) as ctx:
        uninstall(ctx, ["lunch"])
