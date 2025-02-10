# Manage detection rules [security-rules-ui-management]

The Rules page allows you to view and manage all prebuilt and custom detection rules.

:::{image} ../../../images/serverless--detections-all-rules.png
:alt: The Rules page
:class: screenshot
:::

On the Rules page, you can:

* [Sort and filter the rules list](../../../solutions/security/detect-and-alert/manage-detection-rules.md#sort-filter-rules)
* [Check the current status of rules](../../../solutions/security/detect-and-alert/manage-detection-rules.md#rule-status)
* [Modify existing rules settings](../../../solutions/security/detect-and-alert/manage-detection-rules.md#edit-rules-settings)
* [Manage rules](../../../solutions/security/detect-and-alert/manage-detection-rules.md#manage-rules-ui)
* [Manually run rules](../../../solutions/security/detect-and-alert/manage-detection-rules.md#manually-run-rules)
* [Snooze rule actions](../../../solutions/security/detect-and-alert/manage-detection-rules.md#snooze-rule-actions)
* [Export and import rules](../../../solutions/security/detect-and-alert/manage-detection-rules.md#import-export-rules-ui)
* [Confirm rule prerequisites](../../../solutions/security/detect-and-alert/manage-detection-rules.md#rule-prerequisites)
* [Troubleshoot missing alerts](../../../troubleshoot/security/detection-rules.md#troubleshoot-signals)


## Sort and filter the rules list [sort-filter-rules]

To sort the rules list, click any column header. To sort in descending order, click the column header again.

To filter the rules list, enter a search term in the search bar and press **Return**:

* Rule name — Enter a word or phrase from a rule’s name.
* Index pattern — Enter an index pattern (such as `filebeat-*`) to display all rules that use it.
* MITRE ATT&CK tactic or technique — Enter a MITRE ATT&CK tactic name (such as `Defense Evasion`) or technique number (such as `TA0005`) to display all associated rules.

::::{note}
Searches for index patterns and MITRE ATT&CK tactics and techniques must match exactly, are case sensitive, and do *not* support wildcards. For example, to find rules using the `filebeat-*` index pattern, the search term `filebeat-*` is valid, but `filebeat` and `file*` are not because they don’t exactly match the index pattern. Likewise, the MITRE ATT&CK tactic `Defense Evasion` is valid, but `Defense`, `defense evasion`, and `Defense*` are not.

::::


You can also filter the rules list by selecting the **Tags**, **Last response***, ***Elastic rules***, ***Custom rules***, ***Enabled rules**, and **Disabled rules** filters next to the search bar.

The rules list retains your sorting and filtering settings when you navigate away and return to the page. These settings are also preserved when you copy the page’s URL and paste into another browser. Select **Clear filters** above the table to revert to the default view.


## Check the current status of rules [rule-status]

The **Last response** column displays the current status of each rule, based on the most recent attempt to run the rule:

* **Succeeded**: The rule completed its defined search. This doesn’t necessarily mean it generated an alert, just that it ran without error.
* **Failed**: The rule encountered an error that prevented it from running. For example, a {{ml}} rule whose corresponding {{ml}} job wasn’t running.
* **Warning**: Nothing prevented the rule from running, but it might have returned unexpected results. For example, a custom query rule tried to search an index pattern that couldn’t be found in {{es}}.

For {{ml}} rules, an indicator icon (![Error](../../../images/serverless-warning.svg "")) also appears in this column if a required {{ml}} job isn’t running. Click the icon to list the affected jobs, then click **Visit rule details page to investigate** to open the rule’s details page, where you can start the {{ml}} job.


## Modify existing rules settings [edit-rules-settings]

You can edit an existing rule’s settings, and can bulk edit settings for multiple rules at once.

::::{note}
For prebuilt Elastic rules, you can’t modify most settings. You can only edit [rule actions](../../../solutions/security/detect-and-alert/create-detection-rule.md#rule-schedule) and [add exceptions](../../../solutions/security/detect-and-alert/add-manage-exceptions.md). If you try to bulk edit with both prebuilt and custom rules selected, the action will affect only the rules that can be modified.

Similarly, rules will be skipped if they can’t be modified by a bulk edit. For example, if you try to apply a tag to rules that already have that tag, or apply an index pattern to rules that use data views.

::::


1. Go to **Rules** → **Detection rules (SIEM)**.
2. Do one of the following:

    * **Edit a single rule**: Select the **All actions*** menu (![Actions menu](../../../images/serverless-boxesHorizontal.svg "")) on a rule, then select ***Edit rule settings**. The **Edit rule settings** view opens, where you can modify the [rule’s settings](../../../solutions/security/detect-and-alert/create-detection-rule.md).
    * **Bulk edit multiple rules**: Select the rules you want to edit, then select an action from the **Bulk actions** menu:

        * **Index patterns**: Add or delete the index patterns used by all selected rules.
        * **Tags**: Add or delete tags on all selected rules.
        * **Custom highlighted fields**: Add custom highlighted fields on all selected rules. You can choose any fields that are available in the [default {{elastic-sec}} indices](../../../solutions/security/get-started/configure-advanced-settings.md#update-sec-indices), or enter field names from other indices. To overwrite a rule’s current set of custom highlighted fields, select the **Overwrite all selected rules' custom highlighted fields** option, then click **Save**.
        * **Add rule actions**: Add [rule actions](../../../solutions/security/detect-and-alert/create-detection-rule.md) on all selected rules. If you add multiple actions, you can specify an action frequency for each of them. To overwrite the frequency of existing actions select the option to **Overwrite all selected rules actions**.

            ::::{note}
            Rule actions won’t run during a [maintenance window](../../../explore-analyze/alerts-cases/alerts/maintenance-windows.md). They’ll resume running after the maintenance window ends.

            ::::

    * **Update rule schedules**: Update the [schedules](../../../solutions/security/detect-and-alert/create-detection-rule.md#rule-schedule) and look-back times on all selected rules.
    * **Apply Timeline template**: Apply a specified [Timeline template](../../../solutions/security/investigate/timeline-templates.md) to the selected rules. You can also choose **None** to remove Timeline templates from the selected rules.

3. On the page or flyout that opens, update the rule settings and actions.

    ::::{tip}
    To [snooze](../../../solutions/security/detect-and-alert/manage-detection-rules.md#snooze-rule-actions) rule actions, go to the **Actions** tab and click the bell icon.

    ::::

4. If available, select **Overwrite all selected *x*** to overwrite the settings on the rules. For example, if you’re adding tags to multiple rules, selecting **Overwrite all selected rules tags** removes all the rules' original tags and replaces them with the tags you specify.
5. Click **Save**.


## Manage rules [manage-rules-ui]

You can duplicate, enable, disable, delete, and snooze actions for rules:

::::{note}
When duplicating a rule with exceptions, you can choose to duplicate the rule and its exceptions (active and expired), the rule and active exceptions only, or only the rule. If you duplicate the rule and its exceptions, copies of the exceptions are created and added to the duplicated rule’s [default rule list](../../../solutions/security/detect-and-alert/rule-exceptions.md). If the original rule used exceptions from a shared exception list, the duplicated rule will reference the same shared exception list.

::::


1. Go to **Rules** → **Detection rules (SIEM)**.
2. Do one of the following:

    * Select the **All actions** menu (![Actions menu](../../../images/serverless-boxesHorizontal.svg "")) on a rule, then select an action.
    * Select all the rules you want to modify, then select an action from the **Bulk actions** menu.
    * To enable or disable a single rule, switch on the rule’s **Enabled** toggle.
    * To [snooze](../../../solutions/security/detect-and-alert/manage-detection-rules.md#snooze-rule-actions) actions for rules, click the bell icon.



## Run rules manually [manually-run-rules]

[beta]

Manually run enabled rules for a specfied period of time for testing purposes or additional rule coverage.

::::{important}
Before manually running rules, make sure you properly understand and plan for rule dependencies. Incorrect scheduling can lead to inconsistent rule results.

::::


1. Navigate to the detection rules page, and do one of the following:

    * Select the **All actions** menu (![Actions menu](../../../images/serverless-boxesHorizontal.svg "")) on a rule, then select **Manual run**.
    * Select all the rules you want to manually run, select the **Bulk actions** menu, then select **Manual run**.

2. Specify when the manual run starts and ends. The default selection is the current day starting three hours in the past. The rule will search for events during the selected time range.
3. Click **Run** to manually run the rule.

    ::::{note}
    Manual runs can produce multiple rule executions. This is determined by the manual run’s time range and the rule’s execution schedule.

    ::::


The manual run’s details are shown in the [Manual runs](../../../solutions/security/detect-and-alert/monitor-rule-executions.md#manual-runs-table) table on the **Execution results** tab. Changes you make to the manual run or rule settings will display in the Manual runs table after the current run completes.

::::{note}
Be mindful of the following:

* Rule actions are not activated during manual runs.
* Except for threshold rules, duplicate alerts aren’t created if you manually run a rule during a time range that was already covered by a scheduled run.
* Manual runs are executed with low priority and limited concurrency, meaning they might take longer to complete. This can be especially apparent for rules requiring multiple executions.

::::



## Snooze rule actions [snooze-rule-actions]

Instead of turning rules off to stop alert notifications, you can snooze rule actions for a specified time period. When you snooze rule actions, the rule continues to run on its defined schedule, but won’t perform any actions or send alert notifications.

You can snooze notifications temporarily or indefinitely. When actions are snoozed, you can cancel or change the duration of the snoozed state. You can also schedule and manage recurring downtime for actions.

You can snooze rule notifications from the **Installed Rules** tab, the rule details page, or the **Actions** tab when editing a rule.

:::{image} ../../../images/serverless--detections-rule-snoozing.png
:alt: Rules snooze options
:class: screenshot
:::


## Export and import rules [import-export-rules-ui]

You can export custom detection rules to an `.ndjson` file, which you can then import into another {{elastic-sec}} environment.

::::{note}
You cannot export Elastic prebuilt rules, but you can duplicate a prebuilt rule, then export the duplicated rule.

If you try to export with both prebuilt and custom rules selected, only the custom rules are exported.

::::


The `.ndjson` file also includes any actions, connectors, and exception lists related to the exported rules. However, other configuration items require additional handling when exporting and importing rules:

* **Data views**: For rules that use a {{kib}} data view as a data source, the exported file contains the associated `data_view_id`, but does *not* include any other data view configuration. To export/import between {{kib}} spaces, first use the [Saved Objects](../../../explore-analyze/find-and-organize.md) UI (**Project settings*** → ***Stack Management** → **Saved Objects**) to share the data view with the destination space.

To import into a different {{stack}} deployment, the destination cluster must include a data view with a matching data view ID (configured in the [data view’s advanced settings](../../../explore-analyze/find-and-organize/data-views.md)). Alternatively, after importing, you can manually reconfigure the rule to use an appropriate data view in the destination system.

* **Actions and connectors**: Rule actions and connectors are included in the exported file, but sensitive information about the connector (such as authentication credentials) *is not* included. You must re-add missing connector details after importing detection rules.

    ::::{tip}
    You can also use the [Saved Objects](../../../explore-analyze/find-and-organize.md) UI (**Project settings** → **Stack Management** → **Saved Objects**) to export and import necessary connectors before importing detection rules.

    ::::

* **Value lists**: Any value lists used for rule exceptions are *not* included in rule exports or imports. Use the [Manage value lists](../../../solutions/security/detect-and-alert/create-manage-value-lists.md#manage-value-lists) UI (**Rules*** → ***Detection rules (SIEM)** → **Manage value lists**) to export and import value lists separately.

To export and import detection rules:

1. Go to **Rules** → **Detection rules (SIEM)**.
2. To export rules:

    1. In the rules table, select the rules you want to export.
    2. Select **Bulk actions** → **Export**, then save the exported file.

3. To import rules:

    ::::{note}
    To import rules with and without actions, and to manage rule connectors, you must have the appropriate user role. Refer to [Enable and access detections](../../../solutions/security/detect-and-alert/detections-requirements.md#enable-detections-ui) for more information.

    ::::


    1. Click **Import rules**.
    2. Drag and drop the file that contains the detection rules.

        ::::{note}
        Imported rules must be in an `.ndjson` file.

        ::::

    3. (Optional) Select **Overwrite existing detection rules with conflicting "rule_id"** to update existing rules if they match the `rule_id` value of any rules in the import file. Configuration data included with the rules, such as actions, is also overwritten.
    4. (Optional) Select **Overwrite existing exception lists with conflicting "list_id"** to replace existing exception lists with exception lists from the import file if they have a matching `list_id` value.
    5. (Optional) Select **Overwrite existing connectors with conflicting action "id"** to update existing connectors if they match the `action id` value of any rule actions in the import file. Configuration data included with the actions is also overwritten.
    6. Click **Import rule**.
    7. (Optional) If a connector is missing sensitive information after the import, a warning displays and you’re prompted to fix the connector. In the warning, click **Go to connector**. On the Connectors page, find the connector that needs to be updated, click **Fix**, then add the necessary details.



## Confirm rule prerequisites [rule-prerequisites]

Many detection rules are designed to work with specific [Elastic integrations](https://docs.elastic.co/en/integrations) and data fields. These prerequisites are identified in **Related integrations** and **Required fields*** on a rule’s details page (***Rules*** → ***Detection rules (SIEM)**, then click a rule’s name). **Related integrations** also displays each integration’s installation status and includes links for installing and configuring the listed integrations.

Additionally, the **Setup guide** section provides guidance on setting up the rule’s requirements.

:::{image} ../../../images/serverless--detections-rule-details-prerequisites.png
:alt: Rule details page with Related integrations
:class: screenshot
:::

You can also check rules' related integrations in the **Installed Rules** and **Rule Monitoring** tables. Click the **integrations** badge to display the related integrations in a popup.

:::{image} ../../../images/serverless--detections-rules-table-related-integrations.png
:alt: Rules table with related integrations popup
:class: screenshot
:::

::::{tip}
You can hide the **integrations** badge in the rules tables by turning off the `securitySolution:showRelatedIntegrations` advanced setting.

::::
