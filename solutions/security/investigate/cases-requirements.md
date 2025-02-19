---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/case-permissions.html
  - https://www.elastic.co/guide/en/serverless/current/security-cases-requirements.html
---

# Cases requirements

% What needs to be done: Align serverless/stateful

% Use migrated content from existing pages that map to this page:

% - [x] ./raw-migrated-files/security-docs/security/case-permissions.md
% - [ ] ./raw-migrated-files/docs-content/serverless/security-cases-requirements.md

You can create roles and define feature privileges at different levels to manage feature access in {{kib}}. {{kib}} privileges grant access to features within a specified {{kib}} space, and you can grant full or partial access. For more information, refer to [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md#adding_kibana_privileges).

::::{note}
To send cases to external systems, you need the [appropriate license](https://www.elastic.co/subscriptions).

If you are using an on-premises {{kib}} deployment and want the email notifications and the external incident management systems to contain links back to {{kib}}, you must configure the [server.publicBaseUrl](/deploy-manage/deploy/self-managed/configure.md#server-publicBaseUrl) setting.

::::


::::{important}
Certain subscriptions and privileges might be required to manage case attachments. For example, to add alerts to cases, you must have privileges for [managing alerts](/solutions/security/detect-and-alert/detections-requirements.md#enable-detections-ui).
::::


To grant access to cases, set the privileges for the **Cases** and **{{connectors-feature}}** features as follows:

| Action | {{kib}} Privileges |
| --- | --- |
| Give full access to manage cases and settings | * **All** for the **Cases** feature under **Security**<br>* **All*** for the **{{connectors-feature}}** feature under **Management**<br><br>::::{note} <br>Roles without ***All** privileges for the **{{connectors-feature}}** feature cannot create, add, delete, or modify case connectors.<br><br>By default, **All** for the **Cases** feature allows you to delete cases, delete alerts and comments from cases, and edit case settings. You can customize the sub-feature privileges to limit feature access.<br><br>::::<br><br> |
| Give assignee access to cases | **All** for the **Cases** feature under **Security**<br><br>::::{note} <br>Before a user can be assigned to a case, they must log into {{kib}} at least once, which creates a user profile.<br>::::<br><br> |
| Give view-only access for cases | **Read** for the **Security** feature and **All** for the **Cases** feature<br><br>::::{note} <br>You can customize the sub-feature privileges to allow access to deleting cases, deleting alerts and comments from cases, viewing or editing case settings, adding case comments and attachments, and re-opening cases.<br>::::<br><br> |
| Revoke all access to cases | **None** for the **Cases** feature under **Security** |
