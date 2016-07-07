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


Run the tests
-------------

To run ``anthem``'s tests, it is a good idea to to an *editable* install of it
in a virtualenv, and then intall and run ``pytest`` as follows::

  % git clone https://github.com/camptocamp/anthem.git
  Cloning into 'anthem'...
  % cd anthem
  % python2 -m virtualenv env
  % source env/bin/activate
  % pip install -e .
  % pip install pytest
  % py.test
