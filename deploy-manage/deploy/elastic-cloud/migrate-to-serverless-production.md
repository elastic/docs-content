---
navigation_title: Complete the migration and switch to production
description: Complete the final transfer, switch clients to Serverless, validate production, and retire the source.
applies_to:
  serverless: ga
products:
  - id: cloud-serverless
type: how-to
---

# Complete the migration and switch to production [migrate-to-serverless-production]

**Serverless migration process**

:::{image} /deploy-manage/images/serverless-migration-navigation-grouped-production.svg
:alt: Assess, create project, prepare and test, and switch to production. The preparation cycle runs from Prepare to Transfer data to Test and validate and back to Prepare. Switch to production is the current phase.
:::

Previous: [Test and validate](migrate-to-serverless-test-and-validate.md) · [Transfer data](migrate-to-serverless-transfer-data.md)

Follow this procedure after validating the destination. It coordinates the remaining transfer and the switch of production clients using the asset-specific methods you tested during preparation.

This procedure pauses source writes and configuration changes during the final transfer. If that interruption is unsuitable, evaluate the [alternative migration approaches](#migrate-to-serverless-alternatives).

:::::{stepper}

::::{step} Prepare the production transition
:anchor: migrate-to-serverless-cutover-plan

Schedule the migration window. Identify the data and configuration still to transfer, including changes made in the source since preparation, and prepare the client connection changes.

Transfer and verify any remaining stable historical data while the source is active, following [Transfer data](migrate-to-serverless-transfer-data.md). Keep the record of completed copies up to date. Identify provisional copies of changing data that need replacement during the final window.

:::{tip}
Consider [manually rolling over](/manage-data/data-store/data-streams/use-data-stream.md#manually-roll-over-a-data-stream) high-volume data streams in the source to include their former write indices in the historical transfer. This can reduce the data left to copy during the final pause. For [TSDS](/manage-data/data-store/data-streams/time-bound-tsds.md), wait until incoming data with current timestamps starts reaching the new backing index before copying the previous one. Rollover alone does not make those indices immutable.
:::

Define the validation criteria and rollback procedure before starting the transition. Include when to return to the source and how to handle any data written to the destination before returning.

::::

::::{step} Pause source writes and configuration changes
:anchor: migrate-to-serverless-offline

Pause ingestion and other processes that create, update, or delete source data, including automated retention that could remove data selected for transfer. Pause edits to the configuration being transferred. Keep the source available for the reads needed by the final transfer.

If you cannot pause writes while keeping the source available for reads, consider [switching ingestion before completing the historical transfer](#migrate-to-serverless-switch-before-history).

::::

::::{step} Complete the final transfer
:anchor: migrate-to-serverless-final-transfer

Use the methods tested during preparation to finish the transfer:

1. Refresh the source inventory and compare it with your record of verified copies. Include new indices, backing indices created by rollovers since preparation, and each data stream's last write index.
2. Transfer the remaining indices and backing indices. Retain verified copies whose source data has remained unchanged. Replace provisional copies of changing data with complete copies from the paused source, unless you have tested a procedure to reconcile subsequent changes. If you copied backing indices to standalone indices, [add the verified copies to the destination stream](migrate-to-serverless-transfer-data.md#migrate-to-serverless-add-backing-indices).
3. Apply pending configuration changes and [verify the complete transferred dataset](migrate-to-serverless-transfer-data.md#migrate-to-serverless-verify-data) before switching production connections.

If a provisional copy is already attached to a destination data stream, remove it from that stream with `remove_backing_index` before adding its verified replacement. Do not retain both copies. Refer to [the update data streams API]({{es-serverless-apis}}operation/operation-indices-modify-data-stream).

::::

::::{step} Switch production clients and ingestion
:anchor: migrate-to-serverless-production-clients

Update applications and ingestion tools to use the destination endpoints and credentials. For {{fleet}}-managed {{agent}}s, follow the [agent migration instructions](/reference/fleet/migrate-elastic-agent.md#migrate-elastic-agent-migrated-agents) using the destination policies and enrollment settings prepared earlier.

Resume production activity against the destination.

::::

::::{step} Validate production
:anchor: migrate-to-serverless-production-validation

Confirm that production reads and writes use the destination and that the required application, ingestion, and solution workflows meet the validation criteria.

If the criteria are not met and the transition cannot continue, follow the rollback procedure you prepared before the switch.

::::

::::{step} Monitor the destination and retire the source
:anchor: migrate-to-serverless-close

After the bulk transfer ends, check application errors, ingestion rates, query latency, and resource consumption under normal production activity. Repeat the performance checks relevant to your requirements once the workload stabilizes: migration traffic does not represent the project's ongoing workload or cost. Use [AutoOps for Serverless](/deploy-manage/monitor/autoops/autoops-for-serverless.md), where available, to review performance and usage alongside the project's [billing dimensions](/deploy-manage/cloud-organization/billing/serverless-project-billing-dimensions.md).

Keep the source available for the agreed rollback period. Retire it after that period and any requirements to retain source data or state have been met.

::::

:::::

% TODO: Keep this procedure at the coordination level; refer to asset-specific procedures for transfer details.

## Appendix: Alternative migration approaches [migrate-to-serverless-alternatives]

The appropriate migration approach depends on your workload and what interruption, data loss, duplicates, or temporary gaps your application can tolerate. Some logging workloads can accept a brief interruption or incomplete historical data while copying continues. Transactional applications might require coordinated changes to ingestion and application behavior to preserve consistency.

The following alternatives describe approaches to consider, rather than complete synchronization procedures. Design and test your chosen approach against your requirements before switching production traffic.

### Reduce the final transfer with incremental synchronization [migrate-to-serverless-incremental]

- **Approach:** Copy data, including historical and active indices, while the source remains active, then apply subsequent changes incrementally. The main procedure instead leaves changing data for a complete copy during the final pause.
- **When to consider it:** You need a shorter final transfer window and can design and operate a synchronization process that reliably captures the required changes without overloading either environment with reads or writes.
- **Plan for:** You must design and test the incremental process for your workload, including how it identifies new documents, reconciles updates and deletes, handles retries, and controls read and write load. Repeating a document copy does not automatically synchronize the environments. Plan a final pause to apply and verify the remaining changes unless your design also handles writes during the switch.

For the available mechanisms and their limitations, refer to [Incremental transfer mechanisms and limitations](migrate-to-serverless-transfer-data.md#migrate-to-serverless-incremental-mechanisms).

### Switch ingestion before completing the historical transfer [migrate-to-serverless-switch-before-history]

- **Approach:** Redirect clients to the destination, then finish copying the source data. If stopping writes requires stopping the source cluster, redirect clients before bringing it back online for migration reads. Keep the source data stable during the transfer.
- **When to consider it:** The destination can receive new data while historical data is still incomplete, and your workload can tolerate the interruption needed to redirect clients.
- **Plan for:** Whether clients buffer and retry data during the interruption, or whether you accept some data loss or duplicates. Reconcile mutable indices so that older source documents do not overwrite newer destination changes. Define how applications behave until the historical transfer is complete.

% TBD: Refine the guidance on switching production ingestion before completing the historical backfill. This approach requires applications to work correctly while historical data is still incomplete. Keep this coordination guidance here and link to the data transfer procedure for implementation details.

### Parallel ingestion [migrate-to-serverless-parallel]

- **Approach:** Send new data to both environments while preparing the destination and transferring any required historical data.
- **When to consider it:** Your ingestion tools or applications can deliver to both environments, and you want to validate live ingestion before switching production reads.
- **Plan for:** Delivery failures, retries, duplicates, and the boundary between historical copies and new data. Decide how to handle writes that succeed in only one environment, and how to replicate updates or deletes if required. Application changes might be necessary.

### Phased migration [migrate-to-serverless-phased]

- **Approach:** Move separate workloads or applications in stages, validating each before continuing.
- **When to consider it:** Workloads can operate independently, so you can migrate them without switching the whole solution at once.
- **Plan for:** Shared data, queries, and dependencies that span migrated and unmigrated workloads. Decide which environment receives each workload's writes and how clients access its data. Moving clients in stages does not itself synchronize the environments.

Return to the [migration overview](migrate-to-serverless.md).
