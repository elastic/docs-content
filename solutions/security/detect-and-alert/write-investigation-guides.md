---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/interactive-investigation-guides.html
  - https://www.elastic.co/guide/en/serverless/current/security-interactive-investigation-guides.html
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Create Markdown investigation guides with Timeline and Osquery buttons to help analysts triage and respond to alerts.
---

# Write investigation guides [security-interactive-investigation-guides]

Investigation guides are Markdown documents attached to detection rules that help analysts triage, analyze, and respond to alerts. A well-written guide reduces mean time to respond by giving analysts the context and queries they need without leaving the alert details flyout.

You author an investigation guide in the **Investigation guide** Markdown editor, which is available in the rule's [advanced settings](/solutions/security/detect-and-alert/rule-settings-reference.md#rule-ui-advanced-params) (under the **About** step when creating a rule, or the **About** tab when editing one). The guide renders in the **Investigation** tab of the alert details flyout whenever an analyst opens an alert produced by that rule.

:::{image} /solutions/images/security-ig-alert-flyout.png
:alt: Alert details flyout with investigation guide
:screenshot:
:::

::::{note}
You can only author investigation guides for custom rules. Elastic prebuilt rules include their own investigation guides that cannot be edited. To customize a prebuilt rule's guide, duplicate the rule first, then edit the duplicate.
::::

## Supported Markdown syntax [ig-markdown-syntax]

The investigation guide editor supports standard Markdown with several extensions. Use the toolbar above the editor for quick formatting, or write the syntax directly.

| Syntax | Result |
|---|---|
| `# Heading` | Section heading (levels 1–6) |
| `**bold**` | **Bold text** |
| `*italic*` | *Italic text* |
| `` `code` `` | Inline code |
| `[text](url)` | Hyperlink |
| `- item` | Unordered list |
| `1. item` | Ordered list |
| `> quote` | Block quote |
| `---` | Horizontal rule |
| `![alt](url)` | Image |
| ` ``` ` | Fenced code block |
| `\| col \| col \|` | Table |

::::{tip}
Use Markdown headings to break the guide into clear sections (for example, **Triage**, **Analysis**, **Response**) so analysts can scan quickly.
::::

## Best practices for alert triage [ig-best-practices]

Effective investigation guides share several characteristics:

**Start with context, not commands.** Open with a one- or two-sentence summary of what the rule detects and why it matters. Analysts who understand the threat make better decisions.

**Structure the guide around a workflow.** Organize content into sequential sections:

1. **Triage.** Quick checks to confirm whether the alert is a true positive. Include field values to inspect and known false-positive conditions.
2. **Analysis.** Deeper investigation steps such as Timeline queries, Osquery lookups, and correlated data sources.
3. **Response.** Recommended actions if the alert is confirmed, including escalation paths and containment steps.

**Reference alert fields directly.** Use double curly brackets (for example, `{{host.name}}`, `{{user.name}}`) to surface dynamic alert data in Timeline query buttons, making the guide immediately actionable.

**Keep it scannable.** Use bullet lists, bold key terms, and short paragraphs. Analysts read investigation guides under time pressure.

**Link to related resources.** Include links to relevant dashboards, runbooks, or external threat intelligence references so analysts don't have to search for them.

## Timeline query buttons [add-ig-actions-rule]

You can embed interactive query buttons that open pre-populated [Timeline](/solutions/security/investigate/timeline.md) investigations directly from an alert. Each button runs a query using alert field values and hard-coded literals, and displays the number of matching event documents.

:::{image} /solutions/images/security-ig-alert-flyout-invest-tab.png
:alt: Alert details flyout with interactive investigation guide
:screenshot:
:::

Click a query button to load the query in Timeline automatically.

:::{image} /solutions/images/security-ig-timeline.png
:alt: Timeline with query pre-loaded from investigation guide action
:screenshot:
:::

### Add a Timeline query button [add-timeline-query-button]

1. Open the **Investigation guide** Markdown editor (in the rule's **Advanced settings**).

    :::{image} /solutions/images/security-ig-investigation-guide-editor.png
    :alt: Investigation guide editor field
    :screenshot:
    :::

2. Place the cursor where you want the button to appear, then select the Investigate icon (![Investigate icon](/solutions/images/security-ig-investigate-icon.png "title =20x20")) in the toolbar. The **Add investigation query** builder form appears.

    :::{image} /solutions/images/security-ig-investigation-query-builder.png
    :alt: Add investigation guide UI
    :screenshot:
    :::

3. Complete the form:

    1. **Label**: Text displayed on the button.
    2. **Description**: (Optional) Additional text shown with the button.
    3. **Filters**: Select fields, operators, and values to build the query. Click **OR** or **AND** to create multiple filters and define their relationships.

        To use a field value from the alert as a query parameter, enter the field name surrounded by double curly brackets (for example, `{{kibana.alert.example}}`) as a custom option for the filter value.

        :::{image} /solutions/images/security-ig-filters-field-custom-value.png
        :alt: Custom filter value using alert field
        :screenshot:
        :::

    4. **Relative time range**: (Optional) A time range that limits the query relative to the alert's creation time.

4. Click **Save changes**. The syntax is added to the editor.

    ::::{note}
    To modify a query button, either edit the syntax directly in the editor (refer to the [syntax reference](/solutions/security/detect-and-alert/write-investigation-guides.md#query-button-syntax) below) or delete the syntax and recreate it using the builder form.
    ::::

5. Save and enable the rule.

### Query button syntax [query-button-syntax]

The following syntax defines a query button in an investigation guide.

| Field | Description |
|---|---|
| `!{investigate{ }}` | The container object holding all the query button's configuration attributes. |
| `label` | Identifying text on the button. |
| `description` | Additional text included with the button. |
| `providers` | A two-level nested array that defines the query to run in Timeline. Items in the outer level are joined by an `OR` relationship, and items in the inner level are joined by an `AND` relationship. Each item is defined by these attributes: `field` (field name), `excluded` (whether the result is excluded), `queryType` (filter operator, such as `phrase` or `range`), `value` (a literal value or an alert field name in double curly brackets), and `valueType` (data type such as `string` or `boolean`). |
| `relativeFrom`, `relativeTo` | (Optional) The start and end of a relative time range for the query. Times are relative to the alert's creation time, represented as `now` in [date math](elasticsearch://reference/elasticsearch/rest-apis/common-options.md#date-math) format. For example, `"relativeFrom": "now-15m", "relativeTo": "now"`. |

::::{note}
Some characters must be escaped with a backslash, such as `\"` for a quotation mark and `\\` for a literal backslash. Divide Windows paths with double backslashes (for example, `C:\\Windows\\explorer.exe`), and paths that already include double backslashes might require four backslashes for each divider. A clickable error icon (![Error icon](/solutions/images/security-ig-error-icon.png "title =20x20")) displays below the Markdown editor if there are any syntax errors.
::::

