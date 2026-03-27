// BolBachan — Functions
// function keyword  +  wapis (return).

// Simple addition function
function add(a, b) {
    wapis a jodo b;
}

// Greet with a custom message
function greet(name) {
    wapis "Namaste, " jodo name jodo "!";
}

// Check if a number is even
// (uses integer-division trick: n is even if (n/2)*2 == n)
function isEven(n) {
    rakho doubled = (n bhaag 2) guna 2;
    wapis (doubled barabarHai n) ? "sahi (even)" : "galat (odd)";
}

// Compute maximum of two numbers
function max(x, y) {
    wapis (x badaHai y) ? x : y;
}

// Recursive factorial
function factorial(n) {
    agar (n chhotaHai 2) toh {
        wapis 1;
    }
    wapis n guna factorial(n ghatao 1);
}

// ── Calls ─────────────────────────────────────────────────────────────────

bolBhai(greet("BolBachan"));

rakho sum = add(17, 25);
bolBhai("17 jodo 25 = " jodo sum);

bolBhai("4 isEven? " jodo isEven(4));
bolBhai("7 isEven? " jodo isEven(7));

bolBhai("max(13, 29) = " jodo max(13, 29));

bolBhai("5! = " jodo factorial(5));
bolBhai("10! = " jodo factorial(10));
