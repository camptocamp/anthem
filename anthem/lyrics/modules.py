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

    ir_module = ctx.env['ir.module.module']
    if hasattr(ir_module, 'update_translations'):
        # Odoo version <= 10.0
        method_name = 'update_translations'
    else:
        # Odoo version >= 11.0
        method_name = '_update_translations'

    for module in module_list:
        getattr(
            ir_module.with_context(overwrite=True).search(
                [('name', '=', module)]),
            method_name
        )()
