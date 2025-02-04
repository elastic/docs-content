---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-all-permission.html
---

# All permission check [bootstrap-checks-all-permission]

The all permission check ensures that the security policy used during bootstrap does not grant the `java.security.AllPermission` to Elasticsearch. Running with the all permission granted is equivalent to disabling the security manager.

