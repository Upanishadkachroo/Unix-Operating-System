package main

import (
    "encoding/json"
    "fmt"
    "net/http"
)

type Response struct {
    Message string `json:"message"`
    Language string `json:"language"`
    Feature string `json:"feature"`
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
