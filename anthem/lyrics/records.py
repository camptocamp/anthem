# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


def add_xmlid(ctx, record, xmlid, noupdate=False):
    """ Add a XMLID on an existing record """
    if '.' in xmlid:
        module, name = xmlid.split('.')
    else:
        module = ''
        name = xmlid
    return ctx.env['ir.model.data'].create({
        'name': name,
        'module': module,
        'model': record._name,
        'res_id': record.id,
        'noupdate': noupdate,
    })


def create_or_update(ctx, model, xmlid, values):
    """ Create or update a record matching xmlid with values """
    record = ctx.env.ref(xmlid, raise_if_not_found=False)
    if record:
        record.update(values)
    else:
        record = ctx.env[model].create(values)
        add_xmlid(ctx, record, xmlid)
    return record
