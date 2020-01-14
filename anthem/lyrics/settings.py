# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html)

from past.builtins import basestring
from ..cli import odoo


def define_settings(ctx, model, values):
    """ Define settings like being in the interface

    Example:

    model: 'sale.config.settings' or ctx.env['sale.config.settings']
    values: {'default_invoice_policy': 'delivery'}

    Be careful:

    * settings onchange are not triggered with this function.
    * in recent versions, the model is always 'res.config.settings'
    * it cannot be used to install/uninstall modules
    """
    if isinstance(model, basestring):
        model = ctx.env[model]
    if odoo.release.version_info[0] < 13:
        # < 13.0, execute takes care of default values, groups,
        # install/uninstall and call set_values() for the rest.
        # We don't want the install part, but we need default and groups,
        # so call execute().
        model.create(values).execute()
    else:
        # In 13.0, execute calls set_values(), then takes care of
        # install/uninstall. execute() resets the env which breaks
        # computed fields afterwards, so do not call it.
        model.create(values).set_values()
