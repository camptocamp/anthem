# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html)

from past.builtins import basestring


def define_settings(ctx, model, values):
    """ Define settings like being in the interface
     Example :
      - model = 'sale.config.settings' or ctx.env['sale.config.settings']
      - values = {'default_invoice_policy': 'delivery'}
     Be careful, settings onchange are not triggered with this function.
    """
    if isinstance(model, basestring):
        model = ctx.env[model]
    model.create(values).execute()
