#!/usr/bin/env python3
"""
BolBachan CLI
=============
Run BolBachan programs or start an interactive REPL.

Usage:
    python main.py                      # start REPL
    python main.py program.bb           # run a file
    python main.py program.bb --ast     # run + print AST
    python main.py --version            # print version
"""

import sys
import os
import argparse

# Make the 'src' directory importable regardless of where main.py is called from
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from bolbachan import parse, run_string, run_file, __version__
from bolbachan.errors import BolBachanError
from bolbachan.interpreter import Interpreter
from bolbachan.lexer import make_lexer
from bolbachan.parser import make_parser

# ---------------------------------------------------------------------------
# AST pretty-printer
# ---------------------------------------------------------------------------

def print_ast(node, indent=0):
    pad = "  " * indent
    if isinstance(node, tuple):
        print(f"{pad}({node[0]}")
        for child in node[1:]:
            print_ast(child, indent + 1)
        print(f"{pad})")
    elif isinstance(node, list):
        print(f"{pad}[")
        for item in node:
            print_ast(item, indent + 1)
        print(f"{pad}]")
    else:
        print(f"{pad}{repr(node)}")


# ---------------------------------------------------------------------------
# REPL
# ---------------------------------------------------------------------------

REPL_BANNER = f"""
  +========================================+
  |  BolBachan v{__version__} -- Hinglish REPL     |
  |  Type 'chhodo' or Ctrl-D to exit      |
  +========================================+
"""

REPL_HELP = """\
REPL Commands:
  chhodo          — quit
  .ast            — toggle AST display mode
  .reset          — reset interpreter state
  .help           — show this message
"""

def repl():
    print(REPL_BANNER)
    print(REPL_HELP)

    parser  = make_parser()
    interp  = Interpreter()
    show_ast = False

    while True:
        try:
            # Multi-line input: keep reading until we see a complete statement
            lines = []
            try:
                line = input("bolbachan> ")
            except EOFError:
                print("\nAlvida!")
                break

            # REPL meta-commands
            if line.strip() == "chhodo":
                print("Alvida!")
                break
            if line.strip() == ".ast":
                show_ast = not show_ast
                print(f"AST display {'ON' if show_ast else 'OFF'}")
                continue
            if line.strip() == ".reset":
                interp = Interpreter()
                print("Interpreter state reset.")
                continue
            if line.strip() == ".help":
                print(REPL_HELP)
                continue

            lines.append(line)

            # Read continuation lines if brace is unclosed
            while lines and _needs_more(lines):
                try:
                    cont = input("         ... ")
                except EOFError:
                    break
                lines.append(cont)

            source = "\n".join(lines)
            if not source.strip():
                continue

            try:
                lexer = make_lexer()
                ast   = parser.parse(source, lexer=lexer)
                if ast is None:
                    continue
                if show_ast:
                    print("-- AST --")
                    print_ast(ast)
                    print("---------")
                interp.eval(ast)
            except BolBachanError as e:
                print(f"  ✗ {e}")
            except Exception as e:
                print(f"  ✗ Internal error: {e}")

        except KeyboardInterrupt:
            print("\n(Use 'chhodo' to exit)")


def _needs_more(lines: list) -> bool:
    """Return True if the combined source has unclosed braces."""
    combined = " ".join(lines)
    return combined.count("{") > combined.count("}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_arg_parser():
    ap = argparse.ArgumentParser(
        prog="bolbachan",
        description="BolBachan — A Hinglish programming language",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # interactive REPL
  python main.py examples/hello_world.bb  # run a program
  python main.py program.bb --ast         # show AST then run
""",
    )
    ap.add_argument("file",         nargs="?",  help=".bb source file to run")
    ap.add_argument("--ast",        action="store_true", help="print the AST before executing")
    ap.add_argument("--parse-only", action="store_true", help="parse only, do not execute")
    ap.add_argument("--version",    action="version", version=f"BolBachan {__version__}")
    return ap


def main():
    ap    = build_arg_parser()
    args  = ap.parse_args()

    # No file given → REPL
    if args.file is None:
        repl()
        return

    # File mode
    if not os.path.isfile(args.file):
        print(f"Error: File not found: '{args.file}'")
        sys.exit(1)

    with open(args.file, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        parser  = make_parser()
        lexer   = make_lexer()
        ast     = parser.parse(source, lexer=lexer)

        if args.ast or args.parse_only:
            print("-- AST ----------------------------------")
            print_ast(ast)
            print("-----------------------------------------")

        if not args.parse_only:
            interp = Interpreter()
            interp.run(ast)

    except BolBachanError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
