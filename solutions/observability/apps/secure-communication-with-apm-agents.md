---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-secure-agent-communication.html
---

# Secure communication with APM agents [apm-secure-agent-communication]

Communication between APM agents and {{agent}} can be both encrypted and authenticated. It is strongly recommended to use both TLS encryption and authentication as secrets are sent as plain text.

* [TLS encryption](apm-agent-tls-communication.md)
* [API key authentication](api-keys.md)
* [Secret token authentication](secret-token.md)

As soon as an authenticated communication is enabled, requests without a valid token or API key will be denied. If both API keys and a secret token are enabled, APM agents can choose whichever mechanism they support.

In some use-cases, like when an {{apm-agent}} is running on the client side, authentication is not possible. See [Anonymous authentication](anonymous-authentication.md) for more information.





