# Reflection — Lab 5: Static Code Analysis

## 1. What did I learn from static code analysis?

Static code analysis helped me identify code quality, formatting, and security issues without executing every possible program path. Pylint helped improve naming conventions and code quality, Flake8 identified style violations, and Bandit highlighted potential security risks.

## 2. How did the tools complement one another?

The tools served different purposes. Pylint evaluated code quality and maintainability, Flake8 checked Python style and formatting, and Bandit focused on common security issues. Using all three provided a more comprehensive review than relying on a single tool.

## 3. What improvements did I make to the program?

I addressed security findings by removing the hardcoded gateway secret, replacing weak PIN hashing, using secure OTP generation, and replacing unsafe temporary-file creation. I also improved naming conventions, removed an unused parameter, and addressed other Pylint and Flake8 findings while checking that the demonstration's expected output remained consistent.

## 4. What did I learn about the limitations of static analysis?

Static analysis can identify many potential problems, but a clean report does not prove that a program is completely secure or correct. Testing program behaviour is still necessary, and security-sensitive features require additional design and review before they could be used in a real payment system.