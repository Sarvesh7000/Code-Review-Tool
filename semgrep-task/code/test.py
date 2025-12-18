# Purpose: Test file to demonstrate Python coding rule violations
# Author: Test User
# Date: 2025-12-17
# Modified By: N/A

import os
import sys
import time

# Global variable - should be avoided
global_counter = 0
global_config = {}

def main():
    print("Starting Python test application")  # Should use logging
    
    # Empty except block - CRITICAL ERROR
    try:
        result = risky_operation()
        process_data(result)
    except:
        pass  # Ignoring all exceptions - very dangerous!
    
    # Bare except - WARNING
    try:
        data = fetch_data()
        print(data)
    except:
        print("Something went wrong")  # Too generic
    
    # Another empty except
    poor_error_handling()
    
    # Print statements instead of logging
    debug_with_print()
    
    # Good example
    good_error_handling()

def risky_operation():
    return "data"

# Empty except with pass - worst practice
def poor_error_handling():
    try:
        file = open("config.txt")
        content = file.read()
    except:
        pass  # Silently ignoring errors

# Bare except - too generic
def fetch_data():
    try:
        data = read_database()
        return data
    except:
        return None  # Catching all exceptions without specificity

def read_database():
    return "database data"

# Using print instead of logging module
def debug_with_print():
    print("Debug: Starting process")
    print("Debug: Processing data")
    print("Debug: Process complete")
    
    # More print statements
    x = 10
    print(x)
    print("Value is:", x)

# SQL Injection vulnerability
def unsafe_database_query(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id  # SQL injection risk!
    # db.execute(query)
    return query

# Using eval - security risk
def dangerous_eval(user_input):
    result = eval(user_input)  # Never use eval with user input!
    return result

# Hard-coded credentials - SECURITY ISSUE
def connect_to_database():
    password = "admin123"  # Hard-coded password
    api_key = "sk_live_1234567890"  # Hard-coded API key
    
    # Connection logic here
    return f"Connected with {password}"

# Duplicate code - violates DRY principle
def process_user_data(user_id):
    if user_id is not None:
        print(f"Processing user: {user_id}")
        global global_counter
        global_counter += 1

def process_admin_data(admin_id):
    if admin_id is not None:
        print(f"Processing user: {admin_id}")
        global global_counter
        global_counter += 1

# Function doing too many things - violates Single Responsibility
def do_everything():
    print("Starting complex process")
    
    # Database operation
    try:
        data = read_database()
    except:
        pass
    
    # File operation
    try:
        file = open("data.txt")
        content = file.read()
    except:
        pass
    
    # Processing
    result = process_data(data)
    
    # More processing
    final_result = process_data(content)
    
    # Logging with print
    print(result, final_result)
    
    # Sleep
    time.sleep(1)
    
    # More operations
    global global_counter
    global_counter += 1
    global_config["status"] = "updated"
    
    print("Process complete")

def process_data(data):
    return str(data) + "_processed"

# Multiple bare excepts in one function
def multiple_error_issues():
    # First bare except
    try:
        x = 1 / 0
    except:
        print("Error 1")
    
    # Second bare except
    try:
        y = int("not a number")
    except:
        print("Error 2")
    
    # Third empty except
    try:
        z = open("nonexistent.txt")
    except:
        pass

# Good example - proper error handling
def good_error_handling():
    try:
        data = fetch_data()
        result = process_data(data)
        return result
    except FileNotFoundError as e:
        # Specific exception handling
        raise Exception(f"File not found: {e}")
    except ValueError as e:
        # Another specific exception
        raise Exception(f"Invalid value: {e}")
    except Exception as e:
        # Generic catch as last resort, but with proper handling
        raise Exception(f"Unexpected error: {e}")

# Good example - using logging instead of print
def good_logging_example():
    import logging
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting process")
    logger.debug("Debug information")
    logger.warning("Warning message")
    logger.error("Error occurred")

# Good example - parameterized query (safe from SQL injection)
def safe_database_query(user_id):
    # Using parameterized query
    query = "SELECT * FROM users WHERE id = ?"
    # db.execute(query, (user_id,))
    return query

# Good example - avoiding eval
def safe_calculation(expression):
    # Use ast.literal_eval or specific parsing instead of eval
    import ast
    try:
        result = ast.literal_eval(expression)
        return result
    except (ValueError, SyntaxError):
        raise ValueError("Invalid expression")

if __name__ == "__main__":
    main()
