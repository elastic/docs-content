---
applies_to:
  stack: 
  deployment:
    eck: 
    ess: 
    ece: 
    self: 
navigation_title: "Error: Invalid token"
# is mapped_pages needed for newly created docs?
---

# Fix error: Invalid token [invalid-token]

```console
Error: invalid token
```

This error occurs when {{es}} receives a request containing an invalid or [expired token](token-expired.md) during authentication. It's typically caused by missing, incorrect, or outdated tokens.

**Symptoms**

With security enabled in {{es}}, clients must authenticate using valid tokens. If a token is invalid or expired, the request is rejected.

This can be caused by

- Expired or revoked token
- Incorrect or malformed token format
- Missing `Authorization` header or wrong scheme (e.g., missing `Bearer` prefix)
- Token not properly attached by client or middleware
- Misconfigured security settings in {{es}}

**Resolution**

1. **Verify the token** – Ensure it’s correctly formatted and current.
2. **Check expiration** – Generate a new token if needed.
3. **Inspect your client** – Confirm the token is sent in the `Authorization` header.
4. **Review {{es}} settings** – Check that token auth is enabled:

   ```yaml
   xpack.security.authc.token.enabled: true
   ```

5. **Use logs for details** – {{es}} logs may provide context about the failure.

