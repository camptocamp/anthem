# Copyright 2016 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from contextlib import contextmanager


def add_xmlid(ctx, record, xmlid, noupdate=False):
    """Add an XMLID to an existing record"""
    # Plain SQL because _xmlid_lookup changed to private method
    # in Odoo 15, and changed its signature in Odoo 17
    module, name = xmlid.split(".", 1) if "." in xmlid else ("", xmlid)
    query = "SELECT id FROM ir_model_data WHERE module = %s AND name = %s;"
    ctx.env.cr.execute(query, [module, name])
    [ref_id] = ctx.env.cr.fetchone() or [None]
    if ref_id:
        return ctx.env["ir.model.data"].browse(ref_id)
    # Does not exist, then create a new one
    return ctx.env["ir.model.data"].create(
        {
            "name": name,
            "module": module,
            "model": record._name,
            "res_id": record.id,
            "noupdate": noupdate,
        }
    )


def create_or_update(ctx, model, xmlid, values):
    """Create or update a record matching xmlid with values"""
    if isinstance(model, str):
        model = ctx.env[model]

    record = ctx.env.ref(xmlid, raise_if_not_found=False)
    if record:
        record.update(values)
    else:
        record = model.create(values)
        add_xmlid(ctx, record, xmlid)
    return record


def safe_record(ctx, item):
    """Make sure we get a record instance even if we pass an xmlid."""
    if isinstance(item, str):
        return ctx.env.ref(item)
    return item


@contextmanager
def switch_company(ctx, company):
    """Context manager to switch current company.

    Accepts both company record and xmlid.
    """
    current_company = ctx.env.user.company_id
    ctx.env.user.company_id = safe_record(ctx, company)
    yield ctx
    ctx.env.user.company_id = current_company
