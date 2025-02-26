---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/runtime-fields.html
---

# Create runtime fields in Elastic Security [runtime-fields]

Runtime fields are fields that you can add to documents after you’ve ingested your data. For example, you could combine two fields and treat them as one, or perform calculations on existing data and use the result as a separate field. Runtime fields are evaluated when a query is run.

You can create a runtime field and add it to your detection alerts or events from any page that lists alerts or events in a data grid table, such as **Alerts**, **Timelines**, **Hosts**, and **Users**. Once created, the new field is added to the current [data view](/solutions/security/get-started/data-views-elastic-security.md) and becomes available to all {{elastic-sec}} alerts and events in the data view.

::::{note}
Runtime fields can impact performance because they’re evaluated each time a query runs. Refer to [Runtime fields](/manage-data/data-store/mapping/runtime-fields.md) for more information.
::::


To create a runtime field:

1. Go to a page that lists alerts or events (for example, **Alerts** or **Timelines** → **Name of Timeline**).
2. Do one of the following:

    * In the Alerts table, click the **Fields** toolbar button in the table’s upper-left. From the **Fields** browser, click **Create field**. The **Create field** flyout opens.

        :::{image} ../../../images/security-fields-browser.png
        :alt: Fields browser
        :class: screenshot
        :::

    * In Timeline, go to the bottom of the sidebar, then click **Add a field**. The **Create field** flyout opens.

        :::{image} ../../../images/security-create-runtime-fields-timeline.png
        :alt: Create runtime fields button in Timeline
        :class: screenshot
        :::

3. Enter a **Name** for the new field.
4. Select a **Type** for the field’s data type.
5. Turn on the **Set value** toggle and enter a [Painless script](/explore-analyze/scripting/modules-scripting-painless.md) to define the field’s value. The script must match the selected **Type**. For more on adding fields and Painless scripting examples, refer to [Explore your data with runtime fields](/explore-analyze/find-and-organize/data-views.md#runtime-fields).
6. Use the **Preview** to help you build the script so it returns the expected field value.
7. Configure other field settings as needed.

    ::::{note}
    Some runtime field settings, such as custom labels and display formats, display in other areas of {{kib}} but may not display in the {{security-app}}.
    ::::

8. Click **Save**. The new field appears as a new column in the data grid.


## Manage runtime fields [manage-runtime-fields]

You can edit or delete existing runtime fields from the **Alerts**, **Timelines**, **Hosts**, and **Users** pages.

1. Click the **Fields** button to open the **Fields** browser, then search for the runtime field you want.

    ::::{tip}
    Click the **Runtime** column header twice to reorder the fields table with all runtime fields at the top.
    ::::

2. In the **Actions** column, select an option to edit or delete the runtime field.
