---
navigation_title: "SLOs"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/slo-troubleshoot-slos.html
  - https://www.elastic.co/guide/en/serverless/current/slo-troubleshoot-slos.html
---

# Troubleshoot service-level objectives (SLOs) [slo-troubleshoot-slos]


::::{important}
In {{stack}}, to create and manage SLOs, you need an [appropriate license](https://www.elastic.co/subscriptions), an {{es}} cluster with both `transform` and `ingest` [node roles](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html#node-roles) present, and [SLO access](../../solutions/observability/incident-management/configure-service-level-objective-slo-access.md) must be configured.

::::


::::{warning}
Do not edit, delete, or tamper with any "internal" assets mentioned in this document, such as the transforms or ingest pipelines created by the SLO application.

Do not attempt to edit the `.slo-observability.*` indices mentioned in this document by overriding index templates or editing the settings/mappings.

The implementation details described here are subject to change.

::::


This document provides an overview of common issues encountered when working with service-level objectives (SLOs). It explores the relationships between SLOs and other core functionalities within the stack, such as [transforms](../../explore-analyze/transforms.md) and [ingest pipelines](../../manage-data/ingest/transform-enrich/ingest-pipelines.md), highlighting how these integrations can impact the functionality of SLOs.

* [Understanding SLO internals](#slo-understanding-slos)
* [Common problems](#slo-common-problems)
* [SLO troubleshooting actions](#slo-troubleshoot-actions)
* [Upgrade from beta to GA](#slo-troubleshoot-beta)


## Understanding SLO internals [slo-understanding-slos]

::::{tip}
If you’re already familiar with how SLOs work and their relationship with other system components, such as transforms and ingest pipelines, you can jump directly to [Common problems](#slo-common-problems).

::::


An SLO is represented by several system resources:

* **SLO Definition**: Stored as a Kibana Saved Object.
* **Transforms**: For each SLO, {{kib}} creates two transforms:

    * **Rolling-up transform**: `slo-{slo.id}-{slo.revision}`, rolls up the data into a smaller set of documents. The source indices of this transform are defined by the SLO. The target index will be `.slo-observability.sli-v{slo.internal-version}-{monthly date}`.
    * **Rolling-up ingest pipeline**: `slo-observability.sli.pipeline-{slo.id}-{slo.revision}`, used by the rolling-up transform.
    * **Summarizing transform**: `slo-summary-{slo.id}-{slo.revision}`, updates the latest values, such as the observed SLI or remaining error budget, for efficient searching and filtering of SLOs. The source of this transform is `.slo-observability.sli-v{slo.internal-version}*`. The target index is `.slo-observability.summary-v{slo.internal-version}`.
    * **Summarizing ingest pipeline**: `slo-observability.summary.pipeline-{slo.id}-{slo.revision}`, used by the summarizing transform.

* **Additional resources**: {{kib}} also installs and manages shared resources to the SLOs, including index templates, indices, and ingest pipelines, among others.

When an **SLO update** changes any of the `SLI parameters`, the `SLO objective`, or the `time window`, a revision bump (`{slo.revision}`) and a full reinstallation of the associated assets (transforms and ingest pipelines) occur. In addition, the revision bump deletes any previously aggregated data for that SLO. Updates to fields like `name`, `description`, or `tags` do not trigger a revision bump or asset reinstallation.

Ensuring that transforms are functioning correctly and that the cluster is healthy is crucial for maintaining accurate and reliable SLOs.


## Common problems [slo-common-problems]

It’s common for SLO problems to arise when there are underlying problems in the cluster, such as unavailable shards or failed transforms. Because SLOs rely on transforms to aggregate and process data, any failure or misconfiguration in these components can lead to inaccurate or incomplete SLO calculations. Additionally, unavailable shards can affect the data retrieval process, further complicating the reliability of SLO metrics.


### No transform or ingest nodes [slo-no-transform-ingest-node]

Because SLOs depend on both [ingest pipelines](../../manage-data/ingest/transform-enrich/ingest-pipelines.md) and [transforms](../../explore-analyze/transforms.md) to process the data, it’s essential to ensure that the cluster has nodes with the appropriate [roles](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html#node-roles).

Ensure the cluster includes one or more nodes with both `ingest` and `transform` roles to support the data processing and transformations required for SLOs to function properly. The roles can exist on the same node or be distributed across separate nodes.


### Unhealthy or missing transforms [slo-transform-unhealthy]

When working with SLOs, it is crucial to ensure that the associated transforms function correctly. Transforms are responsible for generating the data needed for SLOs, and two transforms are created for each SLO. If you notice that your SLOs are not displaying the expected data, it’s time to check the health of these associated transforms.

{{kib}} shows the following message when any of the associated transforms is in an unexpected state:

* `"The following transform is an unhealthy state"`, followed by a list of transforms.

For detailed guidance on diagnosing and resolving transform-related issues, refer to the [troubleshooting transforms](../elasticsearch/transform-troubleshooting.md) documentation .

It’s also recommended that you perform the following transform checks:

* Ensure the transforms needed for the SLOs haven’t been deleted or stopped.

    If a transform has been deleted, the easiest way to recreate it is using the [Reset SLO](#slo-troubleshoot-reset) action, forcing the recreation of the transforms. If a transform was stopped, try to start it, and then check the `health tab` of the transform.

* [Inspect SLO assets](#slo-troubleshoot-inspect) to analyze the SLO definition and all associated resources.

    Use the direct links offered by the **Inspect UI** and check that all referenced resources exist, as that’s not verified by the inspect functionality.

    Use the `query composite` content to verify if the queries performed by the transforms are valid and return the expected data.

* Check the source data and queries of the SLO.

    The most common cause of legitimate transform failures is issues with the source data, such as timestamp parsing errors or incorrect query structures. The following is an example of an unparsable timestamp causing a transform to fail:

    ```bash
    "reason": """Failed to index documents into destination index due to permanent error:
      [org.elasticsearch.xpack.transform.transforms.BulkIndexingException: Bulk index experienced [500] failures and at least 1 irrecoverable
        [unable to parse date [1702842480000]]. Other failures:
      [IngestProcessorException] message [org.elasticsearch.ingest.IngestProcessorException:
        java.lang.IllegalArgumentException: unable to parse date [1702842480000]]; java.lang.IllegalArgumentException: unable to parse date [1702842480000]]""",
    "issue": "Transform task state is [failed]"
    ```

* As a last resort, consider [resetting the SLO](#slo-troubleshoot-reset).


### Missing Ingest Pipelines [slo-missing-pipeline]

If any of the needed ingest pipelines are missing, try the [Reset SLO](#slo-troubleshoot-reset) action.


### Stack-related problems [slo-missing-template]

As mentioned, maintaining a healthy cluster is crucial for SLOs to function correctly. The following examples show issues **unrelated to SLOs** that can still disrupt their proper operation. While troubleshooting these issues is outside the scope of this document, they are included for illustrative purposes.

* Problems accessing the source data, causing the transform to fail:

    ```bash
    Failed to execute phase [can_match], start; org.elasticsearch.action.search.SearchPhaseExecutionException:
      Search rejected due to missing shards [[index_name_1][1], [index_name_2][1], [index_name_3][1]].
    ```

* Remote cluster not available, if for example an SLO is fetching data from a remote cluster called `remote-metrics`:

    ```sh
    Validation Failed: 1: no such remote cluster: [remote-metrics]
    ```

* [Circuit breaker exceptions](../elasticsearch/circuit-breaker-errors.md) due to nodes being under memory pressure.


## SLO troubleshooting actions [slo-troubleshoot-actions]


### Inspect SLO assets [slo-troubleshoot-inspect]

To be able to inspect SLOs you have to activate the corresponding feature in {{kib}}:

1. Open **Advanced Settings**, by finding **Stack Management** in the main menu or using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Enable `observability:enableInspectEsQueries` setting.

Afterwards visit the **SLO edit page** and click **SLO Inspect**.

The **SLO Inspect** option provides a detailed report of an SLO, including:

* SLO configuration
* Rollup transform configuration
* Summary transform configuration
* Rollup ingest pipeline
* Summary ingest pipeline
* Temporary document
* Rollup transform query composite
* Summary transform query composite

These resources are very useful for tasks such as trying out the queries performed by the transforms and checking the IDs of all associated resources. The view also includes direct links to transforms and ingest pipelines sections in {{kib}}.


### Reset SLO [slo-troubleshoot-reset]

Resetting an SLO forces the deletion of all SLI data, summary data, and transforms, and then reinstalls and processes the data. Essentially, it recreates the SLO as if it had been deleted and re-created by the user.

::::{note}
While resetting an SLO can help resolve certain issues, it may not always address the root cause of errors. Most errors related to transforms typically arise from improperly structured source data, such as unparsable timestamps, which prevent the transform from progressing. Additionally, incorrect formatted SLO queries, and consequently transform queries, can also lead to failures.

Before resetting the SLO, verify that the source data and queries are correctly formatted and validated. Resetting should only be used as a last resort when all other troubleshooting steps have been exhausted.

::::


Follow these steps to reset an SLO:

1. Find **SLOs** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click on the SLO to reset.
3. Select **Actions** → **Reset**.

Alternatively you can use {{kib}} API for the reset action:

```console
POST kbn:/api/observability/slos/{sloId}∫/_reset
```

Where `sloId` can be obtained from the [Inspect SLO assets](#slo-troubleshoot-inspect) action.


### Using API calls to retrieve SLO details [slo-api-calls]

Refer to [SLO API calls](https://www.elastic.co/docs/api/doc/kibana/v8/operation/operation-findslosop) as an alternative to [using SLO Inspect](#slo-troubleshoot-inspect).


## Upgrade from beta to GA [slo-troubleshoot-beta]
```yaml {applies_to}
stack: all
```

Starting in version 8.12.0, SLOs are generally available (GA). If you’re upgrading from a beta version of SLOs (available in 8.11.0 and earlier), you must migrate your SLO definitions to a new format. Otherwise SLOs won’t show up.

::::{dropdown} Migrate your SLO definitions
To migrate your SLO definitions, open the SLO overview. A banner will display the number of outdated SLOs detected. For each outdated SLO, click **Reset**. If you no longer need the SLO, select **Delete**.

If you have a large number of SLO definitions, it is possible to automate this process. To do this, you’ll need to use two Elastic APIs:

* [SLO Definitions Find API](https://github.com/elastic/kibana/blob/9cb830fe9a021cda1d091effbe3e0cd300220969/x-pack/plugins/observability/docs/openapi/slo/bundled.yaml#L453-L514) (`/api/observability/slos/_definitions`)
* [SLO Reset API](https://www.elastic.co/docs/api/doc/kibana/v8/operation/operation-resetsloop)

Pass in `includeOutdatedOnly=1` as a query parameter to the Definitions Find API. This will display your outdated SLO definitions. Loop through this list, one by one, calling the Reset API on each outdated SLO definition. The Reset API loads the outdated SLO definition and resets it to the new format required for GA. Once an SLO is reset, it will start to regenerate SLIs and summary data.

::::


::::{dropdown} Remove legacy summary transforms
After migrating to 8.12 or later, you might have some legacy SLO summary transforms running. You can safely delete the following legacy summary transforms:

```sh
# Stop all legacy summary transforms
POST _transform/slo-summary-occurrences-30d-rolling/_stop?force=true
POST _transform/slo-summary-occurrences-7d-rolling/_stop?force=true
POST _transform/slo-summary-occurrences-90d-rolling/_stop?force=true
POST _transform/slo-summary-occurrences-monthly-aligned/_stop?force=true
POST _transform/slo-summary-occurrences-weekly-aligned/_stop?force=true
POST _transform/slo-summary-timeslices-30d-rolling/_stop?force=true
POST _transform/slo-summary-timeslices-7d-rolling/_stop?force=true
POST _transform/slo-summary-timeslices-90d-rolling/_stop?force=true
POST _transform/slo-summary-timeslices-monthly-aligned/_stop?force=true
POST _transform/slo-summary-timeslices-weekly-aligned/_stop?force=true

# Delete all legacy summary transforms
DELETE _transform/slo-summary-occurrences-30d-rolling?force=true
DELETE _transform/slo-summary-occurrences-7d-rolling?force=true
DELETE _transform/slo-summary-occurrences-90d-rolling?force=true
DELETE _transform/slo-summary-occurrences-monthly-aligned?force=true
DELETE _transform/slo-summary-occurrences-weekly-aligned?force=true
DELETE _transform/slo-summary-timeslices-30d-rolling?force=true
DELETE _transform/slo-summary-timeslices-7d-rolling?force=true
DELETE _transform/slo-summary-timeslices-90d-rolling?force=true
DELETE _transform/slo-summary-timeslices-monthly-aligned?force=true
DELETE _transform/slo-summary-timeslices-weekly-aligned?force=true
```

Do not delete any new summary transforms used by your migrated SLOs.

::::
