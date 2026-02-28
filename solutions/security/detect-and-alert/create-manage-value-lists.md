---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/value-lists-exceptions.html
  - https://www.elastic.co/guide/en/serverless/current/security-value-lists-exceptions.html
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Create and manage value lists to define exceptions for detection rules in Elastic Security.
---

# Create and manage value lists [value-lists-exceptions]

Value lists hold multiple values of the same {{es}} [data type](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md), such as IP addresses or keywords. Use them to [define exceptions](add-manage-exceptions.md) with the `is in list` and `is not in list` operators so that a rule skips alerts for any matching value. You can also use a value list as the [indicator match index](indicator-match.md#using-value-lists) when creating an indicator match rule.

::::{note}
Value lists cannot be used to define endpoint rule exceptions.
::::

## Prerequisites

To create and manage value lists, your role must have the required privileges. Refer to [Manage exception value lists](/solutions/security/detect-and-alert/detections-privileges.md#detections-privileges-manage-value-lists) for details.

## Supported list types and formats [value-list-types]

You can create value lists with the following types:

| List type | Description | Example values |
|---|---|---|
| Keywords | Keyword strings. Many [ECS fields](ecs://reference/ecs-field-reference.md) are keywords. | `svchost.exe`, `admin@example.com` |
| IP addresses | Single IP addresses. | `192.168.1.5` |
| IP ranges | IP ranges in CIDR or dash notation. | `10.0.0.0/8`, `127.0.0.1-127.0.0.4` |
| **Text** | Free-form text strings. | `error: unauthorized access` |

### IP format reference [ip-value-list-formats]

When uploading an **IP addresses** or **IP ranges** value list, each line (or CSV field) must contain exactly one value. The following formats are accepted:

| List type | Format | Example |
|---|---|---|
| IP addresses | Single IP address (IPv4 or IPv6) | `192.168.1.5`, `::1` |
| IP ranges | CIDR notation | `10.0.0.0/8`, `192.168.1.0/24` |
| IP ranges | Dash (range) notation | `10.0.0.0-10.255.255.255` |

The notation you choose for IP range lists affects size-based rule compatibility. Refer to [Value list size and rule type compatibility](#value-list-compatibility) for details.

## Value list size and rule type compatibility [value-list-compatibility]

A value list's size and data type determine which rule types can use it. Lists are classified as either *small* or *large*.

### Small value lists

Small value lists are compatible with all rule types, including threshold rules.

* **Keyword** or **IP address** lists with fewer than 65,536 items
* **IP range** lists with fewer than 65,536 items in CIDR notation (for example, `127.0.0.1/32`)
* **IP range** lists with fewer than 200 items in dash notation (for example, `127.0.0.1-127.0.0.4`)

### Large value lists

Large value lists are compatible only with custom query, saved query, machine learning, and indicator match rules.

* **Keyword**, **IP address**, or **IP range** lists with 65,536 or more items (or 200+ items for IP ranges using dash notation)
* **Text** lists of any size

::::{admonition} Threshold rules and value lists
:class: warning
Threshold rules only support exceptions that use small value lists. If a value list exceeds the size thresholds above, or if it uses the **Text** type, the exception will not be applied to a threshold rule. You may see a warning when this occurs.
::::

## Create a value list [create-value-lists]

1. Prepare a `txt` or `csv` file with all the values you want to include. If you use a `txt` file, new lines act as delimiters.

    ::::{important}
    * All values in the file must be of the same {{es}} type.
    * Wildcards are not supported in value lists. Values must be literal values.
    * The maximum accepted file size is 9 million bytes.
    ::::

2. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
3. Click **Manage value lists**. The **Manage value lists** window opens.

    :::{image} /solutions/images/security-upload-lists-ui.png
    :alt: Manage value lists flyout
    :screenshot:
    :::

4. Select the list type (**Keywords**, **IP addresses**, **IP ranges**, or **Text**) from the **Type of value list** drop-down.
5. Drag or select the `csv` or `txt` file that contains the values.
6. Click **Import value list**.

::::{note}
If you import a file with a name that already exists, a new list is not created. The imported values are added to the existing list instead.
::::


## Edit a value list [edit-value-lists]

1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Manage value lists**. The **Manage value lists** window opens.
3. In the **Value lists** table, click the value list you want to edit.
4. Do any of the following:

    * **Filter items in the list**: Use the KQL search bar to find values in the list. Depending on your list's type, you can filter by the `keyword`, `ip_range`, `ip`, or `text` fields. For example, to filter by Gmail addresses in a value list of the `keyword` type, enter `keyword:*gmail.com` into the search bar.

        You can also filter by the `updated_by` field (for example, `updated_by:testuser`), or the `updated at` field (for example, `updated_at < now`).

    * **Add individual items to the list**: Click **Create list item**, enter a value, then click **Add list item**.
    * **Bulk upload list items**: Drag or select the `csv` or `txt` file that contains the values that you want to add, then click **Upload**.
    * **Edit a value**: In the Value column, go to the value you want to edit and click the **Edit** button (![Edit button from Manage value lists window](/solutions/images/security-edit-value-list-item.png "title =20x20")). When you're done editing, click the **Save** button (![Save button from Manage value lists window](/solutions/images/security-save-value-list-item-changes.png "title =30x30")) to save your changes. Click the **Cancel** button (![Cancel button from Manage value lists window](/solutions/images/security-cancel-value-list-item-changes.png "title =30x30")) to revert your changes.
    * **Remove a value**: Click the **Remove value** button (![Remove value list button from Manage value lists window](/solutions/images/security-remove-value-list-item.png "title =20x20")) to delete a value from the list.


:::{image} /solutions/images/security-edit-value-lists.png
:alt: Manage items in a value lists
:screenshot:
:::

::::{tip}
You can also edit value lists while creating and managing exceptions that use value lists.
::::

## Export or remove a value list [export-remove-value-lists]

1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Manage value lists**. The **Manage value lists** window opens.
3. From the **Value lists** table, you can:

    1. Click the **Export value list** button (![Export button from Manage value lists window](/solutions/images/security-export-value-list.png "title =20x20")) to export the value list.
    2. Click the **Remove value list** button (![Remove button from Manage value lists window](/solutions/images/security-remove-value-list.png "title =20x20")) to delete the value list.

        :::{image} /solutions/images/security-manage-value-list.png
        :alt: Import value list flyout with action buttons highlighted
        :screenshot:
        :::

## Configure upload limits [adv-list-settings]

You can configure limits for uploading value lists to {{elastic-sec}} by editing your [`kibana.yml`](/deploy-manage/stack-settings.md) [configuration file](kibana://reference/configuration-reference/general-settings.md) or your {{kib}} cloud instance.

`xpack.lists.maxImportPayloadBytes`
:   Maximum bytes allowed for uploading value lists. Default: `9000000`. Maximum: `100000000`.

    For every 10 megabytes, reserve an additional 1 gigabyte of RAM for {{kib}}. For example, a {{kib}} instance with 2 GB of RAM can support up to 20 MB (`20000000`).

`xpack.lists.importBufferSize`
:   Buffer size for uploading value lists. Default: `1000`.

    Increase this value to improve throughput (uses more memory), or decrease it to reduce memory usage (slower uploads).
