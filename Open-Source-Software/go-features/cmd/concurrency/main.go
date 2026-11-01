package main

import "fmt"

func main() {
    fmt.Println("GO CONCURRENCY DEMONSTRATION")

    tasks := make(chan int, 10)

    // Start 3 concurrent workers.
    for i := 1; i <= 3; i++ {
        go worker(i, tasks)
    }

    // Send tasks to the workers.
    for i := 1; i <= 10; i++ {
        tasks <- i
    }

    close(tasks)

    // Demonstrate synchronization primitives.
    demonstrateSynchronization()
}
