---
navigation_title: Authorization errors
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-trb-roles.html
---

# Troubleshoot authorization errors  [security-trb-roles]

**Symptoms:**

* I configured the appropriate roles and the users, but I still get an authorization exception.
* I can authenticate to LDAP, but I still get an authorization exception.

**Resolution:**

1. Verify that the role names associated with the users match the roles defined in the `roles.yml` file. You can use the `elasticsearch-users` tool to list all the users. Any unknown roles are marked with `*`.

    ```shell
    bin/elasticsearch-users list
    rdeniro        : admin
    alpacino       : power_user
    jacknich       : monitoring,unknown_role* <1>
    ```

    1. `unknown_role` was not found in `roles.yml`


    For more information about this command, see the [`elasticsearch-users` command](https://www.elastic.co/guide/en/elasticsearch/reference/current/users-command.html).

2. If you are authenticating to LDAP, a number of configuration options can cause this error.

    |     |     |
    | --- | --- |
    | *group identification* | Groups are located by either an LDAP search or by the "memberOf" attribute onthe user. Also, If subtree search is turned off, it will search only onelevel deep. For all the options, see [LDAP realm settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-settings.html#ref-ldap-settings).There are many options here and sticking to the defaults will not work for allscenarios. |
    | *group to role mapping* | Either the `role_mapping.yml` file or the location for this file could bemisconfigured. For more information, see [Security files](../../../deploy-manage/security.md). |
    | *role definition* | The role definition might be missing or invalid. |

    To help track down these possibilities, enable additional logging to troubleshoot further. You can enable debug logging by configuring the following persistent setting:

    ```console
    PUT /_cluster/settings
    {
      "persistent": {
        "logger.org.elasticsearch.xpack.security.authc": "debug"
      }
    }
    ```

    Alternatively, you can add the following lines to the end of the `log4j2.properties` configuration file in the `ES_PATH_CONF`:

    ```properties
    logger.authc.name = org.elasticsearch.xpack.security.authc
    logger.authc.level = DEBUG
    ```

    Refer to [configuring logging levels](../../../deploy-manage/monitor/logging-configuration/elasticsearch-log4j-configuration-self-managed.md#configuring-logging-levels) for more information.

    A successful authentication should produce debug statements that list groups and role mappings.


