---
applies_to:
  stack: 
  deployment:
    eck: 
    ess: 
    ece: 
    self: 
navigation_title: "Error: token expired"
# is mapped_pages needed for newly created docs?
---

# Fix token expired error in Elasticsearch [token-expired]

```console
Error: token expired
```

This error occurs when the access token used for authentication has expired. Tokens are typically time-bound, and this error appears when the session outlasts the token’s validity.

## What it means

When token-based authentication is enabled in Elasticsearch, each access token has a limited lifespan. If a token is used after its expiration time, Elasticsearch rejects the request.

## Common causes

- Access token used beyond its expiration window
- Application not handling token refresh properly
- Long-lived sessions without token renewal

## How to resolve it

1. **Refresh the token** – Obtain a new token using your token refresh workflow.
2. **Implement automatic token refresh** – Ensure your application is configured to refresh tokens before expiration.
3. **Avoid using expired tokens** – Do not reuse tokens after logout or expiration.
4. **Adjust token lifespan if needed** – You can configure a longer token expiration in `elasticsearch.yml`, though this should be balanced against security needs:

   ```yaml
   xpack.security.authc.token.timeout: 20m
   ```
