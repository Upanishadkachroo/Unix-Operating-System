# Go Programming Assignments --- Concepts and Practical Guide

This README covers Go fundamentals and the practical programs
demonstrating concurrency, synchronization, CPU information, HTTP
client/server programming, garbage collection, pointers, clean syntax,
and compilation. All examples use the Go standard library.

## 1. About Go

Go (Golang) is an open-source, statically typed, compiled language
developed at Google. It is designed for readable code, fast compilation,
networking, and concurrent programming.

Common uses include backend services, REST APIs, cloud applications,
command-line tools, network servers, and DevOps utilities.

### Main features

  -----------------------------------------------------------------------
  Feature                             Explanation
  ----------------------------------- -----------------------------------
  Compiled                            Source code is compiled into
                                      executable machine code.

  Statically typed                    Types are checked by the compiler.

  Garbage collected                   Runtime reclaims memory that is no
                                      longer reachable.

  Concurrent                          Goroutines and channels support
                                      concurrent programs.

  Standard library                    Includes HTTP, JSON,
                                      synchronization, file and network
                                      packages.

  Portable                            Supports multiple operating systems
                                      and CPU architectures.

  Formatted                           `gofmt` formats code consistently.

  No pointer arithmetic               Pointers are supported, but
                                      ordinary pointer arithmetic is not.
  -----------------------------------------------------------------------

### Basic Go program

``` go
package main

import "fmt"

func main() {
    fmt.Println("Hello, Go!")
}
```

-   `package main` declares an executable package.
-   `import "fmt"` imports formatted I/O functions.
-   `func main()` is the entry point.
-   `fmt.Println()` prints output.

### Basic syntax concepts

``` go
var age int = 21
name := "Student"
const pi = 3.14159
```

`var` declares a variable, `:=` declares and initializes a local
variable with inferred type, and `const` declares a constant.

Common types include `int`, `float64`, `string`, `bool`, `byte`, and
`rune`.

Functions can return values and errors:

``` go
func add(a int, b int) int {
    return a + b
}
```

Go also supports arrays, slices, maps, structs, interfaces, methods, and
multiple return values.

## 2. Install Go on Ubuntu

Check whether Go is installed:

``` bash
go version
```

Install the Ubuntu package if needed:

``` bash
sudo apt update
sudo apt install -y golang-go
```

Verify:

``` bash
go version
which go
go env GOPATH
go env GOROOT
```

The Ubuntu repository may not contain the latest Go release. If a
specific newer version is required, use the official instructions at
https://go.dev/doc/install. Avoid having multiple Go installations
competing in `PATH`.

## 3. Create the assignment workspace

``` bash
mkdir -p ~/Unix-Operating-System/Open-Source-Software/Go-Assignments
cd ~/Unix-Operating-System/Open-Source-Software/Go-Assignments
go mod init go-assignments
```

Create the program directories:

``` bash
mkdir -p cmd/{concurrency,hardware,server,client,memory,syntax}
```

Recommended structure:

``` text
Go-Assignments/
├── go.mod
├── README.md
└── cmd/
    ├── concurrency/
    │   ├── main.go
    │   ├── workers.go
    │   └── synchronization.go
    ├── hardware/main.go
    ├── server/main.go
    ├── client/main.go
    ├── memory/main.go
    └── syntax/main.go
```

Example `go.mod`:

``` go
module go-assignments

go 1.22
```

Use a Go version directive compatible with the version installed on your
machine.

------------------------------------------------------------------------

# 4. Experiment 1 --- Multithreading and concurrency

## Theory

**Concurrency** means multiple tasks can make progress during
overlapping periods. **Parallelism** means multiple tasks execute at the
same instant, typically on different CPU cores.

A **goroutine** is a lightweight execution unit managed by the Go
runtime. Start one using the `go` keyword:

``` go
go someFunction()
```

A **channel** is a typed communication mechanism used to send values
between goroutines:

``` go
ch := make(chan int)
ch <- 10
value := <-ch
```

A buffered channel can hold a limited number of values:

``` go
ch := make(chan int, 5)
```

## File: `cmd/concurrency/main.go`

