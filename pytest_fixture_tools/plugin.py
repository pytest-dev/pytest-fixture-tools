"""Pytest fixture tools plugin."""

import py

from _pytest.python import getlocation
from collections import defaultdict

tw = py.io.TerminalWriter()
verbose = 1


def pytest_addoption(parser):
    """Add commandline options show-fixture-duplicates and fixture."""
    group = parser.getgroup("general")
    group.addoption('--show-fixture-duplicates',
                    action="store_true", dest="show_fixture_duplicates", default=False,
                    help="show list of duplicates from available fixtures")
    group.addoption('--fixture',
                    action="store", type=str, dest="fixture_name", default='',
                    help="Name of specific fixture for which you want to get duplicates")


def pytest_cmdline_main(config):
    """Check show_fixture_duplicates option to show fixture duplicates."""
    if config.option.show_fixture_duplicates:
        show_fixture_duplicates(config)
        return 0


def show_fixture_duplicates(config):
    """Wrap pytest session to show duplicates."""
    from _pytest.main import wrap_session
    return wrap_session(config, _show_fixture_duplicates_main)


def print_duplicates(argname, fixtures, previous_argname):
    """Print duplicates with TerminalWriter."""
    if len(fixtures) > 1:
        fixtures = sorted(fixtures, key=lambda key: key[2])

        for baseid, module, bestrel, fixturedef in fixtures:

            if previous_argname != argname:
                tw.line()
                tw.sep("-", argname)
                previous_argname = argname

            if verbose <= 0 and argname[0] == "_":
                continue

            funcargspec = bestrel

            tw.line(funcargspec)


def _show_fixture_duplicates_main(config, session):
    """Preparing fixture duplicates for output."""
    session.perform_collect()
    curdir = py.path.local()

    fm = session._fixturemanager

    fixture_name = config.option.fixture_name
    available = defaultdict(list)
    arg2fixturedefs = ([fixture_name]
                       if fixture_name and fixture_name in fm._arg2fixturedefs
                       else fm._arg2fixturedefs)
    for item in session.items:
        for argname in arg2fixturedefs:
            fixturedefs = fm.getfixturedefs(argname, item.nodeid)
            assert fixturedefs is not None
            if not fixturedefs:
                continue

            for fixturedef in fixturedefs:
                loc = getlocation(fixturedef.func, curdir)

                fixture = (
                    len(fixturedef.baseid),
                    fixturedef.func.__module__,
                    curdir.bestrelpath(loc),
                    fixturedef
                )
                if fixture[2] not in [f[2] for f in available[argname]]:
                    available[argname].append(fixture)

    if fixture_name:
        print_duplicates(fixture_name, available[fixture_name], None)
    else:
        available = sorted([(key, items) for key, items in available.items()], key=lambda key: key[0])

        previous_argname = None
        for argname, fixtures in available:
            print_duplicates(argname, fixtures, previous_argname)
            previous_argname = argname
