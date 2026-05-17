---
navigation_title: "Troubleshoot Upgrade Assitant"
description: "Common upgrade issues and resolutions."
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

# Troubleshoot Upgrade Assistant [troubleshooting-upgrade-assistant]

You should run the [Upgrade Assistant](/deploy-manage/upgrade/prepare-to-upgrade/upgrade-assistant.md) from the current major's latest minor and patch before upgrading to the next major stack version. You should end up with a list of steps each with a green filled-in checkmark. Failure to do so causes the [common upgrade issues](/troubleshoot/elasticsearch/troubleshooting-upgrades.md).

## Upgrade assistant errors

The {{kib}} [Upgrade Assistant](/deploy-manage/upgrade/prepare-to-upgrade/upgrade-assistant.md) second step "Migrate system indices" might error `System indices migration failed`. Click "View Migration Details" to show the output of {{es}}'s [Get feature migration information API]({{es-apis}}operation/operation-migration-get-feature-upgrade-status)

- https://support.elastic.dev/knowledge/view/f3c6ea67
```text
IllegalStateException[unable to create new index [X] because it would match composable template [Y]];
```
- https://discuss.elastic.co/t/issues-upgrading-elasticsearch-from-8-to-9-due-to-old-7-x-indices-and-restricted-kibana-indices/379133/11
https://support.elastic.dev/knowledge/view/e3d44d38
```text
IllegalStateException[unable to create new index [X] because it would match legacy template [Y]];
```
- Avoiding "match all" index templates https://support.elastic.dev/knowledge/view/1bbb4cc9
- https://github.com/elastic/kibana/issues/119652#issuecomment-979205209
```text
org.elasticsearch.ElasticsearchException: error occurred while reindexing, bulk failures [{"index":".kibana_1-reindexed-for-8","type":"_doc","id":"space_a:visualization:e1d0f010-9ee7-11e7-8711-e7a007dcef99","cause":{"type":"cluster_block_exception","reason":"index [.kibana_1-reindexed-for-8] blocked by: [FORBIDDEN/8/index write (api)];"},"status":403}
```
https://www.elastic.co/guide/en/elasticsearch/reference/current/fix-watermark-errors.html 
- mapper_parsing_exception from legacy template `.security-*` 
https://github.com/elastic/elasticsearch/issues/86801
https://support.elastic.dev/knowledge/view/794038f9
https://support.elastic.dev/knowledge/view/dd79602f
https://support.elastic.dev/knowledge/view/295e812f
```text
mapping set to strict, dynamic introduction of [allow_restricted_indices] within [indices] is not allowed

[instance-0000000000] Missing _meta field in mapping [_doc] of index [.security]  
instance-0000000000] failed to notify ClusterStateListener
java.lang.IllegalStateException: Cannot read security-version string in index .security

Security index is not on the current version - the native realm will not be operational until the upgrade API is run on the security index
```
- https://support.elastic.dev/knowledge/view/3e27188b
```text
Get disk usage on all nodes below the value specified in cluster.routing.allocation.disk.watermark.low (nodes impacted: [NODE_NAME])
```
- https://support.elastic.dev/knowledge/view/56149373
```text
Enterprise Search host(s) and configuration must be removed.
```
- https://support.elastic.dev/knowledge/view/cb3db1e7
```text
 Cannot update mappings in [.ml-config-reindexed-for-8-reindexed-for-9]: system indices can only use mappings from their descriptors, but the mappings in the request [{\"_doc\":{\"_meta\":{\"managed_index_mappings_version\":1,\"version\":\"8.11.0\"},\"properties\":{\"established_model_memory\":{\"type\":\"keyword\"}}}}] did not match those in the descriptor(s)"}
```
