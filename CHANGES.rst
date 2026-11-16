Changelog
=========


1.2.2
-----

* Fix --fixture-graph with pytest 9.2 (use Node.nodeid) in https://github.com/pytest-dev/pytest-fixture-tools/pull/16
* Fix --show-fixture-duplicates with pytest 9.2 in https://github.com/pytest-dev/pytest-fixture-tools/pull/19
* Tighten duplicates test and fix docstring version in https://github.com/pytest-dev/pytest-fixture-tools/pull/20
* Note: with pytest 9.2 and newer, --show-fixture-duplicates reports the fixture decorator line instead of the def line.

1.2.1
-----

* Fix typo in README.rst by @lebrice in https://github.com/pytest-dev/pytest-fixture-tools/pull/10
* Fix #8 - Remove migrate setup.py to pyproject.toml by @ogajduse in https://github.com/pytest-dev/pytest-fixture-tools/pull/9
* Fix getfixturedefs call by @MaksimKravchuk in https://github.com/pytest-dev/pytest-fixture-tools/pull/12

1.2.0
-----

* Fix --fixture-graph-output-dir and --fixture-graph-output-type by @youtux in https://github.com/pytest-dev/pytest-fixture-tools/pull/5
* Python and pytest compatibility fixes by @ogajduse in https://github.com/pytest-dev/pytest-fixture-tools/pull/7
* Drop support for EOL Python versions

1.1.0
-----

* Added fixture-graph option.


1.0.0
-----

* Initial public release
