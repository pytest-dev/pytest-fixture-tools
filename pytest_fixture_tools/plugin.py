import py

from _pytest.python import getlocation
from collections import defaultdict


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption('--show-fixture-duplicates',
               action="store_true", dest="show_fixture_duplicates", default=False,
               help="show list of duplicates from available fixtures")
    group.addoption('--fixture',
               action="store", type=str, dest="fixture_name", default='',
               help="Name of specific fixture for which you want to get duplicates")


def pytest_cmdline_main(config):
    if config.option.show_fixture_duplicates:
        show_fixture_duplicates(config)
        return 0


def show_fixture_duplicates(config):
    from _pytest.main import wrap_session
    return wrap_session(config, _show_fixture_duplicates_main)


def _show_fixture_duplicates_main(config, session):
    session.perform_collect()
    curdir = py.path.local()

    tw = py.io.TerminalWriter()
    verbose = config.getvalue("verbose")

    fm = session._fixturemanager

    available = defaultdict(list)
    for item in session.items:
        for argname in fm._arg2fixturedefs:
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
                if fixture not in available[argname]:
                    available[argname].append(fixture)

    def print_duplicates(argname, fixtures, currentargname=None):
        if len(fixtures) > 1:
            fixtures = sorted(fixtures, cmp=lambda x, y: cmp(x[2], y[2]))
            for baseid, module, bestrel, fixturedef in fixtures:
                if currentargname != argname:
                    if not module.startswith("_pytest."):
                        tw.line()
                        tw.sep("-", "%s" %(argname,))
                        currentargname = argname
                if verbose <= 0 and argname[0] == "_":
                    continue
                if verbose > 0:
                    funcargspec = "{bestrel}".format(bestrel=bestrel)
                else:
                    funcargspec = argname
                tw.line(funcargspec, green=True)

    fixture_name = config.option.fixture_name
    if fixture_name:
        print_duplicates(fixture_name, available[fixture_name])
    else:
        available = sorted([(key, items) for key, items in available.items()], cmp=lambda x, y: cmp(x[0], y[0]))

        for argname, fixtures in available:
            print_duplicates(argname, fixtures)