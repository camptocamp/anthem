.. :changelog:

Release History
===============

Unreleased
----------

**Features**

**Bugfixes**

**Improvements**

**Documentation**

**Build**

0.13.0 (2019-08-29)
-------------------

**Features**

- BREAKING: Change default `overwrite` value for
   ``lyrics.modules.update_translations`` to False

- Support odoo saas versions

**Bugfixes**

- Make ``lyrics.modules.update_translations`` Odoo >= 11.0 compatible

0.12.2 (2019-06-21)
-------------------

**Improvements**

- Add 'tracking_disable=True' as default context to load CSVs
  (avoid creating 'mail.message' records and speed up the import process)

**Build**

- Packaging: build universal wheels

0.12.1 (2018-11-09)
-------------------

**Documentation**

- Improve API docs

**Build**

- The lib is now automaticaly published to Pypi by Travis when a tag is added

0.12.0 (2018-03-19)
-------------------

**Features**

- Add a new option ``--odoo-data-path`` or env. variable ``ODOO_DATA_PATH``.
- The ``lyrics.loaders.load_csv`` method now accepts a relative path appended to the
  new option "odoo data path". Absolute paths are still allowed.

**Bugfixes**

- ``lyrics.loaders.update_translations`` is now deprecated as it was a duplicate from
  ``lyrics.modules.update_translations``

0.11.0 (2017-12-22)
-------------------

**Features**

 - Make it Python 3 and Odoo 11 compatible

**Build**

 - Switch to unicodecsv instead of custom code to handle that
 - Fix the flapping tests setup. Removed tox which was provoking that for some reason.
 - Add a lint check in build


0.10.0 (2017-09-19)
-------------------

**Bugfixes**

* Disable Odoo's xmlrpc port

**Build**

- Add 'build-release.sh' script with commands to build and upload the dist files

0.9.0 (2017-08-21)
------------------

**Features**

- New lyrics: modules.update_translations to update translations from po files
- Lyrics 'uninstall' has been moved from uninstaller.uninstall to modules.uninstall,
  previous path is still working for backward compatibility
- New lyrics context manager 'records.switch_company'


0.8.0 (2017-07-24)
------------------

**Features**

- New lyrics: Define settings like being in the interface
- Add CSV Loading columns control (columns whitelist and blacklist)

**Bugfixes**

- Fix error when loading CSV with no rows


0.7.0 (2017-04-28)
------------------

**Improvements**

- Split CSV loaders in functions to be able to get rows from a CSV or to load
  rows, enabling to modify the rows before loading them for instance
- create_or_update lyrics accepts now a model so we can change its env (user,
  context, ...)
- New lyrics to uninstall module


0.6.0 (2017-01-18)
------------------

**Features**

- CSV loaders can be used with a model in order to pass a context

**Bugfixes**

- Fix tests by installing eggs from odoo/requirements.txt


0.5.0 (2016-10-12)
------------------

**Features**

- Support Odoo 10
- Allow to specify the encoding of an imported file, default is utf8

**Bugfixes**

- 'records.add_xmlid' lyrics do no longer fail when it already exists


0.4.0 (2016-08-19)
------------------

**Features**

- New lyrics: CSV loaders from path or stream
- New ``ctx.log_line`` to print a line respecting the current indentation

**Improvements**

- Add tests for the existing lyrics

**Build**

- Finally green builds!


0.3.0 (2016-07-26)
------------------

**Features**

- Add --quiet mode

**Fixes**

- Encode the logged strings to the default encoding or utf8
- Allow to use Ctrl-c to stop anthem.
- Set openerp's loglevel to ERROR, its logs clutter anthem's own outputs

0.2.0 (2016-07-22)
------------------

**Features**

* Ability to log descriptions and timings in songs with the
  context manager ``Context.log`` and the decorator ``anthem.log``.

  ::

    from anthem import log

    @log
    def setup_company(ctx):
        """ Setup company """
        # do stuff
        with ctx.log('other stuff'):
            # do other stuff

    @log
    def load_data(ctx):
        """ Load data """
        # load

    @log
    def main(ctx):
        setup_company(ctx)
        load_data(ctx)

  If we run anthem on ``main``, we will get:

  ::

    running... main
       running... Setup company
          running... other stuff
          other stuff: 0.850s
       Setup company: 1.100s
       running... Load data
       Load data: 2.900s
    main: 4.000s

0.1.3 (2016-07-07)
------------------

**Fixes**

- Correct lyric to create or update a record

0.1.2 (2016-07-07)
------------------

- Add a lyric to create a xmlid
- Add a lyric to create or update a record

0.1.1 (2016-06-23)
------------------

- Fixed crash on non-editable install.

0.1.0 (2016-06-23)
------------------

Initial release.
