---
navigation_title: Custom panels
description: Add custom HTML panels to Kibana dashboards with Liquid templates and ES|QL queries. Generate the panel with Agent Builder chat or write the template yourself.
applies_to:
  stack: preview 9.6+
  serverless: preview
products:
  - id: kibana
type: how-to
---

# Custom panels for {{kib}} dashboards [custom-panels]

With a custom panel, you add layouts to a {{kib}} dashboard that other panel types can't produce: status boards, scorecards with colored badges, branded banners, or blocks that mix text with live values. You describe the panel in {{agent-builder}} chat, or write the HTML and CSS template yourself. To show live data, add an {{esql}} query and place its results in the template with [Liquid](https://liquidjs.com/) tags, a template syntax for inserting values into HTML.

:::{image} /explore-analyze/images/custom-panels-dashboard.png
:alt: Dashboard made of custom panels: a banner with a logo and a mascot, a narrative summary with a health score, four KPI tiles, a Sankey diagram, and two status lists
:screenshot:
:::

## Requirements [custom-panels-requirements]

To add custom panels to a dashboard, you need:

- **All** privilege for the **Dashboard** feature in {{kib}}.
- [{{agent-builder}} set up](/explore-analyze/ai-features/agent-builder/get-started.md) in your deployment, if you want to generate or refine panels with chat. Without it, you can still write templates yourself.
- Data that you can query with {{esql}}, if you want the panel to show live values. If you're new to {{esql}}, refer to [Use {{esql}} in the {{kib}} UI](/explore-analyze/query-filter/languages/esql-kibana.md).

## When to use a custom panel [custom-panels-when-to-use]

Use the panel type that fits your data, and choose a custom panel only when none of the standard types does:

- For standard charts such as time series, bar, pie, metric, or tables, use [Visualizations](lens.md), with or without an [{{esql}} query](esorql.md).
- For scatter plots, small multiples, or layered charts, use [Vega](custom-visualizations-with-vega.md).
- For text without data, use a [Markdown text panel](text-panels.md).
- For any other layout that HTML and CSS can express, use a custom panel. For example:
  - Chart types that aren't available in regular {{kib}} visualizations and are complex to build with Vega, such as flowcharts, Sankey diagrams, or Gantt charts.
  - Tables with conditional formatting more advanced than regular {{kib}} visualization options.
  - Banners with your logo or brand colors. Place the logo as inline SVG in the template and it travels with the dashboard when you export it to another space or deployment. Uploaded [image panels](image-panels.md) lose their files on export.
  - Summary cards that combine several metrics, with badges, thresholds, or CSS-only tabs that switch between views.

When you ask {{agent-builder}} to build a dashboard, the agent follows the same order and creates a custom panel only when nothing else fits.

## How custom panels work [custom-panels-how-they-work]

A custom panel stores two things:

- A **template**: HTML, CSS, and, when the panel has a query, Liquid tags that insert the query results. The template is what renders.
- An optional **{{esql}} query**. When the panel has a query, {{kib}} runs it and fills the template with the results.

