---
navigation_title: "ES|QL"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-kibana.html
  - https://www.elastic.co/guide/en/kibana/current/esql.html
description: Overview of the ES|QL editor in Kibana, including query structure, editor tools, AI assistance, time filtering, variables, and query management.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Use ES|QL in the {{kib}} UI [esql-kibana]

The {{esql}} editor lets you write, run, and manage [{{esql}}](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md) queries across {{kib}}. Use it to query and aggregate your data, create visualizations, and set up alerts.

Find the complete list of supported commands, functions, and operators in the [{{esql}} reference](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md).

:::{agent-skill}
:url: https://github.com/elastic/agent-skills/tree/main/skills/elasticsearch/elasticsearch-esql
:::


## Use {{esql}} across {{kib}} [esql-kibana-areas]

Editor support varies by area. Some areas use the {{esql}} editor described on this page, while others provide a task-specific editor or embed {{esql}} in their own editor.

| Area | What you can do | Editing experience |
|------|-----------------|--------------------|
| [Discover](/explore-analyze/discover/try-esql.md) | Explore data, visualize results, and save findings to dashboards | {{esql}} editor |
| [Dashboards and visualizations](/explore-analyze/visualize/esorql.md) | Create visualization panels and interactive controls | {{esql}} editor |
| [Alerting](/explore-analyze/alerting/alerts/rule-type-es-query.md) | Create alerting rules based on {{esql}} queries | {{esql}} editor |
| [{{alerting-v2-system-cap}}](/explore-analyze/alerting/system-overview.md) | Build and preview rules with separate base, alert, and recovery queries | Task-specific editor and YAML editor |
| [Maps](/explore-analyze/visualize/maps.md) {applies_to}`stack: beta` {applies_to}`serverless: beta` | Create map layers from {{esql}} queries | {{esql}} editor |
| [Data Visualizer](/explore-analyze/machine-learning/machine-learning-in-kibana.md) | Explore field statistics from query results | {{esql}} editor |
| [{{agent-builder}}](/explore-analyze/ai-features/agent-builder/tools/esql-tools.md) | Create custom tools that run parameterized queries | Task-specific editor |
| [Streams](/solutions/observability/streams/streams.md) | Define query streams | Task-specific editor |
| [{{elastic-sec}} solution](/solutions/security/esql-for-security.md) | Hunt threats, create detection rules, and investigate events | {{esql}} editor |
| [Dev Tools Console](/explore-analyze/query-filter/tools/console.md) | Run queries through the [{{esql}} REST API](elasticsearch://reference/query-languages/esql/esql-rest.md) | Embedded in the Console editor |
| [Workflows](/explore-analyze/workflows/steps/elasticsearch.md) | Run queries with the `elasticsearch.esql.query` action | Embedded in the YAML editor |
| [Vega visualizations](/explore-analyze/visualize/custom-visualizations-with-vega.md#vega-esql-queries) {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` | Use a query as a visualization data source | Embedded in the specification editor |


## Write queries with the {{esql}} editor [esql-kibana-get-started]


### Query structure [esql-kibana-query-bar]

Every {{esql}} query starts with a [source command](elasticsearch://reference/query-languages/esql/esql-commands.md#esql-source-commands) that retrieves data:

- [`FROM`](elasticsearch://reference/query-languages/esql/commands/source-commands.md#esql-from) allows you to define the data sources to query by specifying data streams, [{{esql}} views](elasticsearch://reference/query-languages/esql/esql-views.md), indices, or aliases.
- [`TS`](elasticsearch://reference/query-languages/esql/commands/ts.md) is optimized for querying time series data streams.
- {applies_to}`stack: preview 9.4` {applies_to}`serverless: preview` [`PROMQL`](elasticsearch://reference/query-languages/esql/commands/promql.md) queries time series data through the {{esql}} editor using [Prometheus Query Language (PromQL)](https://prometheus.io/docs/prometheus/latest/querying/basics/) syntax.

You can then chain one or more [processing commands](elasticsearch://reference/query-languages/esql/esql-commands.md#esql-processing-commands) using pipe (`|`) characters. For example, [`WHERE`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-where) filters rows and [`STATS`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-stats-by) aggregates data:

```esql
FROM kibana_sample_data_logs
| WHERE response.keyword == "200"
| STATS total_bytes = SUM(bytes) BY geo.dest
```

When querying many indices at once without filters, the response might be too large. If you encounter a content length error, use [`DROP`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-drop) or [`KEEP`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-keep) to limit the number of fields returned.

::::{note}
{{esql}} keywords are case-insensitive. `FROM`, `from`, and `From` are all equivalent.
::::


### Editor tools

The {{esql}} editor includes several built-in tools to help you write queries efficiently:

- [Autocomplete and in-app help](#esql-kibana-autocomplete)
- [Query formatting](#_make_your_query_readable)
- [Warnings](#_warnings)
- [Query statistics](#esql-kibana-query-statistics)
- [Keyboard shortcuts](#esql-kibana-keyboard-shortcuts)

#### Autocomplete and in-app help [esql-kibana-autocomplete]

{{esql}} features in-app help, inline suggestions, and an autocomplete menu so you can get started faster and don't have to leave the application to check syntax.

:::{image} /explore-analyze/images/kibana-esql-in-app-help.png
:alt: The ES|QL syntax reference and the autocomplete menu
:screenshot:
:::

{applies_to}`stack: ga 9.4` {applies_to}`serverless: ga` In **Discover**, the editor includes interactive browsers for selecting data sources and field names from the autocomplete menu. Refer to [](/explore-analyze/discover/try-esql.md#discover-esql-resource-browsers) for details.

#### Query formatting [_make_your_query_readable]

For readability, you can put each processing command on a new line and add indentation. Use the {icon}`line_break` **Prettify query** button from the query editor's footer to format your query automatically. You can also adjust the editor's height by dragging its bottom border.

![Automatic line breaks and indentation for ES|QL queries](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/bltb7c28c7b10f58b68/69ebb4e4a7cffb580c9a34c5/prettify-esql.gif "=75%")

#### Warnings [_warnings]

A query might result in warnings, for example when querying an unsupported field type. When that happens, the query bar displays a warning symbol. To see the detailed warning, expand the query bar, and select **warnings**.

#### Query statistics [esql-kibana-query-statistics]
```{applies_to}
stack: ga 9.4
serverless: ga
```

After running a query, the editor's footer displays statistics about the last run, including the number of documents processed. These statistics are available in **Discover** and in **{{esql}} visualizations** in dashboards.

#### Keyboard shortcuts [esql-kibana-keyboard-shortcuts]

| Mac                | Windows/Linux       | Description                 |
|--------------------|---------------------|-----------------------------|
| {kbd}`cmd+enter`   | {kbd}`ctrl+enter`   | Run a query                 |
| {kbd}`cmd+/`       | {kbd}`ctrl+/`       | Comment or uncomment the current line or selected lines |
| {kbd}`cmd+i`       | {kbd}`ctrl+i`       | [Prettify query](#_make_your_query_readable) {applies_to}`stack: ga 9.4+` |
| {kbd}`cmd+j`       | {kbd}`ctrl+j`       | [Generate {{esql}} from a `//` comment](#esql-kibana-ai-comment) {applies_to}`stack: preview 9.5+` |
| {kbd}`cmd+k`       | {kbd}`ctrl+k`       | Open the [search bar](#esql-kibana-quick-search) |

:::{tip}
You can find the list of shortcuts directly from the editor. Look for the ![keyboard](../../images/keyboard.svg "keyboard =2%") icon.
:::


### Build ES|QL queries from KQL syntax [esql-kibana-quick-search]
```{applies_to}
serverless: preview
stack: preview 9.3+
```

The {{esql}} editor includes a search bar that helps you build a query without writing the full {{esql}} syntax. To open it, select the {icon}`magnify` or {icon}`magnify_sparkles` search icon in the editor's toolbar, or press {kbd}`cmd+k` (Mac) or {kbd}`ctrl+k` (Windows/Linux). The search bar offers two modes:

- **KQL**: filter your data with free text or [KQL](kql.md) syntax, as described in this section.
- {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview` **Natural language**: describe the query you want in plain language and let an AI agent generate it for you. Refer to [Generate a full query from natural language](#esql-kibana-quick-search-nl).

The search bar closes automatically when you start typing in the editor or select outside of it.

To filter your data with KQL:

1. Open the editor's search bar ({icon}`magnify` or {icon}`magnify_sparkles`).
2. Select the data sources to search.
3. Type the text you want to search for as free text or using [KQL](kql.md) syntax.
4. Submit your search by pressing {kbd}`enter`. The generated query includes a `FROM` command based on the data sources you selected (or `TS` if the data source is a time series data stream), and a `WHERE KQL()` command that contains the text you typed in the search bar. The query is saved to your [query history](#esql-kibana-query-history) so you can restore it later.
5. Refine your query with any other {{esql}} command or function that you need.

![Search bar in the ES|QL editor](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/bltc3b8614d0ecabbd9/69ebb647065c54efe579b251/esql-quick-search-kql.gif "=60%")


### Write and fix queries with AI [esql-kibana-ai-assistance]
```{applies_to}
stack: preview 9.5+
serverless: preview
```

When your deployment or project has a configured large language model (LLM) connector, {{kib}} can use AI to help you author {{esql}}. The editor uses the same default AI connector as {{kib}}'s other AI features, such as {{agent-builder}}. You don't need to configure a specific connection for the editor.

Choose the entry point that matches what you want to do:

- [**Generate a full query from natural language**](#esql-kibana-quick-search-nl) in the editor's search bar, when you're starting from scratch or want to replace the whole query.
- [**Generate {{esql}} from a comment**](#esql-kibana-ai-comment) to add or change a single pipe inside the query you're writing.
- [**Fix query errors with AI**](#esql-kibana-ai-fix) when a query fails validation.

**Requirements**

- For {{ech}}, {{ece}}, and {{eck}} deployments or self-managed clusters, you need an Enterprise license.
- A configured LLM connector. Refer to [Configure access to LLMs](/explore-analyze/ai-features/llm-guides/llm-connectors.md).

Without these requirements, the AI prompts and actions don't appear and the editor uses only its standard autocomplete behavior. If no connector is available in the search bar, you're prompted to set one up.

#### Generate a full query from natural language [esql-kibana-quick-search-nl]

Not sure how to write an {{esql}} query? Describe what you want from your data in natural language and a specialized AI agent writes the query for you.

1. Open the editor's search bar ({icon}`magnify_sparkles`).
2. From the mode selector, select **Natural language**.
3. In the input, describe the query you want. For example, `Show the average response time per host for the last 24 hours`.
4. Press **Enter** to submit your request. The editor replaces or updates the current query, runs it, and saves it to your [query history](#esql-kibana-query-history).
5. Review the generated query and refine it with any other {{esql}} command or function that you need.

:::{tip}
The current query in the editor is sent to the LLM as context, so you can ask follow-up requests that build on it. For example, after running a generated query, ask `Group the results by region` to extend it.
:::

:::{image} /explore-analyze/images/kibana-esql-search-bar-nl.png
:alt: Natural language mode in the ES|QL editor search bar
:screenshot:
:width: 60%
:::

#### Generate {{esql}} from a comment [esql-kibana-ai-comment]

Write a `//` comment that describes what you want, then press {kbd}`cmd+J` (Mac) or {kbd}`ctrl+J` (Windows/Linux). The editor sends your comment to the AI agent and inserts the generated {{esql}} on the next line.

You can use this to:

- Write a query from scratch when the editor is empty. For example, type `// Show the top 10 destinations by flight count` and press {kbd}`cmd+J` to generate a complete query.
- Add a step to an existing query. Place the comment between pipes (for example `// filter for delayed flights`) and the AI agent generates a single pipe to append. If the AI agent determines that your comment describes a change to the next pipe rather than a new step, it modifies that pipe instead.

As you write, the editor displays inline hints that remind you how to use the feature: on an empty line it suggests starting a `//` comment, and once you've written one it prompts you to press the shortcut. The placeholder in an empty editor conveys the same order: describe what you want in a `//` comment first, then press the shortcut to generate {{esql}} from it.

While the AI agent is generating, a `Generating...` indicator appears next to your comment. Press the shortcut again to cancel the in-flight request and start a new one.

When the generated code is ready, the editor highlights it and shows review actions:

- **Keep** ({kbd}`cmd+shift+enter` on Mac, {kbd}`ctrl+shift+enter` on Windows/Linux) accepts the change and leaves your comment in place so you can refine it and regenerate.
- **Undo** ({kbd}`cmd+shift+backspace` on Mac, {kbd}`ctrl+shift+backspace` on Windows/Linux) removes the generated code.

:::{image} /explore-analyze/images/kibana-esql-generate-from-comment.png
:alt: The ES|QL editor showing a query generated from a comment, highlighted with Keep and Undo review actions
:screenshot:
:width: 50%
:::

When the AI agent rewrites an existing pipe instead of adding one, the original pipe appears with a strikethrough and the **Keep** button becomes **Replace**, indicating that accepting the suggestion removes the original pipe.

#### Fix query errors with AI [esql-kibana-ai-fix]

When your query fails validation, hover over the underlined error in the editor. The error popup includes a **✨ Fix with AI** link. Select it to send the query and the error to the AI agent and have it propose a corrected version.

:::{image} /explore-analyze/images/kibana-esql-fix-with-ai.png
:alt: An ES|QL query error popup showing the Fix with AI link
:screenshot:
:width: 50%
:::

The proposed fix appears directly below your query, with the original lines and the suggested replacement highlighted in different colors. The same review actions as for comment-driven generation apply:

- **Replace** ({kbd}`cmd+shift+enter` on Mac, {kbd}`ctrl+shift+enter` on Windows/Linux) replaces the original lines with the suggested fix.
- **Undo** ({kbd}`cmd+shift+backspace` on Mac, {kbd}`ctrl+shift+backspace` on Windows/Linux) discards the suggestion and restores the original query.

:::{image} /explore-analyze/images/kibana-esql-fix-with-ai-review.png
:alt: An ES|QL editor showing the original lines and the proposed AI fix highlighted in different colors, with Replace and Undo actions
:screenshot:
:width: 50%
:::

:::{tip}
:applies_to: {"stack": "ga 9.5", "serverless": "ga"}
After you run a query in **Discover**, an AI agent can also analyze the results, render a chart of the main finding, and suggest drill-down queries. Refer to [Analyze your data with AI](/explore-analyze/discover/discover-get-started.md#analyze-with-ai).
:::


### Commands with additional editor support

Some {{esql}} commands have dedicated editor features beyond autocomplete, such as in-editor index or policy creation.

#### LOOKUP JOIN command and lookup indices

The {{esql}} editor supports [`LOOKUP JOIN`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-lookup-join) commands and suggests lookup mode indices and join condition fields.

{applies_to}`stack: ga 9.2.0` Remote lookup joins are supported in [cross-cluster queries](elasticsearch://reference/query-languages/esql/esql-cross-clusters.md). The lookup index must exist on _all_ remote clusters being queried, because each cluster uses its local lookup index data.

In **Discover**, LOOKUP JOIN commands let you create or edit lookup indices directly from the editor. Find more information in [](/explore-analyze/discover/try-esql.md#discover-esql-lookup-join).


#### ENRICH command and enrich policies [esql-kibana-enrich]

The {{esql}} [`ENRICH`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-enrich) command enables you to [enrich](elasticsearch://reference/query-languages/esql/esql-enrich-data.md) your query dataset with fields from another dataset. Before you can use `ENRICH`, you need to [create and execute an enrich policy](elasticsearch://reference/query-languages/esql/esql-enrich-data.md#esql-set-up-enrich-policy). If a policy exists, autocomplete suggests it. If not, select **Click to create** to create one.

:::{image} /explore-analyze/images/elasticsearch-reference-esql-kibana-enrich-autocomplete.png
:alt: esql kibana enrich autocomplete
:width: 50%
:::

For detailed steps to create an enrich policy from the editor, refer to [Enrich your data](elasticsearch://reference/query-languages/esql/esql-enrich-data.md).


## Filter by time [esql-kibana-time-filter]

To display data within a specified time range, you can use the standard time filter, custom time parameters, or a WHERE command.


### Standard time filter [_standard_time_filter]

{{kib}} enables the standard [time filter](../filtering.md) when the indices you're querying have a field named `@timestamp`.


### Custom time parameters [_custom_time_parameters]

If your indices do not have a field named `@timestamp`, you can use the `?_tstart` and `?_tend` parameters to specify a time range. These parameters work with any timestamp field and automatically sync with the [time filter](../filtering.md).

```esql
FROM my_index
| WHERE custom_timestamp >= ?_tstart AND custom_timestamp < ?_tend
```

You can also use the `?_tstart` and `?_tend` parameters with the [`BUCKET`](elasticsearch://reference/query-languages/esql/functions-operators/grouping-functions/bucket.md) function to create auto-incrementing time buckets in {{esql}} visualizations. For example:

```esql
FROM kibana_sample_data_logs
| STATS average_bytes = AVG(bytes) BY BUCKET(@timestamp, 50, ?_tstart, ?_tend)
```


### Time ranges with WHERE [_where_command]

You can also limit the time range using the [`WHERE`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-where) command and the [`NOW`](elasticsearch://reference/query-languages/esql/functions-operators/date-time-functions/now.md) function. For example, if the timestamp field is called `timestamp`, to query the last 15 minutes of data:

```esql
FROM kibana_sample_data_logs
| WHERE timestamp > NOW() - 15minutes
```


### Timezone handling [esql-kibana-timezone]
```{applies_to}
stack: ga 9.4
serverless: ga
```

{{esql}} queries use a timezone for date and time functions and time-based filtering. When you run {{esql}} queries in Discover, dashboards, alerting, or Maps, {{kib}} automatically uses the timezone from the **Time zone** (`dateFormat:tz`) [advanced setting](kibana://reference/advanced-settings.md). To change it:

1. Go to **Stack Management** → **Advanced Settings** (or **Management** → **Advanced Settings** in {{serverless-short}}).
2. Search for **Time zone** (`dateFormat:tz`).
3. Set it to **Browser** to use your browser's timezone, or choose a specific timezone such as **UTC** or **America/New_York**.

:::{warning}
Avoid using the {{esql}} [`SET time_zone`](elasticsearch://reference/query-languages/esql/directives/set.md) directive in {{kib}} apps. `SET time_zone` changes how dates are computed by {{es}}, but {{kib}} still displays timestamps following the timezone defined in its `dateFormat:tz` advanced setting, which can produce confusing results.
:::



## Use variables and controls [add-variable-control]

{{esql}} variables help you add interactive controls to your queries and make them more dynamic.

They're available for:
* [Discover queries](/explore-analyze/discover/try-esql.md#add-variable-control) {applies_to}`stack: ga 9.2`
* [{{esql}} visualizations in dashboards](/explore-analyze/visualize/add-variable-controls.md)

:::{include} ../../_snippets/variable-control-procedure.md
:::

:::{include} ../../_snippets/variable-control-examples.md
:::

% Link from the product
### Multi-value variable controls [esql-multi-values-controls]
```{applies_to}
stack: preview 9.3
serverless: preview
```

:::{include} ../../_snippets/multi-value-esql-controls.md
:::


## Manage queries

The {{esql}} editor keeps track of your queries so you can reuse and organize them.

![ES|QL editor query history and starred queries](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt2446c9af9847b87e/69ebb870086ade348a1acc35/esql-recent-starred.gif "=60%")

### Query history [esql-kibana-query-history]

You can reuse your recent {{esql}} queries in the query bar. In the query bar, select **Show recent queries**.

You can then: 
- scroll through your most recent queries
- {applies_to}`stack: ga 9.2` search for specific queries of your history

:::{note}
The maximum number of queries in the history depends on the version you're using:
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2+` The query history can keep up to 50 KB of queries, which represents about 200 large queries, or about 300 short queries.
- {applies_to}`stack: ga 9.0-9.1` The query history keeps your 20 most recent queries.
:::

### Starred queries [esql-kibana-starred-queries]

From the query history, you can mark some queries as favorite to find and access them faster later.

In the query bar, select **Show recent queries**.

From the **Recent** tab, you can star any queries you want.

In the **Starred** tab, find all the queries you have previously starred.


## Define query settings with `SET` [esql-kibana-set]
```{applies_to}
stack: ga 9.4
serverless: ga
```

The [`SET`](elasticsearch://reference/query-languages/esql/directives/set.md) directive lets you configure how {{es}} runs your {{esql}} query. Place one or more `SET` statements at the start of your query, separated by semicolons:

```esql
SET setting_name = setting_value[, ..., settingN = valueN];
<query>
```

The {{esql}} editor autocompletes supported settings and validates their values. Settings particularly useful from {{kib}} include:

- [`approximation`](#approximation-fast-mode): Trade exact results for speed on large `STATS` queries using random sampling. Several {{kib}} apps expose this functionality with a [Fast mode](#approximation-fast-mode) UI option.
- [`project_routing`](#esql-kibana-cps): Limit a [cross-project search](/explore-analyze/cross-project-search.md) to specific projects.
- [`unmapped_fields`](#esql-kibana-unmapped-fields): Choose how to handle fields that are not present in the index mapping.

The `SET` directive also supports a `time_zone` setting. However, to change the timezone used by your {{esql}} queries in {{kib}}, update the `dateFormat:tz` advanced setting rather than using `SET time_zone`. Refer to [Timezone handling](#esql-kibana-timezone) for more information.

For the full list of supported settings and their parameters, refer to the [`SET` directive reference](elasticsearch://reference/query-languages/esql/directives/set.md).


### Search across projects with `SET project_routing` [esql-kibana-cps]
```{applies_to}
serverless: preview
stack: unavailable
```

When [{{cps}}](/explore-analyze/cross-project-search.md) is enabled and you have [linked projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md), you can add [`SET project_routing`](elasticsearch://reference/query-languages/esql/directives/set.md) at the beginning of your {{esql}} query to [override the {{cps}} scope](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md#cps-in-kibana) and target specific projects:

```esql
SET project_routing = "_alias:my_other_project";
FROM logs-*
| WHERE log.level == "error"
| STATS count = COUNT(*) BY service.name
```

The editor autocompletes two built-in values when you type `SET project_routing`:

- `_alias:_origin`: Search only the current (origin) project.
- `_alias:*`: Search all linked projects.

You can use any valid [project routing expression](/explore-analyze/cross-project-search/cross-project-search-project-routing.md), including tag-based and named expressions. For more details on query-level overrides, refer to [Managing {{cps}} scope](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md#cps-query-overrides).


### Handle unmapped fields with `SET unmapped_fields` [esql-kibana-unmapped-fields]
```{applies_to}
stack: preview 9.4
serverless: preview
```

By default, an {{esql}} query fails if it references a field that is not present in the mapping of any searched index. Use [`SET unmapped_fields`](elasticsearch://reference/query-languages/esql/directives/set.md#esql-unmapped_fields) at the start of your query to instead treat unmapped fields as `null` (`NULLIFY`) or load them from `_source` as `keyword` (`LOAD`). For example:

```esql
SET unmapped_fields="NULLIFY";
FROM partial_mapping_sample_data
| KEEP event_duration, unmapped_message
| SORT event_duration
| LIMIT 1
```

The {{esql}} editor autocompletes the setting name and its accepted values. Once `NULLIFY` or `LOAD` is set, unmapped fields referenced in the query are added to autocomplete and treated like other columns. They stop being suggested if you drop or rename them.

The first time a query references an unmapped field, the editor shows a warning so you can confirm the reference is intentional and not a typo. After a `KEEP` or `STATS` command that limits the available columns, references to unmapped fields downstream are flagged as errors.

:::{note}
`LOAD` doesn't work in queries that use `FORK`, `LOOKUP JOIN`, subqueries, views, or full-text search functions. Subfields of `flattened` fields aren't loaded. When querying multiple indices, fields that have a non-keyword type in some indices but are unmapped in others need an explicit cast (for example, `my_field::integer` or `TO_INTEGER(my_field)`) unless referenced in a `KEEP` or `DROP` command.
:::

{applies_to}`stack: preview 9.5` When querying a [wired stream](/solutions/observability/streams/wired-streams.md) and the editor detects an unknown column error, a **Load unmapped fields** quick fix is available. Select it to apply `SET unmapped_fields = "LOAD";` automatically. Refer to [Query unmapped fields](/solutions/observability/streams/wired-streams.md#streams-wired-streams-discover-unmapped) for wired stream–specific details.

For a conceptual overview and use cases, refer to [Unmapped fields](elasticsearch://reference/query-languages/esql/esql-unmapped-fields.md).


## Get faster results with approximate `STATS` [approximation-fast-mode]
```{applies_to}
stack: preview 9.4
serverless: preview
```

On large datasets, you can trade exact results for speed by enabling [approximate results](elasticsearch://reference/query-languages/esql/esql-query-approximation.md) for [`STATS`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-stats-by) queries. Approximation runs your `STATS` aggregations on a sample of the data and extrapolates to estimate results for the full dataset, so the numbers come out close to the exact ones. You can enable approximation in two ways:

- {applies_to}`{stack: "preview 9.5", serverless: "preview"}` From the {{kib}} UI, with [Fast mode](#esql-kibana-fast-mode-toggle).
- From within a query, with the [`SET approximation`](#esql-kibana-approximation) directive.

However you enable it, {{es}} applies approximation only when it actually speeds up the query. When your data is smaller than the sample size (by default around 1 million rows for `STATS ... BY` queries and 100,000 rows for other `STATS` queries), or a filter has already narrowed the results, {{es}} returns exact results instead. Approximation only works with certain aggregations, so functions such as `COUNT_DISTINCT`, `MIN`, `MAX`, and `LAST` always run exactly. Because approximate results are estimates, they can vary between runs and might drop low-frequency groups. For the full conditions and supported functions, refer to [Approximate `STATS` queries](elasticsearch://reference/query-languages/esql/esql-query-approximation.md).

### Use Fast mode [esql-kibana-fast-mode-toggle]
```{applies_to}
stack: preview 9.5
serverless: preview
```

Fast mode is the {{kib}} UI control for {{esql}} approximation. Select the {icon}`bolt` **Fast mode** option to turn it on.

:::{image} /explore-analyze/images/kibana-esql-fast-mode.png
:alt: The Fast mode option turned on in the query bar
:screenshot:
:::

Where it applies depends on the context:

- In [**Discover**](/explore-analyze/discover/try-esql.md), in {{esql}} mode, the button is always available, but **Fast mode** applies only to queries that use exactly one `STATS` command.
- In [**Dashboards**](/explore-analyze/visualize/esorql.md), **Fast mode** applies to the dashboard's {{esql}} visualizations that use one `STATS` command. The option is disabled when the dashboard has no {{esql}} visualizations.

**Fast mode** is preserved when you save or share a dashboard.

To override the toggle for a single query, use the [`SET approximation`](#esql-kibana-approximation) directive.

### Use the `SET approximation` directive [esql-kibana-approximation]
```{applies_to}
stack: preview 9.4
serverless: preview
```

The [`SET approximation`](elasticsearch://reference/query-languages/esql/commands/set.md) directive enables approximation from within a query. It takes precedence over the [Fast mode](#esql-kibana-fast-mode-toggle) toggle, so you can force approximate or exact results for a specific query.

To approximate a `STATS` query with default settings, prepend `SET approximation=true;` to your query:

```esql
SET approximation=true;
FROM kibana_sample_data_logs
| WHERE @timestamp >= NOW()-30d
| STATS total_hits = COUNT(),
        avg_bytes = AVG(bytes)
  BY geo.dest
| SORT total_hits DESC
| LIMIT 5
```

To tune the sample size or turn off confidence intervals, pass a map. For example:

- `SET approximation={"rows":5000000};` increases the sample size from the default.
- `SET approximation={"confidence_level":null};` skips confidence interval computation for additional speedup.

The editor suggests these map parameters as you type.

For supported aggregation functions, output columns, tuning options, and limitations, refer to [Approximate `STATS` queries](elasticsearch://reference/query-languages/esql/esql-query-approximation.md).

### Interpret approximate results [esql-kibana-approximation-columns]

An approximate query returns your usual `STATS` columns, plus two extra columns for each approximated value, where `<column>` is the name of the approximated column (for example, `_approximation_confidence_interval(count)`):

- `_approximation_confidence_interval(<column>)`: The range that the exact value is very likely to fall within (with a 90% confidence level). For example, an estimated count of `769` shown with `[759, 779]` means the exact count is very likely between 759 and 779. A narrower range means a more precise estimate. It's empty when no range can be computed, and zero-width (such as `[769, 769]`) when the result is actually exact.
- `_approximation_certified(<column>)`: Whether the estimate passed the statistical checks behind the confidence interval. `true` means the interval is reliable. `false` means the estimate might still be accurate, but the interval couldn't be fully validated.

{applies_to}`{stack: "preview 9.5", serverless: "preview"}` In [**Discover**](/explore-analyze/discover/try-esql.md), these appear as additional columns in the results table. 

For more details, refer to [Approximate `STATS` queries](elasticsearch://reference/query-languages/esql/esql-query-approximation.md).


## Related pages

- [{{esql}} reference](elasticsearch://reference/query-languages/esql/esql-syntax-reference.md): Complete list of commands, functions, and operators.
- [Using {{esql}} in Discover](/explore-analyze/discover/try-esql.md): Hands-on tutorial and Discover-specific features like result tables, visualizations, and lookup indices.
- [{{esql}} for {{elastic-sec}}](/solutions/security/esql-for-security.md): Use cases and examples for threat hunting and detection rules.
- [{{esql}} visualizations](/explore-analyze/visualize/esorql.md): Create and edit {{esql}}-based visualizations in dashboards.
- [Add variable controls to dashboards](/explore-analyze/visualize/add-variable-controls.md): Add {{esql}}-powered variable controls to dashboards.
- {applies_to}`stack: ga 9.4` {applies_to}`serverless: ga` [Custom Vega visualizations](/explore-analyze/visualize/custom-visualizations-with-vega.md#vega-esql-queries): Use {{esql}} queries as a data source in Vega and Vega-Lite visualizations.
- [Optimize {{esql}} query performance](elasticsearch://reference/query-languages/esql/esql-query-performance.md): Techniques for writing fast queries and identifying slow ones.
