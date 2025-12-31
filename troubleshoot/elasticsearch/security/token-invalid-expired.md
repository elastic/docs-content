---
applies_to:
  stack:
navigation_title: "Error: Token invalid or expired"
---

# Fix errors: Invalid token or token expired in {{es}} [token-invalid-expired]

```console
Error: token expired
```

```console
Error: invalid token
```

These errors occur when {{es}} receives a request containing an invalid or expired token during authentication. They're typically caused by missing, incorrect, or outdated tokens. If an invalid or expired token is used, {{es}} rejects the request.

## Invalid token

{{es}} rejects requests with invalid authentication tokens. Common causes include:

- The token is expired or revoked
- The token format is incorrect or malformed
- The Authorization header is missing or doesn’t start with Bearer
- The client or middleware failed to attach the token properly
- Security settings in {{es}} are misconfigured

To resolve this error:

- Verify the token and ensure it's correctly formatted and current.
- Check expiration and generate a new token if needed.
- Inspect your client and confirm the token is sent in the `Authorization` header.
- Review {{es}} settings and check that token auth is enabled:

   ```yaml
   xpack.security.authc.token.enabled: true
   ```

- Use logs for details: {{es}} logs may provide context about the failure.


## Token expired

This error occurs when {{es}} receives a request containing an expired token during authentication.

To resolve this issue:

- Refresh the token, and obtain a new token using your token refresh workflow.
- Implement automatic token refresh and ensure your application is configured to refresh tokens before expiration.
- Avoid using expired tokens and do not reuse tokens after logout or expiration.
- Adjust token lifespan if needed and configure a longer token expiration in `elasticsearch.yml`, though this should be balanced against security needs:

   ```yaml
   xpack.security.authc.token.timeout: 20m
   ```
   