``` go
package main

import (
    "fmt"
    "sync"
)

func main() {
    fmt.Println("GO CONCURRENCY DEMONSTRATION")

    tasks := make(chan int, 10)
    var workers sync.WaitGroup

    // Start three concurrent workers.
    for i := 1; i <= 3; i++ {
        workers.Add(1)
        go worker(i, tasks, &workers)
    }

    // Send ten tasks.
    for i := 1; i <= 10; i++ {
        tasks <- i
    }

    close(tasks)
    workers.Wait()

    demonstrateSynchronization()
}
```

## File: `cmd/concurrency/workers.go`

``` go
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
```

## File: `cmd/concurrency/synchronization.go`

``` go
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

    for i := 1; i <= 5; i++ {
        wg.Add(1)

        go func(id int) {
            defer wg.Done()

            mutex.Lock()
            counter++
            mutex.Unlock()

            atomic.AddInt64(&atomicCounter, 1)
            fmt.Printf("Goroutine %d executed\n", id)
        }(i)
    }

    wg.Wait()

    fmt.Println("Mutex protected counter:", counter)
    fmt.Println("Atomic counter:", atomic.LoadInt64(&atomicCounter))
}
```

### Explanation

1.  Main creates a buffered channel for ten integer tasks.
2.  Three worker goroutines are started.
3.  Main sends ten tasks through the channel.
4.  Closing the channel tells workers that no more tasks will arrive.
5.  Workers receive tasks using `range` and finish when the closed
    channel is drained.
6.  `WaitGroup` ensures main waits for all workers.
7.  The synchronization function starts five more goroutines.
8.  A mutex protects one shared counter; atomic operations update
    another.

The order of worker output can vary on every run.

### Synchronization primitives

  Primitive          Purpose
  ------------------ -------------------------------------------------
  Goroutine          Executes a function concurrently.
  Channel            Communicates values and coordinates goroutines.
  `sync.WaitGroup`   Waits for goroutines to finish.
  `sync.Mutex`       Protects shared data using mutual exclusion.
  `sync/atomic`      Performs atomic operations on supported values.

A **race condition** occurs when goroutines access shared data
concurrently and at least one access modifies it without appropriate
synchronization.

Run with the race detector:

``` bash
go run -race ./cmd/concurrency
```

A correctly synchronized program should not report a data race.

------------------------------------------------------------------------

# 5. Experiment 2 --- Hardware cores and CPU execution

## Theory

A CPU may have multiple physical cores and expose additional logical
processors. Go's `runtime` package provides CPU information and controls
execution parallelism.

  -----------------------------------------------------------------------
  Function                            Purpose
  ----------------------------------- -----------------------------------
  `runtime.NumCPU()`                  Number of logical CPUs available to
                                      the process according to the
                                      runtime.

  `runtime.GOMAXPROCS(n)`             Sets the maximum number of CPUs
                                      that can execute Go code
                                      simultaneously.

  `runtime.GOMAXPROCS(0)`             Reads the current setting.

  `runtime.NumGoroutine()`            Reports the number of existing
                                      goroutines.
  -----------------------------------------------------------------------

## File: `cmd/hardware/main.go`

``` go
package main

import (
    "fmt"
    "runtime"
    "sync"
    "time"
)

func cpuTask(id int, wg *sync.WaitGroup) {
    defer wg.Done()

    var sum uint64

    for i := 0; i < 100000000; i++ {
        sum += uint64(i % 100)
    }

    fmt.Printf("CPU task %d completed. Result: %d\n", id, sum)
}

func main() {
    cores := runtime.NumCPU()
    fmt.Println("Logical CPU cores:", cores)

    runtime.GOMAXPROCS(cores)
    fmt.Println("GOMAXPROCS:", runtime.GOMAXPROCS(0))

    var wg sync.WaitGroup
    start := time.Now()

    for i := 1; i <= cores; i++ {
        wg.Add(1)
        go cpuTask(i, &wg)
    }

    wg.Wait()

    fmt.Println("All CPU tasks completed.")
    fmt.Println("Execution time:", time.Since(start))
    fmt.Println("Active goroutines:", runtime.NumGoroutine())
}
```

