import py


def test_there_are_not_fixture_duplicates(testdir):
    sub1 = testdir.mkpydir("sub1")
    sub2 = testdir.mkpydir("sub2")
    sub1.join("conftest.py").write(py.code.Source("""
        import pytest

        @pytest.fixture
        def arg1(request):
            pass
    """))
    sub2.join("conftest.py").write(py.code.Source("""
        import pytest

        @pytest.fixture
        def arg2(request):
            pass
    """))
    sub1.join("test_in_sub1.py").write("def test_1(arg1): pass")
    sub2.join("test_in_sub2.py").write("def test_2(arg2): pass")

    result = testdir.runpytest("--show-fixture-duplicates")

    assert result.stdout.lines.count('arg1') == 0


def test_there_are_fixture_duplicates(testdir):

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

    result = testdir.runpytest('--show-fixture-duplicates')
    assert result.stdout.lines.count('arg1') == 2
