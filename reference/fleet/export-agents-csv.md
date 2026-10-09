---
navigation_title: Export agents to CSV
description: Export a filtered and sorted list of Fleet-managed Elastic Agents to a CSV file, select the columns to include, and download the report from Kibana Reporting.
type: how-to
applies_to:
  stack: ga 9.0+
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Export {{agent}}s to a CSV file [export-agents-csv]

Download the {{fleet}} **Agents** list as a CSV file to share or review it outside {{kib}}. The file includes the agents and columns you select and follows the list's active filters and sort order.

## Before you begin [export-agents-csv-before-you-begin]

You need the following privileges:

* {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` The **Generate reports** {{fleet}} sub-feature privilege, and at least `Read` access for **Agents**. Refer to [{{fleet}} privileges and available actions](/reference/fleet/fleet-roles-privileges.md#fleet-roles-and-privileges-sub-features-table).
* {applies_to}`stack: ga 9.0-9.3` The `read` index privilege for the `.fleet-agents` index.
* [Reporting privileges](/deploy-manage/kibana-reporting-configuration.md#grant-user-access), which let you view and download the generated report.

## Export the agents list [export-agents-csv-steps]

1. In {{kib}}, find **Fleet** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select **Agents**.
2. Optional: Filter and sort the list to match the agents you want to export.
3. Select the agents to export. You cannot select agents on [hosted policies](/reference/fleet/agent-policy.md#agent-policy-types).

   To export every agent that matches the current filters, select the checkbox in the table header to select all rows on the current page, then click **Select everything on all pages**. The link appears when more selectable agents match the filters than fit on one page.

4. From the **Actions** menu, select the export action:
   * {applies_to}`serverless: ga` {applies_to}`stack: ga 9.3+` **Maintenance and diagnostics** → **Export _x_ agents as CSV**
   * {applies_to}`stack: ga 9.0-9.2` **Export _x_ agents as CSV**
5. In the **Download table results as a CSV file** window, select the columns to include, then click **Download CSV**.

   By default, the export includes these columns: **Agent ID**, **Status**, **Host Name**, **Policy ID**, **Last Checkin Time**, and **Agent Version**.

   A **Queued report for CSV** notification confirms that {{kib}} started generating the report.
   
6. Follow the link from the notification, or go to **Reporting** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to track the status of the report.
7. When the status of the **Agent List** report is updated to **Done**, select the {icon}`download` icon in the **Actions** column to download the CSV file.

## Related pages [export-agents-csv-related]

* [{{agent}}s](/reference/fleet/manage-agents.md)
* [Add tags to filter the Agents list](/reference/fleet/filter-agent-list-by-tags.md)
* [{{fleet}} roles and privileges](/reference/fleet/fleet-roles-privileges.md)
* [Configure {{kib}} reporting](/deploy-manage/kibana-reporting-configuration.md)
