---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/trb-security-internalserver.html
---

# Internal Server Error in Kibana [trb-security-internalserver]

**Symptoms:**

* In 5.1.1, an `UnhandledPromiseRejectionWarning` occurs and {{kib}} displays an Internal Server Error.

**Resolution:**

If the Security plugin is enabled in {{es}} but disabled in {{kib}}, you must still set `elasticsearch.username` and `elasticsearch.password` in `kibana.yml`. Otherwise, {{kib}} cannot connect to {{es}}.

