# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html)

import anthem.cli
from anthem.lyrics.uninstaller import uninstall
from anthem.exceptions import AnthemError


def test_uninstall_1():
    with anthem.cli.Context(None, anthem.cli.Options(test_mode=True)) as ctx:
        ctx.env['ir.module.module'].search(
            [('name', '=', 'lunch')]).button_immediate_install()
        try:
            uninstall(ctx, [])
        except AnthemError:
            pass
        else:
            assert False


def test_uninstall_2():
    with anthem.cli.Context(None, anthem.cli.Options(test_mode=True)) as ctx:
        ctx.env['ir.module.module'].search(
            [('name', '=', 'lunch')]).button_immediate_install()
        uninstall(ctx, ['lunch'])
