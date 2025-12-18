# Quick Reference: New Enhanced Rules

## 🔴 Critical Security Rules (ERROR)

### All Languages
- **SQL Injection** - Use parameterized queries
- **Hardcoded Credentials** - Use environment variables
- **Weak Crypto (MD5/SHA1)** - Use SHA-256+
- **eval() Usage** - Never use eval with user input

### JavaScript/TypeScript
- **DOM XSS** - Don't use innerHTML with user input
- **Prototype Pollution** - Avoid __proto__ manipulation
- **Unvalidated Redirect** - Validate URLs before redirecting
- **async forEach** - Use for...of or Promise.all()

### Python
- **Pickle Deserialization** - Never unpickle untrusted data
- **Shell Injection** - Use subprocess with shell=False
- **YAML Unsafe Load** - Use yaml.safe_load()

### Java
- **String Equality** - Use .equals() not ==
- **SQL Statement** - Use PreparedStatement

### Go
- **Defer in Loop** - Causes resource exhaustion
- **time.After in Loop** - Causes memory leak

## ⚠️ Important Warnings

### JavaScript/TypeScript
- **Promise without catch** - Always handle promise rejections
- **Unsafe parseInt** - Always specify radix: parseInt(x, 10)
- **Insecure Random** - Use crypto.randomBytes()

### Java
- **Resource Leak** - Use try-with-resources
- **String Concat in Loop** - Use StringBuilder
- **Null Pointer Risk** - Check for null

### Go
- **Goroutine Leak** - Use context or done channel
- **Weak Random** - Use crypto/rand

### Python
- **Assert in Production** - Don't use assert for validation
- **Requests without Timeout** - Always set timeout
- **Hardcoded Temp Path** - Use tempfile module

## 📋 Rule Count by Language

| Language | Total Rules | ERROR | WARNING | INFO |
|----------|-------------|-------|---------|------|
| JavaScript/TypeScript | 35 | 12 | 15 | 8 |
| Java | 23 | 8 | 10 | 5 |
| Go | 13 | 4 | 6 | 3 |
| Python | 16 | 9 | 5 | 2 |
| Generic (All) | 11 | 3 | 4 | 4 |

**Total: 75 Rules** covering security, performance, best practices, and code quality!
