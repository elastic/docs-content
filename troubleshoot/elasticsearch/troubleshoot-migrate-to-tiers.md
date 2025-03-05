---
navigation_title: Incomplete migration to data tiers
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/troubleshoot-migrate-to-tiers.html
---

% old title: Mix of index allocation filters and data tier node roles

# Troubleshoot incomplete migration to data tiers [troubleshoot-migrate-to-tiers]

Elasticsearch standardized the implementation of [hot-warm-cold architectures](https://www.elastic.co/blog/elasticsearch-data-lifecycle-management-with-data-tiers) to [data tiers](../../manage-data/lifecycle/data-tiers.md) in version 7.10. Some indices and deployments might have not fully transitioned to [data tiers](../../manage-data/lifecycle/data-tiers.md) and mix the new way of implementing the hot-warm-cold architecture with [legacy](../../deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md) based node attributes.

This could lead to unassigned shards or shards not transitioning to the desired [tier](../../manage-data/lifecycle/data-tiers.md).

In order to fix this follow the next steps:

:::::::{tab-set}

::::::{tab-item} {{ech}}
In order to get the shards assigned we need to call the [migrate to data tiers routing](../../manage-data/lifecycle/data-tiers.md) API which will resolve the conflicting routing configurations towards using the standardized [data tiers](../../manage-data/lifecycle/data-tiers.md). This will also future-proof the system by migrating the index templates and ILM policies if needed.

**Use {{kib}}**

1. Log in to the [{{ecloud}} console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Hosted deployments** panel, click the name of your deployment.

    ::::{note}
    If the name of your deployment is disabled your {{kib}} instances might be unhealthy, in which case please contact [Elastic Support](https://support.elastic.co). If your deployment doesn’t include {{kib}}, all you need to do is [enable it first](../../deploy-manage/deploy/elastic-cloud/access-kibana.md).
    ::::

3. Open your deployment’s side navigation menu (placed under the Elastic logo in the upper left corner) and go to **Dev Tools > Console**.

    :::{image} ../../images/elasticsearch-reference-kibana-console.png
    :alt: {{kib}} Console
    :class: screenshot
    :::

4. First, let’s [stop](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-stop) {{ilm}}

    ```console
    POST /_ilm/stop
    ```

    The response will look like this:

    ```console-result
    {
      "acknowledged": true
    }
    ```

5. Wait for {{ilm}} to stop. Check the status until it returns `STOPPED` as follows:

    ```console
    GET /_ilm/status
    ```

    When {{ilm}} has successfully stopped the response will look like this:

    ```console-result
    {
      "operation_mode": "STOPPED"
    }
    ```

6. [Migrate to data tiers](../../manage-data/lifecycle/data-tiers.md)

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
    2. The indices that were migrated to [tier preference](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/data-tier-allocation.md#tier-preference-allocation-filter) routing.
    3. The legacy index templates that were updated to not contain custom routing settings for the provided data attribute.
    4. The composable index templates that were updated to not contain custom routing settings for the provided data attribute.
    5. The component templates that were updated to not contain custom routing settings for the provided data attribute.

7. [Restart](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-start) {{ilm}}

    ```console
    POST /_ilm/start
    ```

    The response will look like this:

    ```console-result
    {
      "acknowledged": true
    }
    ```
::::::

::::::{tab-item} Self-managed
In order to get the shards assigned we need to make sure the deployment is using the [data tiers](../../manage-data/lifecycle/data-tiers.md) node roles and then call the [migrate to data tiers routing](../../manage-data/lifecycle/data-tiers.md) API which will resolve the conflicting routing configurations towards using the standardized [data tiers](../../manage-data/lifecycle/data-tiers.md). This will also future-proof the system by migrating the index templates and ILM policies if needed.

1. In case your deployment is not yet using [data tiers](../../manage-data/lifecycle/data-tiers.md) [assign data nodes](../../manage-data/lifecycle/index-lifecycle-management/migrate-index-allocation-filters-to-node-roles.md#assign-data-tier) to the appropriate data tier. Configure the appropriate roles for each data node to assign it to one or more data tiers: `data_hot`, `data_content`, `data_warm`, `data_cold`, or `data_frozen`. For example, the following setting configures a node to be a data-only node in the hot and content tiers.

    ```yaml
    node.roles [ data_hot, data_content ]
    ```

2. [Stop](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-stop) {{ilm}}

    ```console
    POST /_ilm/stop
    ```

    The response will look like this:

    ```console-result
    {
      "acknowledged": true
    }
    ```

3. Wait for {{ilm}} to stop. Check the status until it returns `STOPPED` as follows:

    ```console
    GET /_ilm/status
    ```

    When {{ilm}} has successfully stopped the response will look like this:

    ```console-result
    {
      "operation_mode": "STOPPED"
    }
    ```

4. [Migrate to data tiers](../../manage-data/lifecycle/data-tiers.md)

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
    2. The indices that were migrated to [tier preference](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/data-tier-allocation.md#tier-preference-allocation-filter) routing.
    3. The legacy index templates that were updated to not contain custom routing settings for the provided data attribute.
    4. The composable index templates that were updated to not contain custom routing settings for the provided data attribute.
    5. The component templates that were updated to not contain custom routing settings for the provided data attribute.

5. [Restart](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-start) {{ilm}}

    ```console
    POST /_ilm/start
    ```

    The response will look like this:

    ```console-result
    {
      "acknowledged": true
    }
    ```
::::::

:::::::
