---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/synthetics-manage-retention.html
  - https://www.elastic.co/guide/en/serverless/current/observability-synthetics-manage-retention.html
---

# Manage data retention [synthetics-manage-retention]

When you set up a synthetic monitor, data from the monitor is saved in [{{es}} data streams](../../../manage-data/data-store/data-streams.md), an append-only structure in {{es}}.

There are six data streams recorded by synthetic monitors: `http`, `tcp`, `icmp`, `browser`, `browser.network`, `browser.screenshot`. Elastic will retain data from each data stream for some time period, and the default time period varies by data stream. If you want to reduce the amount of storage required or store data for longer, you can customize how long to retain data for each data stream.


## Synthetics data streams [synthetics-manage-retention-data-streams]

There are six data streams recorded by synthetic monitors:

| Data stream | Data includes | Default retention period |  |
| --- | --- | --- | --- |
| `http` | The URL that was checked, the status of the check, and any errors that occurred | 1 year |  |
| `tcp` | The URL that was checked, the status of the check, and any errors that occurred | 1 year |  |
| `icmp` | The URL that was checked, the status of the check, and any errors that occurred | 1 year |  |
| `browser` | The URL that was checked, the status of the check, and any errors that occurred | 1 year |  |
| `browser.screenshot` | Binary image data used to construct a screenshot and metadata with information related to de-duplicating this data | 14 days |  |
| `browser.network` | Detailed metadata around requests for resources required by the pages being checked | 14 days |  |

All types of checks record core metadata. Browser-based checks store two additional types of data: network and screenshot documents. These browser-specific indices are usually many times larger than the core metadata. The relative sizes of each vary depending on the sites being checked with network data usually being the larger of the two by a significant factor.


## Customize data stream lifecycles [synthetics-manage-retention-customize]

If Synthetics browser data streams are storing data longer than necessary, you can opt to retain data for a shorter period.

To find Synthetics data streams:

::::{tab-set}
:group: stack-serverless

:::{tab-item} Elastic Stack
:sync: stack

1. Navigate to [{{kib}} index management](../../../manage-data/lifecycle/index-lifecycle-management/index-management-in-kibana.md).
2. Filter the list of data streams for those containing the term `synthetics`.

    1. In the UI there will be three types of browser data streams: `synthetics-browser-*`, `synthetics-browser.network-*`, and `synthetics-browser.screenshot-*`.

:::

:::{tab-item} Serverless
:sync: serverless

1. Navigate to **Project settings** → **Management** → **Index Management** → **Data Streams**.
2. Filter the list of data streams for those containing the term `synthetics`.

    1. In the UI there will be three types of browser data streams: `synthetics-browser-*`, `synthetics-browser.network-*`, and `synthetics-browser.screenshot-*`.

:::

::::

Then, you can refer to [Tutorial: Customize data retention for integrations](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/data-streams-ilm-tutorial.md) to learn how to apply a custom {{ilm-init}} policy to the browser data streams.