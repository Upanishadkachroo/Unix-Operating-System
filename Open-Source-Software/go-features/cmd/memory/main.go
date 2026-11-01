package main

import (
	"fmt"
	"runtime"
)

type Student struct {
	Name string
	Age  int
}

func createStudent() *Student {
	// Allocate a Student object.
	student := &Student{
		Name: "Rahul",
		Age:  21,
	}

	return student
}

func main() {
	fmt.Println("GARBAGE COLLECTION AND POINTER DEMONSTRATION")

	// Create a pointer to a Student.
	studentPtr := createStudent()

	// Access data using the pointer.
	fmt.Println("Student Name:", studentPtr.Name)
	fmt.Println("Student Age:", studentPtr.Age)

	// Modify the object through the pointer.
	studentPtr.Age = 22

	fmt.Println("Updated Age:", studentPtr.Age)

	// Display memory statistics.
	var memStats runtime.MemStats

	runtime.ReadMemStats(&memStats)

	fmt.Println("\nMemory Statistics:")
	fmt.Println("Allocated memory:", memStats.Alloc, "bytes")
	fmt.Println("Total allocated:", memStats.TotalAlloc, "bytes")
	fmt.Println("Number of garbage collections:", memStats.NumGC)

	// Request garbage collection.
	runtime.GC()

	fmt.Println("Garbage collection executed.")
}
