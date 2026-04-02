---
navigation_title: Nodes info API response
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-trb-settings.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Troubleshoot a nodes info API response [security-trb-settings]

**Symptoms:**

* When you use the [nodes info API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-info) to retrieve settings for a node, some information is missing.

**Resolution:**

This is intentional. Some of the settings are considered to be highly sensitive: all `ssl` settings, ldap `bind_dn`, and `bind_password`. For this reason, we filter these settings and do not expose them via the nodes info API rest endpoint. You can also define additional sensitive settings that should be hidden using the `xpack.security.hide_settings` setting. For example, this snippet hides the `url` settings of the `ldap1` realm and all settings of the `ad1` realm.

```yaml
xpack.security.hide_settings: xpack.security.authc.realms.ldap1.url,
xpack.security.authc.realms.ad1.*
```

