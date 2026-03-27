int x;
int y;
bool isEven;
string message;

rakho x = 8;
rakho y = 3;
rakho isEven = (x bhaag 2) barabarHai 0;
rakho message = isEven ? "x is even" : "x is odd";
bolBhai(message);

rakho max = (x badaHai y) ? x : y;
bolBhai("Maximum value:");
bolBhai(max);

rakho sum = 0;
baarBaar (rakho i = 1; i chhotaHai 6; i = i jodo 1) {
    rakho sum = sum jodo i;
}
bolBhai("Sum of 1 to 5:");
bolBhai(sum);

rakho n = 5;
rakho fact = 1;
jabTak (n badaHai 1) {
    rakho fact = fact guna n;
    rakho n = n ghatao 1;
}
bolBhai("Factorial:");
bolBhai(fact);

rakho flag = false;
agar (flag) toh {
    bolBhai("Flag is true");
} nahiToh {
    bolBhai("Flag is false");
}
