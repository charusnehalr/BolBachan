"""
BolBachan Error Hierarchy
=========================
All runtime and compile-time errors raised by BolBachan.
"""


class BolBachanError(Exception):
    """Base class for all BolBachan language errors."""

    def __init__(self, message, line=None):
        self.line = line
        location = f" [line {line}]" if line else ""
        super().__init__(f"BolBachan Error{location}: {message}")


class LexError(BolBachanError):
    """Raised when the lexer encounters an unrecognized character."""


class ParseError(BolBachanError):
    """Raised when the parser encounters a syntax error."""


class UndefinedVariable(BolBachanError):
    """Raised when a variable is used before it is defined."""


class UndefinedFunction(BolBachanError):
    """Raised when a function is called before it is defined."""


class ArityError(BolBachanError):
    """Raised when a function is called with the wrong number of arguments."""


class TypeError(BolBachanError):
    """Raised on invalid operand types for an operation."""


class DivisionByZero(BolBachanError):
    """Raised when dividing by zero (bhaag se shoonya nahi kar sakte!)."""


class ReturnSignal(Exception):
    """
    Internal control-flow signal for function return.
    Not a real error — used to unwind the call stack.
    """

    def __init__(self, value):
        self.value = value
