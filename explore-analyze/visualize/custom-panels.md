---
navigation_title: Custom panels
description: Add custom panels to Kibana dashboards from HTML, CSS, and Liquid templates with optional ES|QL data. Generate them with Agent Builder chat or write them yourself.
applies_to:
  stack: preview 9.6+
products:
  - id: kibana
---

# Custom panels [custom-panels]

With a custom panel, you add layouts to a dashboard that other panel types can't produce: status boards, scorecards with colored badges, banners with illustrations, or blocks that mix text with live values. You describe the panel in {{agent-builder}} chat, or write the HTML and CSS template yourself.

To show live data, add an {{esql}} query and place its results in the template with [Liquid](https://liquidjs.com/) tags. {{kib}} runs the query each time the panel renders and fills the template with the results. The panel follows the dashboard time filter, queries, filters, and controls like any other {{esql}} panel.

## Requirements [custom-panels-requirements]

To add custom panels to a dashboard, you need:

- **All** privilege for the **Dashboard** feature in {{kib}}.
- {{agent-builder}} [set up](/explore-analyze/ai-features/agent-builder/get-started.md) in your deployment, if you want to generate or refine panels with chat. Without it, you can still write templates yourself.
- Data that you can query with {{esql}}, if you want the panel to show live values. If you're new to {{esql}}, refer to [Use {{esql}} in the {{kib}} UI](/explore-analyze/query-filter/languages/esql-kibana.md).

## When to use a custom panel [custom-panels-when-to-use]

Start with the panel type that fits your data, and reach for a custom panel only when none of them does:

- For standard charts such as time series, bar, pie, metric, or tables, use [Lens](lens.md), with or without an [{{esql}} query](esorql.md).
- For scatter plots, small multiples, or layered charts, use [Vega](custom-visualizations-with-vega.md).
- For text without data, use a [Markdown text panel](text-panels.md).
- For any other layout that HTML and CSS can express, use a custom panel.

When you ask {{agent-builder}} to build a dashboard, the agent follows the same order. It creates a custom panel only when nothing else fits, or when you explicitly ask for a custom or HTML panel.

## How custom panels work [custom-panels-how-they-work]

A custom panel stores two things:

- A **template**: HTML, CSS, and, when the panel has a query, Liquid tags that insert the query results. The template is what renders.
- An optional **{{esql}} query**. When the panel has a query, {{kib}} runs it and fills the template with the results.

When chat generates a panel, it writes the template once, at creation or edit time. Rendering never calls the model again, so the panel loads as fast as any other {{esql}} panel. Templates render in a sandbox that blocks scripts and external resources. For details, refer to [Limitations](#custom-panels-limitations).

Custom panels are saved with the dashboard.

## Create a custom panel with chat [custom-panels-create-with-chat]

1. Open [{{agent-builder}} chat](/explore-analyze/ai-features/agent-builder/chat.md). If you open the chat from a dashboard, that dashboard is attached to the conversation automatically.
2. Describe the panel you want. To force the panel type, ask for a custom or HTML panel. For example:

   - "Create a health status card for each host."
   - "Create a banner with an animated image."
   - "Show how data flows across the services."

3. Review the result. When the panel needs live data, the agent writes the {{esql}} query, samples its results, and generates a template that matches the returned columns. The panel renders in the dashboard preview.
4. Save the dashboard, or keep chatting to change the panel.

For saving, previewing, and syncing agent-created dashboards, refer to [Dashboards and visualizations in {{agent-builder}} chat](/explore-analyze/ai-features/agent-builder/agent-builder-dashboards-and-visualizations.md).

## Add a custom panel from the dashboard [custom-panels-create-from-dashboard]

1. Open your dashboard in **Edit** mode.
2. Select **Add** in the application menu and, if required, **New panel**. Then select **Custom**.

   {{kib}} adds an empty panel and opens the **Create custom panel** flyout.

3. Fill the panel in one of two ways:

   - Select **Generate with chat** to describe the panel in {{agent-builder}} chat. The flyout closes and a new conversation opens with the panel attached. Refer to [Generate or refine a custom panel with chat](#custom-panels-refine-with-chat).
   - Write the template yourself in **Template (HTML)**, then continue with the following steps. Refer to [Write a template](#custom-panels-write-a-template) for the syntax.

4. Optional: to show live data, expand **Data source (ES|QL)** and enter a query. Select **Preview data** to check the returned columns. The preview shows the first rows of the result.

   You can switch between the template and the query until the column names match.

   If the flyout reports that the query isn't connected to the dashboard time filter, add a `WHERE` clause with the `?_tstart` and `?_tend` parameters. Refer to [Connect the panel to the time filter](#custom-panels-time-filter).

5. Select **Run preview** to render your draft in the panel without saving it.
6. Select **Apply and close**.

   If you select **Cancel** instead, {{kib}} removes the new panel.

7. Save the dashboard.

The panel now shows your content. If it has a query, change the dashboard time range to confirm that the content updates.

## Edit a custom panel [custom-panels-edit]

1. In **Edit** mode, open the {icon}`boxes_vertical` panel menu and select **Edit Custom content configuration**.

   The **Edit custom panel** flyout opens with the current template and query.

2. Change the template, the query, or both. Use **Preview data** to check the query results and **Run preview** to render your draft in the panel.

   If you change only the query, {{kib}} fills the existing template with the new results. Make sure the column names in the template match the new query output.

3. Select **Apply and close**, then save the dashboard.

The panel shows the updated content. If you changed the query, change the dashboard time range to confirm that the content updates.

To reuse a template in another panel, select the {icon}`copy` **Copy template** button in the editor to copy it to your clipboard.

## Generate or refine a custom panel with chat [custom-panels-refine-with-chat]

You can hand a new or existing panel to {{agent-builder}} instead of writing the template yourself:

1. In the **Edit custom panel** flyout, select **Refine with chat**. On an empty panel, the button reads **Generate with chat**. If you already selected it while adding the panel, skip this step.

   A new conversation opens with the panel attached as **Custom content panel**.

2. Describe the panel or the change you want. The agent updates the template, the query, or both, and the panel on the dashboard updates when the answer completes.
3. Select **Preview** on a version card to apply that version to the panel. Each answer adds a card for the new version, so you can move back and forth between versions. Keep the dashboard open while you do this.
4. Save the dashboard to keep the result.

## Write a template [custom-panels-write-a-template]

A template is HTML with inline CSS in `<style>` tags. When the panel has a query, use [Liquid](https://liquidjs.com/) tags to insert the query results. The template receives two variables:

| Variable | Description |
| --- | --- |
| `rows` | One object per result row. Access a column by its exact name in brackets, for example `row["total_revenue"]`. Each column resolves to an object with `.value`, the raw cell value, and `.pct`, the value as a percentage from 0 to 100 of that column's maximum across all rows. `.pct` is set for numeric columns only and is useful for bar widths. |
| `max` | The maximum value of each numeric column, keyed by exact column name, for example `max["total_revenue"]`. |

The following template renders one bar per row, with the bar width proportional to the column maximum:

```html
<style>
  .row { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
  .bar { height: 16px; background: var(--cc-color-primary); }
</style>
{% if rows.size == 0 %}<p>No data for the selected time range.</p>{% endif %}
{% for row in rows %}
  <div class="row">
    <span>{{ row["category"].value }}</span>
    <div class="bar" style="width: {{ row["revenue"].pct }}%"></div>
    <span>{{ row["revenue"].value | round: 2 }}</span>
  </div>
{% endfor %}
```

Keep the following in mind when you write templates:

- Grouping, sorting, and aggregation must happen in the {{esql}} query, for example with `STATS ... BY`. The template receives the rows exactly as the query returns them.
- A column that the query doesn't return renders as an empty string.
- Missing rows are not an error. Check `rows.size` to render an empty state.

### Match the {{kib}} theme [custom-panels-theme]

{{kib}} injects the following CSS custom properties into every custom panel. Use them instead of hard-coded colors so the panel follows the light or dark theme without reloading its data.

| Property | Use for |
| --- | --- |
| `--cc-color-text` | Text |
| `--cc-color-background` | Panel background |
| `--cc-color-surface` | Card and container backgrounds |
| `--cc-color-primary` | Primary accent |
| `--cc-color-accent` | Secondary accent |
| `--cc-color-accent-2` | Additional accent |
| `--cc-color-warning` | Warning states |
| `--cc-color-danger` | Error and danger states |
| `--cc-color-border` | Borders |

There is no dedicated property for a healthy or success state. For a three-state status board, pick one of the accent properties for the healthy state, or set your own color.

## Dashboard interactions [custom-panels-dashboard-interactions]

When a custom panel has a query, it responds to the dashboard like other {{esql}} panels:

- The time filter. Refer to [Connect the panel to the time filter](#custom-panels-time-filter).
- The query bar and filter pills. The query fields are also available for suggestions in the query bar and filter editor.
- [Controls](dashboard-controls.md), including [{{esql}} variable controls](add-variable-controls.md).
- [Fast mode](/explore-analyze/query-filter/languages/esql-kibana.md#esql-kibana-fast-mode-toggle) for approximate `STATS` results.

A panel without a query renders the same content regardless of the dashboard state.

### Connect the panel to the time filter [custom-panels-time-filter]

When the queried indices have a default time field, the dashboard time filter applies to the query automatically. When {{kib}} can't detect a time field, the **Data source (ES|QL)** section of the flyout shows a hint. In that case, add a `WHERE` clause with the `?_tstart` and `?_tend` parameters so the query follows the time filter:

```esql
FROM my-index
| WHERE my_date_field >= ?_tstart AND my_date_field < ?_tend
| STATS revenue = SUM(amount) BY category
```

For details, refer to [Custom time parameters](/explore-analyze/query-filter/languages/esql-kibana.md#_custom_time_parameters).

## Limitations [custom-panels-limitations]

Custom panels render in a sandbox that protects the dashboard and your browser:

- JavaScript doesn't run. `<script>` tags and inline event handlers have no effect. For hover effects such as tooltips, use CSS `:hover` rules.
- Links are removed from the rendered content.
- External resources don't load: no scripts, fonts, or images from URLs. For icons and illustrations, use inline SVG, CSS shapes, or Unicode symbols.
- A template can't exceed 500 KB.
- A panel holds one {{esql}} query.
- You can't save a custom panel to the **Visualize Library**. Custom panels are saved with the dashboard.

## Related pages [custom-panels-related-pages]

- [Panels and visualizations](../visualize.md): all panel types you can add to a dashboard
- [Dashboards and visualizations in {{agent-builder}} chat](/explore-analyze/ai-features/agent-builder/agent-builder-dashboards-and-visualizations.md)
- [Create dashboards using AI](/explore-analyze/dashboards/create-dashboards-using-ai.md)
- [Use {{esql}} in the {{kib}} UI](/explore-analyze/query-filter/languages/esql-kibana.md)
- [LiquidJS documentation](https://liquidjs.com/tutorials/intro-to-liquid.html)
