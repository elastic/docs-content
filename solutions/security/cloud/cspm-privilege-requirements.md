---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/cspm-required-permissions.html
  - https://www.elastic.co/guide/en/serverless/current/cspm-required-permissions.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# CSPM privilege requirements

This page lists required privileges for {{elastic-sec}}'s CSPM features. There are three access levels: read, write, and manage. Each access level and its requirements are described next on this page.


## Read [_read]

Users with these minimum permissions can view data on the **Findings** page and the Cloud Posture dashboard.


### {{es}} index privileges [_es_index_privileges]

`Read` privileges for the following {{es}} indices:

* `logs-cloud_security_posture.findings_latest-*`
* `logs-cloud_security_posture.scores-*`
* {applies_to}`stack: ga 9.1` {applies_to}`serverless: ga` `security_solution-cloud_security_posture.misconfiguration_latest*`


### {{kib}} privileges [_kib_privileges]

* `Security: Read`


## Write [_write]

Users with these minimum permissions can view data on the **Findings** page and the Cloud Posture dashboard, create detection rules from the findings details flyout, and enable or disable benchmark rules.


### {{es}} index privileges [_es_index_privileges_2]

`Read` privileges for the following {{es}} indices:

* `logs-cloud_security_posture.findings_latest-*`
* `logs-cloud_security_posture.scores-*`
* {applies_to}`stack: ga 9.1` {applies_to}`serverless: ga` `security_solution-cloud_security_posture.misconfiguration_latest*`



### {{kib}} privileges [_kib_privileges_2]

* `Security: All`


## Manage [_manage_2]

Users with these minimum permissions can view data on the **Findings** page and the Cloud Posture dashboard, create detection rules from the findings details flyout, enable or disable benchmark rules, and install, update, or uninstall CSPM integrations and assets.


### {{es}} index privileges [_es_index_privileges_3]

`Read` privileges for the following {{es}} indices:

* `logs-cloud_security_posture.findings_latest-*`
* `logs-cloud_security_posture.scores-*`
* {applies_to}`stack: ga 9.1` {applies_to}`serverless: ga` `security_solution-cloud_security_posture.misconfiguration_latest*`



### {{kib}} privileges [_kib_privileges_3]

* `Security: All`
* `Spaces: All`
* `Fleet: All`
* `Integrations: All`
