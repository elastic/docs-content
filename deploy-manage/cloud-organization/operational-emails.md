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

These alerts are sent to all users within an {{ecloud}} organization, as well as to the email addresses listed as operational email contacts. This means that an external distribution list or automated service can receive notifications without the need to be added to the organization directly.

To configure recipients external to an {{ecloud}} organization for these notifications, update the list of [operational email contacts](/deploy-manage/cloud-organization/billing/update-billing-operational-contacts.md).
