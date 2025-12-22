# Code Review Automation with Semgrep

This project provides automated code review tools to enforce coding standards and best practices across multiple programming languages.

$ python semgrep-task/header-validator.py semgrep-task/code/

semgrep --config semgrep-task/rules/coding-rules.yml semgrep-task/code/test.go

semgrep --config semgrep-task/rules/coding-rules.yml semgrep-task/code/ --json -o semgrep-report.json

semgrep --config semgrep-task/rules/coding-rules.yml semgrep-task/code/test.js --severity ERROR --severity WARNING

python header-validator.py code/
.
$ semgrep --config=rules/coding-rules.yml code/test.js --severity=ERROR --severity=WARNING



To automatically detect rules based on language command in vs code, just change code file name at end

python semgrep-task/auto-review.py semgrep-task/code/test.js 


To check header-validation.py file

python semgrep-task/header-validator.py semgrep-task/code/

## 📁 Project Structure old

```
semgrep-task/
├── rules/
│   └── coding-rules.yml      # Semgrep rules for code quality checks
├── code/
│   ├── test.js               # Test file with bad practices (for testing)
│   └── good-example.js       # Example file with proper standards
├── header-validator.py       # Python script to validate file headers
└── README.md                 # This file
```

## 📁 Project Structure new 

C:\Users\apshe\Downloads\sample\CodeReview\
├── auto-review.py          ← NEW FILE (Step 3)
├── header-validator.py     ← Keep as is
├── rules\                  ← NEW FOLDER (Step 1)
│   ├── javascript-rules.yml    ← NEW FILE (Step 2)
│   ├── python-rules.yml        ← NEW FILE (Step 2)
│   ├── java-rules.yml          ← NEW FILE (Step 2)
│   ├── go-rules.yml            ← NEW FILE (Step 2)
│   └── common-rules.yml        ← NEW FILE (Step 2)
└── semgrep-task\
    └── code\               ← Your test files stay here
        ├── test.js
        ├── test.py
        ├── test.java
        └── test.go



## 🎯 Features

### 1. **Semgrep Code Quality Rules** (`rules/coding-rules.yml`)

Comprehensive rules covering:

#### JavaScript/TypeScript (17 rules)
- Strict equality (`===` vs `==`)
- Console usage detection
- Const vs let preferences
- Empty catch blocks
- Hard-coded credentials
- Magic numbers

#### Java (10 rules)
- Empty catch blocks
- System.out.println detection
- Interface vs implementation
- Public field detection
- Exception handling

#### Go (6 rules)
- Error handling
- Panic usage
- Global variables
- Channel management

#### Python (3 rules)
- Empty except blocks
- Print statements
- Bare except clauses

#### Security (3 rules)
- SQL injection detection
- Eval() usage
- Hard-coded credentials

#### Code Quality (11 rules)
- DRY principle violations
- Function length
- Input validation
- Documentation
- Naming conventions

### 2. **File Header Validator** (`header-validator.py`)

Validates that all code files have mandatory header comments with:
- **Purpose**: Description of what the file does
- **Author**: Name of the original author
- **Date**: Creation date (YYYY-MM-DD)
- **Modified By**: Change history (Name - Date - Description)

## 🚀 Usage

### Running Semgrep Code Analysis

```bash
# Scan all files in the code directory
semgrep --config rules/coding-rules.yml code/

# Scan a specific file
semgrep --config rules/coding-rules.yml code/test.js

# Output in JSON format
semgrep --config rules/coding-rules.yml code/ --json
```

### Running File Header Validation

```bash
# Validate all files in the code directory
python header-validator.py code

# Validate a different directory
python header-validator.py /path/to/your/code

# Exclude specific directories
python header-validator.py code --exclude node_modules dist build
```

## 📝 Required File Header Format

### For JavaScript/TypeScript/Java/C/C++:
```javascript
/**
 * Purpose: Brief description of what this file does
 * Author: Your Name
 * Date: 2025-12-16
 * Modified By: Jane Doe - 2025-12-17 - Added validation logic
 */
```

### For Python:
```python
# Purpose: Brief description of what this file does
# Author: Your Name
# Date: 2025-12-16
# Modified By: Jane Doe - 2025-12-17 - Added validation logic
```

### For Go:
```go
// Purpose: Brief description of what this file does
// Author: Your Name
// Date: 2025-12-16
// Modified By: Jane Doe - 2025-12-17 - Added validation logic
```

## 📊 Example Output

### Semgrep Output:
```
┌─────────────────┐
│ 84 Code Findings │
└─────────────────┘

code\test.js
  ❯❯❱ rules.strict-equality
      Use === instead of == for strict equality comparison
      
      4┆ if (a == "5") {

  ❯❯❱ rules.hardcoded-password
      Never hard-code passwords. Use environment variables
      
      48┆ const password = "admin123";
```

### Header Validator Output:
```
======================================================================
FILE HEADER VALIDATION REPORT
======================================================================

Total files checked: 2
Files passed: 1
Files failed: 1

[FAIL] test.js
       Missing fields: purpose, author, date, modified
```

## ✅ Code Review Checklist

The rules enforce the following standards:

- [ ] Code readability and formatting
- [ ] Meaningful naming conventions
- [ ] No hard-coded credentials
- [ ] Proper error handling
- [ ] Input validation
- [ ] No SQL injection vulnerabilities
- [ ] Proper use of constants
- [ ] Single Responsibility Principle
- [ ] DRY (Don't Repeat Yourself)
- [ ] Proper documentation
- [ ] File header with metadata

## 🔧 Installation

### Prerequisites:
```bash
# Install Semgrep
pip install semgrep

# Or using Homebrew (macOS)
brew install semgrep
```

### Python Requirements:
- Python 3.6 or higher (for header-validator.py)
- No additional dependencies required

## 📚 References

- [Semgrep Documentation](https://semgrep.dev/docs/)
- [Semgrep Rule Syntax](https://semgrep.dev/docs/writing-rules/rule-syntax/)
- [OWASP Coding Standards](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)

## 🤝 Contributing

To add new rules:

1. Edit `rules/coding-rules.yml`
2. Add your rule following the existing pattern
3. Test with `semgrep --config rules/coding-rules.yml code/`
4. Update this README with the new rule description

## 📄 License

This project is for educational and internal company use.

---

**Created**: 2025-12-16  
**Last Updated**: 2025-12-16
