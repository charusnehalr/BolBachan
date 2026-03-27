int a;
int b;
bool flag;
string greeting;

rakho a = 15;
rakho b = 5;
rakho flag = true;
rakho greeting = "Namaste BolBachchan";

rakho result1 = true & false;
rakho result2 = true | false;
rakho result3 = false barabarHai false;

rakho sum = a jodo b;
rakho diff = a ghatao b;
rakho product = a guna b;
rakho quotient = a bhaag b;

rakho isGreater = a badaHai b;
rakho isLess = a chhotaHai b;
rakho isEqual = a barabarHai b;

bolBhai(greeting);

rakho c = 100;

rakho whoIsBigger = (a badaHai b) ? "a is bigger" : "b is bigger";
bolBhai(whoIsBigger);

agar (a barabarHai 15) toh {
    bolBhai("a is 15");
} nahiToh {
    bolBhai("a is not 15");
}

baarBaar (rakho i = 0; i chhotaHai 3; i = i jodo 1) {
    bolBhai("for i:");
    bolBhai(i);
}

rakho counter = 0;
jabTak (counter chhotaHai 3) {
    bolBhai("while counter:");
    bolBhai(counter);
    rakho counter = counter jodo 1;
}

bolBhai(a);
bolBhai(flag);
bolBhai(greeting);
bolBhai(result1);
