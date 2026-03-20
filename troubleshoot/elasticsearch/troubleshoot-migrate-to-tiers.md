---
navigation_title: Incomplete migration to data tiers
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/troubleshoot-migrate-to-tiers.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

% old title: Mix of index allocation filters and data tier node roles

# Troubleshoot incomplete migration to data tiers [troubleshoot-migrate-to-tiers]

{{es}} standardized the implementation of [hot-warm-cold architectures](https://www.elastic.co/blog/elasticsearch-data-lifecycle-management-with-data-tiers) to [data tiers](../../manage-data/lifecycle/data-tiers.md) in version 7.10. Some indices and deployments might have not fully transitioned to [data tiers](../../manage-data/lifecycle/data-tiers.md) and mix the new way of implementing the hot-warm-cold architecture with [legacy](../../deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md) based node attributes.

This could lead to unassigned shards or shards not transitioning to the desired [tier](../../manage-data/lifecycle/data-tiers.md).

To fix this issue, use the following steps.

You can run the following steps using either [API console](/explore-analyze/query-filter/tools/console.md) or direct [{{es}} API](elasticsearch://reference/elasticsearch/rest-apis/index.md) calls.

:::{tip}
To learn how to assign tiers to your data nodes, refer to [](/manage-data/lifecycle/index-lifecycle-management/migrate-index-allocation-filters-to-node-roles.md).
:::

To get the shards assigned, call the [migrate to data tiers routing](../../manage-data/lifecycle/data-tiers.md) API, which resolves the conflicting routing configurations to using the standardized [data tiers](../../manage-data/lifecycle/data-tiers.md). This also future-proofs the system by migrating the index templates and ILM policies if needed.

1. [Stop](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-stop) {{ilm}}

    ```console
    POST /_ilm/stop
    ```

    The response will look like this:

    ```console-result
    {
      "acknowledged": true
    }
    ```

2. Wait for {{ilm}} to stop. Check the status until it returns `STOPPED` as follows:

    ```console
    GET /_ilm/status
    ```

    When {{ilm}} has successfully stopped the response will look like this:

    ```console-result
    {
      "operation_mode": "STOPPED"
    }
    ```

3. [Migrate to data tiers](../../manage-data/lifecycle/data-tiers.md)

    ```console
    POST /_ilm/migrate_to_data_tiers
    ```

    The response will look like this:

    ```console-result
    {
      "dry_run": false,
      "migrated_ilm_policies":["policy_with_allocate_action"], <1>
      "migrated_indices":["warm-index-to-migrate-000001"], <2>
      "migrated_legacy_templates":["a-legacy-template"], <3>
      "migrated_composable_templates":["a-composable-template"], <4>
      "migrated_component_templates":["a-component-template"] <5>
    }
    ```

    1. The ILM policies that were updated.
    2. The indices that were migrated to [tier preference](elasticsearch://reference/elasticsearch/index-settings/data-tier-allocation.md#tier-preference-allocation-filter) routing.
    3. The legacy index templates that were updated to not contain custom routing settings for the provided data attribute.
    4. The composable index templates that were updated to not contain custom routing settings for the provided data attribute.
    5. The component templates that were updated to not contain custom routing settings for the provided data attribute.

4. [Restart](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-start) {{ilm}}:

    ```console
    POST /_ilm/start
    ```

    The response will look like this:

    ```console-result
    {
      "acknowledged": true
    }
    ```
