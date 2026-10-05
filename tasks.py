# Copyright 2016 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

import sys
from pathlib import Path

from invoke import Collection, task

ns = Collection()
tests = Collection("tests")
ns.add_collection(tests)

BASE_CONFIG = "tests/config/odoo.cfg"
ODOO_URL = "https://github.com/odoo/odoo/archive/{}.tar.gz"


def dbname(version):
    return f"anthem-test-db-{version}".replace(".", "_")


def assert_version(version):
    assert version in {f"{ver}.0" for ver in range(11, 21)}


@task
def tests_prepare(ctx, version):
    assert_version(version)
    test_dir = Path(f"odoo-{version}")
    if not test_dir.exists():
        url = ODOO_URL.format(version)
        print(f"Getting {url}")
        ctx.run(f"wget -nv -c -O odoo.tar.gz {url}")
        ctx.run("tar xfz odoo.tar.gz")
        ctx.run("rm -vf odoo.tar.gz")
    if sys.version_info[:2] == (3, 10):
        # Workaround: compilation error with Cython an Python 3.10
        ctx.run(rf"sed -i '/^\(gevent\)/ d' {test_dir}/requirements.txt")
    if float(version) <= 13.0:
        # Workaround: remove some requirements for Odoo 12 and 13
        # to avoid build errors
        ctx.run(rf"sed -i '/^\(suds-jurko\|vatnumber\)/ d' {test_dir}/requirements.txt")
        ctx.run(rf"sed -i '/\(suds-jurko\|vatnumber\)/ d' {test_dir}/setup.py")
    print("Installing odoo, now")
    ctx.run(f"pip install -r {test_dir}/requirements.txt -q")
    ctx.run(f"pip install -e {test_dir} -q")


@task
def tests_createdb(ctx, version):
    assert_version(version)
    db = dbname(version)
    print(f"Installing database {db}")
    ctx.run(f"odoo -d {db} --workers=0 --log-level=critical --stop-after-init")


@task
def tests_dropdb(ctx, version):
    assert_version(version)
    print("Dropping the database")
    try:
        import odoo  # noqa

        odoo.tools.config.parse_config(None)
        odoo.service.db.exp_drop(dbname(version))
    except ImportError:
        print("Could not import odoo")
        exit(1)


@task
def tests_prepare_config(ctx, version, source, target):
    assert_version(version)
    assert source and target

    source, target = Path(source), Path(target)
    config_content = source.read_text().splitlines(keepends=True)

    for idx, line in enumerate(config_content):
        if line.startswith("db_name"):
            config_content[idx] = f"db_name = {dbname(version)}\n"

    target.write_text("".join(config_content))
    print(f"Prepared config: {target.resolve()}")


@task(default=True)
def tests_prepare_version(ctx, version):
    tests_prepare(ctx, version)
    config_file = f"/tmp/test-anthem-config-{version}.cfg"
    tests_prepare_config(ctx, version, BASE_CONFIG, config_file)
    tests_createdb(ctx, version)


tests.add_task(tests_prepare_version, "prepare-version")
tests.add_task(tests_createdb, "createdb")
tests.add_task(tests_dropdb, "dropdb")
tests.add_task(tests_prepare, "prepare")
tests.add_task(tests_prepare_config, "prepare-config")
