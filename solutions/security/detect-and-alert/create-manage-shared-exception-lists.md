---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/shared-exception-lists.html
  - https://www.elastic.co/guide/en/serverless/current/security-shared-exception-lists.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
description: Create and manage shared exception lists to apply the same exceptions to multiple rules.
---

# Create and manage shared exception lists [shared-exception-lists]

Shared exception lists allow you to group exceptions together and then apply them to multiple rules. Use the Shared Exception Lists page to set up shared exception lists.

% The following note is only applicable to {{ech}} and is only relevant for users who are upgrading from 8.5 -> 8.6 or later. Might need to add this to the [8.6.x upgrade docs](https://www.elastic.co/guide/en/security/8.6/upgrade-intro.html) later.

% ::::{note}
% Exception lists created in 8.5 and earlier become shared exception lists in 8.6 or later. You can access all shared exception % lists from the Shared Exception Lists page.
% ::::


:::{image} /solutions/images/security-rule-exceptions-page.png
:alt: Shared Exception Lists page
:screenshot:
:::


## Create shared exception lists [create-shared-exception-list]

Set up shared exception lists to contain exception items:

1. Find the **Shared exception lists** page in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Create shared exception list** → **Create shared list**.
3. Give the shared exception list a name.
4. (Optional) Provide a description.
5. Click **Create shared exception list**.


## Add exception items to shared exception lists [add-exception-items]

Add exception items:

1. Find the **Shared exception lists** page in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Create shared exception list** → **Create exception item**.

    ::::{tip}
    You can add exceptions to an empty shared exception list by expanding the list, or viewing its details page and clicking **Create rule exception**. After creating an exception, you can associate the shared exception list with rules. Refer to [Associate shared exception lists with rules](#link-shared-exception-lists) to learn more.
    ::::

3. In the **Add rule exception** flyout, name the exception item and add conditions that define when the exception prevents alerts. When the exception’s query conditions are met (the query evaluates to `true`), rules do not generate alerts even when other rule criteria are met.

    1. **Field**: Select a field to identify the event being filtered.
    2. **Operator**: Select an operator to define the condition:

        * `is` | `is not` — Must be an exact match of the defined value.
        * `is one of` | `is not one of` — Matches any of the defined values.
        * `exists` | `does not exist` — The field exists.
        * `is in list` | `is not in list` — Matches values in a value list.

            ::::{note}
            * An exception defined by a value list must use `is in list` or `is not in list` in all conditions.
            * Wildcards are not supported in value lists.
            * If a value list can’t be used due to [size or data type](create-manage-value-lists.md#manage-value-lists), it’ll be unavailable in the **Value** menu.

            ::::

        * `matches` | `does not match` — Allows you to use wildcards in **Value**, such as `C:\path\*\app.exe`. Available wildcards are `?` (match one character) and `*` (match zero or more characters). The selected **Field** data type must be [keyword](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md#keyword-field-type), [text](elasticsearch://reference/elasticsearch/mapping-reference/text.md#text-field-type), or [wildcard](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md#wildcard-field-type).

            ::::{important}
            Using wildcards can impact performance. To create a more efficient exception using wildcards, use multiple conditions and make them as specific as possible. For example, adding conditions using `process.name` or `file.name` can help limit the scope of wildcard matching.
            ::::

    3. **Value**: Enter the value associated with the **Field**. To enter multiple values (when using `is one of` or `is not one of`), enter each value, then press **Return**.

4. Click **AND** or **OR** to create multiple conditions and define their relationships.
5. Click **Add nested condition** to create conditions using nested fields. This is only required for [these nested fields](add-manage-exceptions.md#nested-field-list). For all other fields, nested conditions should not be used.
6. Choose to add the exception to shared exception lists.

    ::::{note}
    This option will be unavailable if a shared exception list doesn’t exist. In addition, you can’t add an endpoint exception item to the Endpoint Security Exception List from this UI. Refer to [Add {{elastic-endpoint}} exceptions](add-manage-exceptions.md#endpoint-rule-exceptions) for instructions about creating endpoint exceptions.
    ::::

7. (Optional) Enter a comment describing the exception.
8. (Optional) Enter a future expiration date and time for the exception.
9. (Optional) **Close all alerts that match this exception and were generated by this rule**: Closes all alerts that match the exception’s conditions and were generated only by the current rule.
10. Click **Add rule exception**.


## Associate shared exception lists with rules [link-shared-exception-lists]

Apply shared exception lists to rules:

1. Find the **Shared exception lists** page in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Do one of the following:

    * Select a shared exception list’s name to open its details page, then click **Link rules**.
    * Find the shared exception list you want to assign to rules, then from the **More actions** menu (**…**), select **Link rules**.

3. Click the toggles in the **Link** column to select the rules you want to link to the exception list.

    ::::{tip}
    If you know a rule’s name, you can enter it into the search bar.
    ::::

4. Click **Save**.
5. (Optional) To verify that the shared exception list was added to the rules you selected:

    1. Open a rule’s details page (**Rules → Detection rules (SIEM) → Rule name**).
    2. Scroll down the page, and then select the **Rule exceptions** tab.
    3. Navigate to the exception items that are included in the shared exception list. Click the **Affects shared list** link to view the associated shared exception lists.

        :::{image} /solutions/images/security-associated-shared-exception-list.png
        :alt: Associated shared exceptions
        :screenshot:
        :::



## View and filter exception lists [view-shared-exception-lists]

The Shared Exception Lists page displays each shared exception list on an individual row, with the most recently created list at the top. Each row contains these details about the shared exception list:

* Shared exception list name
* Date the list was created
* Username of the user who created the list
* Number of exception items in the shared exception list
* Number of rules the shared exception list affects

To view the details of an exception item within a shared exception list, expand a row.

:::{image} /solutions/images/security-view-filter-shared-exception.png
:alt: Associated shared exceptions
:screenshot:
:::

To filter exception lists by a specific value, enter a value in the search bar. You can search the following attributes:

* `name`
* `list_id`
* `created_by`

If no attribute is selected, the app searches the list name by default.


## Manage shared exception lists [manage-exception-lists]

You can edit, export, import, duplicate, and delete shared exception lists from the Shared Exception Lists page.

% The following note is only applicable to {{ech}} and is only relevant for users who are upgrading from 8.5 -> 8.6 or later. Might need to add this to the [8.6.x upgrade docs](https://www.elastic.co/guide/en/security/8.6/upgrade-intro.html) later.

% ::::{note}
% Exception lists created in 8.5 and earlier become shared exception lists in 8.6 or later. You can access all shared exception lists from the Shared Exception Lists page.
% ::::


To export or delete an exception list, select the required action button on the appropriate list. Note the following:

* Exception lists are exported to `.ndjson` files.
* Exception lists are also exported as part of any exported detection rules configured with exceptions. Refer to [Export and import rules](manage-detection-rules.md#import-export-rules-ui).
* If an exception list is linked to any rules, you’ll get a warning asking you to confirm the deletion.
* If an exception list contains expired exceptions, you can choose whether to include them in the exported file.

:::{image} /solutions/images/security-actions-exception-list.png
:alt: Detail of Exception lists table with export and delete buttons highlighted
:screenshot:
:::
