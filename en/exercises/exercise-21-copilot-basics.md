# Exercise 21: GitHub Copilot Basics in Practice

## Learning Objectives

Through this exercise, you will master the following skills:

- Setting up the GitHub Copilot development environment
- Using Copilot for code auto-completion
- Leveraging Copilot to generate function implementations
- Using Copilot to write unit tests
- Using Copilot to generate code documentation
- Using Copilot Chat for code review

## Prerequisites

- A GitHub account with an active GitHub Copilot subscription (Individual or Business)
- Visual Studio Code installed
- Basic Python or JavaScript programming knowledge
- Git installed and basic environment configured

## Part 1: Environment Setup

### Step 1: Install the GitHub Copilot Extension

Open Visual Studio Code and follow these steps to install the Copilot extension:

1. Click the Extensions icon in the left activity bar (or use the shortcut `Ctrl+Shift+X`)
2. Type `GitHub Copilot` in the search box
3. Find the official GitHub Copilot extension and click the "Install" button
4. Also install the GitHub Copilot Chat extension

After installation, you will see the Copilot icon in the bottom-right corner of VS Code.

### Step 2: Sign in to Your GitHub Account

After installing the extension, you need to link your GitHub account:

```bash
# Open VS Code command palette
# Windows/Linux: Ctrl+Shift+P
# macOS: Cmd+Shift+P
# Type the following command and press Enter
# > GitHub Copilot: Sign in
```

Follow the prompts to complete GitHub authorization in your browser. After successful sign-in, VS Code will display a confirmation message.

### Step 3: Verify Copilot Is Working

Create a new Python file to test Copilot:

```bash
# Create project directory
mkdir copilot-practice
cd copilot-practice

# Create Python file
touch test_copilot.py
```

Enter the following comment in `test_copilot.py` and observe whether Copilot provides completion suggestions:

```python
# Calculate the greatest common divisor of two numbers
def gcd(
```

If Copilot is working properly, you will see gray completion suggestion code. Press `Tab` to accept the suggestion.

### Step 4: Learn Copilot Shortcuts

Here are the commonly used Copilot shortcuts — make sure to become familiar with them:

| Action | Windows/Linux Shortcut | macOS Shortcut |
|--------|----------------------|----------------|
| Accept suggestion | `Tab` | `Tab` |
| Reject suggestion | `Esc` | `Esc` |
| View next suggestion | `Alt+]` | `Option+]` |
| View previous suggestion | `Alt+[` | `Option+[` |
| Trigger inline suggestion | `Alt+\` | `Option+\` |
| Open Copilot Chat | `Ctrl+Shift+I` | `Cmd+Shift+I` |

## Part 2: Writing Functions with Copilot

In this part, you will learn how to guide Copilot in generating high-quality code by writing clear comments. Copilot works by predicting and generating code based on the context you provide (including comments, function signatures, existing code, etc.). Therefore, writing detailed and accurate comments is key to getting high-quality code suggestions. You should develop good programming habits by first describing the desired functionality in natural language, and then letting Copilot help you with the actual code implementation. This approach not only improves the accuracy of code generation but also helps you better understand and plan your code architecture.

### Exercise Task A: Writing Data Processing Functions

Create a file `data_processor.py` and use comments to guide Copilot in generating function implementations.

First, enter the following comment and function signature:

```python
# Parse a CSV-formatted string into a list of dictionaries
# Input: "name,age,city\nAlice,30,Beijing\nBob,25,Shanghai"
# Output: [{"name": "Alice", "age": "30", "city": "Beijing"}, ...]
def parse_csv_string(csv_string: str) -> list[dict]:
```

Observe Copilot's suggestion — it should generate code similar to the following:

```python
def parse_csv_string(csv_string: str) -> list[dict]:
    lines = csv_string.strip().split('\n')
    if not lines:
        return []
    headers = lines[0].split(',')
    result = []
    for line in lines[1:]:
        values = line.split(',')
        row = dict(zip(headers, values))
        result.append(row)
    return result
