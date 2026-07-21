---
navigation_title: Attacks page
applies_to:
  stack: preview 9.4
  serverless: preview
products:
  - id: security
  - id: cloud-serverless
---

# Manage discoveries from the Attacks page [attacks-page]

This page describes how to manage discoveries from the **Attacks** page: view, filter, assign, tag, and act on all attacks in your environment, alongside their correlated alerts. Before you get started, make sure you meet the [prerequisites](/solutions/security/ai/attack-discovery/run-from-attacks-page.md#run-from-attacks-page-prerequisites) for accessing the page.

## How it works [attacks-how-it-works]

At the top of the **Attacks** page, you can find overview visualizations and tables. The **Summary** tab shows the total number of attacks detected and attack volume over time, while the **Trends**, **Count**, and **Treemap** tabs all describe alerts associated with these attacks.

::::{image} /solutions/images/security-attacks-page-ov.png
:alt: Overview of the Attacks page showing the Summary tab
:screenshot:
::::

Below the summary section, the Attacks table lists individual attacks. You can expand an attack to view details including which entities were involved and which steps of the attack chain were performed.

## Filter and search attacks [attacks-filter-search]

Use the controls at the top of the Attacks table to narrow results:

| Filter method | Description |
|---------------|-------------|
| KQL search | Enter queries in the search bar. Autocomplete includes fields from both attacks and alerts. |
| Date/time picker | Set a specific time range. |
| Status filter | Filter by [status](#change-attack-status): **Open**, **Acknowledged**, or **Closed**. |
| Assignees filter | Click **Filter by assignees** to show only attacks or alerts [assigned](#assign-attacks) to specific users. |
| Sort | Use the **Sort by** menu to sort by **Most recent**, **Least recent**, **Most alerts**, or **Least alerts**. |

### View options [attacks-view-options]

Click the **View options** ({icon}`controls`) menu to access the following toggles:

**Show attacks only**: This toggle is enabled by default. It hides standalone alerts (alerts that don't belong to any attack) so you can focus on correlated attack groups. Disable it to see all alerts, including those not linked to any attack.

:::{note}
When **Show attacks only** is disabled, standalone alerts appear in a group labeled `-` (dash). This group acts as a bucket for all alerts that aren't linked to an attack.
:::

**Show anonymized values**: When enabled, replaces attack titles and summaries with anonymized placeholder values. If you're searching the page for specific entities like hostnames or IP addresses, make sure to turn this off.

### How filtering works on the Attacks page [attacks-filtering-behavior]

The **Attacks** page uses a single data view that combines both the attacks index and the alerts index. This enables powerful cross-document filtering, but it also means that filters apply to both document types simultaneously.

:::{dropdown} Filtering behavior details

**Timeframe filtering**: An attack group appears if either the attack itself or any of its related alerts fall within the selected time range. If the attack is within the time range but all its alerts are outside of it, the attack renders but shows 0 alerts when expanded. Conversely, if the attack is outside the time range but some of its alerts are inside, the attack still appears.

**Alert-specific field filters**: Filtering on a field that only exists on alert documents (not attack documents) excludes attack documents from the underlying dataset. Attack groups still appear, but group statistics and sorting may be affected.

**Attack-specific field filters**: Filtering on a field that only exists on attack documents (for example, the connector that generated an attack) hides all related alerts from the dataset. The attack group appears, but expanding it shows 0 alerts because the alert documents don't contain the attack-specific field.

**Status filter**: The status filter evaluates both attacks and their related alerts. A closed attack can still appear when you filter by **Open** status if it has underlying open alerts that match the filter.

**Assignees filter**: The assignees filter applies across both attacks and alerts. Filtering by assigned user may hide an attack's alerts if those alerts have a different assignee.

**Sorting by timestamp**: Sorting evaluates all visible documents in a group. If an alert-specific query filters out an attack document, the group's position in the sort order is based solely on the timestamps of its remaining alerts.

**KQL autocomplete**: The KQL autocomplete shows fields from both attacks and alerts. Be cautious when filtering, because using a field exclusive to one document type filters out the other type from the underlying data.

**Alerts count badge**: The **Alerts: N** badge on each attack group counts only detection alerts that match the current filters — it doesn't include the attack document itself. When you expand a group, the badge may show a format like `2/10`, where the first number is the count of alerts matching your current filters and time range, and the second is the total number of alerts historically linked to the attack.

:::

## Take actions on an attack [attacks-manage]

Access actions from the **Take actions** menu on an attack's row in the Attacks table.

:::{note}
When you change an attack's status, assign or unassign it, or apply attack tags, a modal appears that lets you apply the action to the attack only, or to both the attack and its associated alerts — the same choice available when [changing a discovery's status](/solutions/security/ai/attack-discovery/manage-discoveries-from-attack-discovery-page.md#discovery-status).
:::

| Action | Description |
|--------|-------------|
| [Change status](#change-attack-status) | Mark as acknowledged or closed |
| [Run workflow](#run-workflow-from-attack) | Run an Elastic workflow for on-demand response or investigation |
| [Assign or unassign attack](#assign-attacks) | Assign analysts to investigate |
| [Apply attack tags](#apply-attack-tags) | Categorize attacks for filtering |
| [Investigate in timeline](#attacks-investigate-timeline) | Open the attack in Timeline for analysis |
| [Add to case](#attacks-add-to-case) | Attach the attack to a new or existing case |
| [View in AI Chat](#attacks-view-in-ai-chat) | Continue investigating with an AI agent |

### Change attack status [change-attack-status]

Attacks use the same [status lifecycle as discoveries](/solutions/security/ai/attack-discovery/manage-discoveries-from-attack-discovery-page.md#discovery-status): **Open** (default), **Acknowledged**, or **Closed**.

To change an attack's status, click **Take actions** on the attack row, then select **Mark as acknowledged** or **Mark as closed**.

### Run a workflow from an attack [run-workflow-from-attack]

You can run an [Elastic workflow](/explore-analyze/workflows.md) directly from an attack to trigger an on-demand response or investigation. To use this feature, make sure you meet the [workflows prerequisites](/explore-analyze/workflows/get-started.md).

To run a workflow, click **Take actions** on the attack row, then click **Run workflow**. Use the search bar to select a workflow, then click **Run workflow**.

:::{note}
You can select only enabled workflows.
:::

### Assign or unassign attacks [assign-attacks]

Assign analysts to attacks they should investigate.

| Task | How to do it |
|------|--------------|
| Assign an attack | **Take actions** > **Assign attack** > select users |
| Unassign an attack | **Take actions** > **Unassign attack** |

:::{important}
Users are not notified when assigned or unassigned.
:::

### Apply attack tags [apply-attack-tags]

Tags help organize attacks into filterable categories.

To tag an attack, click **Take actions**, then select **Apply attack tags**.

### Investigate in timeline [attacks-investigate-timeline]

To open an attack in [Timeline](/solutions/security/investigate/timeline.md), click **Take actions** on the attack row, then select **Investigate in timeline**.

:::{note}
Investigating an attack in Timeline includes all alerts that were originally correlated when the attack was created. It doesn't reflect your current page filters or selected time range.
:::

### Add to case [attacks-add-to-case]

To add an attack to a [case](/solutions/security/investigate/security-cases.md), click **Take actions**, then select **Add to new case** or **Add to existing case**.

### View in AI Chat [attacks-view-in-ai-chat]

To continue investigating an attack with an [AI agent](/explore-analyze/ai-features/ai-chat-experiences.md), click **Take actions**, then select **View in AI Chat**. You can ask follow-up questions about the attack or its associated alerts.
