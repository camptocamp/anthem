Anthem: make your Odoo scripts sing 🐜🎵
========================================

.. image:: https://travis-ci.org/camptocamp/anthem.svg?branch=master
    :target: https://travis-ci.org/camptocamp/anthem

Anthem is a tool to help scripting Odoo instances for automated setup,
upgrades, testing and more.

It should be an alternative to the other tools like ``oerpscenario``.


Make your own songs
-------------------

Writing your songs is as easy as creating a Python Package. The
songs functions called by anthem must have a positional ``ctx``
argument.

::

  ## songs/install.py

  def setup_company(ctx):
      """ Setup company """
      company = ctx.env.ref('base.main_company')
      company.name = 'My Company'


  def main(ctx):
      setup_company(ctx)


Logs
----

A song can display some logs when executed with ``@anthem.log``,
``Context.log`` and ``Context.log_line``.

::

  import anthem

  @anthem.log
  def setup_company(ctx):
     """ Setting up company """
     company = ctx.env.ref('base.main_company')
     with ctx.log('Changing name'):
         company.name = 'My Company'
         ctx.log_line('Name changed')
     with ctx.log('Loading a logo'):
         company.logo = b64encode(LOGO_CONTENT)
         ctx.log_line('Logo changed')


The decorator on the function will display the first line of the docstring.
Both the decorator and the context manager will show the timing of the
execution. The upper example gives::

  Setting up company...
      Changing name...
          Name changed
      Changing name: 0.0150s
      Loading a logo...
          Logo changed
      Loading a logo: 0.100s
  Setting up company: 0.300s


Execute your songs
------------------

Use the command line ``anthem``. Provided your songs and ``openerp`` are in the
``PYTHONPATH``::

  anthem songs.install::main -c path/to/openerp.cfg

Anthem will execute the function ``main`` of the module ``songs.install`` with
a ``ctx`` initialized with an Odoo ``env``.

Instead of using ``-c`` for the command line, you can export the environment
variable ``OPENERP_SERVER`` with the path of the configuration file.

::

  export OPENERP_SERVER=path/to/openerp.cfg
  anthem songs.install::main

In order to have ``openerp`` in the ``PYTHONPATH``, you might install it as a
package with ``pip install -e`` or directly modify the ``PYTHONPATH``.

In order to have your ``songs`` in the ``PYTHONPATH``, the better is to make a
Python package out of them.

Testing
-------

Dependencies
~~~~~~~~~~~~

To run the tests, you must have Postgresql running, with accesses for your user
(or you will have to modify ``tests/config/odoo.cfg`` with your database
username and password).

Run the tests
~~~~~~~~~~~~~

To run ``anthem``'s tests, it is a good idea to do an *editable* install of it
in a virtualenv. You must also prepare the environment by installing odoo packages.

Odoo 9.0 (Python 2)::

  $ git clone https://github.com/camptocamp/anthem.git
  Cloning into 'anthem'...
  $ cd anthem
  $ virtualenv -p python2 env-9.0
  $ source env-9.0/bin/activate
  $ pip install -e .
  $ pip install pytest invoke
  $ invoke tests.prepare-version 9.0
  $ OPENERP_SERVER=/tmp/test-anthem-config-9.0.cfg py.test -s tests

Odoo 10.0 (Python 2)::

  $ git clone https://github.com/camptocamp/anthem.git
  Cloning into 'anthem'...
  $ cd anthem
  $ virtualenv -p python2 env-10.0
  $ source env-10.0/bin/activate
  $ pip install -e .
  $ pip install pytest invoke
  $ invoke tests.prepare-version 10.0
  $ OPENERP_SERVER=/tmp/test-anthem-config-10.0.cfg py.test -s tests

Odoo 11.0 (Python 3)::

  $ git clone https://github.com/camptocamp/anthem.git
  Cloning into 'anthem'...
  $ cd anthem
  $ virtualenv -p python3 anthem-env-11.0
  $ source anthem-env-11.0/bin/activate
  $ pip install -e .
  $ pip install pytest invoke
  $ invoke tests.prepare-version 11.0
  $ OPENERP_SERVER=/tmp/test-anthem-config-11.0.cfg py.test -s tests

If need be, you can drop the test database with (adapt the version)::

  $ invoke tests.dropdb 9.0

These steps will download the nightly release of Odoo install it as a package
then install a database, so tests can be run against it (and that's also why it
is important to use a virtualenv!)

When calling ``pytest``, you have to define the ``OPENERP_SERVER`` environment
variable with the configuration file for the Odoo database that will be used
for the tests.
