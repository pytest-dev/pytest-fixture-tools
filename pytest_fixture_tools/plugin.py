"""Pytest fixture tools plugin."""

import py
import os
import errno

from _pytest.python import getlocation
from collections import defaultdict

import pydot

tw = py.io.TerminalWriter()
verbose = 1


def mkdir_recursive(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def pytest_addoption(parser):
    """Add commandline options show-fixture-duplicates and fixture."""
    group = parser.getgroup("general")
    group.addoption('--show-fixture-duplicates',
                    action="store_true", dest="show_fixture_duplicates", default=False,
                    help="show list of duplicates from available fixtures")
    group.addoption('--fixture',
                    action="store", type=str, dest="fixture_name", default='',
                    help="Name of specific fixture for which you want to get duplicates")
    group.addoption('--fixture-graph',
                    action="store_true", dest="fixture_graph", default=False,
                    help="create .dot fixture graph for each test")


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


def pytest_runtest_setup(item):
    if item.config.option.fixture_graph and hasattr(item, "_fixtureinfo"):
        curdir = py.path.local()
        # fixtures came from function parameters names
        data = dict()
        data['func_args'] = item._fixtureinfo.argnames, 'red'
        for fixture_name, fixture_data in list(item._fixtureinfo.name2fixturedefs.items()):

            loc = getlocation(fixture_data[0].func, curdir)
            if 'pytest_vgw' in loc:
                color = 'yellow'
            else:
                color = 'green'
            data[fixture_name] = fixture_data[0].argnames, color

        graph = pydot.Dot(graph_type='digraph')

        for name, depended_list in list(data.items()):
            depended_list, color = depended_list

            node = pydot.Node(name, style="filled", fillcolor=color)
            graph.add_node(node)
            for i in depended_list:
                edge = pydot.Edge(node, i)
                graph.add_edge(edge)

        log_dir = os.environ.get('LOG_DEST_DIR', 'artifacts')
        mkdir_recursive(log_dir)
        filename = "{0}/fixture-graph-{1}".format(log_dir, item._nodeid.replace(":", "_").replace("/", "-"))
        graph.write(filename + ".dot")
        tw.line()
        tw.sep("-", "fixture-graph")
        tw.line("created at {}.dot.".format(filename))
        tw.line("You can convert it to a PNG using 'dot -Tpng {0}.dot -o {0}.png'".format(filename))
