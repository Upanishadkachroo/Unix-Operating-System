#include <iostream>
#include "calculator.h"

using namespace std;

int main() {
    double a, b;
    char op;

    cout << "OpenCalc - C++ Calculator\n";

    cout << "Enter expression (e.g. 10 + 5): ";

    cin >> a >> op >> b;

    try {
        switch (op) {
            case '+':
                cout << Calculator::add(a, b);
                break;

            case '-':
                cout << Calculator::subtract(a, b);
                break;

            case '*':
                cout << Calculator::multiply(a, b);
                break;

            case '/':
                cout << Calculator::divide(a, b);
                break;

            case '%':
                if (a != static_cast<int>(a) ||
                    b != static_cast<int>(b)) {
                    throw runtime_error(
                        "Modulo requires integers"
                    );
                }

                cout << Calculator::modulo(
                    static_cast<int>(a),
                    static_cast<int>(b)
                );
                break;

            default:
                cout << "Invalid operator\n";
                return 1;
        }
    }
    catch (const exception& e) {
        cerr << "Error: " << e.what() << '\n';
        return 1;
    }

    cout << '\n';
    return 0;
}
