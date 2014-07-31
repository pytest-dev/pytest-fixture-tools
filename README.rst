pytest-fixture-tools: Pytest fixture tools plugin
===============================================================

The ``pytest-fixture-tools`` package is a pytest plugin which provides various tools for fixture.

.. image:: https://api.travis-ci.org/paylogic/pytest-fixture-tools.png
   :target: https://travis-ci.org/paylogic/pytest-fixture-tools
.. image:: https://pypip.in/v/pytest-fixture-tools/badge.png
   :target: https://crate.io/packages/pytest-fixture-tools/
.. image:: https://coveralls.io/repos/paylogic/pytest-fixture-tools/badge.png?branch=master
   :target: https://coveralls.io/r/paylogic/pytest-fixture-tools


Installation
------------

.. sourcecode::

    pip install pytest-fixture-tools


Usage
-----

If you have already installed ``pytest-fixture-tools`` plugin then you can use one of its commands.

``--show-fixture-duplicates`` - will collect all fixtures and print you a list of duplicates for each fixture.

With ``--show-fixture-duplicates`` you can use ``--fixture name_of_fixture`` option to get list of duplicates only for specific fixture

.. sourcecode::

    py.test tests/ --show-fixture-duplicates --fixture order

Output can look like this:

.. sourcecode::

    ========================================== test session starts ==========================================
    platform linux2 -- Python 2.7.3 -- pytest-2.5.1 -- /home/batman/.virtualenvs/arkham-city/bin/python
    Tests are shuffled using seed number 355495648184.
    cachedir: /home/batman/.virtualenvs/arkham-city/.cache
    plugins: fixture-tools, random, bdd-splinter, pep8, cov, contextfixture, bdd, xdist, instafail, cache
    collected 2347 items / 1 skipped

    ------------------------------------------------- order -------------------------------------------------
    tests/fixtures/order.py:30
    tests/unit/api/conftest.py:261


Contact
-------

If you have questions, bug reports, suggestions, etc. please create an issue on
the `GitHub project page <http://github.com/paylogic/pytest-fixture-tools>`_.


License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

See `<LICENSE.txt>`_

© 2013 Paylogic International.
