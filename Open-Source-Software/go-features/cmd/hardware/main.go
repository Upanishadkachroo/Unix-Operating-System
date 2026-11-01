package main

import (
    "fmt"
    "runtime"
    "sync"
    "time"
)

func cpuTask(id int, wg *sync.WaitGroup) {
    defer wg.Done()

    sum := 0

    // CPU-intensive calculation.
    for i := 0; i < 100000000; i++ {
        sum += i % 100
    }

    fmt.Printf("CPU task %d completed. Result: %d\n", id, sum)
}

func main() {
    // Get the number of logical CPU cores.
    cores := runtime.NumCPU()

    fmt.Println("Number of logical CPU cores:", cores)

    // Set the maximum number of CPUs executing Go code simultaneously.
    runtime.GOMAXPROCS(cores)

    fmt.Println("GOMAXPROCS:", runtime.GOMAXPROCS(0))

    var wg sync.WaitGroup

    start := time.Now()

    // Launch CPU-intensive tasks.
    for i := 1; i <= cores; i++ {
        wg.Add(1)
        go cpuTask(i, &wg)
    }

    wg.Wait()

    elapsed := time.Since(start)

    fmt.Println("All CPU tasks completed.")
    fmt.Println("Execution time:", elapsed)
    fmt.Println("Active goroutines:", runtime.NumGoroutine())
}

