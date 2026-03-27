// BolBachan — FizzBuzz
// The classic interview problem, BolBachan style.
// Multiples of 3 → "Fizz", multiples of 5 → "Buzz", both → "FizzBuzz"

function fizzBuzz(n) {
    // BolBachan uses integer division, so n/3*3 == n tests divisibility
    rakho divBy3 = (n bhaag 3 guna 3) barabarHai n;
    rakho divBy5 = (n bhaag 5 guna 5) barabarHai n;

    agar (divBy3 & divBy5) toh {
        wapis "FizzBuzz";
    }
    agar (divBy3) toh {
        wapis "Fizz";
    }
    agar (divBy5) toh {
        wapis "Buzz";
    }
    wapis n;
}

baarBaar (rakho i = 1; i chhotaHai 31; i = i jodo 1) {
    bolBhai(fizzBuzz(i));
}
