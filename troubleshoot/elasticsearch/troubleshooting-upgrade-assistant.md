---
navigation_title: "Upgrade Assistant"
description: "Common Upgrade Assistant issues and how to resolve them."
type: troubleshooting
applies_to:
  stack: ga
products:
  - id: kibana
  - id: cloud-enterprise
  - id: cloud-hosted
  - id: cloud-kubernetes
  - id: elasticsearch
---

# Resolve Upgrade Assistant issues [troubleshooting-upgrade-assistant]

The [](/deploy-manage/upgrade/prepare-to-upgrade/upgrade-assistant.md) checks your cluster for problems that can block or affect an upgrade to the next major version, and guides you through resolving them. This page covers the most common issues it reports, and how to fix them.

For issues that can occur during the upgrade itself, refer to [](/troubleshoot/elasticsearch/troubleshooting-upgrades.md).

## Migration errors [troubleshooting-upgrade-assistant-migrations]

{{es}} indices are [compatible across sequential major versions](/deploy-manage/upgrade/deployment-or-cluster/reading-indices-from-older-elasticsearch-versions.md) only. [Migrate older indices]({{es-apis}}group/endpoint-migration) before you upgrade; otherwise, a node fails to start with an [index compatibility error](/troubleshoot/elasticsearch/troubleshooting-upgrades.md#troubleshooting-upgrades-errors-bootstrap-index) when you upgrade it to a later version.

The Upgrade Assistant performs these migrations on your behalf, using your account's [permissions](/deploy-manage/upgrade/prepare-to-upgrade/upgrade-assistant.md#_required_permissions_11). Rely on the {{kib}} UI, and fall back to the {{es}} API only when you need to resolve an error. Errors that need your intervention can appear under these steps:

* **Migrate system indices**: If the error `System indices migration failed` appears after you click **Migrate indices**, then click **View migration details** to show the output of the {{es}} [get feature migration information API]({{es-apis}}operation/operation-migration-get-feature-upgrade-status) for errors.
* **Review deprecated settings and resolve issues** for {{es}}: If the error `Old index with a compatibility version` appears, choose one of the available **Action** items: reindex the index or set it to read-only. If you choose reindexing, any issues that occur appear under a **Reindexing error** banner.

Reindexing errors usually stem from configuration problems with templates or index blocks.

### Index block errors [troubleshooting-upgrade-assistant-migrations-blocks]

{{es}} can return `cluster_block_exception` [index block](elasticsearch:/reference/elasticsearch/index-settings/index-block.md) errors. These blocks protect an index and are usually intentional, so review your index's configuration before you remove one.

The most common is `FORBIDDEN/8/index write (api)`, from an index that has the `index.blocks.write` setting enabled. The error looks like this:

```json
{
    "cause":
    {
        "reason": "index [.test-reindexed-for-8] blocked by: [FORBIDDEN/8/index write (api)];",
        "type": "cluster_block_exception"
    },
    "id": "XXXXX",
    "index": ".test-reindexed-for-8",
    "status": 403,
    "type": "_doc"
}
```

For example, this can happen when the target index of a [reindex API]({{es-apis}}operation/operation-reindex) request already existed and had a write block enabled after ingestion.

A cluster experiencing disk watermark issues might also return `FORBIDDEN/12/index read-only / allow delete (api)`. Resolve [watermark errors](/troubleshoot/elasticsearch/fix-watermark-errors.md) before you proceed.

The Upgrade Assistant can warn you about watermark issues that might worsen during the upgrade, with a message such as:

```text
Get disk usage on all nodes below the value specified in cluster.routing.allocation.disk.watermark.low (nodes impacted: [NODE_NAME, NODE_NAME])
```

Treat this as a warning: confirm you have enough disk space for the rolling upgrade before you proceed.

### Template errors [troubleshooting-upgrade-assistant-migrations-templates]

Reindexing can run into the same problems that occur during normal index creation. The most common involve conflicting [index templates](/manage-data/data-store/templates.md), where:

* **The index can't be created.**

  Conflicting templates can block index creation with `IllegalStateException` errors such as:

  * `unable to create new index [X] because it would match composable template [Y]`
  * `unable to create new index [X] because it would match legacy template [Y]`

  Resolve template conflicts before you proceed. To find `overlapping` templates, use the [simulate an index API]({{es-apis}}operation/operation-indices-simulate-index-template).

* **The index is created, but it inherits the wrong settings or mappings.**

  In earlier {{es}} versions, user-created templates could prevent [system indices](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#system-indices) from being created correctly. This most commonly appears as `.security` reindexing or node startup errors such as:

  * `mapping set to strict, dynamic introduction of [allow_restricted_indices] within [indices] is not allowed`
  * `missing _meta field in mapping [_doc] of index [.security]`
  * `failed to notify ClusterStateListener`
  * `cannot read security-version string in index .security`
  * `security index is not on the current version - the native realm will not be operational until the upgrade API is run on the security index`

  For user-managed indices, an index that inherits from an unexpected template most commonly produces reindexing errors such as:

  * `mapper_parsing_exception` due to `reason` of `failed to parse field [V] of type [X] in document with id 'Y'. Preview of field's value: 'Z'`
  * `limit of total fields [X] in index [Y] has been exceeded` because it exceeds the [mapping limit setting](elasticsearch://reference/elasticsearch/index-settings/mapping-limit.md)


:::{tip}
Make sure to review any index template configured to match all indices (for example, with `index_patterns` of `*` or `.*`). Avoid these patterns, which can cause errors during index creation or unexpected behavior afterward.
:::
