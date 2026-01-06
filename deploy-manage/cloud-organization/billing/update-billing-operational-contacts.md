---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-billing-contacts.html
applies_to:
  deployment:
    ess: all
  serverless: all
products:
  - id: cloud-hosted
---

# Update billing and operational contacts [ec-billing-contacts]

If different persons from your organization are involved in billing and operations, you can specify their relevant contact details. These additional contacts only receive billing or operational emails. 

By default, these notifications are sent to all users within an {{ecloud}} organization. If you specify billing and operational email contacts, then only these contacts and the organization owner will receive billing and operational emails.

::::{note} 
Operational contacts can only receive operational notifications, such as out-of-memory alerts. Operational and billing contacts can’t log in to {{ecloud}}. To log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body),   you must log in as the [organization owner](/deploy-manage/users-roles/cloud-organization/user-roles.md), or be [a member](/deploy-manage/users-roles/cloud-organization.md) of the organization.
::::


To update billing and operational contacts, or set an email address for monitoring alerts:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From a deployment or project on the home page, select **Manage**.
3. From the lower navigation menu, select **Organization**.
4. On the **Contacts** page, specify your new contacts.
  
You can specify multiple email addresses for each category. They become effective immediately and no further confirmation of the email addresses is required.