### Explanation

The program obtains logical CPU count, sets `GOMAXPROCS`, launches one
CPU-intensive goroutine per reported logical CPU, waits for completion,
and measures elapsed time.

**Important:** `runtime.NumCPU()` does not report CPU utilization. The
Go standard runtime does not provide a portable per-core utilization
percentage.

Observe actual system utilization in another terminal:

``` bash
top
```

or:

``` bash
sudo apt install htop
htop
```

Run the Go program while watching `htop`. Utilization depends on the
CPU, operating system, other processes, and environment.

------------------------------------------------------------------------

# 6. Experiment 3 --- Go web technology: HTTP server and client

## Theory

Go's `net/http` package supports HTTP servers and clients.

-   The **server** listens for HTTP requests and sends responses.
-   The **client** sends requests and processes responses.
-   **JSON** is a common text format for exchanging structured data.

Request-response flow:

``` text
Client -- GET / --> HTTP Server
Client <-- JSON response -- HTTP Server
```

## Server file: `cmd/server/main.go`

``` go
package main

import (
    "encoding/json"
    "fmt"
    "net/http"
)

type Response struct {
    Message  string `json:"message"`
    Language string `json:"language"`
    Feature  string `json:"feature"`
}

func homeHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")

    response := Response{
        Message:  "Welcome to Go Web Server",
        Language: "Go",
        Feature:  "Fast and concurrent HTTP server",
    }

    json.NewEncoder(w).Encode(response)
}

func main() {
    http.HandleFunc("/", homeHandler)

    fmt.Println("Server started at http://localhost:8080")

    err := http.ListenAndServe(":8080", nil)
    if err != nil {
        fmt.Println("Server error:", err)
    }
}
```

### Server concepts

-   `http.HandleFunc()` registers a handler for a URL pattern.
-   `http.ResponseWriter` writes the response.
-   `*http.Request` contains request information.
-   `json.NewEncoder()` encodes a Go value as JSON.
-   `http.ListenAndServe()` starts the server.

## Client file: `cmd/client/main.go`

``` go
package main

import (
    "fmt"
    "io"
    "net/http"
)

func main() {
    response, err := http.Get("http://localhost:8080")

    if err != nil {
        fmt.Println("Request failed:", err)
        return
    }

    defer response.Body.Close()

    body, err := io.ReadAll(response.Body)
    if err != nil {
        fmt.Println("Error reading response:", err)
        return
    }

    fmt.Println("HTTP Status:", response.Status)
    fmt.Println("Server Response:")
    fmt.Println(string(body))
}
```

### Run the web demonstration

Terminal 1:

``` bash
go run ./cmd/server
```

Keep the server running.

Terminal 2:

``` bash
go run ./cmd/client
```

Expected output:

``` text
HTTP Status: 200 OK
Server Response:
{"message":"Welcome to Go Web Server","language":"Go","feature":"Fast and concurrent HTTP server"}
```

You can also open `http://localhost:8080` in a browser.

**Terminology note:** This demonstrates an HTTP client and server. The
client is a command-line program, not browser-side JavaScript. Go is
widely used for backend web services; browser interfaces are commonly
written in JavaScript, though Go can also target WebAssembly.

------------------------------------------------------------------------

# 7. Experiment 4 --- Garbage collection and safer pointers

## Theory

A pointer stores the address of a value.

-   `&x` obtains the address of `x`.
-   `*p` accesses the value referenced by pointer `p`.
-   `*T` means a pointer to type `T`.

Go supports pointers but does not permit ordinary pointer arithmetic
such as incrementing a pointer to move to the next memory address.

Go's garbage collector automatically reclaims memory that is no longer
reachable. This reduces the need for manual memory deallocation, but
does not eliminate all memory-management concerns.

## File: `cmd/memory/main.go`

