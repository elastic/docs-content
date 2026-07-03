---
applies_to:
  stack: ga 9.4+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
description: Create and manage Elastic Endpoint exceptions to prevent Elastic Endpoint from generating false positive alerts for specific conditions on your hosts.
---

# {{elastic-endpoint}} exceptions [elastic-endpoint-exceptions]

::::{note}
:applies_to: stack: ga 9.0-9.3
In {{stack}} 9.0–9.3, {{elastic-endpoint}} exceptions are managed through detection rules. For more information, refer to [Add {{elastic-endpoint}} exceptions](/solutions/security/detect-and-alert/add-manage-exceptions.md#endpoint-rule-exceptions).
::::

{{elastic-endpoint}} exceptions prevent {{elastic-endpoint}} from generating alerts for specific conditions on your hosts. Unlike [detection rule exceptions](/solutions/security/detect-and-alert/add-manage-exceptions.md), {{elastic-endpoint}} exceptions are enforced directly on the endpoint — {{elastic-endpoint}} checks for exceptions before most other processing, which means matching processes are not monitored further. This can also improve performance.

::::{tip}
To ensure you're using the right feature for your use case, review [](/solutions/security/manage-elastic-defend/optimize-elastic-defend.md) to understand the differences between {{elastic-endpoint}} exceptions and other endpoint artifacts.
::::

::::{admonition} Requirements
You must have the **Endpoint Exceptions** [privilege](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md) or the appropriate user role to access this feature.
::::

By default, {{elastic-endpoint}} exceptions apply globally across all hosts running {{elastic-defend}}. If you opt in to per-policy behavior, you can also assign exceptions to specific {{elastic-defend}} integration policies, so the exception applies only to hosts assigned to that policy.

{{elastic-endpoint}} exceptions are space-aware: when you create a per-policy exception, it is associated with the space you're working in. For more information on how spaces interact with endpoint artifacts, refer to [](/solutions/security/get-started/spaces-defend-faq.md).

If you're upgrading from an earlier version, your existing {{elastic-endpoint}} exceptions are preserved and are managed from the **Artifacts** page. 

## Opt in to per-policy {{elastic-endpoint}} exceptions [endpoint-exceptions-opt-in]

For deployments upgraded from an earlier version, per-policy assignment for {{elastic-endpoint}} exceptions requires opting in. New deployments are automatically opted in to per-policy {{elastic-endpoint}} exceptions with no action required.

If you're upgrading from an earlier version, a callout appears on the **Artifacts** page prompting you to opt in. You must have the **superuser** role in {{stack}}, or the **admin** role in {{serverless-short}}, to perform the opt-in.

::::{important}
Opting in is permanent and cannot be reversed. After opting in:

* {{elastic-endpoint}} exceptions support per-policy assignment and are no longer evaluated by detection rules during rule execution.
* {{elastic-endpoint}} exceptions can no longer be added to detection rules.
::::

To opt in to per-policy {{elastic-endpoint}} exceptions on an upgraded deployment:

1. Find **Artifacts** in the navigation menu, then select the **Endpoint exceptions** tab.
2. In the callout that appears, click **Update details**.
3. Review the information in the confirmation dialog, then confirm.


## Add an {{elastic-endpoint}} exception [add-endpoint-exception]

You can add {{elastic-endpoint}} exceptions from the following places:

* **Artifacts page**: Find **Artifacts** in the navigation menu, select the **Endpoint exceptions** tab, then click **Add endpoint exception**.
* **Alerts table**: Find **Alerts** in the navigation menu, go to an {{elastic-endpoint}} alert, click the **More actions** menu ({icon}`boxes_vertical`), and select **Add Endpoint exception**.
* **Policy details page**: Find **Policies** in the navigation menu, select an integration policy, then go to the **Endpoint exceptions** tab. If no exceptions are assigned yet, click **Add endpoint exception** to create a new one.

::::{important}
{{elastic-endpoint}} exceptions affect all {{elastic-endpoint}} alerts on matching hosts. Be careful not to unintentionally suppress useful alerts.
::::

The **Add Endpoint Exception** flyout opens.

1. Fill in the **Details** section:

    1. `Name`: Enter a name for the {{elastic-endpoint}} exception.
    2. (Optional) `Description`: Enter a description.

2. In the **Conditions** section, add conditions that define when the exception applies. When the exception's conditions match, {{elastic-endpoint}} does not generate an alert for that event.

    1. `Select operating system`: Select the appropriate operating system.
    2. `Field`: Select a field to identify the event being filtered.
    3. `Operator`: Select an operator to define the condition:

        * `is`
        * `is one of`
        * `matches` | `does not match`: Allows you to use wildcards in `Value`, such as `C:\path\*\app.exe`. Available wildcards are `?` (match one character) and `*` (match zero or more characters).

    4. `Value`: Enter the value associated with the `Field`. To enter multiple values (when using `is one of` or `is not one of`), enter each value, then press **Return**.

    ::::{note}
    Unlike detection rule exceptions, {{elastic-endpoint}} exceptions do not require escaping special characters. Enter file paths and values exactly as they appear on the host (for example, `C:\Windows\explorer.exe`, not `C:\\Windows\\explorer.exe`). Refer to [Exception types and value syntax](/solutions/security/manage-elastic-defend/exception-types-and-syntax.md) for syntax details and examples.
    ::::

    To define multiple conditions, click **AND** or **OR** and configure a new condition. You can also add [nested conditions](#nested-conditions).

3. Select an option in the **Assignment** section to assign the exception to a specific integration policy:

    * `Global`: Apply the exception to all {{elastic-defend}} integration policies.
    * `Per Policy`: Apply the exception to one or more specific {{elastic-defend}} integration policies. Select each policy where you want the exception to apply.

        ::::{note}
        You can also select `Per Policy` without immediately assigning a policy. This lets you create and review exception configurations before putting them into action with a policy.
        ::::

4. (Optional) Add a comment to provide more context about the exception.

5. Click **Add endpoint exception**.

::::{note}
It might take longer for exceptions to be applied to hosts within larger deployments.
::::

::::{tip}
To add multiple exceptions at once, you can import an NDJSON file instead. Refer to [Import and export {{elastic-endpoint}} exceptions](#import-export-endpoint-exceptions).
::::


## Nested conditions [nested-conditions]

Some {{elastic-endpoint}} fields require nested conditions to ensure the exception functions correctly. For details on which fields require nested conditions and an example, refer to [Nested conditions](/solutions/security/detect-and-alert/add-manage-exceptions.md#ex-nested-conditions).


## View and manage {{elastic-endpoint}} exceptions [manage-endpoint-exceptions]

The **Endpoint exceptions** tab on the **Artifacts** page displays all {{elastic-endpoint}} exceptions added to the {{security-app}}. To refine the list, use the search bar to search by name, description, or field value. You can also use the **Policies** filter to narrow the list by policy assignment:

* Select one or more policies to show only exceptions assigned to those policies.
* Under **Additional filters**, select **Global entries** to show exceptions assigned globally, or **Unassigned entries** to show exceptions not assigned to any policy.

:::{image} /solutions/images/security-endpoint-exceptions.png
:alt: List of Elastic Endpoint exceptions
:screenshot:
:::

### Import and export {{elastic-endpoint}} exceptions [import-export-endpoint-exceptions]

::::{admonition} Requirements
* To export {{elastic-endpoint}} exceptions, you need the **Endpoint Exceptions: Read** [privilege](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md).
* To import per-policy items, you need the **Endpoint Exceptions: All** privilege.
* To import global items, you need the **Endpoint Exceptions: All** and the **Global artifact management: All** privilege.
* To import items to a different space, you need the **Global artifact management: All** privilege.
::::

You can import and export {{elastic-endpoint}} exceptions as NDJSON files:

- **When the list is empty**: Click **Import Endpoint exceptions**.
- **When the list has entries**: Click the actions menu {icon}`boxes_vertical`, then select **Import Endpoint exceptions** or **Export Endpoint exceptions**.

::::{note}
The imported file must be an NDJSON file exported from {{kib}}. Files exported from third-party software are not supported.
::::

When you import an NDJSON file, the imported exceptions are appended to your existing exceptions — existing entries are not removed or overwritten.

::::{important}
In versions prior to 9.4, importing offered the option to remove all existing exceptions and replace them with the imported ones. Starting in 9.4, import always appends — existing exceptions are never removed. If you're upgrading from an earlier version, this applies whether or not you have opted in to per-policy exceptions.
::::

Items are processed individually on import — per-policy items that are not visible in the current space are skipped, while the remaining items are imported.

If an imported per-policy item is assigned to a policy that doesn't exist in the current environment, the item is imported with the policy assignment removed.

### Edit an {{elastic-endpoint}} exception [edit-endpoint-exception]

To edit an {{elastic-endpoint}} exception:

1. Click the actions menu ({icon}`boxes_vertical`) on the exception you want to edit, then select **Edit endpoint exception**.
2. Modify details as needed.
3. Click **Save**.


### Delete an {{elastic-endpoint}} exception [delete-endpoint-exception]

To delete an {{elastic-endpoint}} exception:

1. Click the actions menu ({icon}`boxes_vertical`) on the exception you want to delete, then select **Delete endpoint exception**.
2. On the confirmation dialog, click **Delete**. This removes the exception from all {{elastic-defend}} integration policies.
