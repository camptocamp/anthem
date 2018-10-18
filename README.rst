========================================
Anthem: make your Odoo scripts sing 🐜🎵
========================================

.. image:: https://travis-ci.org/camptocamp/anthem.svg?branch=master
    :target: https://travis-ci.org/camptocamp/anthem

Anthem is a tool to help scripting Odoo instances for automated setup,
upgrades, testing and more.

It should be an alternative to the other tools like ``oerpscenario``.


Make your own songs
===================

Writing your songs is as easy as creating a Python Package. The
songs functions called by anthem must have a positional ``ctx``
argument.

``ctx`` is essentially the execution context - you can access ``ctx.env`` from
it, which is an Odoo environment instance that you should be pretty much familiar with.

::

  ## songs/install.py

  def setup_company(ctx):
      """ Setup company """
      company = ctx.env.ref('base.main_company')
      company.name = 'My Company'


  def main(ctx):
      setup_company(ctx)


Logs
====

A song can display some logs when executed with ``@anthem.log``,
``Context.log`` and ``Context.log_line``.

.. code:: python

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
execution. The upper example gives:

.. code

  Setting up company...
      Changing name...
          Name changed
      Changing name: 0.0150s
      Loading a logo...
          Logo changed
      Loading a logo: 0.100s
  Setting up company: 0.300s


Execute your songs
==================

Use the command line ``anthem``. Provided your songs and ``openerp`` are in the
``PYTHONPATH``:

.. code

  anthem songs.install::main -c path/to/openerp.cfg

Anthem will execute the function ``main`` of the module ``songs.install`` with
a ``ctx`` initialized with an Odoo ``env``.

Instead of using ``-c`` for the command line, you can export the environment
variable ``OPENERP_SERVER`` with the path of the configuration file.

.. code

  export OPENERP_SERVER=path/to/openerp.cfg
  anthem songs.install::main

In order to have ``openerp`` in the ``PYTHONPATH``, you might install it as a
package with ``pip install -e`` or directly modify the ``PYTHONPATH``.

In order to have your ``songs`` in the ``PYTHONPATH``, the better is to make a
Python package out of them.

Testing
=======

Dependencies
------------

To run the tests, you must have Postgresql running, with accesses for your user
(or you will have to modify ``tests/config/odoo.cfg`` with your database
username and password).

Run the tests
-------------

To run ``anthem``'s tests, it is a good idea to do an *editable* install of it
in a virtualenv. You must also prepare the environment by installing odoo packages.

Odoo 9.0 (Python 2):

.. code

  $ git clone https://github.com/camptocamp/anthem.git
  Cloning into 'anthem'...
  $ cd anthem
  $ virtualenv -p python2 env-9.0
  $ source env-9.0/bin/activate
  $ pip install -e .
  $ pip install pytest invoke
  $ invoke tests.prepare-version 9.0
  $ OPENERP_SERVER=/tmp/test-anthem-config-9.0.cfg py.test -s tests

Odoo 10.0 (Python 2):

.. code

  $ git clone https://github.com/camptocamp/anthem.git
  Cloning into 'anthem'...
  $ cd anthem
  $ virtualenv -p python2 env-10.0
  $ source env-10.0/bin/activate
  $ pip install -e .
  $ pip install pytest invoke
  $ invoke tests.prepare-version 10.0
  $ OPENERP_SERVER=/tmp/test-anthem-config-10.0.cfg py.test -s tests

Odoo 11.0 (Python 3):

.. code

  $ git clone https://github.com/camptocamp/anthem.git
  Cloning into 'anthem'...
  $ cd anthem
  $ virtualenv -p python3 anthem-env-11.0
  $ source anthem-env-11.0/bin/activate
  $ pip install -e .
  $ pip install pytest invoke
  $ invoke tests.prepare-version 11.0
  $ OPENERP_SERVER=/tmp/test-anthem-config-11.0.cfg py.test -s tests

If need be, you can drop the test database with (adapt the version):

.. code

  $ invoke tests.dropdb 9.0

These steps will download the nightly release of Odoo install it as a package
then install a database, so tests can be run against it (and that's also why it
is important to use a virtualenv!)

When calling ``pytest``, you have to define the ``OPENERP_SERVER`` environment
variable with the configuration file for the Odoo database that will be used
for the tests.

Lyrics
======

Lyrics are predefined snippets written for the most commonly used cases, like:

* `Loading data`_: read (load) a data file (CSV format is supported at the moment)
* `Provide XMLIDs for records`_
* `Upserting a record`_: essentially search for the record and update it with
  given values, or create it in case it isn't there yet
* `Uninstalling a module(s)`_
* `Updating module configuration`_: pre-defining a set of settings for a particular
  module (or set of modules)

.. _loading-data:

Loading data
------------

There's an ability to supply data in a handy CSV format - Anthem is just able to
parse and load those. ``load_csv`` method is meant to be the main entrypoint for
doing so:

+--------------------+----------------------------------------------------------+
| Param              | Description                                              |
+====================+==========================================================+
| ``ctx``            | Anthem context instance                                  |
+--------------------+----------------------------------------------------------+
| ``model``          | Odoo model name or model klass from ``ctx.env``          |
+--------------------+----------------------------------------------------------+
| ``path``           | absolute or relative path to CSV file.                   |
|                    | If a relative path is given you must provide a value for |
|                    | ``ODOO_DATA_PATH`` in your environment                   |
|                    | or set ``--odoo-data-path`` option.                      |
+--------------------+----------------------------------------------------------+
| ``header``         | whitelist of CSV columns to load                         |
+--------------------+----------------------------------------------------------+
| ``header_exclude`` | blacklist of CSV columns to ignore                       |
+--------------------+----------------------------------------------------------+
| ``fmtparams``      | keyword params for ``csv_unireader``                     |
+--------------------+----------------------------------------------------------+

