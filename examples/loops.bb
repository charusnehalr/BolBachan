// BolBachan — Loops
// baarBaar (for) and jabTak (while).

bolBhai("--- baarBaar (for loop) ---");

// Classic counting loop
baarBaar (rakho i = 1; i chhotaHai 6; i = i jodo 1) {
    bolBhai(i);
}

bolBhai("--- jabTak (while loop) ---");

// While loop — countdown
rakho n = 5;
jabTak (n badaHai 0) {
    bolBhai("Countdown: " jodo n);
    rakho n = n ghatao 1;
}
bolBhai("Blastoff!");

bolBhai("--- Sum using baarBaar ---");

// Compute sum 1+2+...+10
rakho total = 0;
baarBaar (rakho j = 1; j chhotaHai 11; j = j jodo 1) {
    rakho total = total jodo j;
}
bolBhai("Sum 1..10 = " jodo total);

bolBhai("--- Multiplication table for 5 ---");

baarBaar (rakho k = 1; k chhotaHai 11; k = k jodo 1) {
    rakho row = "5 x " jodo k jodo " = " jodo (5 guna k);
    bolBhai(row);
}
