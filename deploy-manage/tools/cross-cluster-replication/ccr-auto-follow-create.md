---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-auto-follow-create.html
---

# Create auto-follow patterns [ccr-auto-follow-create]

When you [create an auto-follow pattern](ccr-getting-started-auto-follow.md), you are configuring a collection of patterns against a single remote cluster. When an index is created in the remote cluster with a name that matches one of the patterns in the collection, a follower index is configured in the local cluster. The follower index uses the new index as its leader index.

Use the [create auto-follow pattern API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ccr-put-auto-follow-pattern) to add a new auto-follow pattern configuration.

