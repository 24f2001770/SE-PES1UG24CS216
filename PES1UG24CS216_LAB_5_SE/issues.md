# Static Code Analysis Issues — Digital Wallet

The line numbers refer to the original, unmodified `digital_wallet.py`. Verify them against the original file before submission.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Hard-coded gateway secret | Security — low | 6 | A secret embedded in source code may be exposed if the repository is shared. | Read the secret from the `GATEWAY_SECRET` environment variable. The fallback is for demonstration only and must not be used in production. |
| Hard-coded wallet PIN | Security | 7 | A fixed PIN in source code is unsuitable for production authentication. | Read the PIN from the `WALLET_PIN` environment variable. Production systems should use secure PIN verification and rate limiting. |
| Weak SHA-1 PIN hashing | Security | 13–14, 33 | SHA-1 is unsuitable for password storage, and a four-digit PIN has low entropy. | Removed SHA-1 hashing and used `hmac.compare_digest`. Production authentication requires secure credential storage and rate limiting. |
| Mutable default argument | Bug | 17 | `log=[]` is shared across function calls. | Changed the default to `None` and append only when a list is explicitly supplied. |
| Insecure temporary filename | Security | 60–61 | `tempfile.mktemp()` selects a filename without securely creating the file. | Replaced it with `NamedTemporaryFile(delete=False)`. |
| Non-cryptographic OTP generation | Security | 64 | `random.randint()` is not designed for security-sensitive tokens. | Replaced it with `secrets.randbelow()` to generate a six-digit OTP. |
| Payment amount validation | Bug | 36 | Zero or negative payment amounts were not explicitly rejected. | Reject amounts less than or equal to zero before changing the wallet balance. |
| Naming and formatting problems | Style | Multiple | CamelCase names, long lines, and inconsistent formatting reduce readability. | Used snake_case function names and formatted long statements across multiple lines. |
