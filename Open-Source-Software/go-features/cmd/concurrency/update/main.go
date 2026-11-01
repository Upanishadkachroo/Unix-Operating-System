package main

import (
	"fmt"
	"sync"
)

func main() {
	fmt.Println("GO CONCURRENCY DEMONSTRATION")

	tasks := make(chan int, 10)

	var workers sync.WaitGroup

	// Start 3 concurrent workers.
	for i := 1; i <= 3; i++ {
		workers.Add(1)
		go worker(i, tasks, &workers)
	}

	// Send tasks to the workers.
	for i := 1; i <= 10; i++ {
		tasks <- i
	}

	close(tasks)

	// Wait for all workers to finish.
	workers.Wait()

	demonstrateSynchronization()
}
