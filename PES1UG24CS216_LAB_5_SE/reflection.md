# Reflection — Lab 5: Static Code Analysis

## 1. What is the difference between Pylint, Flake8, and Bandit?

Pylint checks general code quality, likely programming mistakes, naming, and maintainability. Flake8 focuses mainly on Python style and formatting rules. Bandit scans Python source for common security risks, such as unsafe functions and insecure coding patterns. Their checks overlap in places, but they have different main purposes.

## 2. Which issue was most serious, and why?

The insecure temporary-file creation and weak handling of authentication-related values were important security concerns. `tempfile.mktemp()` can leave a gap between choosing a filename and creating the file. SHA-1 is not appropriate for password storage, and a short PIN also needs rate limiting and secure verification. The demo secrets are still hard-coded in this educational example and must be moved to secure configuration before production use.

## 3. How did static analysis improve the program?

Static analysis gives repeatable feedback without requiring every path in the program to be exercised manually. It can reveal security risks, shared mutable state, style inconsistencies, and maintainability problems early. After applying fixes, the same tools can be rerun to check whether the reported issues have been resolved.

## 4. What are the limitations of static analysis?

Static analysis can report false positives and cannot prove that the program is completely secure or correct. It may not detect runtime failures, business-logic errors, or vulnerabilities that depend on configuration and deployment. Testing the program, reviewing the changes, and using secure design practices are still necessary.
