# Security files [security-files]

The {{es}} {security-features} use the following files:

* `ES_PATH_CONF/roles.yml` defines the roles in use on the cluster. See [Defining roles](../../../deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md).
* `ES_PATH_CONF/elasticsearch-users` defines the users and their hashed passwords for the `file` realm. See [File-based user authentication](../../../deploy-manage/users-roles/cluster-or-deployment-auth/file-based.md).
* `ES_PATH_CONF/elasticsearch-users_roles` defines the user roles assignment for the `file` realm. See [File-based user authentication](../../../deploy-manage/users-roles/cluster-or-deployment-auth/file-based.md).
* `ES_PATH_CONF/role_mapping.yml` defines the role assignments for a Distinguished Name (DN) to a role. This allows for LDAP and Active Directory groups and users and PKI users to be mapped to roles. See [Mapping users and groups to roles](../../../deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md).
* `ES_PATH_CONF/log4j2.properties` contains audit information. See [Logfile audit output](../../../deploy-manage/monitor/logging-configuration/logfile-audit-output.md).

::::{important} 
:name: security-files-location

Any files that the {{security-features}} use must be stored in the {{es}} configuration directory. {{es}} runs with restricted permissions and is only permitted to read from the locations configured in the directory layout for enhanced security.
::::


Several of these files are in the YAML format. When you edit these files, be aware that YAML is indentation-level sensitive and indentation errors can lead to configuration errors. Avoid the tab character to set indentation levels, or use an editor that automatically expands tabs to spaces.

Be careful to properly escape YAML constructs such as `:` or leading exclamation points within quoted strings. Using the `|` or `>` characters to define block literals instead of escaping the problematic characters can help avoid problems.

