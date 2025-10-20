---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-getting-started-auto-follow.html
applies_to:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---

# Create an auto-follow pattern to replicate time series indices [ccr-getting-started-auto-follow]

You use [auto-follow patterns](manage-auto-follow-patterns.md) to automatically create new followers for rolling time series indices. Whenever the name of a new index on the remote cluster matches the auto-follow pattern, a corresponding follower index is added to the local cluster. Note that only indices created on the remote cluster after the auto-follow pattern is created will be auto-followed: existing indices on the remote cluster are ignored even if they match the pattern.

An auto-follow pattern specifies the remote cluster you want to replicate from, and one or more index patterns that specify the rolling time series indices you want to replicate.

To create an auto-follow pattern from in {{kib}}:

1. Go to the **Cross Cluster Replication** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Choose the **Auto-follow patterns** tab.
3. Enter a name for the auto-follow pattern, such as `beats`.
4. Choose the remote cluster that contains the index you want to replicate, which in the example scenario is Cluster A.
5. Enter one or more index patterns that identify the indices you want to replicate from the remote cluster. For example, enter `metricbeat-* packetbeat-*` to automatically create followers for {{metricbeat}} and {{packetbeat}} indices.
6. Enter **follower-** as the prefix to apply to the names of the follower indices so you can more easily identify replicated indices.

As new indices matching these patterns are created on the remote, {{es}} automatically replicates them to local follower indices.

:::{image} /deploy-manage/images/elasticsearch-reference-auto-follow-patterns.png
:alt: The Auto-follow patterns page in {{kib}}
:screenshot:
:::

::::{dropdown} API example
Use the [create auto-follow pattern API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ccr-put-auto-follow-pattern) to configure auto-follow patterns.

```console
PUT /_ccr/auto_follow/beats
{
  "remote_cluster" : "leader",
  "leader_index_patterns" :
  [
    "metricbeat-*", <1>
    "packetbeat-*" <2>
  ],
  "follow_index_pattern" : "{{leader_index}}-copy" <3>
}
```

1. Automatically follow new {{metricbeat}} indices.
2. Automatically follow new {{packetbeat}} indices.
3. The name of the follower index is derived from the name of the leader index by adding the suffix `-copy` to the name of the leader index.


::::


