#include "calculator.h"
#include <stdexcept>

namespace Calculator {

double add(double a, double b) {
    return a + b;
}

double subtract(double a, double b) {
    return a - b;
}

double multiply(double a, double b) {
    return a * b;
}

double divide(double a, double b) {
    if (b == 0)
        throw std::runtime_error("Division by zero");

    return a / b;
}

// Newly added feature
int modulo(int a, int b) {
    if (b == 0)
        throw std::runtime_error("Modulo by zero");

    return a % b;
}

}
