---
applies_to:
  stack: all
  serverless:
    security: all
---

# CNVM privilege requirements [cnvm-required-permissions]

This page lists required privileges for {{elastic-sec}}'s CNVM features. There are three access levels: `read`, `write`, and `manage`. Each access level and its requirements are described next on this page.

## Read

Users with these minimum permissions can view data on the **Findings** page.

### {{es}} index privileges

`Read` privileges for the following {{es}} indices:

* `logs-cloud_security_posture.vulnerabilities_latest-default`
* `logs-cloud_security_posture.scores-default`

### {{kib}} privileges

* `Security: Read`

## Write

Users with these minimum permissions can view data on the **Findings** page and create detection rules from the findings details flyout.

### {{es}} index privileges
`Read` privileges for the following {{es}} indices:

* `logs-cloud_security_posture.vulnerabilities_latest-default`
* `logs-cloud_security_posture.scores-default`

### {{kib}} privileges

* `Security: All`


## Manage

Users with these minimum permissions can view data on the **Findings** page, create detection rules from the findings details flyout, and install, update, or uninstall integrations and assets.

### {{es}} index privileges

`Read` privileges for the following {{es}} indices:

* `logs-cloud_security_posture.vulnerabilities_latest-default`
* `logs-cloud_security_posture.scores-default`

### {{kib}} privileges

* `Security: All`
* `Spaces: All`
* `Fleet: All`
* `Integrations: All`