``` go
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
    student := &Student{
        Name: "Rahul",
        Age:  21,
    }

    return student
}

func main() {
    fmt.Println("GARBAGE COLLECTION AND POINTER DEMONSTRATION")

    studentPtr := createStudent()

    fmt.Println("Student Name:", studentPtr.Name)
    fmt.Println("Student Age:", studentPtr.Age)

    studentPtr.Age = 22
    fmt.Println("Updated Age:", studentPtr.Age)

    var memStats runtime.MemStats
    runtime.ReadMemStats(&memStats)

    fmt.Println("\nMemory Statistics:")
    fmt.Println("Allocated memory:", memStats.Alloc, "bytes")
    fmt.Println("Total allocated:", memStats.TotalAlloc, "bytes")
    fmt.Println("Garbage collections:", memStats.NumGC)

    runtime.GC()
    fmt.Println("Garbage collection requested.")
}
```

### Explanation

The program defines a `Student` struct, returns a pointer to a student,
reads and modifies the value through the pointer, reads memory
statistics, and requests garbage collection.

`runtime.GC()` requests collection; the runtime controls when collection
occurs. Reachable objects are not reclaimed.

The compiler uses escape analysis to decide whether values can live on
the stack or need heap allocation. Do not assume every value whose
address is taken must be allocated on the heap.

------------------------------------------------------------------------

# 8. Experiment 5 --- Cleaner syntax and enforced standards

Go emphasizes readable syntax and consistent formatting.

Features include short variable declarations, explicit types,
compile-time type checking, standard formatting, and compiler errors for
unused local variables and imports.

## File: `cmd/syntax/main.go`

``` go
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

    fmt.Println("First number:", x)
    fmt.Println("Second number:", y)
    fmt.Println("Sum:", answer)
}
```

Run:

``` bash
go run ./cmd/syntax
```

Expected output:

``` text
First number: 10
Second number: 20
Sum: 30
```

### Formatting and static analysis

Format source files:

``` bash
gofmt -w .
```

Show formatting differences without modifying files:

``` bash
gofmt -d .
```

Run static checks:

``` bash
go vet ./...
```

`gofmt` enforces consistent formatting. `go vet` reports suspicious code
patterns; it does not prove that a program is correct.

------------------------------------------------------------------------

# 9. Experiment 6 --- Static compilation and dependencies

Go is compiled: the compiler translates source code into an executable
for a target operating system and architecture.

The Go standard library includes:

  Package           Purpose
  ----------------- ----------------------------
  `fmt`             Formatted input/output
  `time`            Dates, times, durations
  `sync`            Synchronization primitives
  `sync/atomic`     Atomic operations
  `runtime`         Go runtime information
  `net/http`        HTTP servers and clients
  `encoding/json`   JSON encoding and decoding
  `io`              Input/output utilities

All programs in this assignment use only the standard library, so no
third-party packages are required.

### Build each program

Run from the project root:

``` bash
go build -o concurrency ./cmd/concurrency
go build -o hardware ./cmd/hardware
go build -o server ./cmd/server
go build -o client ./cmd/client
go build -o memory ./cmd/memory
go build -o syntax ./cmd/syntax
```

Run a compiled program:

``` bash
./concurrency
```

Run the compiled server:

``` bash
./server
```

In another terminal:

``` bash
./client
```

### Build with CGO disabled

``` bash
CGO_ENABLED=0 go build -o server ./cmd/server
```

This avoids a dependency on C libraries through CGO for this build. It
is not a universal guarantee that every Go executable on every platform
has no external runtime or operating-system requirements.

### Module commands

``` bash
go mod init go-assignments
go mod tidy
go list -m all
```

-   `go mod init` initializes a module.
-   `go mod tidy` adds required modules and removes unused requirements.
-   `go list -m all` lists modules in the dependency graph.

------------------------------------------------------------------------

# 10. Running and validating all programs

  Demonstration                     Command
  --------------------------------- ----------------------------
  Goroutines and synchronization    `go run ./cmd/concurrency`
  CPU information and workload      `go run ./cmd/hardware`
  HTTP server                       `go run ./cmd/server`
  HTTP client                       `go run ./cmd/client`
  Pointers and garbage collection   `go run ./cmd/memory`
  Syntax and functions              `go run ./cmd/syntax`

For the web demonstration, start the server in one terminal before
running the client in another.

Run project checks:

