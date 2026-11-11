---
applies_to:
  serverless:
    observability: preview
description: Set up and manage the data that the Elastic nightshift Detection engine watches, and review the significant events that it detects.
products:
  - id: observability
  - id: cloud-serverless
---

# Audit and manage detections [nightshift-audit-detections]

Use these tasks to choose the data that the Detection engine watches, manage it over time, and review what detection found. For how detection works, including rules, signals, alerts, and significant events, refer to the [Detection engine](./core-components/detection-engine.md).

## Set up detection sources [nightshift-detections-sources]

Detection watches your data for problems worth knowing about. Choose the data to watch by adding a source. You don't need a source to run an investigation.

A source is an {{esql}} query that selects the data to watch. Sources are used only by detection. The query starts with `FROM` or `TS`, and only a `WHERE` command can follow. Every index in a source must hold the same kind of data, such as logs, metrics, or traces, which the index names decide.

% TODO(verify): Does detection create rules from metrics or traces sources in Tech Preview, or only from logs?

Before you add a source:

- An admin has [enabled Elastic nightshift](./get-started.md#nightshift-get-started-enable).
- You have the **Manage engines** privilege, which covers creating, editing, turning on, turning off, and deleting sources. Refer to [Grant access to Elastic nightshift](./get-started/privileges.md).
- The data that you want to watch has recent data.

To add a source:

1. From the Elastic nightshift home page, select **Detections**. Before detection is on, the page explains how detection works and shows **Select data sources to analyze**.
1. In the table of sources, which shows each source's **Title** and **Query**, select the sources to analyze. To create your own, select **Create new source**, then:

   1. Enter a **Title**. Optionally, add a **Description** and **Tags**.
   1. In **ES|QL query**, write the query for the data to watch. To generate the query from a description, enter a `//` comment that describes what you're looking for, then press {kbd}`cmd+j`.
   1. Select **Run query** to preview the data in the **Data preview** pane. The preview covers the **Last 15 minutes** by default.
   1. Select **Add source**.

1. Select **Enable detection**.

The table starts with an **All logs** source, which uses the query `FROM logs*`. Elastic nightshift looks into each source, extracts the knowledge it finds, and watches for potential problems. You can change the sources later.

After you add a source, Elastic nightshift learns from the data and generates KIs, then generates detection rules from the KIs and starts running them. When rule firings add up to something meaningful, it surfaces a significant event.

## Manage sources [nightshift-detections-manage-sources]

After you add a source, you can view it, change what it watches, pause it, or remove it, and check what it produced. Managing sources needs the **Manage engines** privilege.

To open the list, select **Sources** at the top of the **Detections** page. The **Sources** page shows how many sources you have and lets you search them by title, tag, or query. For each source, it shows:

- **Title** and **Query**: What the source is called and the {{esql}} query that it runs.
- **Enabled**: A toggle that turns the source on or off.
- **Status**: An icon that shows whether the source is working. A green check means that the source has no error. A red X means that Elastic nightshift hit an error with the source. Hover over the X to read the error.
- **KI Features** and **KI Queries**: How many Knowledge Indicators Elastic nightshift extracted from the source, and how many queries it generated.
- **Events**: How many events the source produced.

To work with a source:

- To add a source, select **Create source**, fill in the same fields as in [Set up detection sources](#nightshift-detections-sources), and select **Create source** again. The **Enabled** toggle is on by default, and onboarding starts as soon as the source is created. Turn it off to create the source without turning it on.
- To edit a source, select its title. The **Edit source** form opens with the title, description, tags, and query filled in, and a **Data preview** of the last 24 hours. Change what you need, select **Run query** to preview the result, and select **Save**.
- To generate Knowledge Indicators from a source on demand, select the source's checkbox, then select **Generate**. **Generate** is unavailable until you select at least one source. To run only one step, open the menu next to **Generate**. **Generate KI Features** runs only feature identification on the selected sources, and **Generate KI Queries** runs only query generation. Each option uses the model that you choose in its submenu.
- To look for significant events on demand, select **Find significant events**. Elastic nightshift starts looking for significant events in your sources without waiting for the next scheduled run. To stop a run that's in progress, open the menu next to the button and select the option to cancel it.
- To pause a source, turn off its **Enabled** toggle.
- To remove a source, select the delete icon in its row. Deleting a source also deletes its Knowledge Indicators and rules. You can also select several sources and remove them together.

To pause all detection activity instead, refer to [Settings and lifecycle](./manage/settings-and-lifecycle.md).

Sources decide which indices the Elastic nightshift service account reads, and the significant events and detections it finds are shown to everyone with Elastic nightshift access in the space.

## Review significant events [nightshift-detections-review-events]

Review significant events to see what detection found, why, and which ones need an investigation. You need read access to Elastic nightshift.

1. From the Elastic nightshift home page, select **Detections**. At the top, the **Detection engine** shows its state, such as **Monitoring**, and counts of knowledge indicators, entities, rules, signals, and significant events.
1. Make sure the **Events** tab is selected. The **Rules** and **Signals** tabs show the rules and signals behind the events. Refer to [Review rules and signals](#nightshift-detections-rules-signals).
1. Find the event you want to review. Each row shows the event's title and a summary, when it was created and last updated, its **Status**, its **Severity**, and its **Investigation**. To narrow the list:

   - Search by text, or change the time range, which defaults to **Last 24 hours**.
   - Filter by **Severity**, **Status**, or **Investigation**.
   - In the **Entities** list on the left, select the services or other entities that you want to see events for.

1. Select an event to open its details. The details show the event's title, when it was created, and badges for its severity, confidence, and status. The **Overview** tab has the following sections:

   - **What happened?**: A summary of what the discovery agent grouped into the event. Select **Show more** to read all of it.
   - **Investigation**: The investigation of the event, if there is one.
   - **Detections**: The detections behind the event, each with the kind of change it found, such as **Distribution change**, and the entity it applies to.

   Select the **Timeline** tab to see how the event developed, in time order. It lists the detections that fed the event, such as a **Distribution change**. It also lists when Elastic nightshift raised the event, with its severity and an explanation of why, including the reason for its confidence, and each later update to the event.

1. Check the event's status:

   - **Active**: A current failure is confirmed, or remains plausibly unverified. The event needs attention.
   - **Recovering**: Every member rule was last judged healthy. The event returns to active if any member rule breaches again.
   - **Inactive**: Every confirming signal on the event was re-checked and cleared, or an operator deactivated the event.

The **Investigation** column shows whether the event has been investigated: **Not started** or **Completed**. To find the likely cause of an event, select **Investigate** in the **Actions** column. You can also select **Actions** in the event's details, then **Run investigation**. Refer to [Start an investigation](./investigate-and-respond.md#nightshift-investigations-start-event).

From the **Actions** menu in an event's details, you can also:

- Select **Open investigation in chat** to continue a completed investigation.
- Select **New chat about this event** to ask questions about the event without starting an investigation.
- Select **Mark inactive** to deactivate an event that no longer needs attention.

% TODO(verify): How is the **Confidence** badge calculated, and what range does it use? Source: the event details show badges such as **Confidence 62%**, and the **Timeline** entry for one event says the confidence is 62.0% because of a very low p-value and aligned feature support, but only one rule confirms the finding.

## Review rules and signals [nightshift-detections-rules-signals]

The **Rules** and **Signals** tabs show what detection ran and what it found. Use them to see which rules match the most, and what each rule detected.

On the **Rules** tab, a chart shows rule matches over time, and a table lists every rule with the following columns:

- **Title**: The name of the rule.
- **Impact**: How serious a rule's matches are, such as **Critical**.
- **Last activity**: When the rule last matched.
- **Status**: Whether the rule is active, such as **Active**.
- **Matches**: How many times the rule matched in the selected time range.

To work with one rule, open its {icon}`boxes_vertical` menu, then select **Open in Discover** to open the rule in Discover, or **Delete rule** to remove it. To remove several rules, select them in the table, then select **Delete selected**. Search for a rule by name, or change the time range, which defaults to **Last 24 hours**.

The **Signals** tab lists the signals that rules recorded, one per row. Each row shows the rule, the kind of change it found, such as **Spike**, **Non-stationary**, or **Distribution change**, the source, a timestamp, and its **Discovery** state: **Pending**, **Skipped**, or **Processed**. Use the **Change** filter to show only certain kinds of change.

## Learn more [nightshift-detections-nav]

- [Detection engine](./core-components/detection-engine.md): Learn how detection works from data to significant events
- [Operator guide](./significant-events/operator-guide.md): Learn about system impact, cost drivers, and recovery
- [Investigate and respond](./investigate-and-respond.md): Investigate a significant event
