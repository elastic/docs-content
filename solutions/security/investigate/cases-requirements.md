---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/case-permissions.html
  - https://www.elastic.co/guide/en/serverless/current/security-cases-requirements.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Cases requirements [security-cases-requirements]

::::{note}
- To send cases to external systems, ensure you have the appropriate [{{stack}} subscription](https://www.elastic.co/pricing) or [{{serverless-short}} project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md).

- You need particular subscriptions and privileges to manage case attachments. For example in {{stack}}, to add alerts to cases, you must have privileges for [managing alerts](/solutions/security/detect-and-alert/detections-requirements.md#enable-detections-ui). In {{serverless-short}}, you need the Security Analytics Complete [project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md).

- If you have an on-premises deployment and want email notifications and external incident management systems to contain links back to {{kib}}, you must configure the [server.publicBaseUrl](kibana://reference/configuration-reference/general-settings.md#server-publicbaseurl) setting.
::::


To grant access to cases in a custom role, set the privileges for the **Cases** and **{{connectors-feature}}** features as follows:

% Management might be called Stack Management in Serverless.

| Action | {{kib}} Privileges |
| --- | --- |
| Give full access to manage cases and settings | - **All** for the **Cases** feature under **Security**<br> - **All** for the **{{connectors-feature}}** feature under **Management**<br><br>**Note:** Roles without **All** privileges for the **{{connectors-feature}}** feature cannot create, add, delete, or modify case connectors. <br><br> By default, **All** for the **Cases** feature allows you to have full control over cases, including deleting them, editing case settings, and more. <br><br><br><br> |
| Give assignee access to cases | **All** for the **Cases** feature under **Security**<br><br>**Note:** Before a user can be assigned to a case, they must log into {{kib}} at least once, which creates a user profile. <br><br> |
| Give view-only access for cases | **Read** for the **Security** feature and **All** for the **Cases** feature<br><br> **Note:** You can customize the sub-feature privileges to allow access to deleting cases, deleting alerts and comments from cases, viewing or editing case settings, adding case comments and attachments, and re-opening cases. <br><br> |
| Revoke all access to cases | **None** for the **Cases** feature under **Security** |