```

Press `Tab` to accept the suggestion, then continue by entering the comment for the next function:

```python
# Filter elements in a list of dictionaries that match a condition
# For example, filter people older than 28
def filter_records(records: list[dict], key: str, min_value) -> list[dict]:
```

Continue letting Copilot generate the following functions:

```python
# Sort a list of dictionaries by a specified key
# Supports ascending and descending order
def sort_records(records: list[dict], key: str, reverse: bool = False) -> list[dict]:

# Convert a list of dictionaries to a Markdown table-formatted string
def records_to_markdown(records: list[dict]) -> str:

# Count occurrences of a specific key's value in a list of dictionaries
def count_by_key(records: list[dict], key: str) -> dict[str, int]:
```

### Exercise Task B: Writing Algorithm Functions

Create a file `algorithms.py` and let Copilot implement classic algorithms:

```python
# Binary search algorithm
# Search for a target value in a sorted array, return the index, or -1 if not found
def binary_search(arr: list[int], target: int) -> int:

# Quicksort algorithm
# Sort a list using the divide-and-conquer approach
def quicksort(arr: list[int]) -> list[int]:

# Find the Kth largest element in a list
# Using heap sort concept, time complexity O(nlogk)
def find_kth_largest(nums: list[int], k: int) -> int:

# Check if a string is a valid parentheses sequence
# Supports (), [], {} types of brackets
def is_valid_parentheses(s: str) -> bool:

