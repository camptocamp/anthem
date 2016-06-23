Anthem: make your Odoo scripts sing 🐜🎵
========================================

.. image:: https://travis-ci.org/camptocamp/anthem.svg?branch=master
    :target: https://travis-ci.org/camptocamp/anthem

Anthem is a tool to help scripting Odoo instances for automated setup,
upgrades, testing and more.

It should be an alternative to the other tools like ``oerpscenario``.

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
