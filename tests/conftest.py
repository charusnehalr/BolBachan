"""
Shared test fixtures for BolBachan test suite.
"""
import sys
import os

# Ensure the src/ package is importable from the tests/ directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from bolbachan.lexer import make_lexer
from bolbachan.parser import make_parser
from bolbachan.interpreter import Interpreter


@pytest.fixture
def parser():
    return make_parser()


@pytest.fixture
def lexer():
    return make_lexer()


@pytest.fixture
def interp():
    return Interpreter()


def parse_and_run(source: str) -> Interpreter:
    """Helper: parse source and return the interpreter after execution."""
    p = make_parser()
    l = make_lexer()
    ast = p.parse(source, lexer=l)
    i = Interpreter()
    i.run(ast)
    return i
