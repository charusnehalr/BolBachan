"""
BolBachan Interpreter Tests
============================
Tests the semantic behaviour of the tree-walking interpreter.
"""

import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from bolbachan.interpreter import Interpreter
from bolbachan.errors import (
    UndefinedVariable,
    UndefinedFunction,
    ArityError,
    DivisionByZero,
)
from tests.conftest import parse_and_run


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run(source: str) -> Interpreter:
    return parse_and_run(source)


def get(source: str, var: str):
    return run(source).env.get(var)


# ---------------------------------------------------------------------------
# Literals
# ---------------------------------------------------------------------------

class TestLiterals:
    def test_number(self):
        assert get("rakho x = 42;", "x") == 42

    def test_negative_via_subtraction(self):
        assert get("rakho x = 0 ghatao 5;", "x") == -5

    def test_string(self):
        assert get('rakho s = "hello";', "s") == "hello"

    def test_bool_true(self):
        assert get("rakho b = true;", "b") is True

    def test_bool_false(self):
        assert get("rakho b = false;", "b") is False

    def test_bool_sahi(self):
        assert get("rakho b = sahi;", "b") is True

    def test_bool_galat(self):
        assert get("rakho b = galat;", "b") is False


# ---------------------------------------------------------------------------
# Arithmetic
# ---------------------------------------------------------------------------

class TestArithmetic:
    def test_add(self):
        assert get("rakho r = 3 jodo 4;", "r") == 7

    def test_subtract(self):
        assert get("rakho r = 10 ghatao 3;", "r") == 7

    def test_multiply(self):
        assert get("rakho r = 6 guna 7;", "r") == 42

    def test_divide(self):
        assert get("rakho r = 10 bhaag 3;", "r") == 3   # integer division

    def test_divide_by_zero(self):
        with pytest.raises(DivisionByZero):
            run("rakho r = 10 bhaag 0;")

    def test_precedence_mul_before_add(self):
        # 2 + 3 * 4 should be 14, not 20
        assert get("rakho r = 2 jodo 3 guna 4;", "r") == 14

    def test_string_concat(self):
        assert get('rakho r = "Hello" jodo " World";', "r") == "Hello World"

    def test_string_num_concat(self):
        assert get('rakho r = "x=" jodo 5;', "r") == "x=5"


# ---------------------------------------------------------------------------
# Relational & Logical
# ---------------------------------------------------------------------------

class TestRelational:
    def test_gt_true(self):
        assert get("rakho r = 5 badaHai 3;", "r") is True

    def test_gt_false(self):
        assert get("rakho r = 3 badaHai 5;", "r") is False

    def test_lt(self):
        assert get("rakho r = 3 chhotaHai 5;", "r") is True

    def test_eq_true(self):
        assert get("rakho r = 5 barabarHai 5;", "r") is True

    def test_eq_false(self):
        assert get("rakho r = 5 barabarHai 6;", "r") is False

    def test_neq(self):
        assert get("rakho r = 5 naBrabar 6;", "r") is True

    def test_logical_and(self):
        assert get("rakho r = true & false;", "r") is False

    def test_logical_or(self):
        assert get("rakho r = true | false;", "r") is True

    def test_logical_not(self):
        assert get("rakho r = !true;", "r") is False


# ---------------------------------------------------------------------------
# Ternary
# ---------------------------------------------------------------------------

class TestTernary:
    def test_ternary_true_branch(self):
        assert get("rakho r = true ? 1 : 2;", "r") == 1

    def test_ternary_false_branch(self):
        assert get("rakho r = false ? 1 : 2;", "r") == 2

    def test_ternary_with_comparison(self):
        assert get("rakho r = (10 badaHai 5) ? \"yes\" : \"no\";", "r") == "yes"


# ---------------------------------------------------------------------------
# Control Flow
# ---------------------------------------------------------------------------

