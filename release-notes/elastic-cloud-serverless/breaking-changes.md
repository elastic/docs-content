---
navigation_title: Breaking changes
products:
  - id: cloud-serverless
---

# {{serverless-full}} breaking changes [elastic-cloud-serverless-breaking-changes]

## August 25, 2025 [elastic-cloud-serverless-08252025-breaking]

* Allows partial results by default in {{esql}} [#125060](https://github.com/elastic/elasticsearch/pull/125060)

## August 11, 2025 [elastic-cloud-serverless-08112025-breaking]

* Improves advanced settings management APIs privilege checks [#230067]({{kib-pull}}230067)

## March 10, 2025 [serverless-changelog-03102025-breaking]

:::{dropdown} Drop `TLS_RSA` cipher support for JDK 24

 This change removes `TLS_RSA` ciphers from the list of default supported ciphers, for {{es}} deployments running on JDK 24.
 
 **Impact:**
 
 The dropped ciphers are `TLS_RSA_WITH_AES_256_GCM_SHA384`, `TLS_RSA_WITH_AES_128_GCM_SHA256`, `TLS_RSA_WITH_AES_256_CBC_SHA256`, `TLS_RSA_WITH_AES_128_CBC_SHA256`, `TLS_RSA_WITH_AES_256_CBC_SHA`, and `TLS_RSA_WITH_AES_128_CBC_SHA`.
TLS connections to {{es}} using these ciphers will no longer work.
Configure your clients to use one of supported cipher suites.

For more information, view [#123600](https://github.com/elastic/elasticsearch/pull/123600).

## June 23, 2025 [serverless-changelog-06232025]

* {{esql}}: Disallows mixed quoted/unquoted patterns in `FROM` commands [#127636]({{es-pull}}127636)
