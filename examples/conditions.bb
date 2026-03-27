// BolBachan — Conditionals
// agar (if), nahiToh (else), and ternary operator.

rakho score = 85;

// if-else (agar-toh-nahiToh)
agar (score badaHai 90) toh {
    bolBhai("Grade: A+");
} nahiToh {
    agar (score badaHai 80) toh {
        bolBhai("Grade: A");
    } nahiToh {
        agar (score badaHai 70) toh {
            bolBhai("Grade: B");
        } nahiToh {
            bolBhai("Grade: C ya kam");
        }
    }
}

// Ternary operator  (condition ? value_if_true : value_if_false)
rakho status = (score badaHai 50) ? "Pass" : "Fail";
bolBhai("Result: " jodo status);

// Logical operators  & (and),  | (or)
rakho isAdult  = true;
rakho hasTicket = true;
rakho canEnter  = isAdult & hasTicket;
bolBhai("Can enter cinema: " jodo canEnter);

// if without else (just agar-toh)
agar (canEnter) toh {
    bolBhai("Welcome! Enjoy the show.");
}
