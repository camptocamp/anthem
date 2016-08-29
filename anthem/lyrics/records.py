# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html)


def add_xmlid(ctx, record, xmlid, noupdate=False):
    """ Add a XMLID on an existing record """
    try:
        ref_id, __, __ = ctx.env['ir.model.data'].xmlid_lookup(xmlid)
    except ValueError:
        pass  # does not exist, we'll create a new one
    else:
        return ctx.env['ir.model.data'].browse(ref_id)
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
