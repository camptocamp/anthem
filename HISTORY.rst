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


0.5.0 (2016-10-12)
------------------

**Features**

- Support Odoo 10

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
