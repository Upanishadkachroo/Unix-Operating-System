package main

import "fmt"

func calculate(a int, b int) int {
	result := a + b
	return result
}

func main() {
	x := 10
	y := 20

	answer := calculate(x, y)

	fmt.Println("Sum:", answer)
}
