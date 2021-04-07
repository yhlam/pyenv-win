import subprocess

import pytest

from test_pyenv import TestPyenvBase


class TestPyenvFeatureExec(TestPyenvBase):
    @pytest.mark.parametrize(
        "command",
        [
            lambda setup: [str(setup / "pyenv.bat"), "exec", "python"],
            lambda setup: [str(setup.parent / "shims"/ "python.bat")],
        ],
        ids=["pyenv exec", "python shim"],
    )
    @pytest.mark.parametrize(
        "arg",
        [
            "Hello",
            "Hello World",
            "Hello 'World'",
            'Hello "World"',
            "Hello %World%",
            "Hello %22World%22",
            "Hello !World!",
            "Hello #World#",
            "Hello World'",
            'Hello World"',
            "Hello ''World'",
            'Hello ""World"',
        ],
        ids=[
            "One Word",
            "Two Words",
            "Single Quote",
            "Double Quote",
            "Percentage",
            "Escaped",
            "Exclamation Mark",
            "Pound",
            "One Single Quote",
            "One Double Quote",
            "Imbalance Single Quote",
            "Imbalance Double Quote",
        ]
    )
    def test_arg(self, setup, command, arg):
        result = subprocess.run(
            [*command(setup), "-c", "import sys;print(sys.argv[1])", arg],
            capture_output=True,
            encoding="utf8",
        )
        assert result.stdout == arg + "\n"
