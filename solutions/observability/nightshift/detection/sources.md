---
navigation_title: Manage what detection monitors
applies_to:
  serverless:
    observability: preview
description: Turn on detection, choose the logs that Elastic nightshift learns from and watches, and manage your sources over time.
products:
  - id: observability
  - id: cloud-serverless
---

# Manage what detection monitors [nightshift-detection-sources]

Tell {{nightshift}} which logs to learn from and watch for problems. Start with all your logs in one step, or narrow detection down to the services you care about most.

Each set of data that detection watches is a *source*. You choose sources when you turn detection on, and you can add, change, pause, or remove them at any time.

## Before you begin [nightshift-detection-sources-before]

- An admin has [enabled {{nightshift}}](../get-started/investigations.md#nightshift-get-started-enable).
- You have the privileges to manage detection sources. Refer to [Grant access](../get-started/privileges.md#nightshift-privileges-admin).
- Your project has recent logs, or can reach them through {{cps}}.

## Turn on detection [nightshift-detection-sources-enable]

To turn on detection, follow [Set up detection](../get-started/detection.md). To watch only some of your logs from the start, [create a source](#nightshift-detection-sources-create) first, then select it when you enable detection. **All logs** watches all your logs with the query `FROM logs*`.

{{nightshift}} starts to learn from each source right away. Refer to [How long learning takes](./learning.md#nightshift-detection-learning-warmup).

## What a source is [nightshift-detection-sources-what]

A source is an {{esql}} query that selects rows of data, and nothing else. The query must:

- Start with `FROM` or `TS`.
- Contain only `WHERE` commands after that. Commands that change the rows, such as `STATS`, `EVAL`, or `KEEP`, aren't allowed.
- Target one kind of data. All indices in the query must be logs, all metrics, or all traces, which {{nightshift}} derives from the index names. For example, `FROM logs-*, my-app-*` is rejected because `my-app-*` isn't recognized as logs. A wildcard for everything, such as `*`, is also rejected.

Detection currently learns only from logs, so use logs sources.

Sources apply to detection only. Investigations don't need a source. They query all the logs, metrics, and traces that your connectors reach.

For example:

- All your logs: `FROM logs*`
- The services of one application:

  ```esql
  FROM logs-*
  | WHERE service.name IN ("inventory-api", "web", "ticket-issuer")
  ```

- One environment:

  ```esql
  FROM logs-*
  | WHERE deployment.environment == "production"
  ```

Each source is learned separately, and cost grows with the number of sources. Start with **All logs**. Add narrower sources when you want detection to focus on a part of your system.

:::{note}
Detection reads data from all projects linked through {{cps}}, whatever project scope is configured for this space.
:::

## Create a source [nightshift-detection-sources-create]

To create a source from the **Detections** page:

1. At the top of the **Detections** page, select **Sources**, then select **Create source**.
1. Enter a **Title**. Optionally, add a **Description** and **Tags**.
1. In **ES|QL query**, write the query for the logs to watch. To have the query written for you, enter a `//` comment that describes the data, then press {kbd}`cmd+j`.
1. Select **Run query**. Check the rows in **Data preview**.
1. Keep **Enabled** on, so that {{nightshift}} starts to learn from the source right away.
1. Select **Create source**.

The source appears in the list, and learning starts. On the **Detections** page before detection is on, the same form ends with **Add source** instead.

## Manage sources [nightshift-detection-sources-manage]

To open the list, select **Sources** at the top of the **Detections** page. Search by title, tag, or query.

% SCREENSHOT: The Sources page with the All logs source and one custom source, showing the Enabled toggle, Events, KI Queries, KI Features, and Status columns, and the Generate and Find significant events buttons.

| Column | What it shows |
| --- | --- |
| **Title**, **Query** | The name of the source and its {{esql}} query. |
| **Enabled** | Whether detection learns from and watches this source. |
| **Events** | How many results the source's rules produced in the last 24 hours. |
| **KI Queries**, **KI Features** | How many query KIs and feature KIs {{nightshift}} extracted from the source. Refer to [How detection learns your system](./learning.md). |
| **Status** | A green check if the source works. A red X if {{nightshift}} hit an error. Hover over the X to read the error. |

To work with a source:

- **Change it.** Select its title, change the fields in **Edit source**, and select **Save**. If you change the query, the source's KIs and rules no longer match it, so {{nightshift}} deletes them and learns the source again. Confirm with **Save and reset knowledge**.
- **Learn from it again now.** Select **Onboard source** in its row. To stop a run, select **Stop source onboarding**. For several sources, select them and then **Generate**. To run only one step, open the menu next to **Generate** and select **Generate KI Features** or **Generate KI Queries**.
- **Look for significant events now.** Select **Find significant events** to run discovery without waiting for the next scheduled run. To stop it, open the menu next to the button and select **Cancel**.
- **Pause it.** Turn off **Enabled**.
- **Delete it.** Select the delete icon in its row, then **Delete source**. This deletes the source, its KIs, and its rules. Significant events that detection already found are kept.

Runs that you start yourself don't count toward the daily run limits. If you delete your last source, detection stops and the **Detections** page shows only earlier results.

To pause all detection instead of one source, go to **Settings** → **Detections** and select **Pause detection engine**. Refer to [Settings and limits](../settings.md).

## Next steps [nightshift-detection-sources-next]

- [How detection learns your system](./learning.md): Find out what {{nightshift}} extracts from your sources and how long it takes.
- [Review significant events](./significant-events.md): Review what detection finds and investigate it.
- [Settings and limits](../settings.md): Set run limits and continuous learning, or pause detection.
