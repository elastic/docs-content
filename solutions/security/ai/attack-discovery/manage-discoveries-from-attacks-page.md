---
navigation_title: Manage from Attacks view
description: "Triage Attack Discovery findings alongside related alerts from the Attacks view under Detections."
applies_to:
  stack: preview =9.4, ga 9.5+
  serverless: ga
products:
  - id: security
  - id: cloud-serverless
---

# Manage discoveries from the Attacks view [attacks-page]

The **Attacks** view brings Attack Discovery findings together with their related alerts so you can triage them in one place under **Detections**. Open it at **Detections > Views > Attacks**. It is a sibling of **Alerts**, not a standalone top-level page.

This page covers how to filter and search attacks, tell manually generated and scheduled attacks apart, review linked alerts, and take triage actions. Before you get started, make sure you meet the [Before you begin](/solutions/security/ai/attack-discovery/run-from-attacks-page.md#run-from-attacks-page-before-you-begin) requirements for accessing the view.

## How it works [attacks-how-it-works]

At the top of the **Attacks** view, overview visualizations summarize activity. The **Summary** tab shows the total number of attacks detected and attack volume over time. The **Trends**, **Count**, and **Treemap** tabs describe alerts associated with those attacks.

::::{image} /solutions/images/security-attacks-page-ov.png
:alt: Overview of the Attacks view showing the Summary tab
:screenshot:
::::

Below the summary, the Attacks table lists individual attacks. Expand an attack to see involved entities and steps in the attack chain.

## Manually generated and scheduled attacks [manually-generated-attacks]

::::{applies-switch}

:::{applies-item} { "stack": "ga 9.5+", "serverless": "ga" }

The Attacks table lists both manually generated and scheduled discoveries. Both types share the same details flyout and triage actions. To start a manual run, refer to [Manually run Attack Discovery](/solutions/security/ai/attack-discovery/manual-runs-from-attacks-page.md).

| Type | What it is | How to recognize it |
|---|---|---|
| **Scheduled** | Created by a recurring Attack Discovery schedule. | A calendar icon appears in the attack title column and in the Attack flyout header. Hover for the **Scheduled Attack discovery** tooltip. Select the icon to open schedule details, including execution history and configuration. |
| **Manually generated** | Created when you select **Run** on the Attacks view or the Attack Discovery page. | The attack subtitle shows who ran it: detected time, **Run by** with the user's avatar, and the attack summary. The same **Run by** details appear in the Attack flyout summary. |

:::

:::{applies-item} stack: preview =9.4

In 9.4, the **Attacks** view lists scheduled discoveries. Manual runs appear after you start them from the [Attack Discovery page](/solutions/security/ai/attack-discovery/run-from-attack-discovery-page.md).

:::

::::

## Filter and search attacks [attacks-filter-search]

Use the controls at the top of the Attacks table to narrow results:

| Filter method | Description |
|---------------|-------------|
| KQL search | Enter queries in the search bar. Autocomplete includes fields from both attacks and alerts. |
| Date/time picker | Set a specific time range. |
| Status filter | Filter by [status](#attacks-manage): **Open**, **Acknowledged**, or **Closed**. |
| {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` Type filter | Show **Scheduled** attacks, **Manually generated** attacks, or both. |
| {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` Connector filter | Filter attacks by the LLM connector that generated them. |
| Assignees filter | Click **Filter by assignees** to show only attacks or alerts [assigned](#attacks-manage) to specific users. |
| Sort | Use the **Sort by** menu to sort by **Most recent**, **Least recent**, **Most alerts**, or **Least alerts**. |

:::{note}
:applies_to: {"stack": "ga 9.5+", "serverless": "ga"}
**Type**, **Connector**, and **Assignees** filter selections persist across page reloads. The **Attacks volume over time** summary graph updates to match the filters you apply.
:::

### View options [attacks-view-options]

Open the **View options** ({icon}`controls`) menu for these toggles:

* **Show attacks only** (on by default): Hides standalone alerts that don't belong to any attack. Turn it off to see all alerts, including unlinked ones. Unlinked alerts appear in a group labeled `-` (dash).
* **Show anonymized values**: Replaces attack titles and summaries with anonymized placeholders. Turn this off if you are searching for specific entities such as hostnames or IP addresses.

### How filtering works [attacks-filtering-behavior]

The **Attacks** view uses one data view that combines the attacks index and the alerts index, so filters apply to both document types at once.

:::{dropdown} Filtering behavior details

**Timeframe filtering**: An attack group appears if either the attack itself or any of its related alerts fall within the selected time range. If the attack is within the time range but all its alerts are outside of it, the attack renders but shows 0 alerts when expanded. Conversely, if the attack is outside the time range but some of its alerts are inside, the attack still appears.

**Alert-specific field filters**: Filtering on a field that only exists on alert documents (not attack documents) excludes attack documents from the underlying dataset. Attack groups still appear, but group statistics and sorting may be affected.

**Attack-specific field filters**: Filtering on a field that only exists on attack documents (for example, the connector that generated an attack) hides all related alerts from the dataset. The attack group appears, but expanding it shows 0 alerts because the alert documents don't contain the attack-specific field.

**Status filter**: The status filter evaluates both attacks and their related alerts. A closed attack can still appear when you filter by **Open** status if it has underlying open alerts that match the filter.

**Assignees filter**: The assignees filter applies across both attacks and alerts. Filtering by assigned user may hide an attack's alerts if those alerts have a different assignee.

**Sorting by timestamp**: Sorting evaluates all visible documents in a group. If an alert-specific query filters out an attack document, the group's position in the sort order is based solely on the timestamps of its remaining alerts.

**KQL autocomplete**: The KQL autocomplete shows fields from both attacks and alerts. Be cautious when filtering, because using a field exclusive to one document type filters out the other type from the underlying data.

**Alerts count badge**: The **Alerts: N** badge on each attack group counts only detection alerts that match the current filters. It doesn't include the attack document itself. When you expand a group, the badge may show a format like `2/10`, where the first number is the count of alerts matching your current filters and time range, and the second is the total number of alerts historically linked to the attack.

:::

## Review alerts for an attack [attacks-alerts-tab]
```{applies_to}
stack: ga 9.5+
serverless: ga
```

When you open an attack's details, the **Alerts** tab shows the alerts linked to that attack.

By default, the tab shows **all** linked alerts, even when page filters are active. Alerts that do not match the current filters stay visible but are visually de-emphasized (greyed out), so the list still matches the attack's total alert count.

A callout above the alerts table explains this behavior and includes a **Show matching alerts only** toggle. Turn the toggle on if you want to hide non-matching alerts. Your toggle choice persists across attacks.

Attack group statistics in the Attacks table, such as the total alert count, continue to reflect the full set of linked alerts, not only the filtered subset.

## Take actions on an attack [attacks-manage]

Access actions from the **Take actions** menu on an attack's row in the Attacks table.

:::{note}
When you change an attack's status, assign or unassign it, or apply attack tags, a modal lets you apply the action to the attack only, or to both the attack and its associated alerts. This is the same choice available when [changing a discovery's status](/solutions/security/ai/attack-discovery/manage-discoveries-from-attack-discovery-page.md#discovery-status).
:::

| Action | How to do it | Notes |
|--------|--------------|-------|
| Change status | **Take actions** > **Mark as acknowledged** or **Mark as closed** | Status lifecycle matches [discoveries](/solutions/security/ai/attack-discovery/manage-discoveries-from-attack-discovery-page.md#discovery-status): **Open** (default), **Acknowledged**, or **Closed**. |
| Run workflow | **Take actions** > **Run workflow** > select a workflow > **Run workflow** | Requires [workflows prerequisites](/explore-analyze/workflows/get-started.md). You can select only enabled workflows. |
| Assign or unassign | **Take actions** > **Assign attack** or **Unassign attack** | Users are not notified when assigned or unassigned. |
| Apply attack tags | **Take actions** > **Apply attack tags** | Use tags to categorize attacks for filtering. |
| Investigate in timeline | **Take actions** > **Investigate in timeline** | Includes all alerts originally correlated when the attack was created. It does not reflect your current page filters or time range. |
| Add to case | **Take actions** > **Add to new case** or **Add to existing case** | Attaches the attack to a [case](/solutions/security/investigate/security-cases.md). |
| View in AI Chat | **Take actions** > **View in AI Chat** | Continue investigating with an [AI agent](/explore-analyze/ai-features/ai-chat-experiences.md). Ask follow-up questions about the attack or its alerts. |
