.. :changelog:

Release History
---------------

Unreleased
++++++++++

0.2.0 (2016-07-22)
++++++++++++++++++

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
++++++++++++++++++

**Fixes**

- Correct lyric to create or update a record

0.1.2 (2016-07-07)
++++++++++++++++++

- Add a lyric to create a xmlid
- Add a lyric to create or update a record

0.1.1 (2016-06-23)
++++++++++++++++++

- Fixed crash on non-editable install.

0.1.0 (2016-06-23)
++++++++++++++++++

Initial release.