### Example [ig-timeline-example]

```json
!{investigate{
  "label": "Test action",
  "description": "Click to investigate.",
  "providers": [
    [
      {"field": "event.id", "excluded": false, "queryType": "phrase", "value": "{{event.id}}", "valueType": "string"}
    ],
    [
      {"field": "event.action", "excluded": false, "queryType": "phrase", "value": "rename", "valueType": "string"},
      {"field": "process.pid", "excluded": false, "queryType": "phrase", "value": "{{process.pid}}", "valueType": "string"}
    ]
  ],
  "relativeFrom": "now-15m",
  "relativeTo": "now"
}}
```

This creates the following Timeline query:

`(event.id : <alert value>)`<br> `OR (event.action : "rename" AND process.pid : <alert value>)`

:::{image} /solutions/images/security-ig-timeline-query.png
:alt: Timeline query
:screenshot:
:::

### Timeline template fields [ig-timeline-template-fields]

When viewing an investigation guide outside the context of a specific alert (such as on a rule's details page), queries open as [Timeline templates](/solutions/security/investigate/timeline-templates.md), and parameter fields are treated as Timeline template fields.

:::{image} /solutions/images/security-ig-timeline-template-fields.png
:alt: Timeline template
:screenshot:
:::

## Osquery buttons [ig-osquery-syntax]

You can embed Osquery buttons that let analysts run live queries against {{agent}}s directly from the investigation guide. This is useful for gathering host-level context, such as running processes, installed software, or open network connections, while triaging an alert.

::::{admonition} Requirements
* The [Osquery manager integration](/solutions/security/investigate/manage-integration.md) must be installed.
* {{agent}}'s [status](/reference/fleet/monitor-elastic-agent.md) must be `Healthy`. Refer to [](/troubleshoot/ingest/fleet/common-problems.md) if it isn't.
* In {{stack}}, your role must have [Osquery feature privileges](/solutions/security/investigate/osquery.md).
* In {{serverless-short}}, you must have the appropriate user role.
::::

:::{image} /solutions/images/security-osquery-investigation-guide.png
:alt: A live query in an investigation guide
:screenshot:
:::

### Add an Osquery button [add-osquery-button]

1. Open the **Investigation guide** Markdown editor (in the rule's **Advanced settings**).
2. In the toolbar, click the **Osquery** button (![Osquery button](/solutions/images/security-osquery-button.png "title =20x20")).

    1. Add a descriptive label (for example, `Search for executables`).
    2. Select a saved query or enter a new one.

        ::::{tip}
        Use [placeholder fields](/solutions/security/investigate/use-placeholder-fields-in-osquery-queries.md) to dynamically add existing alert data to your query.
        ::::

    3. Expand the **Advanced** section to set a timeout period for the query and view or set [mapped ECS fields](/solutions/security/investigate/osquery.md#osquery-map-fields) included in the results (optional).

        ::::{note}
        Overwriting the query's default timeout period allows you to support queries that take longer to run. The default and minimum supported value for the **Timeout** field is `60`. The maximum supported value is `86400` (24 hours).
        ::::

        :::{image} /solutions/images/security-setup-osquery-investigation-guide.png
        :alt: Setting up an Osquery investigation guide query
        :screenshot:
        :::

3. Click **Save changes** to add the query to the rule's investigation guide.

### Run an Osquery from an investigation guide [run-osquery-from-ig]

1. Open an alert's details flyout and go to the **Investigation** tab.
2. Click the Osquery button. The **Run Osquery** pane opens with the **Query** field autofilled.

    1. Select one or more {{agent}}s or groups to query. Start typing in the search field to get suggestions for {{agent}}s by name, ID, platform, and policy.
    2. (Optional) Expand the **Advanced** section to set a timeout period and view or set [mapped ECS fields](/solutions/security/investigate/osquery.md#osquery-map-fields).

3. Click **Submit** to run the query. Results display in the flyout.

    ::::{note}
    Refer to [Examine Osquery results](/solutions/security/investigate/examine-osquery-results.md) for more about query results.
    ::::

4. (Optional) Click **Save for later** to save the query for future use.

    :::{image} /solutions/images/security-run-query-investigation-guide.png
    :alt: Results from running an Osquery query from an investigation guide
    :screenshot:
    :::

For the complete Osquery reference, refer to [Run Osquery from investigation guides](/solutions/security/investigate/run-osquery-from-investigation-guides.md).
