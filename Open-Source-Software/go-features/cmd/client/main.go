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

    fmt.Println("Server Response:")
    fmt.Println(string(body))
}
