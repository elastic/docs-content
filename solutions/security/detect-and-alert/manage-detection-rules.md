---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/rules-ui-management.html
  - https://www.elastic.co/guide/en/serverless/current/security-rules-ui-management.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Manage detection rules [security-rules-ui-management]

The Rules page allows you to view and manage all prebuilt and custom detection rules.

:::{image} /solutions/images/security-all-rules.png
:alt: The Rules page
:screenshot:
:::

On the Rules page, you can:

* [Sort and filter the rules list](/solutions/security/detect-and-alert/manage-detection-rules.md#sort-filter-rules)
* [Check the current status of rules](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-status)
* [Modify existing rules settings](/solutions/security/detect-and-alert/manage-detection-rules.md#edit-rules-settings)
* [Manage rules](/solutions/security/detect-and-alert/manage-detection-rules.md#manage-rules-ui)
* [Run rules manually](/solutions/security/detect-and-alert/manage-detection-rules.md#manually-run-rules)
* [Snooze rule actions](/solutions/security/detect-and-alert/manage-detection-rules.md#snooze-rule-actions)
* [Export and import rules](/solutions/security/detect-and-alert/manage-detection-rules.md#import-export-rules-ui)
* [Confirm rule prerequisites](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-prerequisites)
* [Troubleshoot missing alerts](/troubleshoot/security/detection-rules.md#troubleshoot-signals)


## Sort and filter the rules list [sort-filter-rules]

To sort the rules list, click any column header. To sort in descending order, click the column header again.

To filter the rules list, enter a search term in the search bar and press **Return**:

* Rule name — Enter a word or phrase from a rule’s name.
* Index pattern — Enter an index pattern (such as `filebeat-*`) to display all rules that use it.
* MITRE ATT&CK tactic or technique — Enter a MITRE ATT&CK tactic name (such as `Defense Evasion`) or technique number (such as `TA0005`) to display all associated rules.

::::{note}
Searches for index patterns and MITRE ATT&CK tactics and techniques must match exactly, are case sensitive, and do *not* support wildcards. For example, to find rules using the `filebeat-*` index pattern, the search term `filebeat-*` is valid, but `filebeat` and `file*` are not because they don’t exactly match the index pattern. Likewise, the MITRE ATT&CK tactic `Defense Evasion` is valid, but `Defense`, `defense evasion`, and `Defense*` are not.
::::


You can also filter the rules list by selecting the **Tags**, **Last response**, **Elastic rules**, **Custom rules**, **Enabled rules**, and **Disabled rules** filters next to the search bar.

The rules list retains your sorting and filtering settings when you navigate away and return to the page. These settings are also preserved when you copy the page’s URL and paste into another browser. Select **Clear filters** above the table to revert to the default view.


## Check the current status of rules [rule-status]

The **Last response** column displays the current status of each rule, based on the most recent attempt to run the rule:

* **Succeeded**: The rule completed its defined search. This doesn’t necessarily mean it generated an alert, just that it ran without error.
* **Failed**: The rule encountered an error that prevented it from running. For example, a {{ml}} rule whose corresponding {{ml}} job wasn’t running.
* **Warning**: Nothing prevented the rule from running, but it might have returned unexpected results. For example, a custom query rule tried to search an index pattern that couldn’t be found in {{es}}.

For {{ml}} rules, an indicator icon (![Error icon from rules table](/solutions/images/security-rules-table-error-icon.png "title =20x20")) also appears in this column if a required {{ml}} job isn’t running. Click the icon to list the affected jobs, then click **Visit rule details page to investigate** to open the rule’s details page, where you can start the {{ml}} job.


## Modify existing rules settings [edit-rules-settings]

::::{admonition} Requirements
* You can edit custom rules and bulk-modify them with any [{{stack}} subscription](https://www.elastic.co/pricing) or [{{serverless-short}} project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md).
* You can edit [rule notifications](/solutions/security/detect-and-alert/create-detection-rule.md#rule-notifications) (notifications and response actions) for prebuilt rules with any {{stack}} subscription or {{serverless-short}} project feature tier.
* You must have an [Enterprise subscription](https://www.elastic.co/pricing) {{stack}} or a [Security Analytics Complete project](../../../deploy-manage/deploy/elastic-cloud/project-settings.md) on {{serverless-short}} to edit all prebuilt rule settings (except for the **Author** and **License** fields) and bulk-modify them.

::::


1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Do one of the following:

    * Edit a single rule: Select the **All actions** menu (**…**) on a rule, then select **Edit rule settings**. Alternatively, open the rule’s details page and click **Edit rule settings**. The **Edit rule settings** view opens, where you can modify the [rule’s settings](/solutions/security/detect-and-alert/create-detection-rule.md).
    * Bulk edit multiple rules: Select the rules you want to edit, then select an action from the **Bulk actions** menu:

        ::::{note}
        Rules will be skipped if they can’t be modified by a bulk edit. For example, if you try to apply a tag to rules that already have that tag, or apply an index pattern to rules that use data views.
        ::::

        * **Index patterns**: Add or delete the index patterns used by all selected rules.
        * **Tags**: Add or delete tags on all selected rules.
        * **Custom highlighted fields**: Add custom highlighted fields on all selected rules. You can choose any fields that are available in the [default {{elastic-sec}} indices](/solutions/security/get-started/configure-advanced-settings.md#update-sec-indices), or enter field names from other indices. To overwrite a rule’s current set of custom highlighted fields, select the **Overwrite all selected rules' custom highlighted fields** option, then click **Save**.
        * **Add rule actions**: Add [rule actions](/solutions/security/detect-and-alert/create-detection-rule.md#rule-notifications) on all selected rules. If you add multiple actions, you can specify an action frequency for each of them. To overwrite the frequency of existing actions select the option to **Overwrite all selected rules actions**.

        ::::{important}
        After upgrading to {{stack}} 8.8 or later, frequency settings for rule actions created in 8.7 or earlier are moved from the rule level to the action level. The action schedules remain the same and will continue to run on their previously specified frequency (`On each rule execution`, `Hourly`, `Daily`, or `Weekly`).
        ::::


        :::{note}
        Rule actions won’t run during a [maintenance window](/explore-analyze/alerts-cases/alerts/maintenance-windows.md). They’ll resume running after the maintenance window ends.
        ::::


        * **Update rule schedules**: Update the [schedules](/solutions/security/detect-and-alert/create-detection-rule.md#rule-schedule) and look-back times on all selected rules.
        * **Apply Timeline template**: Apply a specified [Timeline template](/solutions/security/investigate/timeline-templates.md) to the selected rules. You can also choose **None** to remove Timeline templates from the selected rules.

3. On the page or flyout that opens, update the rule settings and actions.

    ::::{tip}
    To [snooze](/solutions/security/detect-and-alert/manage-detection-rules.md#snooze-rule-actions) rule actions, go to the **Actions** tab and click the bell icon.
    ::::

4. If available, select **Overwrite all selected _x_** to overwrite the settings on the rules. For example, if you’re adding tags to multiple rules, selecting **Overwrite all selected rules tags** removes all the rules' original tags and replaces them with the tags you specify.
5. Click **Save**.

::::{note}

```{applies_to}
   stack: ga 9.1 
```

Modified fields on prebuilt rules are marked with the **Modified** badge. From the rule's details page, click the badge to view the changed fields. Changes are displayed in a side-by-side comparison of the original Elastic version and the modified version. Deleted characters are highlighted in red; added characters are highlighted in green. You can also view this comparison by clicking the **Modified Elastic rule** badge under the rule's name on the rule's details page.

::::

## Revert modifications to prebuilt rules [revert-rule-changes]

```{applies_to}
   stack: ga 9.1 
```

After modifying a prebuilt rule, you can restore it's original version. To do this:

1. Open the rule's details page, click the **All actions** menu, then **Revert to Elastic version**.
2. In the flyout, review the modified fields. Deleted characters are highlighted in red; added characters are highlighted in green.
3. Click **Revert** to restore the modified fields to their original versions. 

::::{note}
If you haven’t updated the rule in a while, its original version might be unavailable for comparison. You can avoid this by regularly updating prebuilt rules.
::::


## Manage rules [manage-rules-ui]

You can duplicate, enable, disable, delete, and do more to rules:

::::{note}
When duplicating a rule with exceptions, you can choose to duplicate the rule and its exceptions (active and expired), the rule and active exceptions only, or only the rule. If you duplicate the rule and its exceptions, copies of the exceptions are created and added to the duplicated rule’s [default rule list](/solutions/security/detect-and-alert/rule-exceptions.md). If the original rule used exceptions from a shared exception list, the duplicated rule will reference the same shared exception list.
::::


1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the Rules table, do one of the following:

    * Select the **All actions** menu (**…**) on a rule, then select an action.
    * Select all the rules you want to modify, then select an action from the **Bulk actions** menu.
    * To enable or disable a single rule, switch on the rule’s **Enabled** toggle.
    * To [snooze](/solutions/security/detect-and-alert/manage-detection-rules.md#snooze-rule-actions) actions for rules, click the bell icon.



## Run rules manually [manually-run-rules]

Manually run enabled rules for a specified period of time to deliberately test them, provide additional rule coverage, or fill gaps in rule executions.

::::{important}
Before manually running rules, make sure you properly understand and plan for rule dependencies. Incorrect scheduling can lead to inconsistent rule results.
::::


1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the **Rules** table, do one of the following:

    * Select the **All actions** menu (**…**) on a rule, then select **Manual run**.
    * Select all the rules you want to manually run, select the **Bulk actions** menu, then select **Manual run**.

3. Specify when the manual run starts and ends. The default selection is the current day starting three hours in the past. The rule will search for events during the selected time range.
4. Click **Run** to manually run the rule.

The rule will run over the time range that you selected. Note that all [rule actions](/solutions/security/detect-and-alert/create-detection-rule.md#rule-notifications) will also be activated, except for **Summary of alerts** actions that run at a custom frequency.

Go to the [Manual runs table](/solutions/security/detect-and-alert/monitor-rule-executions.md#manual-runs-table) on the **Execution results** tab to track the manual rule executions. If you manually ran the rule over a gap, you can also monitor the gap fill's progress from the [Gaps table](/solutions/security/detect-and-alert/monitor-rule-executions.md#gaps-table).

::::{note}
Be mindful of the following:

* Any changes that you make to the manual run or rule settings will display in the Manual runs table after the current run completes.
* Except for threshold rules, duplicate alerts aren't created if you manually run a rule during a time range that was already covered by a scheduled run.
* Manually running a custom query rule with suppression may incorrectly inflate the number of suppressed alerts.

::::

## Fill gaps for multiple rules [bulk-fill-gaps-multiple-rules]

```{applies_to}
   stack: ga 9.1
```

From the Rules table, fill gaps for multiple rules by using the **Fill gaps** bulk action.

1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the Rules table, click the **Rule Monitoring** tab, then do one of the following:

   * Fill rules with unfilled or partially filled gaps: Select the appropriate rules or all rules on the page, then click **Bulk actions → Fill gaps**.
   
   * Only fill rules with unfilled gaps: In the panel above the table, click the **Only rules with unfilled gaps** filter to only show rules with unfilled gaps (rules with gaps that are being filled are excluded). Select the appropriate rules or all of them, then click **Bulk actions → Fill gaps**. 

3. Specify when to start and end the manual run that will fill the gaps. 
4. Click **Schedule gap fills**. The rule will manually run over unfilled gaps in the selected time range. 

After scheduling the manual run, you can track gap fill progress by checking the **Total rules with gaps:** field in the panel above the Rules table. The field displays two metrics separated by a forward slash. The metric on the left tells you the remaining number of rules with unfilled gaps. The metric on the right tells you the number of rules that are currently having their gaps filled. 

Alternatively, you can check gap fill progress for individual rules by going to their details page, clicking the **Execution results** tab, then going to the [Gaps table](/solutions/security/detect-and-alert/monitor-rule-executions.md#gaps-table).
 

## Snooze rule actions [snooze-rule-actions]

Instead of turning rules off to stop alert notifications, you can snooze rule actions for a specified time period. When you snooze rule actions, the rule continues to run on its defined schedule, but won’t perform any actions or send alert notifications.

You can snooze notifications temporarily or indefinitely. When actions are snoozed, you can cancel or change the duration of the snoozed state. You can also schedule and manage recurring downtime for actions.

You can snooze rule notifications from the **Installed Rules** tab, the rule details page, or the **Actions** tab when editing a rule.

:::{image} /solutions/images/security-rule-snoozing.png
:alt: Rules snooze options
:width: 75%
:screenshot:
:::


## Export and import rules [import-export-rules-ui]

::::{admonition} Requirements
* You can export and import custom rules and prebuilt rules (modified and unmodified) with any [{{stack}} subscription](https://www.elastic.co/pricing) or [{{serverless-short}} project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md).
* At minimum, your role needs `Read` privileges for the **Action and Connectors** feature to import rules with actions. To overwrite or add new connectors, you need `All` privileges. Refer to [Enable and access detections](/solutions/security/detect-and-alert/detections-requirements.md#enable-detections-ui) to learn more about the required privileges for managing rules.
::::

You can export custom detection rules to an `.ndjson` file, which you can then import into another {{elastic-sec}} environment.

The `.ndjson` file also includes any actions, connectors, and exception lists related to the exported rules. However, other configuration items require additional handling when exporting and importing rules:

* **Data views**: For rules that use a {{kib}} data view as a data source, the exported file contains the associated `data_view_id`, but does *not* include any other data view configuration. To export/import between {{kib}} spaces, first use the [Saved Objects](/explore-analyze/find-and-organize/saved-objects.md#managing-saved-objects-share-to-space) UI to share the data view with the destination space.

    To import into a different {{stack}} deployment, the destination cluster must include a data view with a matching data view ID (configured in the [data view’s advanced settings](/explore-analyze/find-and-organize/data-views.md)). Alternatively, after importing, you can manually reconfigure the rule to use an appropriate data view in the destination system.

* **Actions and connectors**: Rule actions and connectors are included in the exported file, but sensitive information about the connector (such as authentication credentials) *is not* included. You must re-add missing connector details after importing detection rules.

    ::::{tip}
    You can also use the [Saved Objects](/explore-analyze/find-and-organize/saved-objects.md#saved-objects-export) UI to export and import necessary connectors before importing detection rules.
    ::::

* **Value lists**: Any value lists used for rule exceptions are *not* included in rule exports or imports. Use the [Manage value lists](/solutions/security/detect-and-alert/create-manage-value-lists.md#edit-value-lists) UI to export and import value lists separately.

### Export rules [export-rules-ui]

1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Do one of the following:

    * Export a single rule: Find the rule in the Rules table, then select **All actions** → **Export**. Alternatively, export the rule from its details page (click on the rule name to open its details, then click **All actions** → **Export**).
    * Export multiple rules: In the Rules table, select the rules you want to export, then click **Bulk actions → Export**.

The rules are exported to an `.ndjson` file.

### Import rules [impr=ort-rules-ui]

1. Above the Rules table, click *Import rules*.
2. In the Import rules modal:

    1. Drag and drop the `.ndjson` file that contains the exported rules.
    2. (Optional) Select the appropriate options to overwrite existing data:

        * **Overwrite existing detection rules with conflicting "rule_id"**: Updates existing rules if they match the `rule_id` value of any rules in the import file. Configuration data included with the rules, such as actions, is also overwritten.
        * **Overwrite existing exception lists with conflicting "list_id"**: Replaces existing exception lists with exception lists from the import file if they have a matching `list_id` value.
        * **Overwrite existing connectors with conflicting action "id"**: Updates existing connectors if they match the `action id` value of any rule actions in the import file. Configuration data included with the actions is also overwritten.

The imported rules are added to the Rules table.


## Confirm rule prerequisites [rule-prerequisites]

Many detection rules are designed to work with specific [Elastic integrations](https://docs.elastic.co/en/integrations) and data fields. These prerequisites are identified in **Related integrations** and **Required fields** on a rule’s details page. **Related integrations** also displays each integration’s installation status and includes links for installing and configuring the listed integrations.

Additionally, the **Setup guide** section provides guidance on setting up the rule’s requirements.

:::{image} /solutions/images/security-rule-details-prerequisites.png
:alt: Rule details page with Related integrations
:screenshot:
:::

You can also check rules' related integrations in the **Installed Rules** and **Rule Monitoring** tables. Click the **integrations** badge to display the related integrations in a popup.

:::{image} /solutions/images/security-rules-table-related-integrations.png
:alt: Rules table with related integrations popup
:screenshot:
:::

::::{tip}
You can hide the **integrations** badge in the Rules tables by turning off the `securitySolution:showRelatedIntegrations` [advanced setting](/solutions/security/get-started/configure-advanced-settings.md#show-related-integrations).
::::

## Manage rules as code [manage-rule-dac]

Utilize the [Detection-as-Code](https://dac-reference.readthedocs.io/en/latest/dac_concept_and_workflows.html) (DaC) principles to externally manage your detection rules.

The {{elastic-sec}} Labs team uses the [detection-rules](https://github.com/elastic/detection-rules) repo to develop, test, and release {{elastic-sec}}'s[ prebuilt rules](https://github.com/elastic/detection-rules/tree/main/rules). The repo provides DaC features and allows you to customize settings to simplify the setup for managing user rules with the DaCe pipeline.

To get started, refer to the [DaC documentation](https://github.com/elastic/detection-rules/blob/main/README.md#detections-as-code-dac).