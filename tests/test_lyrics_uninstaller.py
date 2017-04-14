# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html)

import anthem.cli
from anthem.lyrics.uninstaller import uninstall
from anthem.exceptions import AnthemError


def test_uninstall():
    with anthem.cli.Context(None, anthem.cli.Options(test_mode=True)) as ctx:
        env = ctx.env
        env['ir.module.module'].search([
            ('name', '=', 'sale_order_dates')]).button_immediate_install()
        try:
            uninstall(ctx, ['sale_order_dates'])
        except AnthemError:
            pass
        else:
            assert False
