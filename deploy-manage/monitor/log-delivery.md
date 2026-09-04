---
navigation_title: Serverless log delivery
description: Ship selected log types from any Elastic Cloud Serverless project to a Security or Observability project in your organization.
applies_to:
  serverless: preview
products:
  - id: cloud-serverless
---

# Log delivery in {{serverless-full}} [log-delivery]

Log delivery lets you ship selected log types from any {{serverless-full}} project to any {{sec-serverless}} or {{obs-serverless}} project in your organization.

## Key concepts

With log delivery, you can:

* Select [source and destination projects](#source-and-destination-projects) in your organization.
* Apply [ignore filters](#ignore-filters) to exclude events you don't need delivered.
* Manage [billing and usage](#billing-and-usage) by adjusting delivered volume and retention.

### Source and destination projects

The **source** is the {{serverless-short}} project that produces the logs. You configure log delivery here. Any project type ({{es-serverless}}, {{sec-serverless}}, or {{obs-serverless}}) can be a source. 

The **destination** is the {{serverless-short}} project that receives and stores the delivered logs. Destinations must be {{sec-serverless}} or {{obs-serverless}} projects in the same organization.

You can use the same project as both source and destination. The destination can be in a different cloud provider region than the source, however, cross-region delivery can incur data transfer charges. Refer to [Billing and usage](#billing-and-usage).

Logs are encrypted while moving from your source project to the destination project and while they are stored on the destination.

### Ignore filters

When configuring log delivery, you can apply **ignore filters** to exclude certain events from being delivered. For example, if you're setting up an audit trail log delivery and you don't need data on every role check, you could apply the **Ignore routine user and role checks** filter. Role check information will not be delivered to your selected destination project.

Ignore filters help you drill down into the data you actually need and ignore the rest. Also, ignore filters exclude matching events *before* delivery, reducing the volume of your delivery and the overall cost. 

:::{important}
If you don't choose any ignore filters, *all* events for your chosen log type will be delivered. This is the highest volume option and directly affects your {{serverless-short}} bill.
:::

### Billing and usage

Log delivery usage is metered. Cost is proportional to the volume of the delivery and retention of the data delivered, so you can control it by managing these parameters:

* Usage depends on the combination of source project, log type, and destination project you choose. Adjust these combinations to see which ones drive higher volume.
* Data transfer charges depend on the combination of source and destination projects. For example, same-project delivery does not incur transfer charges, but delivery to a different project in a different region does. Consider this in your configuration.
* Ignore filters exclude events *before* delivery. Use them to reduce the volume of delivered data.
* Ingestion and retention of delivered data is billed on the destination project. For exact rates, refer to [{{sec-serverless}} pricing](https://www.elastic.co/pricing/serverless-security) and [{{obs-serverless}} pricing](https://www.elastic.co/pricing/serverless-observability). Use [AutoOps](/deploy-manage/monitor/autoops/autoops-for-serverless.md) on your destination project to monitor your ingest rate and storage retained, and adjust accordingly.

## Log types

[Audit trail](/deploy-manage/monitor/log-delivery/audit-trail.md) is the first log type available for delivery. More log types are coming soon.