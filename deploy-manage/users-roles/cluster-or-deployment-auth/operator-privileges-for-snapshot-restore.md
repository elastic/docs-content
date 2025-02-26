---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/operator-only-snapshot-and-restore.html
applies_to:
  deployment:
    ess: 
    ece: 
    eck: 
---

# Operator privileges for snapshot and restore [operator-only-snapshot-and-restore]

::::{admonition} Indirect use only
This feature is designed for indirect use by {{ech}}, {{ece}}, and {{eck}}. Direct use is not supported.
::::


Invoking [operator-only APIs](operator-only-functionality.md#operator-only-apis) or updating [operator-only dynamic cluster settings](operator-only-functionality.md#operator-only-dynamic-cluster-settings) typically results in changes in the cluster state. The cluster state can be included in a cluster [snapshot](../../tools/snapshot-and-restore.md). Snapshots are a great way to preserve the data of a cluster, which can later be restored to bootstrap a new cluster, perform migration, or disaster recovery, for example. In a traditional self-managed environment, the intention is for the restore process to copy the entire cluster state over when requested. However, in a more managed environment, such as [{{ech}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body), data that is associated with [operator-only functionality](operator-only-functionality.md) is explicitly managed by the infrastructure code.

Restoring snapshot data associated with operator-only functionality could be problematic because:

1. A snapshot could contain incorrect values for operator-only functionalities. For example, the snapshot could have been taken in a different cluster where requirements are different or the operator privileges feature is not enabled. Restoring data associated with operator-only functionality breaks the guarantee of operator privileges.
2. Even when the infrastructure code can correct the values immediately after a restore, there will always be a short period of time when the cluster could be in an inconsistent state.
3. The infrastructure code prefers to configure operator-only functionality from a single place, that is to say, through API calls.

Therefore, [when the operator privileges feature is enabled](configure-operator-privileges.md), snapshot data that is associated with any operator-only functionality is **not** restored.

::::{note} 
That information is still included when taking a snapshot so that all data is always preserved.
::::


