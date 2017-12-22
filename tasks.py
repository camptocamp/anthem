# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html)

from __future__ import print_function

import os

from distutils.version import LooseVersion
from invoke import task, Collection

ns = Collection()
tests = Collection('tests')
ns.add_collection(tests)

ODOO_URL = 'https://github.com/odoo/odoo/archive/{}.tar.gz'


def is_below_odoo_10(version):
    return LooseVersion(version) < LooseVersion('10.0')


def dbname(version):
    return 'anthem-test-db-{}'.format(version.replace('.', '_'))


def assert_version(version):
    assert version in ('11.0', '10.0', '9.0')


@task
def tests_prepare(ctx, version):
    assert_version(version)
    if not os.path.exists('odoo-{}'.format(version)):
        url = ODOO_URL.format(version)
        print('Getting {}'.format(url))
        ctx.run('wget -nv -c -O odoo.tar.gz {}'.format(url))
        ctx.run('tar xfz odoo.tar.gz')
        ctx.run('rm -f odoo.tar.gz')
    print('Installing odoo, now')
    ctx.run('pip install -r odoo-{}/requirements.txt -q'.format(version))
    ctx.run('pip install -e odoo-{} -q'.format(version))


@task
def tests_createdb(ctx, version):
    assert_version(version)
    db = dbname(version)
    print('Installing database {}'.format(db))
    if is_below_odoo_10(version):
        ctx.run('odoo.py -d {} --workers=0 --log-level=critical '
                '--stop-after-init'.format(db))
    else:
        ctx.run('odoo -d {} --workers=0 --log-level=critical '
                '--stop-after-init'.format(db))


@task
def tests_dropdb(ctx, version):
    assert_version(version)
    print('Dropping the database')
    try:
        if is_below_odoo_10(version):
            import openerp as odoo
        else:
            import odoo  # noqa
        odoo.tools.config.parse_config(None)
        odoo.service.db.exp_drop(dbname(version))
    except ImportError:
        print('Could not import odoo')
        exit(1)


@task
def tests_prepare_config(ctx, version, source, target):
    assert_version(version)
    assert source and target
    with open(source, 'rU') as source_file:
        config_content = source_file.readlines()

    for idx, line in enumerate(config_content):
        if line.startswith('db_name'):
            config_content[idx] = 'db_name = {}\n'.format(dbname(version))

    with open(target, 'w') as config_file:
        for line in config_content:
            config_file.write(line)


@task(default=True)
def tests_prepare_version(ctx, version):
    tests_prepare(ctx, version)
    config_file = '/tmp/test-anthem-config-%s.cfg' % version
    tests_prepare_config(ctx, version, 'tests/config/odoo.cfg', config_file)
    tests_createdb(ctx, version)


tests.add_task(tests_prepare_version, 'prepare-version')
tests.add_task(tests_createdb, 'createdb')
tests.add_task(tests_dropdb, 'dropdb')
tests.add_task(tests_prepare, 'prepare')
tests.add_task(tests_prepare_config, 'prepare-config')
