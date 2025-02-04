# Create and manage value lists [security-value-lists-exceptions]

Value lists hold multiple values of the same Elasticsearch data type, such as IP addresses, which are used to determine when an exception prevents an alert from being generated. You can use value lists to define exceptions for detection rules; however, you cannot use value lists to define endpoint rule exceptions.

Value lists are lists of items with the same {{es}} [data type](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html). You can create value lists with these types:

* `Keywords` (many [ECS fields](https://www.elastic.co/guide/en/ecs/{{ecs_version}}/ecs-field-reference.html) are keywords)
* `IP Addresses`
* `IP Ranges`
* `Text`

After creating value lists, you can use `is in list` and `is not in list` operators to [define exceptions](../../../solutions/security/detect-and-alert/add-manage-exceptions.md).

::::{tip}
You can also use a value list as the [indicator match index](../../../solutions/security/detect-and-alert/create-detection-rule.md#indicator-value-lists) when creating an indicator match rule.

::::



## Create value lists [create-value-lists]

When you create a value list for a rule exception, be mindful of the list’s size and data type. All rule types support value list exceptions, but extremely large lists or certain data types have limitations.

Custom query, machine learning, and indicator match rules support the following value list types and sizes:

* **Keywords** or **IP addresses** list types with more than 65,536 values
* **IP ranges** list type with over 200 dash notation values (for example, `127.0.0.1-127.0.0.4` is one value) or more than 65,536 CIDR notation values

To create a value list:

1. Prepare a `txt` or `csv` file with all the values you want to use for determining exceptions from a single list. If you use a `txt` file, new lines act as delimiters.

    ::::{important}
    * All values in the file must be of the same {{es}} type.
    * Wildcards are not supported in value lists. Values must be literal values.
    * The maximum accepted file size is 9 million bytes.

    ::::

2. Go to **Rules** → **Detection rules (SIEM)**.
3. Click **Manage value lists**. The **Manage value lists** window opens.

    ![Manage value lists flyout](../../../images/serverless--detections-upload-lists-ui.png "")

4. Select the list type (**Keywords**, **IP addresses***, ***IP ranges***, or ***Text**) from the **Type of value list** drop-down.
5. Drag or select the `csv` or `txt` file that contains the values.
6. Click **Import value list**.

::::{note}
If you import a file with a name that already exists, a new list is not created. The imported values are added to the existing list instead.

::::



## Manage value lists [manage-value-lists]

You can edit, remove, or export existing value lists.


### Edit value lists [edit-value-lists]

1. Go to **Rules** → **Detection rules (SIEM)**.
2. Click **Manage value lists**. The **Manage value lists** window opens.
3. In the **Value lists** table, click the value list you want to edit.
4. Do any of the following:

    * **Filter items in the list**: Use the KQL search bar to find values in the list. Depending on your list’s type, you can filter by the `keyword`, `ip_range`, `ip`, or `text` fields. For example, to filter by Gmail addresses in a value list of the `keyword` type, enter `keyword:*gmail.com` into the search bar.

        You can also filter by the `updated_by` field (for example, `updated_by:testuser`), or the `updated at` field (for example, `updated_at < now`).

    * **Add individual items to the list**: Click **Create list item**, enter a value, then click **Add list item**.
    * **Bulk upload list items**: Drag or select the `csv` or `txt` file that contains the values that you want to add, then click **Upload**.
    * **Edit a value**: In the Value column, go to the value you want to edit and click the **Edit*** button (![Edit](../../../images/serverless-pencil.svg "")). When you’re done editing, click the ***Save** button (![Save](../../../images/serverless-check.svg "")) to save your changes. Click the **Cancel** button (![Edit](../../../images/serverless-cross.svg "")) to revert your changes.
    * **Remove a value**: Click the **Remove value** button (![Remove value list](../../../images/serverless-trash.svg "")) to delete a value from the list.

        ![Manage items in a value list](../../../images/serverless--detections-edit-value-lists.png "")


::::{tip}
You can also edit value lists while creating and managing exceptions that use value lists.

::::



### Export or remove value lists [export-remove-value-lists]

1. Go to **Rules** → **Detection rules (SIEM)**.
2. Click **Manage value lists**. The **Manage value lists** window opens.
3. From the **Value lists** table, you can:

    * Click the **Export value list** button (![Export value list](../../../images/serverless-exportAction.svg "")) to export the value list.
    * Click the **Remove value list** button (![Remove value list](../../../images/serverless-trash.svg "")) to delete the value list.


:::{image} ../../../images/serverless--detections-manage-value-list.png
:alt: Import value list flyout with action buttons highlighted
:class: screenshot
:::
