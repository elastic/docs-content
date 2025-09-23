---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-auto-follow-delete.html
applies_to:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---

# Delete auto-follow patterns [ccr-auto-follow-delete]

To delete an auto-follow pattern collection, [access {{kib}}](manage-auto-follow-patterns.md#ccr-access-ccr-auto-follow), select the auto-follow pattern, and pause replication.

When the pattern status changes to Paused, choose **Manage pattern > Delete pattern**.

Use the [delete auto-follow pattern API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ccr-delete-auto-follow-pattern) to delete a configured auto-follow pattern collection.