When chat generates a panel, it writes the template once, at creation or edit time. Rendering never calls the model again, so the panel loads as fast as any other {{esql}} panel. Templates render in a sandbox that blocks scripts and external resources. For details, refer to [Limitations](#custom-panels-limitations).

## Create a custom panel [custom-panels-create]

A custom panel needs a template and, to show live data, an {{esql}} query. You can write the template yourself or generate it with {{agent-builder}}. Start from the dashboard to add the panel where you want it and work in the flyout. Start from a conversation to let the agent build the panel, or a whole dashboard, for you.

### Start from the dashboard [custom-panels-create-from-dashboard]

1. Open your dashboard in **Edit** mode.
2. Select **Add** in the application menu.
3. Select **Custom** under **Other visualizations**.

   :::{image} /explore-analyze/images/custom-panels-add-flyout.png
   :alt: Add to dashboard flyout with the Custom entry highlighted under Other visualizations
   :screenshot:
   :width: 50%
   :::

   {{kib}} adds an empty panel and opens the **Create custom panel** flyout.

   :::{image} /explore-analyze/images/custom-panels-create-flyout.png
   :alt: Dashboard in edit mode with an empty custom panel that reads Create your custom panel, next to the Create custom panel flyout with the Template (HTML) editor and the Data source (ES|QL) section
   :screenshot:
   :::

4. Provide the template and, optionally, the {{esql}} query that returns the data required by the template. You have several options to define these elements:

   - Manually, in **Template (HTML)** and **Data source (ES|QL)**. For the template syntax, refer to [Write a template](#custom-panels-write-a-template). For the {{esql}} query, refer to [](/explore-analyze/query-filter/languages/esql-kibana.md).
   - Using AI. Select **Generate with chat** and describe the panel. The flyout closes and a conversation opens with the panel attached. When the answer completes, the panel shows the generated template and, for live data, its query. Save the dashboard, or refer to [Refine a custom panel with chat](#custom-panels-refine-with-chat) to adjust the result.

5. If you chose to provide the template and the query manually, select **Preview data** to check the returned columns. The preview shows the first rows of the result.

   You can switch between the template and the query until the column names match.

   If the flyout reports that the query isn't connected to the dashboard time filter, add a `WHERE` clause with the `?_tstart` and `?_tend` parameters on your time field. Refer to [Connect the panel to the time filter](#custom-panels-time-filter).

6. Select **Run preview** to render your draft in the panel without saving it.

   If the query or the template is invalid, the panel shows **Failed to render panel** with the {{esql}} or Liquid error.

7. Select **Apply and close**.

   If you select **Cancel** instead, {{kib}} removes the new panel.

8. Save the dashboard.

The panel now shows your content. If it has a query, change the dashboard time range to confirm that the content updates.

### Start from a conversation [custom-panels-create-with-chat]

1. Open [{{agent-builder}} chat](/explore-analyze/ai-features/agent-builder/chat.md). To add the panel to an existing dashboard, open that dashboard first and select **AI Agent** in the header, which opens the [chat sidebar](/explore-analyze/ai-features/agent-builder/standalone-and-flyout-modes.md#sidebar-mode) with the dashboard attached. From a conversation without a dashboard, the agent creates a new dashboard for the panel.

   You can also select **Add** → **Custom** → **Generate with chat** from an existing dashboard.
2. Describe the panel you want. The agent chooses the panel type and uses a custom panel only when a standard visualization doesn't fit. If you want a custom panel, say so in the prompt by asking for a custom panel or an HTML panel. For example:

   - "Create a custom panel with a health status card for each host."
   - "Create an HTML banner with an animated image."
   - "Create a custom panel that shows how data flows across the services."

3. Review the result. When the panel needs live data, the agent writes the {{esql}} query, samples its results, and generates a template that matches the returned columns. The panel renders on the dashboard, or in the dashboard preview of the conversation.

   :::{image} /explore-analyze/images/custom-panels-sankey-chat.png
   :alt: Dashboard with a Sankey diagram custom panel next to the Agent Builder conversation that created it
   :screenshot:
   :::

4. Save the dashboard, or keep chatting to change the panel.

For saving, previewing, and syncing agent-created dashboards, refer to [Dashboards and visualizations in {{agent-builder}} chat](/explore-analyze/ai-features/agent-builder/agent-builder-dashboards-and-visualizations.md).

## Edit a custom panel [custom-panels-edit]

1. In **Edit** mode, hover over the panel and select {icon}`pencil` **Edit Custom content configuration**.

   The **Edit custom panel** flyout opens with the current template and query.

2. Change the template, the query, or both. Use **Preview data** to check the query results and **Run preview** to render your draft in the panel.

   If you change only the query, {{kib}} fills the existing template with the new results. Make sure the column names in the template match the new query output.

   If the query or the template is invalid, the panel shows **Failed to render panel** with the {{esql}} or Liquid error. Select **Preview data** before you apply to catch query errors early. For a template that chat generated, paste the error into the conversation and the agent corrects the template.

3. Select **Apply and close**, then save the dashboard.

The panel shows the updated content. If you changed the query, change the dashboard time range to confirm that the content updates.

To reuse a template in another panel, select the {icon}`copy` **Copy template** button in the editor to copy it to your clipboard.

## Refine a custom panel with chat [custom-panels-refine-with-chat]

When a panel is attached to a conversation, the agent can change its template and query, and each answer keeps a version you can go back to. To attach a panel, select **Refine with chat** in the **Edit custom panel** flyout. On an empty panel, the button reads **Generate with chat**. A new conversation opens with the panel attached as **Custom content panel**.

1. Describe the panel or the change you want. The agent updates the template, the query, or both, and the panel on the dashboard updates when the answer completes.
2. To go back to an earlier version, select **Preview** on the card of that answer. Each answer adds a card for its version, and the newest version is already applied to the panel. Keep the dashboard open while you do this.
3. Save the dashboard to keep the result.

The panel shows the version you applied last, and that version is what the dashboard saves.

## Write a template [custom-panels-write-a-template]

A template is HTML with inline CSS in `<style>` tags. When the panel has a query, use [Liquid](https://liquidjs.com/) tags to insert the query results. The template receives two variables:

| Variable | Description |
| --- | --- |
| `rows` | One object per result row. Access a column by its exact name in brackets, for example `row["total_revenue"]`. Each column resolves to an object with `.value`, the raw cell value, and `.pct`, the value as a percentage from 0 to 100 of that column's maximum across all rows. `.pct` is set for numeric columns only and is useful for bar widths. |
| `max` | The maximum value of each numeric column, keyed by exact column name, for example `max["total_revenue"]`. |

The following template renders one bar per row for a query that returns `category` and `revenue` columns. The bar width is proportional to the column maximum:

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
- A column that the query doesn't return has no value. Its `.value` and `.pct` render as empty strings, and filters such as `round` turn it into `0`. If the panel shows zeros or full-width bars after a query change, check the column names in the template.
- Missing rows are not an error. Check `rows.size` to render an empty state.

For complete templates with their queries and screenshots, refer to [Custom panel examples](custom-panel-examples.md).

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

When the queried indices have a field named `@timestamp`, the dashboard time filter applies to the query automatically. For any other time field, add a `WHERE` clause with the `?_tstart` and `?_tend` parameters so the query follows the time filter. When a query has neither, the **Data source (ES|QL)** section of the flyout shows a hint. The following query follows the time filter through `my_date_field`:

```esql
FROM my-index
| WHERE my_date_field >= ?_tstart AND my_date_field < ?_tend
| STATS revenue = SUM(amount) BY category
```

For details, refer to [Custom time parameters](/explore-analyze/query-filter/languages/esql-kibana.md#_custom_time_parameters).

## Limitations [custom-panels-limitations]

Custom panels render in a sandbox that protects the dashboard and your browser:

- JavaScript doesn't run. `<script>` tags and inline event handlers have no effect. For interactivity, use CSS only: `:hover` rules for tooltips, or hidden radio inputs with `:checked` rules for tabs.
- Links are removed from the rendered content.
- External resources don't load: no scripts, fonts, or images from URLs. For icons and illustrations, use inline SVG, CSS shapes, or Unicode symbols.
- A template can't exceed 500 KB.
- A panel holds one {{esql}} query.
- You can't save a custom panel to the **Visualize Library**. Custom panels are saved with the dashboard.

## Related pages [custom-panels-related-pages]

- [Custom panel examples](custom-panel-examples.md): complete templates with their queries and screenshots
- [Panels and visualizations](../visualize.md): all panel types you can add to a dashboard
- [Dashboards and visualizations in {{agent-builder}} chat](/explore-analyze/ai-features/agent-builder/agent-builder-dashboards-and-visualizations.md)
- [Create dashboards using AI](/explore-analyze/dashboards/create-dashboards-using-ai.md)
- [Use {{esql}} in the {{kib}} UI](/explore-analyze/query-filter/languages/esql-kibana.md)
- [LiquidJS documentation](https://liquidjs.com/tutorials/intro-to-liquid.html)
