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

This error occurs when the access token used for authentication has expired. When token-based authentication is enabled in {{es}}, each access token has a limited lifespan. If a token is used after its expiration time, {{es}} rejects the request.

To fix, 
- **Refresh the token** – Obtain a new token using your token refresh workflow.
- **Implement automatic token refresh** – Ensure your application is configured to refresh tokens before expiration.
- **Avoid using expired tokens** – Do not reuse tokens after logout or expiration.
- **Adjust token lifespan if needed** – You can configure a longer token expiration in `elasticsearch.yml`, though this should be balanced against security needs:

   ```yaml
   xpack.security.authc.token.timeout: 20m
   ```
