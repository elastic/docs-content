---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-auto-follow-retrieve.html
applies_to:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---

# Retrieve auto-follow patterns [ccr-auto-follow-retrieve]

To view existing auto-follow patterns and edit their settings, [access {{kib}}](manage-auto-follow-patterns.md#ccr-access-ccr-auto-follow) on your local cluster.

Select the auto-follow pattern that you want to view or edit. You can also view the follower indices created by the pattern.

Use the [get auto-follow pattern API]({{es-apis}}operation/operation-ccr-get-auto-follow-pattern-1) to inspect all configured auto-follow pattern collections.

