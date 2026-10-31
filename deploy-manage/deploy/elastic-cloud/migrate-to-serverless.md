---
navigation_title: Migrate to Serverless
description: Plan and complete a migration from an existing Elasticsearch deployment to an Elasticsearch Serverless project.
applies_to:
  serverless:
    elasticsearch: ga
products:
  - id: cloud-serverless
  - id: elasticsearch
---

# Migrate to an {{es-serverless}} project [migrate-to-elasticsearch-serverless]

Moving to {{es-serverless}} is not an in-place conversion. You create a project, prepare it for your workload, move your data and configuration, update your applications, and then switch production traffic.

This guide covers the complete migration journey from {{ech}}, {{ece}}, {{eck}}, or a self-managed {{es}} cluster. It helps you make decisions specific to {{serverless-short}} and links to the procedures for each data transfer method.

## Before you begin [migrate-to-serverless-before-you-begin]

Before planning the migration:

- Make sure that you can administer the source deployment and create or administer the destination project.
- Identify the owners of your data, applications, ingestion, security, and compliance requirements.
- Define acceptable downtime, data loss tolerance, rollback requirements, and the date when you want to switch production traffic.
- Confirm that an {{es-serverless}} project is the correct target. {{observability}} and {{elastic-sec}} projects provide solution-specific features and can require different configuration.

## Step 1: Assess {{serverless-short}} compatibility [migrate-to-serverless-assess-compatibility]

Start with [Compare {{ech}} and {{serverless-short}}](differences-from-other-elasticsearch-offerings.md). Review every feature, API, and setting that your workload uses, even when your source is not {{ech}}.

Review the destination's [index and project limits](differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-index-size), [available APIs](differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-apis-availability), [available settings](differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-settings-availability), and [version reporting behavior](differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-version-reporting). Don't use the version returned by the root API as a list of available features.

Pay particular attention to these architectural differences:

- Elastic manages upgrades, nodes, shards, replicas, capacity, high availability, and backups.
- A project provides one solution instead of combining all {{stack}} capabilities in one deployment.
- User authentication is managed at the {{ecloud}} organization level. {{serverless-short}} does not support {{es}} authentication realms or deployment-local users.
- {{serverless-short}} does not support {{ilm}} ({{ilm-init}}) or expose data tiers. Data stream lifecycle ({{dlm-init}}) manages data streams, but it does not manage regular indices.
- User-initiated snapshot and restore is unavailable.
- Custom shard allocation, custom routing, and settings that depend on node access are unavailable.
- {{ccr-cap}} is unavailable. You can't use it to keep the source and destination synchronized during migration.
- Cross-origin resource sharing (CORS) is unavailable. Browser applications must send requests through a backend service.
- Some plugins, APIs, and {{kib}} features are unavailable or have alternatives specific to {{serverless-short}}.

Record each incompatibility and decide whether to remove the dependency, redesign it, or use a supported alternative. Don't start the production migration until you have tested the required alternatives.

## Step 2: Inventory the source [migrate-to-serverless-inventory]

Build an inventory of everything that the workload needs. The data transfer methods copy documents, but they don't move every dependency.

| Area | What to inventory and plan |
| --- | --- |
| Ingested data | Indices, data streams, aliases, document counts, storage size, typical index size, retention, distribution of `@timestamp` values, update and delete patterns, stable document IDs, and whether the original data source is still available. Exclude system indices. |
| Data structures | Mappings, component templates, index templates, regular indices, data streams, time series data streams, small or empty indices, aliases, routing requirements, and lifecycle policies. |
| Data processing | Ingest pipelines, {{ls}} pipelines, {{agent}} policies, {{beats}} configuration, transforms, and external enrichment dependencies. |
| {{kib}} content | {{data-sources-cap}}, dashboards, visualizations, maps, alerting rules, connectors, and other saved objects. |
| Feature configuration | {{fleet}}, integrations, security rules, {{ml-jobs}}, synonyms, and any other feature-specific state. |
| Security | Users, roles, API keys, single sign-on, network policies, private connectivity, and audit or compliance requirements. |
| Applications | Endpoints, clients, software development kits (SDKs), APIs, index names, routing values, credentials, timeouts, retry behavior, and every process that creates, updates, or deletes documents. |
| Workload behavior | Typical and peak indexing and search rates, burst patterns, frequency of index creation, rollover, deletion, and mapping updates, and queries that search across many indices or long time ranges. |
| Versions | Source {{es}} and {{kib}} versions, client versions, and the compatibility requirements of exported objects and migration tools. |

