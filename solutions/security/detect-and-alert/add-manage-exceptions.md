---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/add-exceptions.html
  - https://www.elastic.co/guide/en/serverless/current/security-add-exceptions.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Add and manage exceptions [add-exceptions]

You can add exceptions to a rule from the rule details page, the Alerts table, the alert details flyout, or the Shared Exception Lists page. When you add an exception, you can also close all alerts that meet the exception’s criteria.

::::{important}
* To ensure an exception is successfully applied, ensure that the fields you’ve defined for its query are correctly and consistently mapped in their respective indices. Refer to [ECS](ecs://reference/index.md) to learn more about supported mappings.
* Be careful when adding exceptions to [event correlation](create-detection-rule.md#create-eql-rule) rules. Exceptions are evaluated against every event in the sequence, and if an exception matches any events that are necessary to complete the sequence, alerts are not created.

    To exclude values from a specific event in the sequence, update the rule’s EQL statement. For example:

    ```eql
    `sequence
      [file where file.extension == "exe"
      and file.name != "app-name.exe"]
      [process where true
      and process.name != "process-name.exe"]`
    ```

* Be careful when adding exceptions to [indicator match](/solutions/security/detect-and-alert/rule-types/indicator-match.md) rules. Exceptions are evaluated against source and indicator indices, so if the exception matches events in *either* index, alerts are not generated.

::::



## Add exceptions to a rule [detection-rule-exceptions]

1. Do one of the following:

    * To add an exception from the rule details page:

        1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
        2. In the Rules table, search for the rule that you want to add an exception to, then click its name to open the rule details.
        3. Scroll down the rule details page, select the **Rule exceptions** tab, then click **Add rule exception**.

            :::{image} /solutions/images/security-rule-exception-tab.png
            :alt: Detail of rule exceptions tab
            :screenshot:
            :::

    * To add an exception from the Alerts table:

        1. Find **Alerts** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
        2. Scroll down to the Alerts table, go to the alert you want to create an exception for, click the **More Actions** menu (**…**), then select **Add rule exception**.

    * To add an exception from the alert details flyout:

        1. Find **Alerts** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
        2. Click the **View details** button from the Alerts table.
        3. In the alert details flyout, click **Take action → Add rule exception**.

    * To add an exception from the Shared Exception Lists page:

        1. Find the **Shared exception lists** page in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
        2. Click **Create shared exception list** → **Create exception item**.

2. In the **Add rule exception** flyout, name the exception.
3. Add conditions that define the exception. When the exception’s query evaluates to `true`, rules don’t generate alerts even when their criteria are met.

    ::::{important}
    Rule exceptions are case-sensitive, which means that any character that’s entered as an uppercase or lowercase letter will be treated as such. In the event you *don’t* want a field evaluated as case-sensitive, some ECS fields have a `.caseless` version that you can use.
    ::::


    ::::{note}
    When you create a new exception from an alert, exception conditions are auto-populated with relevant alert data. Data from custom highlighted fields is listed first. A comment that describes the auto-generated exception conditions is also added to the **Add comments** section.
    ::::

    ::::{note}
    When using ES|QL, you can append new fields with commands such as [`EVAL`](https://www.elastic.co/docs/reference/query-languages/esql/commands/eval), but you can't apply exceptions to these appended fields. Exceptions are only applied to the index source fields.
    ::::

    1. **Field**: Select a field to identify the event being filtered.

        ::::{note}
        A warning displays for fields with conflicts. Using these fields might cause unexpected exceptions behavior. Refer to [Troubleshooting type conflicts and unmapped fields](../../../troubleshoot/security/detection-rules.md#rule-exceptions-field-conflicts) for more information.

        ::::

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

        * `matches` | `does not match` — Allows you to use wildcards in **Value**, such as `C:\\path\\*\\app.exe`. Available wildcards are `?` (match one character) and `*` (match zero or more characters). The selected **Field** data type must be [keyword](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md#keyword-field-type), [text](elasticsearch://reference/elasticsearch/mapping-reference/text.md#text-field-type), or [wildcard](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md#wildcard-field-type).

            ::::{note}
            For detection rule exceptions, some characters must be escaped with a backslash, such as `\\` for a literal backslash, `\*` for an asterisk, and `\?` for a question mark. Windows paths must be divided with double backslashes (for example, `C:\\Windows\\explorer.exe`), and paths that already include double backslashes might require four backslashes for each divider.
            ::::


            ::::{important}
            Using wildcards can impact performance. To create a more efficient exception using wildcards, use multiple conditions and make them as specific as possible. For example, adding conditions using `process.name` or `file.name` can help limit the scope of wildcard matching.
            ::::

    3. **Value**: Enter the value associated with the **Field**. To enter multiple values (when using `is one of` or `is not one of`), enter each value, then press **Return**.

        ::::{note}
        The `is one of` and `is not one of` operators support identical, case-sensitive values. For example, if you want to match the values `Windows` and `windows`, add both values to the **Value** field.
        ::::


        In the following example, the exception was created from the Rules page and prevents the rule from generating alerts when the `svchost.exe` process runs on hostname `siem-kibana`.

        :::{image} /solutions/images/security-add-exception-ui.png
        :alt: add exception ui
        :screenshot:
        :::

5. Click **AND** or **OR** to create multiple conditions and define their relationships.
6. Click **Add nested condition** to create conditions using nested fields. This is only required for [these nested fields](#nested-field-list). For all other fields, nested conditions should not be used.
7. Choose to add the exception to a rule or a shared exception list.

    ::::{note}
    If you are creating an exception from the Shared Exception Lists page, you can add the exception to multiple rules.
    ::::


    ::::{tip}
    If a shared exception list doesn’t exist, you can [create one](create-manage-shared-exception-lists.md) from the Shared Exception Lists page.
    ::::

8. (Optional) Enter a comment describing the exception.
9. (Optional) Enter a future expiration date and time for the exception.
10. Select one of the following alert actions:

    * **Close this alert**: Closes the alert when the exception is added. This option is only available when adding exceptions from the Alerts table.
    * **Close all alerts that match this exception and were generated by this rule**: Closes all alerts that match the exception’s conditions and were generated only by the current rule.

11. Click **Add rule exception**.


## Add {{elastic-endpoint}} exceptions [endpoint-rule-exceptions]

You can add {{elastic-endpoint}} exceptions to [endpoint protection rules](../manage-elastic-defend/endpoint-protection-rules.md) or to rules that are associated with {{elastic-endpoint}} rule exceptions. To associate rules when creating or editing a rule, select the [**{{elastic-endpoint}} exceptions**](create-detection-rule.md#rule-ui-advanced-params) option.

Endpoint exceptions are added to the endpoint protection rules **and** the {{elastic-endpoint}} on your hosts.

::::{important}
Exceptions added to the endpoint protection rules affect all alerts sent from {{elastic-endpoint}}. Be careful not to unintentionally prevent useful Endpoint alerts.

Additionally, to add an Endpoint exception to an endpoint protection rule, there must be at least one {{elastic-endpoint}} alert generated in the system. For non-production use, if no alerts exist, you can trigger a test alert using malware emulation techniques or tools such as the Anti Malware Testfile from the [European Institute for Computer Anti-Virus Research (EICAR)](https://www.eicar.org/).

::::


::::{important}
[Binary fields](elasticsearch://reference/elasticsearch/mapping-reference/binary.md) are not supported in detection rule exceptions.

::::


1. Do one of the following:

    * To add an Endpoint exception from the rule details page:

        1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
        2. In the Rules table, search for and select one of the [endpoint protection rules](../manage-elastic-defend/endpoint-protection-rules.md).
        3. Scroll down the rule details page, select the **Endpoint exceptions** tab, then click **Add endpoint exception**.

    * To add an Endpoint exception from the Alerts table:

        1. Find **Alerts** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
        2. Scroll down to the Alerts table, and from an {{elastic-endpoint}} alert, click the **More actions** menu (**…**), then select **Add Endpoint exception**.

    * To add an Endpoint exception from Shared Exception Lists page:

        1. Find the **Shared exception lists** page in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
        2. Expand the Endpoint Security Exception List or click the list name to open the list’s details page. Next, click **Add endpoint exception**.

            ::::{note}
            The Endpoint Security Exception List is automatically created. By default, it’s associated with endpoint protection rules and any rules with the [**{{elastic-endpoint}} exceptions**](create-detection-rule.md#rule-ui-advanced-params) option selected.
            ::::


    The **Add Endpoint Exception** flyout opens.

    :::{image} /solutions/images/security-endpoint-add-exp.png
    :alt: endpoint add exp
    :screenshot:
    :::

2. If required, modify the conditions.

    ::::{important}
    Rule exceptions are case-sensitive, which means that any character that’s entered as an uppercase or lowercase letter will be treated as such. In the event you *don’t* want a field evaluated as case-sensitive, some ECS fields have a `.caseless` version that you can use.
    ::::


    ::::{note}
    * Fields with conflicts are marked with a warning icon (![Field conflict warning icon](/solutions/images/security-field-warning-icon.png "title =20x20")). Using these fields might cause unexpected exceptions behavior. For more information, refer to [Troubleshooting type conflicts and unmapped fields](../../../troubleshoot/security/detection-rules.md#rule-exceptions-field-conflicts).
    * The `is one of` and `is not one of` operators support identical, case-sensitive values. For example, if you want to match the values `Windows` and `windows`, add both values to the **Value** field.
    * Unlike detection rule exceptions, Elastic Endpoint exceptions do not require escaping special characters.

    ::::

3. (Optional) Add a comment to the exception.
4. You can select any of the following:

    * **Close this alert**: Closes the alert when the exception is added. This option is only available when adding exceptions from the Alerts table.
    * **Close all alerts that match this exception and were generated by this rule**: Closes all alerts that match the exception’s conditions.

5. Click **Add Endpoint Exception**. An exception is created for both the detection rule and the {{elastic-endpoint}}.

    ::::{note}
    It might take longer for exceptions to be applied to hosts within larger deployments.
    ::::



## Exceptions with nested conditions [ex-nested-conditions]

Some Endpoint objects contain nested fields, and the only way to ensure you are excluding the correct fields is with nested conditions. One example is the `process.Ext` object:

```json
{
  "ancestry": [],
  "code_signature": {
    "trusted": true,
    "subject_name": "LFC",
    "exists": true,
    "status": "trusted"
  },
  "user": "WDAGUtilityAccount",
  "token": {
    "elevation": true,
    "integrity_level_name": "high",
    "domain": "27FB305D-3838-4",
    "user": "WDAGUtilityAccount",
    "elevation_type": "default",
    "sid": "S-1-5-21-2047949552-857980807-821054962-504"
  }
}
```

### Nested fields [nested-field-list]

Only these objects require nested conditions to ensure the exception functions correctly:

* `Endpoint.policy.applied.artifacts.global.identifiers`
* `Endpoint.policy.applied.artifacts.user.identifiers`
* `Target.dll.Ext.code_signature`
* `Target.process.Ext.code_signature`
* `Target.process.Ext.token.privileges`
* `Target.process.parent.Ext.code_signature`
* `Target.process.thread.Ext.token.privileges`
* `dll.Ext.code_signature`
* `file.Ext.code_signature`
* `file.Ext.macro.errors`
* `file.Ext.macro.stream`
* `process.Ext.code_signature`
* `process.Ext.token.privileges`
* `process.parent.Ext.code_signature`
* `process.thread.Ext.token.privileges`


### Nested condition example [_nested_condition_example]

Creates an exception that excludes all LFC-signed trusted processes:

:::{image} /solutions/images/security-nested-exp.png
:alt: nested exp
:screenshot:
:::


## View and manage exceptions [manage-exception]

To view a rule’s exceptions:

1. Open the rule’s details page. To do this, find **Detection rules (SIEM)** in the navigation menu or look for “Detection rules (SIEM)” using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), search for the rule that you want to examine, then click the rule’s name to open its details.
2. Scroll down and select the **Rule exceptions** or **Endpoint exceptions** tab. All exceptions that belong to the rule will display in a list.

    From the list, you can filter, edit, and delete exceptions. You can also toggle between **Active exceptions** and **Expired exceptions**.

    :::{image} /solutions/images/security-manage-default-rule-list.png
    :alt: A default rule list
    :screenshot:
    :::



## Find rules using the same exceptions [rules-using-same-exception]

To find out if an exception is used by other rules, select the **Rule exceptions** or **Endpoint exceptions** tab, navigate to an exception list item, then click **Affects *X* rules**.

::::{note}
Changes that you make to the exception also apply to other rules that use the exception.
::::


:::{image} /solutions/images/security-exception-affects-multiple-rules.png
:alt: Exception that affects multiple rules
:screenshot:
:::
