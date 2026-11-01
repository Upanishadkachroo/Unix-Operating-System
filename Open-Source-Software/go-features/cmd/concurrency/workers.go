package main

import (
    "fmt"
    "time"
)

// Worker receives and processes tasks.
func worker(id int, tasks <-chan int) {
    for task := range tasks {
        fmt.Printf("Worker %d processing task %d\n", id, task)

        // Simulate some processing time.
        time.Sleep(500 * time.Millisecond)

        fmt.Printf("Worker %d completed task %d\n", id, task)
    }
}