Classify each item as one of the following:

- Move with a data migration method.
- Export and import separately.
- Recreate in the destination.
- Replace with an alternative supported by {{serverless-short}}.
- Retire because the destination does not support it.

You can't migrate {{es}} system indices to or from {{serverless-short}}. Don't try to copy hidden system indices as regular user data.

## Step 3: Create and secure the destination [migrate-to-serverless-create-destination]

1. Select an available [{{serverless-short}} region](regions.md) that meets latency, data residency, and compliance requirements. You can't change a project's region after creation.
2. [Create an {{es-serverless}} project](create-serverless-project.md).
3. Recreate user access with {{ecloud}} organization roles and [{{serverless-short}} custom roles](/deploy-manage/users-roles/serverless-custom-roles.md). Translate source cluster and index privileges instead of assuming that deployment roles transfer automatically.
4. Create [{{serverless-short}} project API keys](/deploy-manage/api-keys/serverless-project-api-keys.md) for applications and migration tools. Grant only the required privileges and plan to rotate temporary migration keys after the migration.
5. Configure [network security](/deploy-manage/security/network-security.md). Projects allow public traffic by default. After you attach a network security policy, traffic that does not match an associated policy is denied.
6. If required, configure [private connectivity](/deploy-manage/security/private-connectivity.md). {{serverless-short}} supports private connectivity in {{aws}} and Azure, but not {{gcp}}, and it does not publish static public IP address lists.
7. Verify applicable certifications and controls in the [Elastic Trust Center](https://www.elastic.co/trust). Don't assume that certifications or controls available in the source deployment apply to the destination project and region.

Test access from every migration tool, ingestion service, and application environment before copying production data. A successful browser login does not prove that application or migration traffic can reach the {{es}} endpoint.

Reindex from remote connects to the source from the destination project, and {{serverless-short}} does not publish static public egress IP address ranges. If the source accepts traffic only from fixed IP addresses or through a private endpoint that the destination can't reach, use {{ls}} from an allowed network or reingest from the original source instead. Resolve this before selecting the migration method.

## Step 4: Prepare data structures and processing [migrate-to-serverless-prepare-destination]

Create destination data structures before copying documents:

1. Recreate compatible component templates, index templates, and mappings.
2. Decide how to replace each {{ilm-init}} policy:
   - For time series or other timestamped append-only data, consider using a data stream with [data stream lifecycle](/manage-data/lifecycle/data-stream.md). Create a compatible data stream template and decide how long to retain data before starting a large migration.
   - For regular indices, decide whether to redesign them as data streams or manage index creation, rollover, and deletion using available APIs and your own automation. {{dlm-init}} does not manage regular indices.
   - Remove dependencies on data tiers and {{ilm-init}} actions that have no {{serverless-short}} equivalent. Don't copy an {{ilm-init}} policy and assume that {{dlm-init}} provides the same phases or actions.
3. Recreate compatible [ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md). Decide whether migrated documents must pass through those pipelines again. Avoid applying transformations twice to data that the source already transformed.
4. Remove unsupported index settings and dependencies on custom routing, shard allocation, or local node storage.
5. Create regular destination indices and destination data streams. Create standalone aliases after their destination indices exist. Aliases defined in an index template can be installed with the template.
6. Test representative documents in temporary destination indices or data streams and verify mappings, pipelines, retention, and search behavior.

Reindex and {{ls}} copy documents but don't copy mappings, templates, lifecycle policies, or ingest pipelines automatically.

## Step 5: Select a data transfer method [migrate-to-serverless-choose-strategy]

Use [Migrate your {{es}} data](/manage-data/migrate.md#data-migration-guides-serverless) as the canonical reference for supported source and destination combinations.

Select a transfer method based on the source, data model, volume, transformation requirements, and network connectivity:

- **Reingest from the original source**: Use the original files, database, object store, event stream, or other system of record when it is still available. This avoids dependencies on the layout and version of the source {{es}} deployment.
- **Reindex from remote**: Copy documents directly when the destination is {{serverless-short}} and the remote source is {{ech}} or another {{serverless-short}} project. Follow [Migrate {{es}} data using the reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md).
- **{{ls}}**: Use {{ls}} when the source is {{ech}}, {{ece}}, {{eck}}, self-managed, or another {{serverless-short}} project, or when you need transformation and more control over transfer behavior. Follow [Migrate {{es}} data using {{ls}}](/manage-data/migrate/migrate-with-logstash.md).

You can't register a snapshot repository or restore a user-managed snapshot into {{serverless-short}}. Snapshot and restore is therefore not a migration option.

When the destination is a data stream, create its matching template and the data stream before the transfer. Write to the data stream name, not directly to a `.ds-*` backing index. Reindexing into a data stream requires `op_type: create`. With {{ls}}, use data stream–compatible output settings. Refer to [Modify a data stream](/manage-data/data-store/data-streams/modify-data-stream.md#data-streams-use-reindex-to-change-mappings-settings) and the selected migration method for details.

Choosing Reindex or {{ls}} does not determine how you keep an active source synchronized. Plan the production synchronization and cutover separately in Step 8.

## Step 6: Move configuration and update applications [migrate-to-serverless-update-applications]

### Move saved objects and feature configuration

Use the {{kib}} [saved object import and export tools](/explore-analyze/find-and-organize/saved-objects.md#saved-objects-import-and-export) to move compatible dashboards, visualizations, maps, and {{data-sources}}. After the destination indices and data streams are available, import the saved objects and verify their references.

Before exporting, verify [saved object version compatibility](/explore-analyze/find-and-organize/saved-objects.md#_compatibility_across_versions). An export can be imported only into the same version, a later minor version of the same major, or the next major version. If the source is older, plan an intermediate upgrade or recreate the affected objects. Export and validate each required {{kib}} space.

Saved object import and export does not replace feature-specific migration. Review the documentation for each feature in your inventory. Recreate supported configuration such as integrations, connectors, rules, transforms, and {{ml-jobs}} when no supported export and import workflow exists. Re-enter connector secrets or other sensitive values that are missing after import.

An {{es-serverless}} project does not include hosted {{fleet-server}}. Hosted {{fleet-server}} is included with {{observability}} and {{elastic-sec}} projects. If the source uses {{fleet}} or {{agent}}, confirm that an {{es-serverless}} project is the correct target. Depending on the workload, you might need to select a different project type, use standalone {{agent}}s, or keep {{fleet}} management in another deployment and evaluate a [remote {{es}} output](/reference/fleet/remote-elasticsearch-output.md). Remote outputs have additional feature and network security restrictions. A snapshot-based {{fleet}} migration does not work with {{serverless-short}}.

Validate saved objects in a non-production space first. References to unavailable features, missing {{data-sources}}, changed object IDs, connectors, or credentials can require manual changes.

### Update applications and ingestion

1. [Find the destination endpoint and create API keys](/solutions/elasticsearch-solution-project/search-connection-details.md).
2. Update clients, SDKs, ingestion tools, and secrets to use the destination endpoint and credentials.
3. Remove Cloud IDs where a tool requires the {{serverless-short}} endpoint. For {{ls}}, use HTTPS and explicitly specify port `443`.
4. Remove custom `routing` parameters and redesign indices that require `_routing`.
5. Route browser-based requests through a backend service because {{serverless-short}} does not support CORS.
6. Review the [feature comparison](differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-infrastructure-management) for APIs and settings that require alternatives.
7. Test each application with an official [{{es}} client](/reference/elasticsearch-clients/index.md) version that is compatible with the APIs it uses.
8. Configure clients to retry transient `429` responses with randomized exponential backoff. Record the response body, limit retries, and alert when rejections persist or exhaust the retry limit. Load test indexing and search behavior instead of assuming that source deployment concurrency settings transfer unchanged.

Don't reuse administrative migration credentials in production applications. Create separate, least-privilege API keys for each workload.

## Step 7: Rehearse the migration [migrate-to-serverless-rehearse]

Run at least one representative end-to-end migration before selecting the production cutover date:

1. Record source document counts by index or data stream and relevant time range, representative query results, ingestion rates, and application behavior.
2. Migrate a representative subset that includes current data, older retained data, and the data patterns that are hardest to transform.
3. Use non-production credentials and test clients to run application and ingestion workflows against the destination endpoint.
4. Measure transfer time, search latency, indexing throughput, rejected requests, and resource consumption.
5. Validate mappings, aliases, data streams, lifecycle settings, pipelines, saved objects, permissions, and application workflows.
6. Compare counts by index or data stream and time range. Sample document IDs and field values, and run representative searches and aggregations.
7. Where the workload permits updates or deletes, test that your synchronization and retry design produces the expected result.
8. Test the production authentication path, including single sign-on and {{kib}} access, under representative load.
9. Repeat performance tests after bulk migration traffic stops and the project reaches its normal ingestion and search pattern.
10. Resolve migration failures and repeat the test until the procedure and duration are reproducible.

Use storage sizes for capacity and cost estimates, not as an equality check. Storage layout and reported size can differ between the source and {{serverless-short}}.

### Test migration and steady-state workloads

Performance during a bulk migration might not represent normal production behavior. Migration traffic can temporarily cause the project to use more resources. After the transfer finishes and the workload stabilizes, resource usage and performance characteristics can change. Test both the migration workload and the expected steady-state workload.

For data with a concrete `@timestamp` field, the [Search Boost Window](project-settings.md#elasticsearch-manage-project-search-ai-lake-settings) determines how much recent data remains search-ready. If a large migrated dataset contains timestamps from a narrow period, a significant volume can move outside the window around the same time. The data remains searchable, but searches over historical or non-search-ready data can have different latency and resource requirements. Include recent and historical data in your tests.

The following workload patterns need additional validation:

- Many small indices that are queried together.
- Frequent or bursty index creation, rollover, deletion, or mapping updates.
- Large time series datasets with timestamps concentrated in a narrow period.
- Dashboards, aggregations, or application queries that search across many indices or long time ranges.
- Indexing or search peaks that are significantly higher than the average rate.

Autoscaling does not remove every per-project limit. Don't schedule the production switch if representative tests produce sustained `429` responses, `circuit_breaking_exception` errors, exhausted retries, data loss, or unacceptable application and authentication performance.

## Step 8: Select a synchronization and cutover pattern [migrate-to-serverless-cutover]

Choose how to handle writes that occur while the production data is moving. Document every process that writes to the source, including applications, ingestion tools, scheduled jobs, transforms, and administrative scripts.

### Stop writes before the production copy

Use this pattern when you can accept enough downtime to copy and validate all required data:

1. Stop every source writer and confirm that indexing, updates, and deletes have stopped.
2. Run the production transfer.
3. Reconcile the source and destination and validate applications.
4. Update ingestion and applications to use the destination.

This is the simplest pattern because no changes occur during the copy. Its downtime includes the final transfer, validation, and application switch.

### Run an initial copy and synchronize later changes

Use this pattern for an active source when you can identify every change after a known checkpoint:

1. Record the starting checkpoint and run the initial bulk copy while the source remains active.
2. Copy documents created or updated after the checkpoint. Preserve stable document IDs so retries overwrite the intended destination document.
3. Pause writes briefly and run a final synchronization before switching applications.

This pattern is safest for append-only data or when an external change data capture process records creates, updates, and deletes. {{ls}} field tracking can resume from a tracking value, but it is a technical preview feature and does not by itself reproduce source deletions. A timestamp is suitable only when its update behavior and ordering prevent changes from being skipped. Define how you handle late updates, deletes, and failed events before using this pattern.

### Ingest into both environments

Use dual ingest when the ingestion system can send each operation to both environments and you can monitor failures independently:

1. Test the dual-ingest path and use deterministic document IDs and equivalent transformations in both destinations.
2. Start sending new operations to both environments and record the transition boundary.
3. Backfill the required historical data.
4. Reconcile both environments. Include updates and deletes if the workload is not append-only.
5. Pause writes briefly, drain pending operations, perform the final comparison, and switch application reads and writes to {{serverless-short}}.

Dual ingest works well for immutable time series data. For mutable data, make sure that the historical backfill can't overwrite a more recent document that dual ingest has already written. Define conflict handling and what happens when one destination accepts an operation and the other rejects it. If an immediate rollback is required, decide whether to continue dual writes during the rollback period and account for the additional failure modes and cost.

### Perform the production switch

Regardless of the pattern:

1. Compare counts by index or data stream and time range, sample documents, and run representative searches.
2. Validate dashboards, alerting, ingestion, permissions, and application operations.
3. Confirm that no writers still use the old endpoint.
4. Update production applications and ingestion to use destination credentials and endpoints.
5. Monitor errors, rejected requests, latency, indexing, search results, and cost before declaring the migration complete.

Keep the source available for an agreed rollback period. Define the rollback trigger, owner, endpoint switch, and treatment of documents created, updated, or deleted after cutover. A source that no longer receives those changes is not a complete rollback target.

## Step 9: Monitor usage and retire the source [migrate-to-serverless-monitor]

Elastic manages infrastructure capacity and scales {{serverless-short}} resources according to workload demand. You still need to validate performance and control the workload characteristics that affect consumption.

Define a post-migration observation period that continues after bulk migration traffic ends. For time series data, include a representative transition across the Search Boost Window when practical. If waiting for the complete window isn't practical, use realistic timestamp ranges during rehearsal and continue monitoring throughout the rollback period.

- Use [AutoOps for {{serverless-full}}](/deploy-manage/monitor/autoops/autoops-for-serverless.md), where available, to monitor performance, usage patterns, and billing dimensions. Don't migrate a {{stack-monitor-app}} cluster for the destination. Elastic manages the underlying {{serverless-short}} infrastructure.
- Review [{{es-serverless}} billing dimensions](/deploy-manage/cloud-organization/billing/elasticsearch-billing-dimensions.md). Storage, ingest, search, {{ml}}, and other enabled capabilities contribute to cost.
- Review [project settings](project-settings.md), including Search Power, the Search Boost Window, and data retention.
- Monitor migration ingestion and the steady-state period because a large bulk transfer increases ingest activity and stored data temporarily.
- Adjust {{dlm-init}} retention and data organization after validating production access patterns.
- Rotate or delete temporary migration API keys.
- Keep the source until the rollback period and any retention or audit requirements have passed. Then stop ingestion, take any required source-side archive, and decommission it.

## Troubleshoot common migration problems [migrate-to-serverless-troubleshooting]

| Problem | What to check |
| --- | --- |
| Authentication returns `401` or `403` | Verify that you use a project API key in the format required by the client and that it has privileges for the target indices and APIs. Don't use `cloud_auth`, deployment-local users, or native realm credentials with {{serverless-short}}. |
| Requests return a traffic-filtering `403` | Review the network security policies associated with the source and destination. An allowed remote hostname does not bypass a source network policy. |
| Requests repeatedly return `429` | Inspect the response body to identify the rejected operation, reduce concurrency or request rate, and review [rejected requests](/troubleshoot/elasticsearch/rejected-requests.md). Confirm that clients limit retries and report operations that exhaust the retry limit. |
| A `429` response contains `circuit_breaking_exception` | Stop increasing the workload and investigate which searches or indexing operations cause memory pressure. Review recent and historical search behavior and AutoOps before continuing the migration or production switch. |
| Index creation or rollover times out or returns `429` | Review the number and size of indices and the peak rate of index creation, rollover, deletion, and mapping updates. Consolidate small indices and spread management operations over time where possible. |
| Requests return `409` conflicts | Check document IDs, versioning, and `op_type`. A conflict is different from backpressure and should not be retried as though it were a `429`. |
| Documents fail with mapping or data stream errors | Install compatible mappings and templates first. For a data stream, create a matching data stream template and use data stream–compatible output settings. |
| Documents are duplicated after restarting a migration | Preserve source document IDs and use deterministic destination IDs. Review the checkpoint or field-tracking state before rerunning the transfer. |
| Source and destination counts drift after synchronization | Confirm that all source writers are known, no writes crossed an unrecorded checkpoint, failed events were retried, and the selected method accounts for updates and deletes. Compare counts by time range to locate the gap. |
| Dashboards or rules are missing or broken | Export and import compatible saved objects separately, then recreate feature configuration, connectors, credentials, and unsupported objects. |
| An application query or index request fails | Check the {{serverless-short}} feature comparison for unsupported APIs, settings, custom routing, or CORS-dependent browser access. |
| Usage or cost is higher than expected | Review AutoOps, billing dimensions, index count and size, ingest activity, Search Power, the Search Boost Window, and retention. |

If you can't resolve a migration failure, collect the request or tool error, affected index names, timestamps, and migration method before [contacting Support](/troubleshoot/index.md#contact-us).

## Completion criteria [migrate-to-serverless-completion]

The migration is complete when:

- All required documents and data structures are present.
- Applications and ingestion use destination endpoints and dedicated credentials.
- Searches, indexing, dashboards, alerting, and required feature workflows pass validation.
- Creates, updates, deletes, retries, and final synchronization behave as required for the workload.
- Migration and steady-state workloads, including relevant Search Boost Window transitions, pass validation without sustained rejected requests or exhausted retries.
- Roles and network policies provide the intended access.
- Applicable lifecycle management, project settings, monitoring, and cost controls match your operational requirements.
- The rollback procedure and treatment of post-cutover writes are documented and tested.
- The rollback period has ended and the source can be safely retired.
