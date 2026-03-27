// BolBachan — Fibonacci Sequence
// Demonstrates recursion and iteration side-by-side.

// Recursive approach
function fib(n) {
    agar (n chhotaHai 2) toh {
        wapis n;
    }
    wapis fib(n ghatao 1) jodo fib(n ghatao 2);
}

bolBhai("--- Fibonacci (recursive) ---");
baarBaar (rakho i = 0; i chhotaHai 10; i = i jodo 1) {
    bolBhai("fib(" jodo i jodo ") = " jodo fib(i));
}

// Iterative approach using jabTak
bolBhai("--- Fibonacci (iterative, first 15 terms) ---");
rakho prev = 0;
rakho curr = 1;
rakho count = 0;

bolBhai(prev);
bolBhai(curr);

jabTak (count chhotaHai 13) {
    rakho next = prev jodo curr;
    bolBhai(next);
    rakho prev = curr;
    rakho curr = next;
    rakho count = count jodo 1;
}
