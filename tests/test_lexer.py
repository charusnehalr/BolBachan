"""
BolBachan Lexer Tests
=====================
Verifies that the lexer produces correct token streams.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from bolbachan.lexer import make_lexer
from bolbachan.errors import LexError


def tokenize(source: str) -> list:
    """Return list of (type, value) tuples for source."""
    lex = make_lexer()
    lex.input(source)
    return [(tok.type, tok.value) for tok in lex]


class TestKeywords:
    def test_rakho(self):
        assert tokenize("rakho")[0] == ("ASSIGN", "rakho")

    def test_bolBhai(self):
        assert tokenize("bolBhai")[0] == ("PRINT", "bolBhai")

    def test_agar(self):
        assert tokenize("agar")[0] == ("AGAR", "agar")

    def test_toh(self):
        assert tokenize("toh")[0] == ("TOH", "toh")

    def test_nahiToh(self):
        assert tokenize("nahiToh")[0] == ("NAHITOH", "nahiToh")

    def test_jabTak(self):
        assert tokenize("jabTak")[0] == ("JABTAK", "jabTak")

    def test_baarBaar(self):
        assert tokenize("baarBaar")[0] == ("BAARBAAR", "baarBaar")

    def test_jodo(self):
        assert tokenize("jodo")[0] == ("PLUS", "jodo")

    def test_ghatao(self):
        assert tokenize("ghatao")[0] == ("MINUS", "ghatao")

    def test_guna(self):
        assert tokenize("guna")[0] == ("TIMES", "guna")

    def test_bhaag(self):
        assert tokenize("bhaag")[0] == ("DIVIDE", "bhaag")

    def test_badaHai(self):
        assert tokenize("badaHai")[0] == ("GT", "badaHai")

    def test_chhotaHai(self):
        assert tokenize("chhotaHai")[0] == ("LT", "chhotaHai")

    def test_barabarHai(self):
        assert tokenize("barabarHai")[0] == ("EQ", "barabarHai")

    def test_naBrabar(self):
        assert tokenize("naBrabar")[0] == ("NEQ", "naBrabar")

    def test_bool_true(self):
        assert tokenize("true")[0] == ("BOOL", "true")

    def test_bool_false(self):
        assert tokenize("false")[0] == ("BOOL", "false")

    def test_bool_sahi(self):
        assert tokenize("sahi")[0] == ("BOOL", "sahi")

    def test_bool_galat(self):
        assert tokenize("galat")[0] == ("BOOL", "galat")

    def test_function(self):
        assert tokenize("function")[0] == ("FUNCTION", "function")

    def test_wapis(self):
        assert tokenize("wapis")[0] == ("RETURN", "wapis")


class TestLiterals:
    def test_integer(self):
        assert tokenize("123")[0] == ("NUMBER", 123)

    def test_float(self):
        assert tokenize("3.14")[0] == ("FLOAT_NUM", 3.14)

    def test_string(self):
        assert tokenize('"hello world"')[0] == ("STRING", "hello world")

    def test_string_strips_quotes(self):
        tok = tokenize('"BolBachan"')[0]
        assert tok == ("STRING", "BolBachan")


class TestSymbols:
    def test_assign_op(self):
        assert tokenize("=")[0] == ("ASSIGN_OP", "=")

    def test_incr(self):
        assert tokenize("++")[0] == ("INCR", "++")

    def test_decr(self):
        assert tokenize("--")[0] == ("DECR", "--")

    def test_lparen(self):
        assert tokenize("(")[0] == ("LPAREN", "(")

    def test_semi(self):
        assert tokenize(";")[0] == ("SEMI", ";")

    def test_and(self):
        assert tokenize("&")[0] == ("AND", "&")

    def test_or(self):
        assert tokenize("|")[0] == ("OR", "|")

    def test_not(self):
        assert tokenize("!")[0] == ("NOT", "!")

    def test_ternary(self):
        toks = tokenize("? :")
        assert toks[0] == ("QMARK", "?")
        assert toks[1] == ("COLON", ":")


class TestComments:
    def test_line_comment_ignored(self):
        toks = tokenize("// this is a comment\nrakho")
        assert len(toks) == 1
        assert toks[0][0] == "ASSIGN"

    def test_inline_comment(self):
        toks = tokenize("rakho // comment")
        assert len(toks) == 1

    def test_comment_does_not_affect_lineno(self):
        lex = make_lexer()
        lex.input("// line one\nrakho")
        toks = list(lex)
        assert toks[0].lineno == 2


class TestIdentifiers:
    def test_simple_id(self):
        assert tokenize("myVar")[0] == ("ID", "myVar")

    def test_underscore_id(self):
        assert tokenize("my_var")[0] == ("ID", "my_var")

    def test_camel_case_id(self):
        assert tokenize("myVariable123")[0] == ("ID", "myVariable123")


class TestErrors:
    def test_illegal_char(self):
        with pytest.raises(LexError):
            tokenize("@")
