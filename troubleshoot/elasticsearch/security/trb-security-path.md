---
navigation_title: Configuration file locations
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/trb-security-path.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
---

# Diagnose configuration file location issues [trb-security-path]

**Symptoms:**

* Active Directory or LDAP realms might stop working after upgrading to {{es}} 6.3 or later releases. In 6.4 or later releases, you might see messages in the {{es}} log that indicate a config file is in a deprecated location.

**Resolution:**

By default, in 6.2 and earlier releases, the security configuration files are located in the `ES_PATH_CONF/x-pack` directory, where `ES_PATH_CONF` is an environment variable that defines the location of the [config directory](../../../deploy-manage/deploy/self-managed/configure-elasticsearch.md#config-files-location).

In 6.3 and later releases, the config directory no longer contains an `x-pack` directory. The files that were stored in this folder, such as the `log4j2.properties`, `role_mapping.yml`, `roles.yml`, `users`, and `users_roles` files, now exist directly in the config directory.

::::{important}
If you upgraded to 6.3 or later releases, your old security configuration files still exist in an `x-pack` folder. That file path is deprecated, however, and you should move your files out of that folder.
::::


In 6.3 and later releases, settings such as `files.role_mapping` default to `ES_PATH_CONF/role_mapping.yml`. If you do not want to use the default locations, you must update the settings appropriately. See [Security settings](../../../deploy-manage/deploy/self-managed/configure-elasticsearch.md).

