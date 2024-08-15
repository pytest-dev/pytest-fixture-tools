import py


def test_fixture_graph_created(testdir):
    """Check that --fixture-graph will create the graph .dot file"""
    sub1 = testdir.mkpydir("sub1")
    sub2 = testdir.mkpydir("sub1/sub2")
    sub1.join("conftest.py").write(py.code.Source("""
        import pytest

        @pytest.fixture
        def arg1(request):
            pass
    """))
    sub2.join("conftest.py").write(py.code.Source("""
        import pytest

        @pytest.fixture
        def arg1(request):
            pass
    """))
    sub1.join("test_in_sub1.py").write("def test_1(arg1): pass")
    sub2.join("test_in_sub2.py").write("def test_2(arg1): pass")

    result = testdir.runpytest_subprocess('--fixture-graph', '-s', '--fixture-graph-output-type', 'dot')

    result.stdout.fnmatch_lines("created artifacts/fixture-graph-sub1-test_in_sub1.py__test_1.dot.")
    result.stdout.fnmatch_lines('created artifacts/fixture-graph-sub1-sub2-test_in_sub2.py__test_2.dot.')
