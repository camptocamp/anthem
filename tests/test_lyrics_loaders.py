# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html)

from io import BytesIO

import pytest

from anthem.exceptions import AnthemError
import anthem.cli
from anthem.lyrics.loaders import load_csv, load_csv_stream

csv_partner = (b"id,name,street,city\n"
               b"__test__.partner1,Partner 1,Street 1,City 1\n"
               b"__test__.partner2,Partner 2,Street 2,City 2\n"
               )


def test_load_csv_stream_model():
    csv_stream = BytesIO()
    csv_stream.write(csv_partner)
    csv_stream.seek(0)
    with anthem.cli.Context(None, anthem.cli.Options(test_mode=True)) as ctx:
        load_csv_stream(ctx, ctx.env['res.partner'], csv_stream, delimiter=',')
        partner1 = ctx.env.ref('__test__.partner1', raise_if_not_found=False)
        assert partner1
        assert partner1.name == 'Partner 1'
        partner2 = ctx.env.ref('__test__.partner2', raise_if_not_found=False)
        assert partner2
        assert partner2.name == 'Partner 2'


def test_load_csv_file_model(tmpdir):
    csvfile = tmpdir.mkdir("files").join("res.partner.csv")
    csvfile.write(csv_partner)
    with anthem.cli.Context(None, anthem.cli.Options(test_mode=True)) as ctx:
        load_csv(ctx, ctx.env['res.partner'], csvfile.strpath, delimiter=',')
        partner1 = ctx.env.ref('__test__.partner1', raise_if_not_found=False)
        assert partner1
        assert partner1.name == 'Partner 1'
        partner2 = ctx.env.ref('__test__.partner2', raise_if_not_found=False)
        assert partner2
        assert partner2.name == 'Partner 2'


def test_load_csv_stream_model_string():
    """ Pass string instead of model to load_csv_stream """
    csv_stream = BytesIO()
    csv_stream.write(csv_partner)
    csv_stream.seek(0)
    with anthem.cli.Context(None, anthem.cli.Options(test_mode=True)) as ctx:
        load_csv_stream(ctx, 'res.partner', csv_stream, delimiter=',')
        partner1 = ctx.env.ref('__test__.partner1', raise_if_not_found=False)
        assert partner1
        assert partner1.name == 'Partner 1'
        partner2 = ctx.env.ref('__test__.partner2', raise_if_not_found=False)
        assert partner2
        assert partner2.name == 'Partner 2'


def test_load_csv_file_model_string(tmpdir):
    csvfile = tmpdir.mkdir("files").join("res.partner.csv")
    csvfile.write(csv_partner)
    with anthem.cli.Context(None, anthem.cli.Options(test_mode=True)) as ctx:
        load_csv(ctx, 'res.partner', csvfile.strpath, delimiter=',')
        partner1 = ctx.env.ref('__test__.partner1', raise_if_not_found=False)
        assert partner1
        assert partner1.name == 'Partner 1'
        partner2 = ctx.env.ref('__test__.partner2', raise_if_not_found=False)
        assert partner2
        assert partner2.name == 'Partner 2'


def test_load_erroneous_csv():
    err_csv = (b"id,name,category_id/id\n"
               b"__test__.partner_fail,Test, xmlid_not_found\n")
    csv_stream = BytesIO()
    csv_stream.write(err_csv)
    csv_stream.seek(0)
    with anthem.cli.Context(None, anthem.cli.Options(test_mode=True)) as ctx:
        with pytest.raises(AnthemError):
            load_csv_stream(ctx, 'res.partner', csv_stream, delimiter=',')