``` bash
gofmt -w .
go vet ./...
go test ./...
go build ./cmd/concurrency
go build ./cmd/hardware
go build ./cmd/server
go build ./cmd/client
go build ./cmd/memory
go build ./cmd/syntax
```

`go test ./...` runs available tests. If no test files exist, Go reports
that packages have no test files.

Race detector:

``` bash
go run -race ./cmd/concurrency
```

The race detector adds overhead and should not be used to measure normal
performance.

## Understanding concurrency output

The program starts three workers and sends ten tasks. Output order is
not fixed because goroutines are scheduled concurrently. Do not expect
tasks to complete in numerical order.

The final counters should be:

``` text
Mutex protected counter: 5
Atomic counter: 5
```

The order of goroutine messages may differ between executions.

------------------------------------------------------------------------

# 11. Key concepts quick reference

  -----------------------------------------------------------------------
  Concept                             Meaning
  ----------------------------------- -----------------------------------
  Goroutine                           Lightweight execution unit managed
                                      by Go runtime.

  Channel                             Typed communication path between
                                      goroutines.

  Buffered channel                    Channel that can store a limited
                                      number of values.

  Unbuffered channel                  Send and receive synchronize
                                      directly.

  WaitGroup                           Waits for goroutines to finish.

  Mutex                               Protects shared data using mutual
                                      exclusion.

  Atomic operation                    Indivisible operation on supported
                                      shared values.

  Race condition                      Unsynchronized conflicting access
                                      to shared data.

  Concurrency                         Overlapping progress on multiple
                                      tasks.

  Parallelism                         Simultaneous execution of tasks.

  GOMAXPROCS                          Maximum number of CPUs executing Go
                                      code simultaneously.

  HTTP                                Request-response protocol used by
                                      web applications.

  JSON                                Text-based data interchange format.

  Garbage collection                  Automatic reclamation of
                                      unreachable memory.

  Pointer                             Value containing the address of
                                      another value.

  Static typing                       Types are checked by the compiler.

  Compilation                         Translation of source code into
                                      executable machine code.

  Standard library                    Packages included with the Go
                                      toolchain.

  Module                              Collection of Go packages managed
                                      as a unit.

  `gofmt`                             Standard Go source formatter.

  `go vet`                            Tool that identifies suspicious
                                      code patterns.
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 12. Screenshots for the practical journal

Create a screenshot directory:

``` bash
mkdir -p screenshots
```

Capture genuine screenshots from your own computer:

-   [ ] Go version (`go version`).
-   [ ] Project directory structure.
-   [ ] `go.mod` file.
-   [ ] Concurrency source code.
-   [ ] Worker output showing multiple workers.
-   [ ] Synchronization output showing both counters equal to 5.
-   [ ] Hardware output showing logical CPU count and execution time.
-   [ ] `htop` or `top` while the CPU workload runs.
-   [ ] Web server running on port 8080.
-   [ ] Client output showing the JSON response.
-   [ ] Browser displaying `http://localhost:8080`.
-   [ ] Pointer and garbage-collection output.
-   [ ] Syntax program output.
-   [ ] Successful formatting, vet, and build commands.

------------------------------------------------------------------------

# 13. Troubleshooting

### `go: command not found`

``` bash
sudo apt update
sudo apt install golang-go
which go
go version
```

### `go.mod file not found`

Run commands from the project root:

``` bash
cd ~/Unix-Operating-System/Open-Source-Software/Go-Assignments
```

If it is a new project:

``` bash
go mod init go-assignments
```

### Address already in use on port 8080

``` bash
sudo ss -ltnp | grep ':8080'
```

Identify the process using the port. Stop it only if appropriate, or
change the port consistently in the server and client.

### Client reports connection refused

-   Ensure the server is running.
-   Confirm the server listens on port 8080.
-   Confirm the client URL is `http://localhost:8080`.
-   Check that the server has not been stopped with `Ctrl+C`.

### Undefined worker or synchronization functions

All three files must be in `cmd/concurrency` and use `package main`:

-   `main.go`
-   `workers.go`
-   `synchronization.go`

Run from the module root:

