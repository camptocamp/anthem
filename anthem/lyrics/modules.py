# -*- coding: utf-8 -*-
# Copyright 2016-2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from ..exceptions import AnthemError


def uninstall(ctx, module_list):
    """ uninstall module """
    if not module_list:
        raise AnthemError(u"You have to provide a list of "
                          "module's name to uninstall")

    mods = ctx.env['ir.module.module'].search([('name', 'in', module_list)])
    try:
        mods.button_immediate_uninstall()
    except Exception:
        raise AnthemError(u'Cannot uninstall modules. See the logs')


def update_translations(ctx, module_list):
    """ Update translations from module list"""
    if not module_list:
        raise AnthemError(u"You have to provide a list of "
                          "module's name to update the translations")

    for module in module_list:
        ctx.env['ir.module.module'].with_context(overwrite=True).search(
            [('name', '=', module)]).update_translations()
