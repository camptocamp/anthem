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


def update_translations(ctx, module_list, overwrite=False):
    """ Update translations from module list"""
    if not isinstance(module_list, list):
        raise AnthemError(u"You have to provide a list of "
                          "module's name to update the translations")

    domain = [('name', 'in', module_list)]
    mods = ctx.env['ir.module.module'].search(domain)
    ctx.log_line('Reloading translations for %s' % str(module_list))
    mods.with_context(overwrite=overwrite).update_translations()
