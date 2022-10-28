# Copyright 2016-2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import os

import unicodecsv as csv

from ..exceptions import AnthemError
from . import modules
from .records import switch_company


def load_model_csv(ctx, path):
    """Use to load any model

    :param ctx: Anthem context
    :param path: Absolute or relative path to CSV file.

    Usage::

        @anthem.log
        def import_res_partner(ctx):
            load_model_csv(ctx, 'res.partner.csv')

    """
    model = os.path.splitext(os.path.basename(path))[0]
    load_csv(ctx, model, path)


def load_users_csv(ctx, path):
    """Use to load users without sending emails

    :param ctx: Anthem context
    :param path: Absolute or relative path to CSV file.

    Usage::

        @anthem.log
        def import_res_users(ctx):
            load_users_csv(ctx, 'res.users.csv')

    """
    # make sure we don't send any email
    model = ctx.env["res.users"].with_context(
        {"no_reset_password": True, "tracking_disable": True}
    )
    load_csv(ctx, model, path)


def load_warehouses(ctx, company, path):
    """Use to load warehouses in multi-company

    In multi-company mode we must force the company otherwise the sequences that stock
    module generates automatically will have the wrong company assigned.

    :param ctx: Anthem context
    :param company: Company record or XML ID
    :param path: Absolute or relative path to CSV file.

    Usage::

        @anthem.log
        def import_warehouses(ctx):
            load_warehouses(ctx, ctx.env.user.company_id, 'stock.warehouse.csv')

    """
    with switch_company(ctx, company) as ctx:
        load_model_csv(ctx, path)
        # TODO: dirty hack here.
        # We are forced to load the CSV twice because
        # if you are modifying the existing base warehouse (stock.warehouse0)
        # and you've changed the `code` (short name)
        # the changes are not reflected on existing sequences
        # until you load warehouse data again.
        # We usually don't have that many WHs so... it's fine :)
        load_model_csv(ctx, path)


def load_csv(ctx, model, path, header=None, header_exclude=None, **fmtparams):
    """Load a CSV from a file path.

    :param ctx: Anthem context
    :param model: Odoo model name or model klass from env
    :param path: absolute or relative path to CSV file.
        If a relative path is given you must provide a value for
        `ODOO_DATA_PATH` in your environment
        or set `--odoo-data-path` option.
    :param header: whitelist of CSV columns to load
    :param header_exclude: blacklist of CSV columns to not load
    :param fmtparams: keyword params for `csv_unireader`

    Usage example::

      from pkg_resources import Requirement, resource_string

      req = Requirement.parse('my-project')
      load_csv(ctx, ctx.env['res.users'],
               resource_string(req, 'data/users.csv'),
               delimiter=',')

    """
    if not os.path.isabs(path):
        if ctx.options.odoo_data_path:
            path = os.path.join(ctx.options.odoo_data_path, path)
        else:
            raise AnthemError(
                "Got a relative path. "
                "Please, provide a value for `ODOO_DATA_PATH` "
                "in your environment or set `--odoo-data-path` option."
            )

    with open(path, "rb") as data:
        load_csv_stream(
            ctx, model, data, header=header, header_exclude=header_exclude, **fmtparams
        )


def read_csv(data, dialect="excel", encoding="utf-8", **fmtparams):
    rows = csv.reader(data, encoding=encoding, **fmtparams)
    header = next(rows)
    return header, rows


def load_rows(ctx, model, header, rows):
    if isinstance(model, str):
        model = ctx.env[model].with_context(tracking_disable=True)
    else:
        if "tracking_disable" not in model.env.context:
            model = model.with_context(tracking_disable=True)
    result = model.load(header, rows)
    ids = result["ids"]
    if not ids:
        messages = "\n".join("- %s" % msg for msg in result["messages"])
        ctx.log_line(
            "Failed to load CSV " "in '%s'. Details:\n%s" % (model._name, messages)
        )
        raise AnthemError("Could not import CSV. See the logs")
    else:
        ctx.log_line("Imported %d records in '%s'" % (len(ids), model._name))


def load_csv_stream(ctx, model, data, header=None, header_exclude=None, **fmtparams):
    """Load a CSV from a stream.

    :param ctx: current anthem context
    :param model: model name as string or model klass
    :param data: csv data to load
    :param header: csv fieldnames whitelist
    :param header_exclude: csv fieldnames blacklist

    Usage example::

      from pkg_resources import Requirement, resource_stream

      req = Requirement.parse('my-project')
      load_csv_stream(ctx, ctx.env['res.users'],
                      resource_stream(req, 'data/users.csv'),
                      delimiter=',')
    """
    _header, _rows = read_csv(data, **fmtparams)
    header = header if header else _header
    if _rows:
        # check if passed header contains all the fields
        if header != _header and not header_exclude:
            # if not, we exclude the rest of the fields
            header_exclude = [x for x in _header if x not in header]
        if header_exclude:
            # exclude fields from header as well as respective values
            header = [x for x in header if x not in header_exclude]
            # we must loop trough all the rows too to pop values
            # since odoo import works only w/ reader and not w/ dictreader
            pop_idxs = [_header.index(x) for x in header_exclude]
            rows = []
            for _i, row in enumerate(_rows):
                rows.append([x for j, x in enumerate(row) if j not in pop_idxs])
        else:
            rows = list(_rows)
        if rows:
            load_rows(ctx, model, header, rows)


def update_translations(ctx, module_list):
    """Update translations from module list

    :param module_list: a list of modules
    """
    modules.update_translations(ctx, module_list)
    ctx.log_line(
        "Deprecated: use anthem.lyrics.modules.update_translations"
        "instead of anthem.lyrics.loaders.update_translations"
    )
