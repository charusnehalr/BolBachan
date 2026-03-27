import streamlit as st
import sys, os, io, contextlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from bolbachan.lexer import make_lexer
from bolbachan.parser import make_parser
from bolbachan.interpreter import Interpreter
from bolbachan.errors import BolBachanError

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BolBachan Playground",
    page_icon="🎬",
    layout="wide",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Hide streamlit branding */
#MainMenu, footer { visibility: hidden; }

/* Editor textarea */
textarea {
    font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace !important;
    font-size: 14px !important;
    background: #1e1e2e !important;
    color: #cdd6f4 !important;
    border: 1px solid #313244 !important;
    border-radius: 8px !important;
}

/* Output box */
.output-box {
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 14px;
    background: #181825;
    color: #a6e3a1;
    padding: 16px;
    border-radius: 8px;
    border: 1px solid #313244;
    min-height: 200px;
    white-space: pre-wrap;
    line-height: 1.6;
}

.error-box {
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 14px;
    background: #181825;
    color: #f38ba8;
    padding: 16px;
    border-radius: 8px;
    border: 1px solid #f38ba8;
    min-height: 80px;
    white-space: pre-wrap;
}

/* Keyword pills */
.pill {
    display: inline-block;
    background: #313244;
    color: #cba6f7;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 13px;
    font-family: monospace;
    margin: 2px;
}

/* Run button */
div.stButton > button {
    background: #89b4fa;
    color: #1e1e2e;
    font-weight: 700;
    font-size: 15px;
    border: none;
    border-radius: 8px;
    padding: 10px 32px;
    width: 100%;
    transition: background 0.2s;
}
div.stButton > button:hover {
    background: #74c7ec;
    color: #1e1e2e;
}
</style>
""", unsafe_allow_html=True)

# ── Examples ───────────────────────────────────────────────────────────────
EXAMPLES = {
    "Hello World": """\
// Namaste, Duniya!
bolBhai("Namaste, Duniya!");
bolBhai("Hello, World!");
""",
    "Arithmetic": """\
// All math operators
rakho a = 42;
rakho b = 8;

bolBhai("42 jodo 8 = " jodo (a jodo b));
bolBhai("42 ghatao 8 = " jodo (a ghatao b));
bolBhai("42 guna 8 = " jodo (a guna b));
bolBhai("42 bhaag 8 = " jodo (a bhaag b));

// Precedence: 2 + 3*4 = 14
bolBhai("2 jodo 3 guna 4 = " jodo (2 jodo 3 guna 4));
""",
    "If / Else": """\
rakho score = 85;

agar (score badaHai 90) toh {
    bolBhai("Grade: A+");
} nahiToh {
    agar (score badaHai 80) toh {
        bolBhai("Grade: A");
    } nahiToh {
        bolBhai("Grade: B");
    }
}

// Ternary operator
rakho label = (score badaHai 50) ? "Pass" : "Fail";
bolBhai("Result: " jodo label);
""",
    "For Loop": """\
// Count 1 to 5
baarBaar (rakho i = 1; i chhotaHai 6; i = i jodo 1) {
    bolBhai("i = " jodo i);
}

// Sum 1..10
rakho total = 0;
baarBaar (rakho j = 1; j chhotaHai 11; j = j jodo 1) {
    rakho total = total jodo j;
}
bolBhai("Sum 1..10 = " jodo total);
""",
    "While Loop": """\
rakho n = 5;
jabTak (n badaHai 0) {
    bolBhai("Countdown: " jodo n);
    rakho n = n ghatao 1;
}
bolBhai("Blastoff!");
""",
    "Functions": """\
function add(a, b) {
    wapis a jodo b;
}

function greet(name) {
    wapis "Namaste, " jodo name jodo "!";
}

function factorial(n) {
    agar (n chhotaHai 2) toh {
        wapis 1;
    }
    wapis n guna factorial(n ghatao 1);
}

bolBhai(greet("BolBachan"));
bolBhai("3 + 4 = " jodo add(3, 4));
bolBhai("5! = " jodo factorial(5));
bolBhai("10! = " jodo factorial(10));
""",
    "Fibonacci": """\
function fib(n) {
    agar (n chhotaHai 2) toh {
        wapis n;
    }
    wapis fib(n ghatao 1) jodo fib(n ghatao 2);
}

