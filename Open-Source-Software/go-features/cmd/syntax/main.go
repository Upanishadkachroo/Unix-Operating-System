package main

import "fmt"

// Function with explicitly declared parameter and return types.
func calculate(a int, b int) int {
    result := a + b
    return result
}

func main() {
    // Short variable declarations.
    x := 10
    y := 20

    answer := calculate(x, y)

    fmt.Println("First number:", x)
    fmt.Println("Second number:", y)
    fmt.Println("Sum:", answer)
}
