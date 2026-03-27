// BolBachan — Arithmetic Operations
// Demonstrates all math operators and string concatenation.

rakho a = 42;
rakho b = 8;

bolBhai("--- Arithmetic in BolBachan ---");

// jodo  = add (+)
rakho sum = a jodo b;
bolBhai("42 jodo 8 = " jodo sum);

// ghatao = subtract (-)
rakho diff = a ghatao b;
bolBhai("42 ghatao 8 = " jodo diff);

// guna  = multiply (*)
rakho product = a guna b;
bolBhai("42 guna 8 = " jodo product);

// bhaag = integer divide (/)
rakho quotient = a bhaag b;
bolBhai("42 bhaag 8 = " jodo quotient);

// Operator precedence — should be 42 + (8 * 2) = 58, not (42 + 8) * 2 = 100
rakho precedence_test = a jodo b guna 2;
bolBhai("42 jodo 8 guna 2 = " jodo precedence_test);

// String concatenation via jodo
rakho first = "Bol";
rakho last  = "Bachan";
bolBhai(first jodo last jodo "!");
