"""
BolBachan — A Hinglish programming language.

Public API:
    run_file(path)       — execute a .bb file
    run_string(source)   — execute BolBachan source code from a string
    parse(source)        — return the AST without executing
"""

from .lexer import make_lexer
from .parser import make_parser
from .interpreter import Interpreter
from .errors import BolBachanError

__version__ = "1.0.0"
__all__ = ["run_file", "run_string", "parse", "BolBachanError", "__version__"]

_parser = None


def _get_parser():
    global _parser
    if _parser is None:
        _parser = make_parser()
    return _parser


def parse(source: str):
    """Parse BolBachan source and return the AST tuple."""
    return _get_parser().parse(source, lexer=make_lexer())


def run_string(source: str):
    """Execute BolBachan source code given as a string."""
    ast = parse(source)
    interp = Interpreter()
    interp.run(ast)


def run_file(path: str):
    """Execute a BolBachan source file (.bb)."""
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    run_string(source)
