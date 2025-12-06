---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/internal-users.html
applies_to:
  stack: all
products:
  - id: elasticsearch
---

# Internal users [internal-users]

::::{note} 
These users are designed for internal use by {{es}} only. Authenticating with these users is not supported.
::::


The {{stack-security-features}} use eight *internal* users (`_system`, `_xpack`, `_xpack_security`, `_async_search`, `_security_profile`, `_data_stream_lifecycle`, `_synonyms` and `_storage`), which are responsible for the operations that take place inside an {{es}} cluster.

These users are only used by requests that originate from within the cluster. For this reason, they cannot be used to authenticate against the API and there is no password to manage or reset.

From time-to-time you may find a reference to one of these users inside your logs, including [audit logs](../../security/logging-configuration/enabling-audit-logs.md).

