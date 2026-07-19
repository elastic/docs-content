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

<!-- Per docs-content#6949 item 7 (pending), this page is expected to GA and be enabled by default in 9.5 — at that point, update the applies_to tag above (currently preview 9.4) and remove/revise the "Enable alerts and attacks alignment" opt-in callout under Prerequisites below, plus the corresponding entry in configure-advanced-settings.md. Not done here — deferred to a separate PR. -->

The **Attacks** page is the triage hub where you view, filter, assign, tag, and act on all attacks in your environment, alongside their correlated alerts. It pairs with the [**Attack Discovery**](/solutions/security/ai/attack-discovery/attack-discovery.md) page, which is where you manually generate new discoveries using large language models (LLMs):

- Go to **Attack Discovery** to run LLM analysis on demand and create new attack discoveries.
- Go to **Attacks** for day-to-day triage of all attacks (manual and scheduled), and to manage their investigation lifecycle.

You can also schedule recurring Attack Discovery runs from either page; schedules created on one page appear on the other. For guidance on which page to use for your version, refer to [Manage saved discoveries](/solutions/security/ai/attack-discovery/manage-saved-discoveries.md).

## Prerequisites [attacks-prerequisites]

The **Attacks** page requires the same privileges as Attack Discovery. Refer to [Role-based access control (RBAC) for Attack Discovery](/solutions/security/ai/attack-discovery/rbac.md) for details.

:::{important}
To access the Attacks page, you must turn on the [**Enable alerts and attacks alignment**](/solutions/security/get-started/configure-advanced-settings.md#enable-alerts-and-attacks-alignment) setting under **Security Solution** in **Advanced Settings**.
:::

## How it works [attacks-how-it-works]

At the top of the **Attacks** page, you can find overview visualizations and tables. The **Summary** tab shows the total number of attacks detected and attack volume over time, while the **Trends**, **Count**, and **Treemap** tabs all describe alerts associated with these attacks.

::::{image} /solutions/images/security-attacks-page-ov.png
:alt: Overview of the Attacks page showing the Summary tab
:screenshot:
::::

<!-- Per docs-content#6949, 9.5 adds: (1) manually-generated (ad-hoc) attacks integrated into this same unified table alongside scheduled ones — previously only scheduled attacks appeared here; (2) a Run button (triggers an on-demand attack discovery run from this page, with a confirmation notification) and a Settings button (opens the Attack Discovery settings flyout) in the page header, bringing feature parity with the legacy Attack Discovery page. Both belong near this "How it works" section. Content deferred to a separate PR — not included here. -->

Below the summary section, the Attacks table lists individual attacks. You can expand an attack to view details including which entities were involved and which steps of the attack chain were performed.

## Schedule attack discoveries [attacks-schedule-discoveries]

You can schedule Attack Discovery runs directly from the Attacks page. The scheduling flow is the same as on the Attack Discovery page, and schedules you create on either page appear on both. For step-by-step instructions, refer to [Scheduled runs](/solutions/security/ai/attack-discovery/run-from-ui.md#schedule-discoveries).

## Filter and search attacks [attacks-filter-search]

Use the controls at the top of the Attacks table to narrow results:

| Filter method | Description |
|---------------|-------------|
| KQL search | Enter queries in the search bar. Autocomplete includes fields from both attacks and alerts. |
| Date/time picker | Set a specific time range. |
| Status filter | Filter by [status](#change-attack-status): **Open**, **Acknowledged**, or **Closed**. |
| Assignees filter | Click **Filter by assignees** to show only attacks or alerts [assigned](#assign-attacks) to specific users. |
| Sort | Use the **Sort by** menu to sort by **Most recent**, **Least recent**, **Most alerts**, or **Least alerts**. |

<!-- Per docs-content#6949, 9.5 adds a Type filter (Scheduled / Manually generated / both) as a new row in the table above. Type, Connector, and Assignee filter states persist across page reloads, and the "Attacks volume over time" KPI graph respects active filters — note both alongside the new filter. Content deferred to a separate PR — not included here. -->

### View options [attacks-view-options]

Click the **View options** ({icon}`controls`) menu to access the following toggles:

**Show attacks only**: This toggle is enabled by default. It hides standalone alerts (alerts that don't belong to any attack) so you can focus on correlated attack groups. Disable it to see all alerts, including those not linked to any attack.

:::{note}
When **Show attacks only** is disabled, standalone alerts appear in a group labeled `-` (dash). This group acts as a bucket for all alerts that aren't linked to an attack.
:::

**Show anonymized values**: When enabled, replaces attack titles and summaries with anonymized placeholder values. If you're searching the page for specific entities like hostnames or IP addresses, make sure to turn this off.

<!-- Per docs-content#6949, 9.5 adds visual indicators for attack type: scheduled attacks show a calendar icon in the title column and flyout header (clicking opens the schedule details flyout with execution logs and a "Scheduled Attack Discovery" tooltip); manually-generated attacks show the triggering user's avatar in the attack group subtitle ("Detected on [timestamp] | Run by: [avatar]") and in the flyout summary. Add as a new subsection here, alongside View options. Content deferred to a separate PR — not included here. -->

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
When you change an attack's status, assign or unassign it, or apply attack tags, a modal appears that lets you apply the action to the attack only, or to both the attack and its associated alerts — the same choice available when [changing a discovery's status](/solutions/security/ai/attack-discovery/manage-discoveries.md#discovery-status).
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

Attacks use the same [status lifecycle as discoveries](/solutions/security/ai/attack-discovery/manage-discoveries.md#discovery-status): **Open** (default), **Acknowledged**, or **Closed**.

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

<!-- Per docs-content#6949, 9.5 reworks the Alerts tab within an expanded attack's details: all alerts are shown by default regardless of page-level filters; alerts not matching current filters are visually de-emphasized (greyed-out background) instead of hidden; a callout above the alerts table explains this and provides a "Show matching alerts only" toggle; the toggle preference persists across all attacks; attack group statistics always reflect the true total alert count, not the filtered subset. Add as a new section here, since it's about drilling into a specific attack's details. Content deferred to a separate PR — not included here. -->