class TestControlFlow:
    def test_if_taken(self):
        i = run("rakho x = 0; agar (true) toh { rakho x = 1; }")
        assert i.env.get("x") == 1

    def test_if_not_taken(self):
        i = run("rakho x = 0; agar (false) toh { rakho x = 1; }")
        assert i.env.get("x") == 0

    def test_if_else_true(self):
        i = run("rakho x = 0; agar (true) toh { rakho x = 1; } nahiToh { rakho x = 2; }")
        assert i.env.get("x") == 1

    def test_if_else_false(self):
        i = run("rakho x = 0; agar (false) toh { rakho x = 1; } nahiToh { rakho x = 2; }")
        assert i.env.get("x") == 2

    def test_while(self):
        i = run("""
            rakho n = 0;
            jabTak (n chhotaHai 5) {
                rakho n = n jodo 1;
            }
        """)
        assert i.env.get("n") == 5

    def test_for_loop_sum(self):
        i = run("""
            rakho total = 0;
            baarBaar (rakho i = 1; i chhotaHai 6; i = i jodo 1) {
                rakho total = total jodo i;
            }
        """)
        assert i.env.get("total") == 15

    def test_for_loop_counter(self):
        i = run("""
            rakho c = 0;
            baarBaar (rakho i = 0; i chhotaHai 10; i = i jodo 1) {
                rakho c = c jodo 1;
            }
        """)
        assert i.env.get("c") == 10


# ---------------------------------------------------------------------------
# Increment / Decrement
# ---------------------------------------------------------------------------

class TestUnaryOps:
    def test_increment(self):
        i = run("rakho x = 5; rakho y = x++;")
        assert i.env.get("x") == 6

    def test_decrement(self):
        i = run("rakho x = 5; rakho y = x--;")
        assert i.env.get("x") == 4


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

class TestFunctions:
    def test_simple_return(self):
        i = run("""
            function double(n) {
                wapis n guna 2;
            }
            rakho r = double(7);
        """)
        assert i.env.get("r") == 14

    def test_multiple_params(self):
        i = run("""
            function add(a, b) {
                wapis a jodo b;
            }
            rakho r = add(3, 4);
        """)
        assert i.env.get("r") == 7

    def test_recursion_factorial(self):
        i = run("""
            function factorial(n) {
                agar (n chhotaHai 2) toh {
                    wapis 1;
                }
                wapis n guna factorial(n ghatao 1);
            }
            rakho r = factorial(5);
        """)
        assert i.env.get("r") == 120

    def test_recursion_fibonacci(self):
        i = run("""
            function fib(n) {
                agar (n chhotaHai 2) toh {
                    wapis n;
                }
                wapis fib(n ghatao 1) jodo fib(n ghatao 2);
            }
            rakho r = fib(10);
        """)
        assert i.env.get("r") == 55

    def test_undefined_function(self):
        with pytest.raises(UndefinedFunction):
            run("rakho r = foo(1);")

    def test_arity_error(self):
        with pytest.raises(ArityError):
            run("""
                function add(a, b) { wapis a jodo b; }
                rakho r = add(1);
            """)

    def test_functions_do_not_mutate_globals(self):
        """Functions operate on a local copy; globals should be unchanged."""
        i = run("""
            rakho x = 10;
            function changeX() {
                rakho x = 99;
                wapis x;
            }
            rakho local = changeX();
        """)
        assert i.env.get("x") == 10
        assert i.env.get("local") == 99


# ---------------------------------------------------------------------------
# Error Handling
# ---------------------------------------------------------------------------

class TestErrors:
    def test_undefined_variable(self):
        with pytest.raises(UndefinedVariable):
            run("bolBhai(ghost);")

    def test_division_by_zero(self):
        with pytest.raises(DivisionByZero):
            run("rakho r = 10 bhaag 0;")


# ---------------------------------------------------------------------------
# Print output (integration via capsys)
# ---------------------------------------------------------------------------

class TestPrint:
    def test_print_number(self, capsys):
        run("bolBhai(42);")
        out = capsys.readouterr().out.strip()
        assert out == "42"

    def test_print_string(self, capsys):
        run('bolBhai("Namaste");')
        out = capsys.readouterr().out.strip()
        assert out == "Namaste"

    def test_print_bool_true(self, capsys):
        run("bolBhai(true);")
        out = capsys.readouterr().out.strip()
        assert out == "sahi"

    def test_print_bool_false(self, capsys):
        run("bolBhai(false);")
        out = capsys.readouterr().out.strip()
        assert out == "galat"

    def test_print_concat(self, capsys):
        run('rakho name = "World"; bolBhai("Hello " jodo name);')
        out = capsys.readouterr().out.strip()
        assert out == "Hello World"
