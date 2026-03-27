"""
BolBachan Tree-Walking Interpreter
====================================
Evaluates a BolBachan AST produced by the parser.

Scoping model:
  • Global scope is a flat Environment.
  • Loop / if bodies share the enclosing scope (no new scope boundary).
  • Each function call gets an isolated copy of the global environment
    plus its own local bindings — functions cannot mutate globals.
  • 'rakho x = val' creates or updates x in the current environment.
"""

from .errors import (
    BolBachanError,
    UndefinedVariable,
    UndefinedFunction,
    ArityError,
    DivisionByZero,
    ReturnSignal,
)


# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

class Environment:
    """Simple variable store with copy-on-call isolation for functions."""

    def __init__(self):
        self._bindings: dict = {}

    # -- Access --

    def get(self, name: str):
        if name in self._bindings:
            return self._bindings[name]
        raise UndefinedVariable(f"'{name}' is not defined — did you forget 'rakho {name} = ...'?")

    def set(self, name: str, value):
        self._bindings[name] = value

    def has(self, name: str) -> bool:
        return name in self._bindings

    # -- Isolation --

    def copy(self) -> "Environment":
        new = Environment()
        new._bindings = self._bindings.copy()
        return new

    def __repr__(self):
        return f"Environment({self._bindings})"


# ---------------------------------------------------------------------------
# Interpreter
# ---------------------------------------------------------------------------

class Interpreter:
    """Walks the AST and executes each node."""

    def __init__(self):
        self.env = Environment()
        self.functions: dict = {}   # name → (params, body)

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self, ast):
        """Execute a full program AST. Returns None."""
        self.eval(ast)

    # ------------------------------------------------------------------
    # Core dispatcher
    # ------------------------------------------------------------------

    def eval(self, node):  # noqa: C901 (intentionally large dispatch)
        if node is None:
            return None

        kind = node[0]

        # ── Top-level ──────────────────────────────────────────────
        if kind == "program":
            for stmt in node[1]:
                self.eval(stmt)

        # ── Variables ──────────────────────────────────────────────
        elif kind == "declare":
            _, var_type, var_name = node
            if not self.env.has(var_name):
                self.env.set(var_name, None)   # forward declaration

        elif kind == "assign":
            _, name, expr = node
            self.env.set(name, self.eval(expr))

        elif kind == "var":
            _, name = node
            return self.env.get(name)

        # ── Output ─────────────────────────────────────────────────
        elif kind == "print":
            value = self.eval(node[1])
            print(self._display(value))

        # ── Literals ───────────────────────────────────────────────
        elif kind == "number":
            return node[1]
        elif kind == "float":
            return node[1]
        elif kind == "string":
            return node[1]
        elif kind == "bool":
            return node[1]   # already a Python bool from parser

        # ── Arithmetic ─────────────────────────────────────────────
        elif kind == "binary_op":
            _, op, left_node, right_node = node
            left  = self.eval(left_node)
            right = self.eval(right_node)
            return self._binary_op(op, left, right)

        # ── Relational ─────────────────────────────────────────────
        elif kind == "relational_op":
            _, op, left_node, right_node = node
            left  = self.eval(left_node)
            right = self.eval(right_node)
            return self._relational_op(op, left, right)

        # ── Logical ────────────────────────────────────────────────
        elif kind == "logical_op":
            _, op, left_node, right_node = node
            if op == "&":
                return bool(self.eval(left_node)) and bool(self.eval(right_node))
            elif op == "|":
                return bool(self.eval(left_node)) or bool(self.eval(right_node))

        elif kind == "not_op":
            return not bool(self.eval(node[1]))

        # ── Increment / Decrement ──────────────────────────────────
        elif kind == "unary_op":
            _, op, var_name = node
            current = self.env.get(var_name)
            if op == "++":
                self.env.set(var_name, current + 1)
                return current + 1
            elif op == "--":
                self.env.set(var_name, current - 1)
                return current - 1

        # ── Ternary ────────────────────────────────────────────────
        elif kind == "ternary":
            _, cond, true_expr, false_expr = node
            return self.eval(true_expr) if self.eval(cond) else self.eval(false_expr)

        # ── Control Flow ───────────────────────────────────────────
        elif kind == "if_else":
            _, cond, then_block, else_block = node
            if self.eval(cond):
                for stmt in then_block:
                    self.eval(stmt)
            else:
                for stmt in else_block:
                    self.eval(stmt)

        elif kind == "if":
            _, cond, then_block = node
            if self.eval(cond):
                for stmt in then_block:
                    self.eval(stmt)

        elif kind == "while":
            _, cond, body = node
            while self.eval(cond):
                for stmt in body:
                    self.eval(stmt)

        elif kind == "for":
            _, init, cond, post, body = node
            self.eval(init)
            while self.eval(cond):
                for stmt in body:
                    self.eval(stmt)
                self.eval(post)

        # ── Functions ──────────────────────────────────────────────
        elif kind == "function_def":
            _, name, params, body = node
            self.functions[name] = (params, body)

        elif kind == "function_call":
            return self._call_function(node)

        elif kind == "return":
            _, expr = node
            raise ReturnSignal(self.eval(expr))

        else:
            raise BolBachanError(f"Unknown AST node: '{kind}'")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _binary_op(self, op, left, right):
        if op == "jodo":
            # Support string concatenation via jodo
            if isinstance(left, str) or isinstance(right, str):
                return self._display(left) + self._display(right)
            return left + right
        if op == "ghatao":
            return left - right
        if op == "guna":
            return left * right
        if op == "bhaag":
            if right == 0:
                raise DivisionByZero(
                    "Cannot divide by zero (bhaag se shoonya nahi ho sakta!)"
                )
            # Integer divide if both operands are ints, else float divide
            if isinstance(left, int) and isinstance(right, int):
                return left // right
            return left / right
        raise BolBachanError(f"Unknown binary operator: '{op}'")

    def _relational_op(self, op, left, right):
        ops = {
            "badaHai":    lambda a, b: a > b,
            "chhotaHai":  lambda a, b: a < b,
            "barabarHai": lambda a, b: a == b,
            "naBrabar":   lambda a, b: a != b,
        }
        if op not in ops:
            raise BolBachanError(f"Unknown relational operator: '{op}'")
        return ops[op](left, right)

    def _call_function(self, node):
        _, name, arg_nodes = node
        if name not in self.functions:
            raise UndefinedFunction(
                f"Function '{name}' is not defined — "
                f"declare it with 'function {name}(...){{...}}'"
            )
        params, body = self.functions[name]
        if len(params) != len(arg_nodes):
            raise ArityError(
                f"'{name}' expects {len(params)} argument(s), "
                f"got {len(arg_nodes)}"
            )

        # Evaluate arguments in the *caller's* environment
        arg_values = [self.eval(arg) for arg in arg_nodes]

        # Create an isolated local environment seeded with current globals
        saved_env = self.env
        local_env = saved_env.copy()
        for param, value in zip(params, arg_values):
            local_env.set(param, value)

        self.env = local_env
        result = None
        try:
            for stmt in body:
                self.eval(stmt)
        except ReturnSignal as sig:
            result = sig.value
        finally:
            self.env = saved_env   # always restore caller's environment

        return result

    def _display(self, value):
        """Format a value for bolBhai output."""
        if value is True:
            return "sahi"
        if value is False:
            return "galat"
        if value is None:
            return "khaali"
        return str(value)
