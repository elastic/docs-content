---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-operational-emails.html
applies_to:
  deployment:
    ess: all
---

# Operational emails [ec-operational-emails]

To help keep you aware of potential performance issues in your {{ech}} clusters, we send email alerts based on certain types of activity. These alerts let you know about:

* High disk usage
* A node out-of-memory restart

For high disk usage, an email alert is activated when the space consumed on one of your nodes is greater than or equal to 90% of capacity, over two consecutive 15-minute intervals. If the problem persists, a new alert is sent every 24 hours. Once the disk usage is no longer above the threshold, we send another note to let you know that the problem is resolved.

We also send an email alert if one of the nodes in your cluster is restarted due to an out-of-memory condition.

By default, these alerts are sent to all users within an {{ecloud}} organization.

Alternatively, you can configure recipients external to an {{ecloud}} organization for these notifications by updating the list of [operational email contacts](/deploy-manage/cloud-organization/billing/update-billing-operational-contacts.md). These can be any email address, meaning that an external distribution list or automated service can receive notifications without the need to be added to the organization directly. If you specify operational email contacts, then only these contacts and the organization owner will receive operational emails.