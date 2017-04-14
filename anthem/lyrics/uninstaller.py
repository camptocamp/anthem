# -*- coding: utf-8 -*-
# Copyright 2016-2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from ..exceptions import AnthemError


def uninstall(ctx, module_list):
    """ uninstall module """
    mods = ctx.env['ir.module.module'].search([('name', 'in', module_list)])
    try:
        mods.button_immediate_uninstall()
    except:
        raise AnthemError(u'Cannot uninstall modules. See the logs')
