---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-secure-agent-communication.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
---

# Secure communication with APM agents [apm-secure-agent-communication]

Communication between APM agents and {{agent}} can be both encrypted and authenticated. It is strongly recommended to use both TLS encryption and authentication as secrets are sent as plain text.

* [TLS encryption](/solutions/observability/apm/apm-agent-tls-communication.md)
* [API key authentication](/solutions/observability/apm/api-keys.md)
* [Secret token authentication](/solutions/observability/apm/secret-token.md)

As soon as an authenticated communication is enabled, requests without a valid token or API key will be denied. If both API keys and a secret token are enabled, APM agents can choose whichever mechanism they support.

In some use-cases, like when an {{apm-agent}} is running on the client side, authentication is not possible. See [Anonymous authentication](/solutions/observability/apm/anonymous-authentication.md) for more information.

