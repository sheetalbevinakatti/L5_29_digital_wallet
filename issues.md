# Static Code Analysis Issues

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Hardcoded gateway secret | Security | Original line 6 | The gateway secret was embedded directly in the Python source code. | Read the secret from the `GATEWAY_SECRET` environment variable using `os.getenv()`. |
| Insecure OTP generation | Security | Original line 54 | The OTP was generated using `random.randint()`, which is not designed for security-sensitive randomness. | Use `secrets.randbelow()` to generate a six-digit OTP. |
| Weak PIN hashing | Security | Original line 17 | SHA-1 was used to hash the wallet PIN, which is not suitable for secure password storage. | Replace SHA-1 with PBKDF2-HMAC-SHA256 and use constant-time comparison for verification. |
| Unsafe temporary-file creation | Security | Original line 47 | `tempfile.mktemp()` generates a temporary filename without securely creating the file. | Use `tempfile.NamedTemporaryFile()` to create the temporary file securely. |