CSV format is similar to that of an Odoo export format, namely:
* it should contain a set of field names in a header
* each consecutive row defines a set of values to use to create records on a given model

Records
-------

This section is dedicated to methods that operate on records.

Provide XMLIDs for records
^^^^^^^^^^^^^^^^^^^^^^^^^^

This is as simple as calling ``anthem.records.add_xmlid`` with a record as a
first parameter and a desired XMLID as a second.

E.g., you have a very special ``res.partner`` record ``foo``:

.. code:: python

  from anthem.records import add_xmlid

  [...]
  @anthem.log
  def add_xmlid_to_foo(ctx):
      """Make Jhony Foo great again."""
      foo = ctx.env['res.partner'].create({
          'name': 'Jhony',
          'lastname': 'Foo',
      })
      add_xmlid(foo, '__setup__.res_partner_foo_jhony')

From now on, Jhony could be referred to as
``ctx.env.ref('__setup__.res_partner_foo_jhony')``.

Upserting a record
^^^^^^^^^^^^^^^^^^

**"Upsert"** is a commonly used term that basically stands for UPDATE or INSERT.
Anthem features a facility that is capable of executing that kind of operations
on Odoo databases. There is a method called ``anthem.records.create_or_update``
that relies on the model, a set of values and a record XMLID.

If your goal is to create the record in the first place as well as provide an
XMLID, as was shown in a previous section, ``create_or_update`` does just what
you need.

Example
+++++++

.. code:: python

  from anthem.records import create_or_update

  [...]
  @anthem.log
  def create_partner_foo(ctx):
      """Ensure that Jhony Foo is known to our Company."""
      create_or_update(
          ctx,
          model='res.partner',
          xmlid='__setup__.res_partner_foo_jhony',
          values={
              'name': 'Jhony',
              'lastname': 'Foo',
          }
      )


Upon calling, it would:

* Try to fetch the record by a given XMLID
* If the record was found:
   * Update it with the given values (call ``record.update(values)`` on it)
* Otherwise:
   * Create a record with given values (call ``model.create(values)``)
   * Provide an XMLID to it (using ``anthem.records.add_xmlid``)
* In any case: return that record back

Modules
-------

This section is dedicated to methods that operate on modules.

Uninstalling a module(s)
^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes you just need some particular module to be gone from your instance(s)
and you'd like it done programmatically, without having to reach for each
instance, search for it and hit the **"Uninstall"** button. Anthem can do the
job for you: you can simply call an ``anthem.lyrics.modules.uninstall`` with a
list of module names that you won't use anymore.

Example (given that there are modules ``foo`` and ``bar`` that you want gone):
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code:: python

  from anthem.lyrics.modules import uninstall

  [...]
  @anthem.log
  def uninstall_foo(ctx):
      """Get rid of legacy `foo` and `bar`."""
      uninstall(['foo', 'bar'])

Updating translations on module(s)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In a similar fashion, sometimes you need to update translations on a set of
modules - ``anthem.lyrics.modules.update_translations`` is there for you :wink:

Example is similar to the previous case - just call the different method instead.

Updating module configuration
=============================

By using this feature, you're able to preconfigure your module setup via Anthem
song: you'll just need a straight idea what needs to be done, an instance of a
configuration settings model for your module (model name will do as well) and a
mapping (in a form of Python dictionary) of technical configuration names with
desired values.

Here's a brief example of ``sale`` module configuration:

.. code:: python

  from anthem.lyrics import settings

  [...]
  @anthem.log
  def define_sale_settings(ctx):
      """Configure `sale` module."""
      model = ctx.env['sale.config.settings']
      # it's okay to use 'sale.config.settings' as a string though
      model = 'sale.config.settings'
      settings(ctx, model, {
          'default_invoice_policy': 'delivery',
          ...: ...,
          'et': 'cetera',
      })

Be advised: settings onchange are not triggered by this function.

Usage within Marabunta
======================

Anthem and `Marabunta <https://github.com/camptocamp/marabunta>`_ are powerful
when combined: you can call a set of songs inside Marabunta's migration steps
using following syntax:

.. code:: yaml

  ...
  - version: 10.0.1.0.0
    operations:
      pre:
        - anthem songs.upgrade.your_pre_song::main
      post:
        - anthem songs.upgrade.your_post_song::main

By using this approach, you possess the power of full-pledged Odoo
``Environment`` instance initialized on a live database while performing a
regular upgrade powered by Marabunta.

Let's say that you have to enable multicompany with inter-company transactions
on a migration to next version, lets say, 10.0.1.1.0. In this case, you'll need
a song to back this up on a Python side first:

.. code:: python

   # songs.upgrade.upgrade_10_0_1_1_0.py
   from anthem.lyrics import settings

   [...]
   @anthem.log
   def enable_multicompany(ctx):
       """Set up multicompany."""
       settings(ctx, 'base.config.settings', {
           # enable multicompany as it is
           'group_light_multi_company': True,
           # enable inter-company transactions
           'module_inter_company_rules': True,
       })

    [...]
    @anthem.log
    def main(ctx):
        enable_multicompany(ctx)

And then you'll need to call it on a migration step:

.. code:: yaml

  ...
  - version: 10.0.1.1.0
    operations:
      post:
        - anthem songs.upgrade.upgrade_10_0_1_1_0::main

Boom! Enjoy your new multicompany settings.

That's all, folks!
==================

Thanks for reading. Happy hacking and enjoy your songwriting skills!
