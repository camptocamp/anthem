# Copyright 2016 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html)

from io import BytesIO

import pytest

import anthem.cli
from anthem.exceptions import AnthemError
from anthem.lyrics.loaders import load_csv, load_csv_stream

csv_partner = (
    b"id,name,street,city\n"
    b"__test__.partner1,Partner 1,Street 1,City 1\n"
    b"__test__.partner2,Partner 2,Street 2,City 2\n"
)


def clear_cache(ctx, model):
    # clear_cache is necessary to make the models.exists work
    # after loading csv with models.load (self.env.ref relies on models.exists)
    if hasattr(ctx.env.registry, "clear_cache"):  # Odoo 17 to 19
        ctx.env.registry.clear_cache()
    elif hasattr(ctx.env[model], "clear_caches"):  # Odoo 12 to 16
        ctx.env[model].clear_caches()
    # No need to clear cache for Odoo >= 20


def test_load_csv_stream_model():
    csv_stream = BytesIO()
    csv_stream.write(csv_partner)
    csv_stream.seek(0)
    with anthem.cli.Context(None, anthem.cli.Options(test_mode=True)) as ctx:
        load_csv_stream(ctx, ctx.env["res.partner"], csv_stream, delimiter=",")
        partner1 = ctx.env.ref("__test__.partner1", raise_if_not_found=False)
        assert partner1
        assert partner1.name == "Partner 1"
        partner2 = ctx.env.ref("__test__.partner2", raise_if_not_found=False)
        assert partner2
        assert partner2.name == "Partner 2"


def test_load_csv_file_model(tmpdir):
    csvfile = tmpdir.mkdir("files").join("res.partner.csv")
    csvfile.write(csv_partner)
    with anthem.cli.Context(None, anthem.cli.Options(test_mode=True)) as ctx:
        load_csv(ctx, ctx.env["res.partner"], csvfile.strpath, delimiter=",")
        clear_cache(ctx, "res.partner")
        partner1 = ctx.env.ref("__test__.partner1", raise_if_not_found=False)
        assert partner1
        assert partner1.name == "Partner 1"
        partner2 = ctx.env.ref("__test__.partner2", raise_if_not_found=False)
        assert partner2
        assert partner2.name == "Partner 2"


def test_load_csv_stream_model_string():
    """Pass string instead of model to load_csv_stream"""
    csv_stream = BytesIO()
    csv_stream.write(csv_partner)
    csv_stream.seek(0)
    with anthem.cli.Context(None, anthem.cli.Options(test_mode=True)) as ctx:
        load_csv_stream(ctx, "res.partner", csv_stream, delimiter=",")
        clear_cache(ctx, "res.partner")
        partner1 = ctx.env.ref("__test__.partner1", raise_if_not_found=False)
        assert partner1
        assert partner1.name == "Partner 1"
        partner2 = ctx.env.ref("__test__.partner2", raise_if_not_found=False)
        assert partner2
        assert partner2.name == "Partner 2"


def test_load_csv_file_model_string(tmpdir):
    csvfile = tmpdir.mkdir("files").join("res.partner.csv")
    csvfile.write(csv_partner)
    with anthem.cli.Context(None, anthem.cli.Options(test_mode=True)) as ctx:
        load_csv(ctx, "res.partner", csvfile.strpath, delimiter=",")
        clear_cache(ctx, "res.partner")
        partner1 = ctx.env.ref("__test__.partner1", raise_if_not_found=False)
        assert partner1
        assert partner1.name == "Partner 1"
        partner2 = ctx.env.ref("__test__.partner2", raise_if_not_found=False)
        assert partner2
        assert partner2.name == "Partner 2"


def test_load_erroneous_csv():
    err_csv = (
        b"id,name,category_id/id\n" b"__test__.partner_fail,Test, xmlid_not_found\n"
    )
    csv_stream = BytesIO()
    csv_stream.write(err_csv)
    csv_stream.seek(0)
    with anthem.cli.Context(None, anthem.cli.Options(test_mode=True)) as ctx:
        with pytest.raises(AnthemError):
            load_csv_stream(ctx, "res.partner", csv_stream, delimiter=",")
