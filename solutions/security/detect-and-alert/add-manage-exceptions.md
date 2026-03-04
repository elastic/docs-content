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
description: Add and manage rule exceptions to prevent false positives and reduce alert noise.
---

# Add and manage exceptions [add-exceptions]

Exceptions prevent a rule from generating alerts when specific conditions are met. You can add exceptions to individual rules, or create [shared exception lists](create-manage-shared-exception-lists.md) that apply to multiple rules.

## Prerequisites [exceptions-requirements]

To use exceptions, your role must have the appropriate access. To learn how to access other detection features, refer to [](/solutions/security/detect-and-alert/requirements-privileges.md).

### Exception privileges

::::{applies-switch}

:::{applies-item} { "stack": "ga 9.4", "serverless": "ga" }

- **View only access**: To view exceptions for individual and multiple rules, your role needs at least `Read` [{{kib}} privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for the `Security > Rules, Alerts, and Exceptions` {{kib}} feature and deselect **Manage Exceptions** for the `Exceptions` sub-feature.
- **Manage access**: To create and manage exceptions for individual and multiple rules, your role needs at least `Read` {{kib}} privileges for the `Security > Rules, Alerts, and Exceptions` {{kib}} feature and ensure **Manage Exceptions** remains selected for the `Exceptions` sub-feature.

:::

:::{applies-item} { "stack": "ga =9.3" }

- **View only access**: To view exceptions for individual and multiple rules, your role needs at least `Read` [{{kib}} privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for the `Security > Rules, Alerts, and Exceptions` {{kib}} feature.
- **Manage access**: To create and manage exceptions for individual and multiple rules, your role needs `All` {{kib}} privileges for the `Security > Rules, Alerts, and Exceptions` {{kib}} feature.

:::

:::{applies-item} { "stack": "ga 9.0-9.2" }

**Manage access**: To create and manage exceptions for individual and multiple rules, your role needs `All` [{{kib}} privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for the `Security > Security` feature. 

:::

::::

### {{elastic-endpoint}} exception privileges 

```yaml {applies_to}
stack: ga 
serverless: ga
```

For required privileges to view and manage {{elastic-endpoint}} exceptions, refer to [](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md). 

## Add exceptions to a rule [detection-rule-exceptions]

You can add exceptions from several places in the UI:

* **Rule details page**: Find **Detection rules (SIEM)** in the navigation menu, select a rule, scroll to the **Rule exceptions** tab, and click **Add rule exception**.

    :::{image} /solutions/images/security-rule-exception-tab.png
    :alt: Detail of rule exceptions tab
    :screenshot:
    :::

* **Alerts table**: Find **Alerts** in the navigation menu, go to the alert, click the **More Actions** menu {icon}`boxes_horizontal`, and select **Add rule exception**.
* **Alert details flyout**: Click **View details** on an alert, then click **Take action > Add rule exception**.
* **Shared Exception Lists page**: Find **Shared exception lists** in the navigation menu, click **Create shared exception list** > **Create exception item**.

### Configure exception conditions

After selecting one of the entry points above, the **Add rule exception** flyout opens. Follow these steps:

1. Name the exception.
2. Add conditions that define when the exception applies. When the exception's query evaluates to `true`, the rule does not generate alerts even when its other criteria are met.

    ::::{note}
    When you create an exception from an alert, conditions are auto-populated with relevant alert data. Data from custom highlighted fields is listed first.
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
            * If a value list can't be used due to [size or data type](create-manage-value-lists.md#value-list-compatibility), it'll be unavailable in the **Value** menu.
            ::::

        * `matches` | `does not match` — Allows you to use wildcards in **Value**, such as `C:\\path\\*\\app.exe`. Available wildcards are `?` (match one character) and `*` (match zero or more characters). The selected **Field** data type must be [keyword](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md#keyword-field-type), [text](elasticsearch://reference/elasticsearch/mapping-reference/text.md#text-field-type), or [wildcard](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md#wildcard-field-type).

            ::::{note}
            Some characters must be escaped with a backslash, such as `\\` for a literal backslash, `\*` for an asterisk, and `\?` for a question mark. Windows paths must be divided with double backslashes (for example, `C:\\Windows\\explorer.exe`), and paths that already include double backslashes might require four backslashes for each divider.
            ::::

            ::::{important}
            Using wildcards can impact performance. To create a more efficient exception using wildcards, use multiple conditions and make them as specific as possible. For example, adding conditions using `process.name` or `file.name` can help limit the scope of wildcard matching.
            ::::

    3. **Value**: Enter the value associated with the **Field**. To enter multiple values (when using `is one of` or `is not one of`), enter each value, then press **Return**.

        ::::{note}
        The `is one of` and `is not one of` operators support identical, case-sensitive values. For example, if you want to match the values `Windows` and `windows`, add both values to the **Value** field.
        ::::

        In the following example, the exception prevents the rule from generating alerts when the `svchost.exe` process runs on hostname `siem-kibana`.

        :::{image} /solutions/images/security-add-exception-ui.png
        :alt: add exception ui
        :screenshot:
        :::

3. Click **AND** or **OR** to create multiple conditions and define their relationships.
4. Click **Add nested condition** to create conditions using nested fields. This is only required for [these nested fields](#nested-field-list). For all other fields, nested conditions should not be used.
5. Choose to add the exception to a rule or a shared exception list.

    ::::{tip}
    If a shared exception list doesn't exist, you can [create one](create-manage-shared-exception-lists.md) from the Shared Exception Lists page.
    ::::

6. (Optional) Enter a comment describing the exception.
7. (Optional) Enter a future expiration date and time for the exception.
8. Select one of the following alert actions:

    * **Close this alert**: Closes the alert when the exception is added. This option is only available when adding exceptions from the Alerts table.
    * **Close all alerts that match this exception and were generated by this rule**: Closes all alerts that match the exception's conditions and were generated only by the current rule.

9. Click **Add rule exception**.

::::{important}
Rule exceptions are case-sensitive. Any character entered as an uppercase or lowercase letter will be treated as such. If you don't want a field evaluated as case-sensitive, some ECS fields have a `.caseless` version that you can use.
::::

::::{important}
When using ES|QL, you can append new fields with commands such as [`EVAL`](https://www.elastic.co/docs/reference/query-languages/esql/commands/eval), but you can't apply exceptions to these appended fields. Exceptions are only applied to the index source fields.
::::

### Rule type considerations

* **Event correlation (EQL) rules**: Exceptions are evaluated against every event in the sequence. If an exception matches any event necessary to complete the sequence, alerts are not created. To exclude values from a specific event in the sequence, update the rule's EQL statement instead. For example:

    ```eql
    `sequence
      [file where file.extension == "exe"
      and file.name != "app-name.exe"]
      [process where true
      and process.name != "process-name.exe"]`
    ```

* **Indicator match rules**: Exceptions are evaluated against both source and indicator indices. If the exception matches events in *either* index, alerts are not generated.

## Add {{elastic-endpoint}} exceptions [endpoint-rule-exceptions]

{{elastic-endpoint}} exceptions apply to [endpoint protection rules](../manage-elastic-defend/endpoint-protection-rules.md) and to any rules with the [**{{elastic-endpoint}} exceptions**](common-rule-settings.md#rule-ui-advanced-params) option selected. These exceptions are applied to both the detection rule and the {{elastic-endpoint}} on your hosts.

::::{important}
* Exceptions added to endpoint protection rules affect all alerts sent from {{elastic-endpoint}}. Be careful not to unintentionally prevent useful Endpoint alerts.
* To add an Endpoint exception to an endpoint protection rule, there must be at least one {{elastic-endpoint}} alert generated in the system. For non-production use, if no alerts exist, you can trigger a test alert using malware emulation techniques or tools such as the Anti Malware Testfile from the [European Institute for Computer Anti-Virus Research (EICAR)](https://www.eicar.org/).
* [Binary fields](elasticsearch://reference/elasticsearch/mapping-reference/binary.md) are not supported in detection rule exceptions.
::::

You can add Endpoint exceptions from the following places:

* **Rule details page**: Find **Detection rules (SIEM)** in the navigation menu, select an [endpoint protection rule](../manage-elastic-defend/endpoint-protection-rules.md), scroll to the **Endpoint exceptions** tab, and click **Add endpoint exception**.
* **Alerts table**: Find **Alerts** in the navigation menu, go to an {{elastic-endpoint}} alert, click the **More actions** menu {icon}`boxes_horizontal`, and select **Add Endpoint exception**.
* **Shared Exception Lists page**: Find **Shared exception lists** in the navigation menu, expand the **Endpoint Security Exception List** (or click its name), and click **Add endpoint exception**.

    ::::{note}
    The Endpoint Security Exception List is automatically created. By default, it's associated with endpoint protection rules and any rules with the [**{{elastic-endpoint}} exceptions**](common-rule-settings.md#rule-ui-advanced-params) option selected.
    ::::

The **Add Endpoint Exception** flyout opens.

:::{image} /solutions/images/security-endpoint-add-exp.png
:alt: endpoint add exp
:screenshot:
:::

1. Modify the conditions as needed. The same [operators](#detection-rule-exceptions) apply, with these differences:

    * Fields with conflicts are marked with a warning icon {icon}`warning`. For more information, refer to [Troubleshooting type conflicts and unmapped fields](../../../troubleshoot/security/detection-rules.md#rule-exceptions-field-conflicts).
    * Unlike detection rule exceptions, Elastic Endpoint exceptions do not require escaping special characters.

2. (Optional) Add a comment to the exception.
3. Select any applicable alert actions:

    * **Close this alert**: Closes the alert when the exception is added. This option is only available when adding exceptions from the Alerts table.
    * **Close all alerts that match this exception and were generated by this rule**: Closes all alerts that match the exception's conditions.

4. Click **Add Endpoint Exception**.

::::{note}
It might take longer for exceptions to be applied to hosts within larger deployments.
::::

## Nested conditions [ex-nested-conditions]

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

To view a rule's exceptions:

1. Open the rule's details page. To do this, find **Detection rules (SIEM)** in the navigation menu or using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), search for the rule that you want to examine, then click the rule's name to open its details.
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
