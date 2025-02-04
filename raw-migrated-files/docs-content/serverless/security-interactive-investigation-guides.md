# Launch Timeline from investigation guides [security-interactive-investigation-guides]

Detection rule investigation guides suggest steps for triaging, analyzing, and responding to potential security issues. For custom rules, you can create an interactive investigation guide that includes buttons for launching runtime queries in [Timeline](../../../solutions/security/investigate/timeline.md), using alert data and hard-coded literal values. This allows you to start detailed Timeline investigations directly from an alert using relevant data.

:::{image} ../../../images/serverless--detections-ig-alert-flyout.png
:alt: Alert details flyout with interactive investigation guide
:class: screenshot
:::

Under the Investigation section, click **Show investigation guide** to open the **Investigation** tab in the left panel of the alert details flyout.

:::{image} ../../../images/serverless--detections-ig-alert-flyout-invest-tab.png
:alt: Alert details flyout with interactive investigation guide
:class: screenshot
:::

The **Investigation** tab displays query buttons, and each query button displays the number of event documents found. Click the query button to automatically load the query in Timeline, based on configuration settings in the investigation guide.

:::{image} ../../../images/serverless--detections-ig-timeline.png
:alt: Timeline with query pre-loaded from investigation guide action
:class: screenshot
:::


## Add investigation guide actions to a rule [add-ig-actions-rule]

::::{note}
You can only create interactive investigation guides with custom rules because Elastic prebuilt rules can’t be edited. However, you can duplicate a prebuilt rule, then configure the investigation guide for the duplicated rule.

::::


You can configure an interactive investigation guide when you [create a new rule](../../../solutions/security/detect-and-alert/create-detection-rule.md) or [edit an existing rule](../../../solutions/security/detect-and-alert/manage-detection-rules.md#edit-rules-settings).

1. When configuring the rule’s settings (the **About rule** step for a new rule, or the **About*** tab for an existing rule), expand the ***Advanced settings**, then scroll down to the **Investigation guide** Markdown editor.

    :::{image} ../../../images/serverless--detections-ig-investigation-guide-editor.png
    :alt: Investigation guide editor field
    :class: screenshot
    :::

2. Place the editor cursor where you want to add the query button in the investigation guide, then select the Investigate icon in the toolbar. The **Add investigation query** builder form appears.

    ![Add investigation guide UI](../../../images/serverless--detections-ig-investigation-query-builder.png "")

3. Complete the query builder form to create an investigation query:

    1. **Label**: Enter the text to appear on the query button.
    2. **Description**: (Optional) Enter additional text to include with the button.
    3. **Filters**: Select fields, operators, and values to build the query. Click **OR** or **AND** to create multiple filters and define their relationships.

        To use a field value from the alert as a query parameter, enter the field name surrounded by double curly brackets — such as `{{kibana.alert.example}}` — as a custom option for the filter value.

        ![Add investigation guide UI](../../../images/serverless--detections-ig-filters-field-custom-value.png "")

    4. **Relative time range**: (Optional) Select a time range to limit the query, relative to the alert’s creation time.

4. Click **Save changes**. The syntax is added to the investigation guide editor.

    ::::{note}
    If you need to change the query button’s configuration, you can either edit the syntax directly in the editor (refer to the [syntax reference](../../../solutions/security/detect-and-alert/launch-timeline-from-investigation-guides.md#query-button-syntax) below), or delete the syntax and use the query builder form to recreate the query.

    ::::

5. Save and enable the rule.


### Query button syntax [query-button-syntax]

The following syntax defines a query button in an interactive investigation guide.

| Field | Description |
| --- | --- |
| `!{investigate{ }}` | The container object holding all the query button’s configuration attributes. |
| `label` | Identifying text on the button. |
| `description` | Additional text included with the button. |
| `providers` | A two-level nested array that defines the query to run in Timeline. Similar to the structure of queries in Timeline, items in the outer level are joined by an `OR` relationship, and items in the inner level are joined by an `AND` relationship.<br><br>Each item in `providers` corresponds to a filter created in the query builder UI and is defined by these attributes:<br><br>* `field`: The name of the field to query.<br>* `excluded`: Whether the query result is excluded (such as **is not one of**) or included (*is one of*).<br>* `queryType`: The query type used to filter events, based on the filter’s operator. For example, `phrase` or `range`.<br>* `value`: The value to search for. Either a hard-coded literal value, or the name of an alert field (in double curly brackets) whose value you want to use as a query parameter.<br>* `valueType`: The data type of `value`, such as `string` or `boolean`.<br> |
| `relativeFrom`, `relativeTo` | (Optional) The start and end, respectively, of the relative time range for the query. Times are relative to the alert’s creation time, represented as `now` in [date math](https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#date-math) format. For example, selecting **Last 15 minutes** in the query builder form creates the syntax `"relativeFrom": "now-15m", "relativeTo": "now"`. |

::::{note}
Some characters must be escaped with a backslash, such as `\"` for a quotation mark and `\\` for a literal backslash. Divide Windows paths with double backslashes (for example, `C:\\Windows\\explorer.exe`), and paths that already include double backslashes might require four backslashes for each divider. A clickable error icon (![Error](../../../images/serverless-error.svg "")) displays below the Markdown editor if there are any syntax errors.

::::



### Example syntax [security-interactive-investigation-guides-example-syntax]

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

This example creates the following Timeline query, as illustrated below:

`(event.id : <alert value>)` `OR (event.action : "rename" AND process.pid : <alert value>)`

:::{image} ../../../images/serverless--detections-ig-timeline-query.png
:alt: Timeline query
:class: screenshot
:::


### Timeline template fields [security-interactive-investigation-guides-timeline-template-fields]

When viewing an interactive investigation guide in contexts unconnected to a specific alert (such a rule’s details page), queries open as [Timeline templates](../../../solutions/security/investigate/timeline-templates.md), and `parameter` fields are treated as Timeline template fields.

:::{image} ../../../images/serverless--detections-ig-timeline-template-fields.png
:alt: Timeline template
:class: screenshot
:::
