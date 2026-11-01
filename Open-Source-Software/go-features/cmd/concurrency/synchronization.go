package main

import (
    "fmt"
    "sync"
    "sync/atomic"
)

func demonstrateSynchronization() {
    fmt.Println("\nSYNCHRONIZATION DEMONSTRATION")

    var wg sync.WaitGroup
    var mutex sync.Mutex
    var counter int
    var atomicCounter int64

    // Run 5 goroutines.
    for i := 1; i <= 5; i++ {
        wg.Add(1)

        go func(id int) {
            defer wg.Done()

            // Mutex protects shared data.
            mutex.Lock()
            counter++
            mutex.Unlock()

            // Atomic operation safely updates a counter.
            atomic.AddInt64(&atomicCounter, 1)

            fmt.Printf("Goroutine %d executed\n", id)
        }(i)
    }

    // Wait until all goroutines finish.
    wg.Wait()

    fmt.Println("Mutex protected counter:", counter)
    fmt.Println("Atomic counter:", atomic.LoadInt64(&atomicCounter))
}