baarBaar (rakho i = 0; i chhotaHai 10; i = i jodo 1) {
    bolBhai("fib(" jodo i jodo ") = " jodo fib(i));
}
""",
    "FizzBuzz": """\
function fizzBuzz(n) {
    rakho divBy3 = (n bhaag 3 guna 3) barabarHai n;
    rakho divBy5 = (n bhaag 5 guna 5) barabarHai n;

    agar (divBy3 & divBy5) toh { wapis "FizzBuzz"; }
    agar (divBy3) toh { wapis "Fizz"; }
    agar (divBy5) toh { wapis "Buzz"; }
    wapis n;
}

baarBaar (rakho i = 1; i chhotaHai 21; i = i jodo 1) {
    bolBhai(fizzBuzz(i));
}
""",
}

# ── Interpreter helper ─────────────────────────────────────────────────────
def run_source(source: str):
    """Run BolBachan source. Returns (output, error, ast_str)."""
    output, error, ast_str = "", "", ""
    try:
        p = make_parser()
        l = make_lexer()
        ast = p.parse(source, lexer=l)

        # Capture AST
        ast_str = repr(ast)

        # Capture stdout from interpreter
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            interp = Interpreter()
            interp.run(ast)
        output = buf.getvalue()

    except BolBachanError as e:
        error = str(e)
    except Exception as e:
        error = f"Unexpected error: {e}"

    return output, error, ast_str

# ── Session state defaults ─────────────────────────────────────────────────
if "code" not in st.session_state:
    st.session_state.code = EXAMPLES["Hello World"]
if "output" not in st.session_state:
    st.session_state.output = ""
if "error" not in st.session_state:
    st.session_state.error = ""
if "ast_str" not in st.session_state:
    st.session_state.ast_str = ""

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("# 🎬 BolBachan Playground")
st.markdown("*A Hinglish programming language — `rakho`, `bolBhai`, `agar`, `jodo`, `wapis`*")
st.divider()

# ── Main layout ────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    # Example picker
    chosen = st.selectbox(
        "Load an example",
        options=list(EXAMPLES.keys()),
        index=0,
    )
    if st.button("Load Example", use_container_width=True):
        st.session_state.code = EXAMPLES[chosen]
        st.session_state.output = ""
        st.session_state.error = ""
        st.rerun()

    st.markdown("**Code Editor**")
    code = st.text_area(
        label="editor",
        value=st.session_state.code,
        height=380,
        label_visibility="collapsed",
        placeholder="Write BolBachan code here...",
    )
    st.session_state.code = code

    run_col, clear_col = st.columns([3, 1])
    with run_col:
        run_clicked = st.button("▶  Run", use_container_width=True)
    with clear_col:
        if st.button("Clear", use_container_width=True):
            st.session_state.output = ""
            st.session_state.error = ""
            st.rerun()

with col_right:
    st.markdown("**Output**")

    if run_clicked and code.strip():
        out, err, ast_str = run_source(code)
        st.session_state.output = out
        st.session_state.error = err
        st.session_state.ast_str = ast_str

    if st.session_state.error:
        st.markdown(
            f'<div class="error-box">{st.session_state.error}</div>',
            unsafe_allow_html=True,
        )
    elif st.session_state.output:
        st.markdown(
            f'<div class="output-box">{st.session_state.output}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="output-box" style="color:#585b70;">Output will appear here...</div>',
            unsafe_allow_html=True,
        )

    # AST expander
    if st.session_state.ast_str:
        with st.expander("View AST (parse tree)"):
            st.code(st.session_state.ast_str, language="python")

# ── Keyword reference ──────────────────────────────────────────────────────
st.divider()
st.markdown("### Quick Reference")

keywords = {
    "rakho": "assign / let",
    "bolBhai": "print",
    "agar / toh": "if / then",
    "nahiToh": "else",
    "jabTak": "while",
    "baarBaar": "for",
    "jodo": "+ (add / concat)",
    "ghatao": "− subtract",
    "guna": "× multiply",
    "bhaag": "÷ divide",
    "badaHai": "> greater than",
    "chhotaHai": "< less than",
    "barabarHai": "== equal",
    "naBrabar": "!= not equal",
    "function / wapis": "define / return",
    "sahi / galat": "true / false",
}

cols = st.columns(4)
items = list(keywords.items())
per_col = len(items) // 4 + 1
for i, col in enumerate(cols):
    for kw, meaning in items[i * per_col:(i + 1) * per_col]:
        col.markdown(f'`{kw}` — {meaning}')
