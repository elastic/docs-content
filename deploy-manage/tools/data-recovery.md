---
navigation_title: Data recovery in Serverless
description: Learn how data recovery in Elastic Cloud Serverless automatically protects your indices and data streams, and how you can recover them to an earlier point in time.
applies_to:
  serverless: preview
products:
  - id: cloud-serverless
---

% TODO: Confirm availability state (preview or GA) and update applies_to.
% TODO: Confirm product IDs and which Serverless project types are in scope.

# Data recovery in {{serverless-full}}

Data recovery in {{serverless-full}} helps you recover from accidental deletions and unintended updates. 

Elastic automatically protects your indices and data streams by creating recovery points in the background. If data is deleted or overwritten by mistake, you can recover an earlier version of it from the last 7 days. Data recovery is designed for short-window recovery.

You can recover data as new copies of your indices or data streams, or replace your existing instances. You can also recover several indices and data streams at once, by listing them by name or using [wildcard patterns](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#api-multi-index).


## What data recovery protects

Data recovery covers the data you own in a project: your indices and your [data streams](/manage-data/data-store/data-streams.md). Data streams are always recovered as a whole.

**Data recovery includes:**

* Indices that you created.
* Data streams that you created, including their full history within the recovery window.

**Data recovery doesn't include:**

* {{kib}} content, such as dashboards and other [saved objects](/explore-analyze/find-and-organize/saved-objects.md).
* Project configuration, such as ingest pipelines, roles, and {{ml}} jobs.
* [Index templates](/manage-data/data-store/templates.md#index-templates), [component templates](/manage-data/data-store/templates.md#component-templates), and [lifecycle policies](/manage-data/lifecycle.md).
* System indices, which store internal data for {{es}} and {{kib}}.
* Individual [backing indices](/manage-data/data-store/data-streams.md#backing-indices) of a data stream. You can recover only the data stream as a whole.

Data recovery applies to data only. To protect configuration, manage it through your own deployment tooling, such as [saved object exports](/explore-analyze/find-and-organize/saved-objects.md#saved-objects-export), Terraform, or a CI/CD pipeline.

Data recovery works within a single project. You can recover data only into the project that it belongs to, not into another {{serverless-short}} project, an {{ech}} deployment, or a self-managed cluster.

## How data recovery works

{{serverless-short}} manages data recovery for you, so there's nothing to set up or maintain. Elastic creates recovery points in the background. When you need to recover data, you choose what to recover and a point in time to recover it from, and Elastic runs the recovery as a background job. By default, Elastic recovers your indices and data streams as new copies, so you can check the data before replacing it.

You can start a recovery and follow its progress in the {{ecloud}} Console or through the <endpoint_name> API. In the Console, find your project on the home page and select **Manage**, and then select **Data recovery** from the navigation menu. 

When a recovery finishes, you get a summary of what was recovered, what was skipped and why, and the resolved recovery time. This is the time that the data was actually recovered from, which can be earlier than the time you requested.

A recovered data stream needs a matching [index template](/manage-data/data-store/templates.md#index-templates) to keep working, for example to roll over and create new backing indices. Data recovery doesn't recover templates, so Elastic skips any data stream that has no matching template and reports the reason in the summary.

% TODO: Cover these data stream details in the how-to and troubleshooting pages: the new copy's name must also match an index template (link to /manage-data/data-store/data-streams/set-up-data-stream.md#create-index-template), and the data stream follows the project's current matching template and lifecycle settings.
% TODO: Confirm lifecycle behavior (ILM or data stream lifecycle) after recovering as new copies and after replacing current data. This is an open question in the PRD.
% TODO: Confirm the final Console entry point and the **Data recovery** menu label with Design. The PRD lists the entry point as TBD.
% TODO: Confirm the behavior of live indexing and search while a recovery is running, and which safeguards apply when replacing current data in a data stream that's receiving writes.
% TODO: Add a diagram showing recovery points over the 7-day window, the requested time, and the resolved recovery time.

### Recovery points

Elastic automatically creates recovery points for your project and keeps them for 7 days. This period is called the recovery window.

A recovery point isn't a single instant. Different parts of your data are captured at slightly different moments, so each recovery point covers a short span of time that runs from the earliest capture to the latest.

As a result, changes made very close to a recovery point might be only partly included, and changes made to different indices around the same time might not reflect exactly the same moment. Review recovered data before you rely on it, especially when it spans several indices.

% TODO: Confirm with Engineering how to describe consistency across multiple indices in one recovery.

### Recovery options

You choose how to recover your data: as new copies, or by replacing your current data.

| | Recover as new copies | Replace current data |
|---|---|---|
| **What happens** | Recovered data is added alongside your current data as new indices or data streams. Elastic adds a prefix or suffix to each original name. | Recovered data replaces the current index or data stream and keeps its original name. |
| **Effect on current data** | None. | Overwritten. Changes made after the recovery point are lost. |
| **Can be undone** | Yes. Delete the new copy. | No. |
| **Best for** | Checking recovered data first, comparing it with current data, or recovering only part of it. | Putting everything back exactly as it was, when you're sure about the time. |
| **Default** | Yes. | No. Requires explicit confirmation. |

Recovering as new copies never overwrites existing resources. If a resource with the new name already exists, Elastic doesn't recover that resource, and the recovery results explain why.

% TODO: Confirm availability of replacing current data. The PRD notes a dependency on engine support for recovering over open indices (elastic/elasticsearch#101031). Replacing current data might ship after recovering as new copies.
% TODO: Confirm the default naming behavior (prefix or suffix), the generated name format, and whether an existing name for a new copy fails the whole recovery (preflight) or only skips that resource.


## Other ways to protect your data

Data recovery isn't the right tool for every kind of data protection. Use these options for needs that data recovery doesn't cover.

| If you need to | Use |
|---|---|
| Keep data for months or years, or search older data affordably | Your data lifecycle settings, such as [{{ilm}}](/manage-data/lifecycle/index-lifecycle-management.md) or [data stream lifecycle](/manage-data/lifecycle/data-stream.md) |
| Recover from a regional outage or fail over to another region | [Resilience in {{serverless-full}}](/deploy-manage/production-guidance/availability-and-resilience/resilience-in-serverless.md). Data recovery doesn't cover this scenario. |
| Restore dashboards, templates, pipelines, or other configuration | Your own deployment tooling, such as [saved object exports](/explore-analyze/find-and-organize/saved-objects.md#saved-objects-export), Terraform, or CI/CD |
| Copy data into another project | Not supported by data recovery |

% TODO: The PRD says these related capabilities are deferred, not committed. Keep wording neutral and avoid implying future availability.
% TODO: Decide whether to add a short "Coming from {{ech}}?" note here. The PRD says docs must not reference snapshots, so this needs a policy decision.

