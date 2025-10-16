---
applies_to:
  stack: preview 9.0, ga 9.1
  serverless:
    security: ga
---

# Automatic migration

Automatic Migration for detection rules helps you quickly migrate Splunk assets to {{elastic-sec}}. The following asset types are supported:

* {applies_to}`stack: preview 9.0, ga 9.1` {applies_to}`serverless: ga` Splunk rules
* {applies_to}`stack: preview 9.2` {applies_to}`serverless: preview` Splunk dashboards

For rule migrations, if comparable Elastic-authored rules exist, Automatic Migration simplifies onboarding by mapping your rules to them. Otherwise, it creates custom rules and dashboards on the fly so you can verify and edit them instead of writing them from scratch.

You can ingest your data before migrating your assets, or migrate your assets first in which case the tool will recommend which data sources you need to power your migrated rules.

::::{admonition} Requirements
* The `SIEM migrations: All` Security sub-feature privilege.
* A working [LLM connector](/solutions/security/ai/set-up-connectors-for-large-language-models-llm.md).
* {{stack}} users: an [Enterprise](https://www.elastic.co/pricing) subscription.
* {{Stack}} users: {{ml}} must be enabled.
* {{serverless-short}} users: a [Security Complete](/deploy-manage/deploy/elastic-cloud/project-settings.md) subscription.
* {{ecloud}} users: {{ml}} must be enabled. We recommend a minimum size of 4GB of RAM per {{ml}} zone.
::::

## Get started with Automatic Migration

1. Find **Get started** in the navigation menu or use the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Under **Configure AI provider**, select a configured model or [add a new one](/solutions/security/ai/set-up-connectors-for-large-language-models-llm.md). For information on how different models perform, refer to the [LLM performance matrix](/solutions/security/ai/large-language-model-performance-matrix.md).
3. Next, under **Migrate rules & dashboards**, select either **Translate your existing SIEM rules to Elastic** or **Migrate your existing SIEM dashboards to Elastic**, then click **Upload**. The upload flyout appears. 
4. Follow the instructions on the upload flyout to export your Splunk assets as JSON.

   :::{image} /solutions/images/security-siem-migration-1.png
   :alt: the Upload Splunk SIEM rules flyout
   :width: 700px
   :screenshot:
   :::


   ::::{note}
   The provided queries download a default selection of Splunk assets. Alternatively, as long as you export your results as JSON, you can use a different query. For example, the following custom query would download rules related to just the `splunksysmonsecurity` app:

   ```
   | rest /servicesNS/-/-/saved/searches
   | search is_scheduled=1 AND eai:acl.app=splunksysmonsecurity
   | where disabled=0
   | table id, title, search, description, action.escu.eli5,
   ```

   We don't recommend downloading all searches (for example with `| rest /servicesNS/-/-/saved/searches`) since much of the data would be irrelevant to asset migration.
   ::::

5. Select your JSON file and click **Upload**. If the file is large, you may need to separate it into multiple parts and upload them individually to avoid exceeding your LLM's context window.

6. After you upload your Splunk assets, Automatic Migration will detect whether they use any macros or lookups. If so, follow the instructions which appear to export and upload them. Alternatively, you can complete this step later — however, until you upload them, some of your migrated assets will have a `partially translated` status. If you upload them now, you don't have to wait on the page for them to be processed — a notification will appear when processing is complete.

7. Click **Translate** to start the rule translation process. The **Start rules migration** popup appears. Use the dropdown menu to select which AI connector to use. For rule migrations there is a **Match to Elastic prebuilt rules** option, which is enabled by default; when it's enabled, any rules you translate that are similar to Elastic prebuilt rules are converted to those prebuilt rules. When it's disabled, each of your rules will be converted into a new custom rule. 
8. Click **Translate**. A name for the migration is automatically created, and you can track its progress on this page. The **More actions** ({icon}`boxes_vertical`) button lets you rename or delete the migration. 

   ::::{image} /solutions/images/security-siem-migration-rule-status-more-actions.png
   :alt: The rule migration status view
   :width: 850px
   :screenshot:
   ::::

   You don't need to stay on this page. A notification will appear when the migration is complete.


9. Use the **Add SIEM data with Integrations** section to set up data ingestion from third-party sources. If at least one migration has completed, the **Recommended** tab shows integrations that provide the data needed by your translated assets. These include both Elastic-managed integrations and any applicable custom creations you made using [automatic import](/solutions/security/get-started/automatic-import.md).

   ::::{image} /solutions/images/security-siem-migration-integrations-panel.png
   :alt: The add integrations panel.
   :width: 850px
   :screenshot:
   ::::

10. When migration is complete, click the notification or return to the **Get started** page then click **View translated rules** to open the **Translated rules** page. 


## The Translated rules page

This section describes the **Translated rules** page's interface and the data it displays.

Use the **Migrations** dropdown menu in the upper right to select which migration appears. 

::::{image} /solutions/images/security-siem-migration-processed-rules.png
:alt: The translated rules page
:width: 850px
:screenshot:
::::

The table's fields are as follows:

* **Name:** The names of Elastic-authored rules cannot be edited until after rule installation. To edit the name of a custom translated rule, click the name and select **Edit**.
* **Status:** The rule's translation status:
  * `Installed`: Already added to Elastic SIEM. Click **View** to manage and enable it.
  * `Translated`: Ready to install. This rule was mapped to an Elastic-authored rule, or translated by Automatic Import. Click **Install** to install it.
  * `Partially translated`: Part of the query could not be translated. You may need to specify an index pattern for the rule query, upload missing macros or lookups, or fix broken rule syntax. 
    ::::{note}
    To fix partially translated rules that are missing an index pattern, use the **Update missing index pattern** button. This affects all migrated assets that contain the placeholder `[indexPattern]`, not just those currently visibly on the table page.
    ::::
  * `Not translated`: None of the original query could be translated.
  * `Error`: Translation failed. Refer to the the error details.
* **Risk Score:** For Elastic-authored rules, risk scores are predefined. For custom translated rules, risk scores are defined as follows:
  * If the source rule has a field comparable to Elastic's `risk score`, we use that value.
  * Otherwise, if the source rule has a field comparable to Elastic's `rule severity` field, we base the risk score on that value according to [these guidelines](/solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-basic-params).
  * If neither of the above apply, we assign a default value.
* **Rule severity:** For Elastic-authored rules, severity scores are predefined. For custom translated rules, risk scores are based on the source rule's severity field. Splunk severity scores are translated to Elastic rule severity scores as follows:

  | Splunk severity | Elastic rule severity |
  | ------- | ----------- |
  | 1 (Info)     | Low      |
  | 2 (Low)      | Low      |
  | 3 (Medium)   | Medium   |
  | 4 (High)     | High     |
  | 5 (Critical) | Critical |

* **Author:** Shows one of two possible values: `Elastic`, or `Custom`. Elastic-authored rules are created by Elastic and update automatically. Custom rules are translated by the Automatic Migration tool or your team, and do not update automatically.
* **Integrations:** Shows the number of Elastic integrations that must be installed to provide data for the rule to run successfully.
* **Actions:** 
  * To add a rule to Elastic, select one or more `translated` rules then click **Install**. Then select them again and click **Enable**.
  * To reprocess a rule using the same or a different LLM connector, select one or more rules that weren't successfully translated then click **Reprocess**. A menu appears where you can select which AI connector to use. 

::::{image} /solutions/images/security-siem-migration-reprocess-modal.png
:alt: The reprocess rule modal
:width: 450px
:screenshot:
::::

## Finalize translated assets

Once you're on the **Translated rules** or **Translated dashboards** page, to install any assets that were partially translated or not translated, you will need to edit them. Optionally, you can also edit custom assets that were successfully translated to finetune them.

:::{note}
You cannot edit Elastic-authored rules using this interface, but after they are installed you can [edit them](/solutions/security/detect-and-alert/manage-detection-rules.md) from the **Rules** page.
:::

### Edit a custom rule

Click the rule's name to open the rule's details flyout to the **Translation** tab, which shows the source rule alongside the translated — or partially translated — Elastic version. You can update any part of the rule. When finished, click **Save**.

::::{image} /solutions/images/security-siem-migration-edit-rule.png
:alt: The rule details flyout
:width: 850px
:screenshot:
::::

::::{note}
If you haven't yet ingested your data, you will likely encounter `Unknown index` or `Unknown column` errors while editing. You can ignore these and add your data later.
::::

### View rule details

The rule details flyout (which appears when you click on a rule's name in the **Translate rules** table) has two other tabs, **Overview** and **Summary**. The **Overview** tab displays information such as the rule's severity, risk score, rule type, and how frequently it runs. The **Summary** tab explains the logic behind how the rule was translated, such as why specific {{esql}} commands were used, or why a source rule was mapped to a particular Elastic-authored rule.

::::{important}
All the details about your migrations is stored in the `.kibana-siem-rule-migrations-rules-default` index. You can use [Discover](/explore-analyze/discover.md) to review a variety of metrics, analyze metrics, and more.
::::

## Frequently asked questions (FAQ)

**How does Automatic Migration handle assets that can't be exactly translated for various reasons, such as feature parity issues?**

After translation, assets that can't be translated appear with a status of either partially translated (yellow) or not translated (red). From there, you can address them individually.

**Are nested macros supported?**

Yes, Automatic Migration can handle nested macros.

**How can we ensure rules stay up to date?**

With the exception of rules that were matched to Elastic-authored rules (which are updated automatically), assets created by Automatic Migration must be maintained by you.

**What index does information about each migration appear in?**

No matter how many times you use Automatic Migration, migration data will continue to appear in `.kibana-siem-rule-migrations-rules-default`.

**How does Automatic Migration handle Splunk assets which lookup other indices?**

Assets that fall into this category will typically appear with a status of partially translated. You can use the [`LOOKUP JOIN`](elasticsearch://reference/query-languages/esql/esql-lookup-join.md) capability to help in this situation.
