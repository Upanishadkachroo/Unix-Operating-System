package main

import (
	"fmt"
	"sync"
	"time"
)

func worker(id int, tasks <-chan int, wg *sync.WaitGroup) {
	defer wg.Done()

	for task := range tasks {
		fmt.Printf("Worker %d processing task %d\n", id, task)

		time.Sleep(500 * time.Millisecond)

		fmt.Printf("Worker %d completed task %d\n", id, task)
	}
}
