# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html)

import anthem.cli
from anthem.lyrics.records import add_xmlid, create_or_update


def test_add_xmlid():
    with anthem.cli.Context(None, anthem.cli.Options(test_mode=True)) as ctx:
        env = ctx.env
        record = env['res.partner'].create({'name': 'test'})
        assert not record.get_metadata()[0]['xmlid']
        ref1 = add_xmlid(ctx, record, 'test.add_xmlid')
        assert record.get_metadata()[0]['xmlid'] == 'test.add_xmlid'
        ref2 = add_xmlid(ctx, record, 'test.add_xmlid')
        assert ref1 == ref2


def test_create_or_update():
    with anthem.cli.Context(None, anthem.cli.Options(test_mode=True)) as ctx:
        record = create_or_update(ctx, 'res.partner', 'test.upsert',
                                  {'name': 'test'})
        assert record.name == 'test'
        assert record._name == 'res.partner'
        record2 = create_or_update(ctx, 'res.partner', 'test.upsert',
                                   {'name': 'test2'})
        assert record2 == record
        assert record2.name == 'test2'