``` bash
go run ./cmd/concurrency
```

Do not use only `go run main.go` from the concurrency folder, because
that compiles only the named file and may omit the other source files.

### Formatting or vet warnings

``` bash
gofmt -w .
go vet ./...
```

Read and fix remaining diagnostics.

------------------------------------------------------------------------

# 14. Viva questions and answers

**1. What is Go?**\
Go is an open-source, statically typed, compiled language designed for
simplicity, concurrency, and efficient software development.

**2. Who developed Go?**\
Go was developed at Google.

**3. What is the extension of a Go source file?**\
`.go`

**4. What is a goroutine?**\
A lightweight execution unit managed by the Go runtime.

**5. How do you start a goroutine?**\
Use the `go` keyword before a function call.

**6. What is a channel?**\
A typed mechanism used by goroutines to communicate and synchronize.

**7. Difference between concurrency and parallelism?**\
Concurrency is overlapping progress on tasks; parallelism is
simultaneous execution.

**8. What is a WaitGroup?**\
A synchronization primitive used to wait for a group of goroutines to
complete.

**9. What is a mutex?**\
A mutual-exclusion lock that protects shared data from simultaneous
access.

**10. What is an atomic operation?**\
An operation that appears indivisible to other concurrent operations on
the same atomic value.

**11. What is a race condition?**\
A situation in which results depend on unsynchronized concurrent access
to shared data.

**12. What does `runtime.NumCPU()` return?**\
The number of logical CPUs available to the process according to the
runtime.

**13. What is GOMAXPROCS?**\
It controls the maximum number of CPUs that can execute Go code
simultaneously.

**14. Does `runtime.NumCPU()` return CPU utilization?**\
No. It reports logical CPU availability, not utilization percentage.

**15. Which package is used for HTTP server programming?**\
`net/http`.

**16. What is JSON?**\
A text-based format for representing and exchanging structured data.

**17. What is garbage collection?**\
Automatic reclamation of memory occupied by objects that are no longer
reachable.

**18. Does Go support pointers?**\
Yes, but it does not support ordinary pointer arithmetic.

**19. What does `runtime.GC()` do?**\
It requests garbage collection; the runtime controls the collection
process.

**20. What is static typing?**\
Types are checked by the compiler.

**21. What is `gofmt`?**\
The standard Go source-code formatter.

**22. What is `go vet`?**\
A tool that checks for suspicious code patterns.

**23. What is a Go module?**\
A collection of Go packages managed as a unit with module metadata and
dependency information.

**24. Does this practical require third-party packages?**\
No. The examples use only Go's standard library.

**25. What does `go build` do?**\
It compiles packages and produces an executable for a main package.

**26. What does `go run` do?**\
It compiles and runs a Go program during development.

**27. Difference between a Go server and client?**\
The server listens for requests and sends responses; the client sends
requests and processes responses.

**28. Is Go used for browser-side JavaScript?**\
Not in this example. Go is widely used for backend services; browser
interfaces are commonly written in JavaScript. Go can also compile to
WebAssembly.

------------------------------------------------------------------------

# 15. Suggested practical conclusion

The Go programming-language features were studied and demonstrated
through independent programs. Goroutines and channels were used for
concurrent task processing. WaitGroup, Mutex, and atomic operations
demonstrated synchronization. The runtime package was used to inspect
logical CPU availability and configure parallel execution. An HTTP
server and client demonstrated web communication. Pointers, memory
statistics, and garbage collection demonstrated Go's memory-management
approach. Finally, Go formatting, static analysis, and compilation tools
demonstrated its emphasis on consistent syntax and compiled executables.

**Technical points to state accurately in the viva:**

-   Go uses goroutines, not one manually created operating-system thread
    per task.
-   Concurrency and parallelism are related but not identical.
-   `runtime.NumCPU()` reports logical CPU availability, not CPU
    utilization.
-   The HTTP client shown is a command-line client, not browser-side
    JavaScript.
-   Garbage collection is automatic, but the runtime controls when
    collection happens.
-   Go supports pointers but not ordinary pointer arithmetic.
-   The examples use the standard library and require no third-party
    packages.
