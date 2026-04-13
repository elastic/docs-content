---
navigation_title: The Attacks page
description: "Use the Attacks page to view, triage, and manage correlated attack chains alongside individual alerts in a unified interface."
applies_to:
  stack: preview 9.4
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# Attacks page [attacks-page]

The **Attacks** page provides a dedicated triage and management interface for alerts and [Attack Discovery](/solutions/security/ai/attack-discovery.md) findings. You can use it to schedule Attack Discovery runs, view summary information about attacks and alerts in your environment, triage them, and update their statuses and assignees.


## Prerequisites [attacks-prerequisites]

The **Attacks** page requires the same privileges as Attack Discovery. Refer to [Role-based access control (RBAC) for Attack Discovery](/solutions/security/ai/attack-discovery.md#attack-discovery-rbac) for details.

:::{important}
To access the Attacks page, you must turn on **Enable alerts and attacks alignment** in the **Security Solution** section of **Advanced Settings**.
:::


## How it works [attacks-how-it-works]

At the top of the **Attacks** page, you can find overview visualizations and tables. The **Summary** tab shows the total number of attacks detected and attack volume over time, while the **Trends**, **Count**, and **Treemap** tabs all describe alerts associated with these attacks. 


::::{image} /solutions/images/security-attacks-page-ov.png
:alt: Overview of the Attacks page showing the Summary tab
:screenshot:
::::

:::{note}
The **Attacks** page lets you schedule Attack Discovery runs and view their findings. For ad-hoc, manual Attack Discovery runs, use the **Attack Discovery** page.
:::



## Triage attacks [attacks-triage]

The Attacks table appears under the summary section and lists individual attacks. You can expand an attack to view details including which entities were involved and which steps of the attack chain were performed.


## Filter and search attacks [attacks-filter-search]

Use the controls at the top of the Attacks table to narrow results:

| Filter method | Description |
|---------------|-------------|
| KQL search | Enter queries in the search bar. Autocomplete includes fields from both attacks and alerts. |
| Date/time picker | Set a specific time range. |
| Status filter | Filter by **Open**, **Acknowledged**, or **Closed**. |
| Assignees filter | Click **Filter by assignees** to show only attacks or alerts assigned to specific users. |
| Sort | Use the **Sort by** menu to sort by **Most recent**, **Least recent**, **Most alerts**, or **Least alerts**. |

### View options [attacks-view-options]

Click the **View options** ({icon}`controls`) menu to access the following toggles:

**Show attacks only**: This toggle is enabled by default. It hides standalone alerts (alerts that don't belong to any attack) so you can focus on correlated attack groups. Disable it to see all alerts, including those not linked to any attack.

:::{note}
When **Show attacks only** is disabled, standalone alerts appear in a group labeled `-` (dash). This group acts as a bucket for all alerts that aren't linked to an attack.
:::

**Show anonymized values**: When enabled, replaces attack titles and summaries with anonymized placeholder values. If you're searching the page for specific entities like hostnames or IP addresses, make sure to turn this off.

### How filtering works on the Attacks page [attacks-filtering-behavior]

The **Attacks** page uses a single data view that combines both the attacks index and the alerts index. This enables powerful cross-entity filtering, but it also means that filters apply to both entity types simultaneously. 

:::{dropdown} Filtering behavior details

**Timeframe filtering**: An attack group appears if either the attack itself or any of its related alerts fall within the selected time range. If the attack is within the time range but all its alerts are outside of it, the attack renders but shows 0 alerts when expanded. Conversely, if the attack is outside the time range but some of its alerts are inside, the attack still appears.

**Alert-specific field filters**: Filtering on a field that only exists on alert documents (not attack documents) excludes attack documents from the underlying dataset. Attack groups still appear, but group statistics and sorting may be affected.

**Attack-specific field filters**: Filtering on a field that only exists on attack documents (for example, the connector that generated an attack) hides all related alerts from the dataset. The attack group appears, but expanding it shows 0 alerts because the alert documents don't contain the attack-specific field.

**Status filter**: The status filter evaluates both attacks and their related alerts. A closed attack can still appear when you filter by **Open** status if it has underlying open alerts that match the filter.

**Assignees filter**: The assignees filter applies across both attacks and alerts. Filtering by assigned user may hide an attack's alerts if those alerts have a different assignee.

**Sorting by timestamp**: Sorting evaluates all visible documents in a group. If an alert-specific query filters out an attack document, the group's position in the sort order is based solely on the timestamps of its remaining alerts.

**KQL autocomplete**: The KQL autocomplete shows fields from both attacks and alerts. Be cautious when filtering, because using a field exclusive to one entity type filters out the other type from the underlying data.

**Alerts count badge**: The **Alerts: N** badge on each attack group counts only detection alerts that match the current filters — it doesn't include the attack document itself. When you expand a group, the badge may show a format like `2/10`, where the first number is the count of alerts matching your current filters and time range, and the second is the total number of alerts historically linked to the attack.

:::


## Manage attacks [attacks-manage]

Access actions from the **Take actions** menu on an attack's row in the Attacks table.

| Action | Description |
|--------|-------------|
| [Change status](#change-attack-status) | Mark as acknowledged or closed |
| [Run workflow](#run-workflow-from-attack) | Run an Elastic workflow for on-demand response or investigation |
| [Assign or unassign attack](#assign-attacks) | Assign analysts to investigate |
| [Apply attack tags](#apply-attack-tags) | Categorize attacks for filtering |
| [Investigate in timeline](#attacks-investigate-timeline) | Open the attack in Timeline for analysis |
| [Add to case](#attacks-add-to-case) | Attach the attack to a new or existing case |
| [View in AI Assistant](#attacks-view-in-ai-assistant) | Continue investigating with the AI Assistant |

### Change attack status [change-attack-status]

Attack statuses track investigation progress:

| Status | Meaning |
|--------|---------|
| Open | Needs investigation (default) |
| Acknowledged | Under active investigation |
| Closed | Resolved |

To change an attack's status, click **Take actions** on the attack row, then select **Mark as acknowledged** or **Mark as closed**.

To take bulk actions on multiple attacks, select the checkboxes next to each attack, then click **Selected *x* attacks** and choose the status you want to apply.

### Run a workflow from an attack [run-workflow-from-attack]

You can run an [Elastic workflow](/explore-analyze/workflows.md) directly from an attack to trigger an on-demand response or investigation. To use this feature, make sure you meet the [workflows prerequisites](/explore-analyze/workflows/get-started.md#workflows-prerequisites).

To run a workflow, click **Take actions** on the attack row, then click **Run workflow**. Use the search bar to select a workflow, then click **Run workflow**.

:::{note}
You can select only enabled workflows.
:::

### Assign or unassign attacks [assign-attacks]

Assign analysts to attacks they should investigate.

| Task | How to do it |
|------|--------------|
| Assign to a single attack | **Take actions** > **Assign attack** > select users |
| Assign to multiple attacks | Select attacks > **Selected *x* attacks** > **Assign attack** |
| Unassign from a single attack | **Take actions** > **Unassign attack** |

:::{important}
Users are not notified when assigned or unassigned.
:::

### Apply attack tags [apply-attack-tags]

Tags help organize attacks into filterable categories.

| Task | How to do it |
|------|--------------|
| Tag a single attack | **Take actions** > **Apply attack tags** |
| Tag multiple attacks | Select attacks > **Selected *x* attacks** > **Apply attack tags** |

### Investigate in timeline [attacks-investigate-timeline]

To open an attack in [Timeline](/solutions/security/investigate/timeline.md), click **Take actions** on the attack row, then select **Investigate in timeline**.

:::{note}
Investigating an attack in Timeline includes all alerts that were originally correlated when the attack was created. It doesn't reflect your current page filters or selected time range.
:::

### Add to case [attacks-add-to-case]

To add an attack to a [case](/solutions/security/investigate/security-cases.md), click **Take actions**, then select **Add to new case** or **Add to existing case**.

### View in AI Chat [attacks-view-in-ai-assistant]

To continue investigating an attack with an AI agent, click **Take actions**, then select **View in AI Chat**. You can ask follow-up questions about the attack or its associated alerts.


## Next steps [attacks-next-steps]

- [Learn about Attack Discovery](/solutions/security/ai/attack-discovery.md)
- [Investigate threats with Timeline](/solutions/security/investigate/timeline.md)
- [Manage security cases](/solutions/security/investigate/security-cases.md)