# Calculate the edit distance (Levenshtein distance) between two strings
def edit_distance(word1: str, word2: str) -> int:
```

**Key Point:** Pay attention to whether Copilot's algorithm implementations are correct. For complex algorithms, Copilot may provide multiple implementation approaches. You can use the `Alt+]` and `[` shortcuts to switch between different suggestions.

### Exercise Task C: Writing Object-Oriented Code

Create a file `library_system.py` and use comments to guide Copilot in generating classes:

```python
# Library management system
# Includes the following features:
# 1. Book class: represents a book with title, author, ISBN, and borrow status
# 2. Library class: manages a book collection, supports add, borrow, return, and search operations
# 3. All operations need to be logged

class Book:
    """Data class representing a book"""
    # Initialization method, accepts title, author, isbn parameters

    # Method to check if the book is available for borrowing

    # Method to borrow the book

    # Method to return the book

    # String representation method, returns book title and author

class Library:
    """Library management class"""
    # Initialization method, creates empty book list and operation log

    # Method to add a new book to the library

    # Method to borrow a book by ISBN

    # Method to return a book by ISBN

    # Method to search for books by author or title

    # Method to get all available books

    # Method to get the operation history log
```

Let Copilot generate complete class implementations based on these comments. Review the generated code to ensure the logic is correct.

## Part 3: Writing Tests with Copilot

Writing tests is a crucial part of software development, but many developers find it tedious. GitHub Copilot can greatly simplify the test writing process. You just need to clearly describe the scenarios to test and expected results, and Copilot can generate complete test case code for you. This is very helpful for improving test coverage and code quality. In practice, it's recommended to write tests before writing feature code (test-driven development) to better leverage Copilot's capabilities. When you clearly describe the expected behavior of the tests, Copilot's generated test code is usually more accurate and comprehensive. Additionally, you can ask Copilot to generate various types of test cases, such as boundary condition tests, exception tests, and performance tests.

### Exercise Task D: Generating Unit Tests

Create a file `test_data_processor.py` and write tests for the data processing functions from earlier:

```python
import pytest
from data_processor import parse_csv_string, filter_records, sort_records

# Test parse_csv_string function
# Need to test the following scenarios:
# 1. Normal CSV string parsing
# 2. Empty string input
# 3. Only header row with no data rows
# 4. Data containing special characters

class TestParseCsvString:
    # Test normal parsing

    # Test empty string

    # Test only header row

    # Test data containing commas

# Test filter_records function
# Need to test the following scenarios:
# 1. Normal filtering
# 2. No matching records
# 3. All records match
# 4. Empty list input

class TestFilterRecords:
    # Write various test cases

# Test sort_records function
# Need to test the following scenarios:
# 1. Ascending sort
# 2. Descending sort
# 3. Records with identical values
# 4. Empty list input

class TestSortRecords:
    # Write various test cases
```

Copilot should generate specific test code for each test method. Observe and accept reasonable suggestions.

### Exercise Task E: Generating Integration Tests

Create a file `test_library_system.py` and write integration tests for the library management system:

```python
import pytest
from library_system import Book, Library

# Test Book class
class TestBook:
    # Test creating a book object

    # Test that a new book is available by default

    # Test the borrow operation

    # Test the return operation

    # Test that a book cannot be borrowed twice

    # Test that a book that hasn't been borrowed cannot be returned

# Test Library class
class TestLibrary:
    # Test adding a book

    # Test borrowing a non-existent book

    # Test borrowing an already borrowed book

    # Test the search function

    # Test getting the list of available books

    # Test operation log recording

# Integration test: simulate a complete borrow-return workflow
class TestLibraryIntegration:
    # Test the complete borrow-return flow

    # Test conflict handling when multiple people borrow the same book

    # Test batch add and search operations
```

**Important Note:** If Copilot's generated tests are not comprehensive enough, you can guide it by adding more detailed comments. For example:

```python
# Test boundary case: should raise ValueError when ISBN is an empty string
def test_empty_isbn_raises_error(self):
```

## Part 4: Generating Documentation with Copilot

Good documentation is one of the key factors for project success. However, writing documentation is often overlooked by developers because it is time-consuming and lacks immediate gratification. GitHub Copilot can help you quickly generate high-quality documentation, including function docstrings, module descriptions, usage examples, and even complete project documentation. By analyzing your code logic, Copilot can automatically generate docstrings that accurately describe function functionality, parameter meanings, return value types, and possible exceptions. This not only saves a significant amount of time but also ensures that documentation stays in sync with the code. In team collaboration, thorough documentation can greatly reduce communication costs and help new team members get up to speed on project development faster.

### Exercise Task F: Generating Docstrings

Open the previously created `data_processor.py` and enter `"""` above each function, then let Copilot generate complete docstrings:

```python
def parse_csv_string(csv_string: str) -> list[dict]:
    """
    Copilot should generate detailed docstrings, including:
    - Function description
    - Parameter description
    - Return value description
    - Exception description
    - Usage example
    """
```

### Exercise Task G: Generating a README

Create a file `README.md`, enter the following content and let Copilot expand on it:

```markdown
# Data Processing Toolkit

A Python toolkit for processing and analyzing structured data.

## Features

Let Copilot continue generating the following content:

## Installation

## Quick Start

## API Documentation

## Contributing Guide

## License
```

## Part 5: Code Review with Copilot Chat

Code review is an important step in ensuring code quality, but traditional code review requires senior developers to invest significant time. Copilot Chat offers a completely new way to do code review — it can serve as your intelligent assistant, helping you discover potential issues, security vulnerabilities, and improvement suggestions in your code. Through conversations with Copilot Chat, you can get feedback on code architecture design, performance optimization, security best practices, and more. While Copilot Chat cannot completely replace human code review, it can help you self-review before submitting code, improving overall code quality.

### Step 1: Open Copilot Chat

Use the shortcut `Ctrl+Shift+I` (on macOS, `Cmd+Shift+I`) to open the Copilot Chat panel.

### Step 2: Request a Code Review

Select all the code in `data_processor.py`, then enter the following in the Chat panel:

```
@workspace Please review this code, pointing out potential issues and improvement suggestions. Consider the following aspects:
1. Code quality and readability
2. Error handling completeness
3. Performance optimization suggestions
4. Type hints accuracy
5. Compliance with PEP8 standards
```

### Step 3: Request a Security Review

Continue asking in Chat:

```
Please check if these functions have security risks, such as:
1. Whether input validation is sufficient
2. Whether there are injection attack risks
3. Memory usage issues with large data volumes
```

### Step 4: Request Refactoring Suggestions

```
Please suggest how to refactor this code to improve maintainability. Consider:
1. Whether common logic can be extracted
2. Whether design patterns should be used
3. How to improve testability
```

### Step 5: Use Copilot Chat to Explain Code

If you encounter code you don't understand, you can use Chat to get an explanation:

```
/explain Please explain in detail how this code works, including the execution logic of each step
```

### Step 6: Use Copilot Chat to Fix Issues

When Copilot Chat identifies issues, you can ask it to fix them directly:

```
/fix Please fix all the issues mentioned above and generate the complete fixed code
```

## Part 6: Advanced Challenges

After completing the basic exercises, you can try the following advanced challenges to further improve your Copilot skills. These challenges will help you explore more advanced features of Copilot and learn to leverage it in more complex scenarios to improve development efficiency. Remember, proficient use of Copilot requires continuous practice and experimentation — only by applying it extensively in real projects can you truly master its essence.

### Challenge 1: Use Copilot Chat to Generate Regular Expressions

Describe the pattern you need to match in Chat:

```
Please help me write a regular expression to validate Chinese mobile phone numbers (11 digits, starting with 1, second digit is 3-9)
Also provide a regular expression for matching Chinese ID card numbers (18 digits)
```

### Challenge 2: Use Copilot to Implement a Complete Project

Create a new project and guide Copilot to complete the entire project through comments only:

```python
# Project: Simple To-Do List Manager
# Requirements:
# 1. Command-line interface
# 2. Support adding, deleting, marking as complete, and listing to-do items
# 3. Data persistence to a JSON file
# 4. Support sorting by priority and due date
# 5. Support searching by keyword
# 6. Use argparse for command-line argument handling

# Please start implementing from here...
```

### Challenge 3: Compare the Effects of Different Prompting Approaches

Try using different comment styles to guide Copilot and observe differences in the quality of generated code:

```python
# Approach 1: Brief comments
# Sorting function

# Approach 2: Detailed comments
# Sort a user list by registration date in descending order
# If registration dates are the same, sort by username alphabetically
# Return a new list without modifying the original list

# Approach 3: Example-driven
# Input: [{"name": "Alice", "date": "2024-01-01"}, {"name": "Bob", "date": "2024-01-02"}]
# Output: [{"name": "Bob", "date": "2024-01-02"}, {"name": "Alice", "date": "2024-01-01"}]
```

## Verification Checklist

After completing the exercise, please confirm the following:

- [ ] Successfully installed and configured the GitHub Copilot extension
- [ ] Able to use Copilot to generate function implementations
- [ ] Able to use Copilot to generate unit tests
- [ ] Able to use Copilot to generate docstrings
- [ ] Able to use Copilot Chat for code review
- [ ] Understand how to guide Copilot by writing better comments

## FAQ

### Q1: What should I do if Copilot doesn't provide any suggestions?

Check the following:
- Confirm you are signed in to your GitHub account
- Confirm your Copilot subscription is active
- Check if the Copilot icon in the bottom-right corner of VS Code is functioning normally
- Try reloading the VS Code window

### Q2: What should I do if Copilot generates code with errors?

Copilot's generated code may not always be correct. You should:
- Always review the generated code logic
- Run tests to verify code correctness
- Use Copilot Chat to request explanations and corrections

### Q3: How can I improve the quality of Copilot's suggestions?

- Write clear and detailed comments
- Use meaningful variable and function names
- Provide type hints
- Keep code context complete

## Summary

Through this exercise, you learned how to use GitHub Copilot to improve development efficiency. Copilot can not only complete code but also help you write tests, generate documentation, and review code. Remember, Copilot is an auxiliary tool — the generated code still needs human review and verification. Using Copilot Chat effectively can help you better understand and improve your code. In practice, it's recommended to integrate Copilot into your daily development workflow and let it become your reliable programming assistant. As you gain more experience, you'll find that Copilot can significantly boost your programming efficiency and code quality. At the same time, be aware that Copilot-generated code may have copyright or security issues, so exercise caution when using it in commercial projects. Maintain your enthusiasm for learning new technology, keep exploring Copilot's new features and techniques, and you will go further in your software development journey.
