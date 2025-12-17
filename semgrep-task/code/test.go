// Purpose: Test file to demonstrate Go coding rule violations
// Author: Test User
// Date: 2025-12-17
// Modified By: N/A

package main

import (
	"fmt"
	"time"
)

// Global variable - should be avoided
var globalCounter int

// Global configuration - avoid when possible
var globalConfig string

func main() {
	fmt.Println("Starting Go test application")
	
	// Unhandled error - CRITICAL
	result, err := riskyOperation()
	processData(result)  // Using result without checking err!
	
	// Another unhandled error
	data, err := fetchData()
	fmt.Println(data)  // err is assigned but never checked
	
	// Using panic instead of returning error
	dangerousFunction()
	
	// Empty error handling
	poorErrorHandling()
	
	// Good example
	goodErrorHandling()
}

// Function with unhandled error
func riskyOperation() (string, error) {
	return "data", nil
}

// Function that uses panic - should return error instead
func dangerousFunction() {
	if globalCounter < 0 {
		panic("Counter cannot be negative!")  // Bad practice
	}
}

// Poor error handling - ignoring errors
func poorErrorHandling() {
	file, err := openFile("config.txt")
	_ = err  // Ignoring error with blank identifier
	fmt.Println(file)
}

// Empty error check
func fetchData() (string, error) {
	data, err := readDatabase()
	if err != nil {
		// Empty error handling - just returning
	}
	return data, err
}

func readDatabase() (string, error) {
	return "database data", nil
}

func openFile(filename string) (string, error) {
	return "file content", nil
}

// Unclosed channel - potential goroutine leak
func channelLeak() {
	ch := make(chan int)  // Channel created but never closed
	
	go func() {
		ch <- 42
	}()
	
	// Channel is never closed - potential leak
}

// Duplicate code - violates DRY principle
func processUserData(userId string) {
	if userId != "" {
		fmt.Println("Processing user:", userId)
		globalCounter++
	}
}

func processAdminData(adminId string) {
	if adminId != "" {
		fmt.Println("Processing user:", adminId)
		globalCounter++
	}
}

// Function doing too many things - violates Single Responsibility
func doEverything() {
	fmt.Println("Starting complex process")
	
	// Database operation
	data, err := readDatabase()
	_ = err
	
	// File operation
	file, err := openFile("data.txt")
	_ = err
	
	// Processing
	result := processData(data)
	
	// More processing
	finalResult := processData(file)
	
	// Logging
	fmt.Println(result, finalResult)
	
	// Sleep
	time.Sleep(1 * time.Second)
	
	// More operations
	globalCounter++
	globalConfig = "updated"
	
	fmt.Println("Process complete")
}

func processData(data string) string {
	return data + "_processed"
}

// Good example - proper error handling
func goodErrorHandling() error {
	data, err := fetchData()
	if err != nil {
		return fmt.Errorf("failed to fetch data: %w", err)
	}
	
	result := processData(data)
	fmt.Println("Processed result:", result)
	
	return nil
}

// Good example - returning error instead of panic
func safeFunction(value int) error {
	if value < 0 {
		return fmt.Errorf("value cannot be negative: %d", value)
	}
	return nil
}

// Good example - proper channel management
func properChannelUsage() {
	ch := make(chan int)
	
	go func() {
		ch <- 42
		close(ch)  // Properly closing the channel
	}()
	
	result := <-ch
	fmt.Println("Received:", result)
}
