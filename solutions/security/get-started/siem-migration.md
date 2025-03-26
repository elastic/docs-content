# AI-powered SIEM migration

::::{warning}
This feature is in technical preview. It may change in the future, and you should exercise caution when using it in production environments. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of GA features.
::::

Elastic's AI-powered SIEM migration helps you quickly convert SIEM rules from the Splunk Processing Language (SPL) to the Elasticsearch Query Language ({{esql}}). It simplifies onboarding by matching your rules to Elastic-authored rules, if comparable rules exist. Otherwise, it automatically translates rules on the fly so you can verify and edit them instead of rewriting them from scratch.

You can ingest your data before migrating your rules, or migrate your rules first, in which case the tool will recommend which data sources you need to power your migrated rules. 

::::{admonition} Requirements
* The `SIEM migrations: All` Security sub-feature privilege.
* A working [LLM connector](/solutions/security/ai/set-up-connectors-for-large-language-models-llm.md).
* {{stack}} users: an [Enterprise](https://www.elastic.co/pricing) subscription. 
* {{Stack}} users: {{ml}} must be enabled.
* {{serverless-short}} users: a [Security Complete](../../../deploy-manage/deploy/elastic-cloud/project-settings.md) subscription.

::::

## Get started with AI-powered SIEM migration

1. Find **Get started** in the navigation menu or use the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Under **Configure AI provider** select a model, or [add a new one](/solutions/security/ai/set-up-connectors-for-large-language-models-llm.md). For information on how different models perform, refer to the [LLM performance matrix](../../../solutions/security/ai/large-language-model-performance-matrix.md).
3. Next, under **Migrate rules & add data**, click **Translate your existing SIEM rules to Elastic**, then **Upload rules**.
4. Follow the instructions on the **Upload Splunk SIEM rules** flyout to export your rules from Splunk as JSON. 

   :::{image} ../../../images/security-siem-migration-1.png
   :alt: the Upload Splunk SIEM rules flyout
   :width: 700px
   :screenshot:
   :::


   ::::{note}
   The provided query downloads Splunk correlation rules and saved searches. Alternatively, as long as you    export your results in a JSON format, you can use a different query. For example:

   ```
   | rest /servicesNS/-/-/saved/searches
   | search is_scheduled=1 AND eai:acl.app=splunksysmonsecurity
   | where disabled=0
   | table id, title, search, description, action.escu.eli5, 
   ```
   Which would download rules related to just the `splunksysmonsecurity` app.

   We don't recommend downloading all searches (for example with `| rest /servicesNS/-/-/saved/searches`) since most of the data will be irrelevant to SIEM rule migration. 
   ::::

5. Select your JSON file and click **Upload**. 
   ::::{note}
   If the file is large, you may need to separate it into multiple parts and upload them individually to avoid exceeding your LLM's context window.
   ::::

6. After you upload your Splunk rules, SIEM migration will detect whether they use any Splunk macros or lookups. If so, follow the instructions which appear to export and upload them. Alternatively, you can complete this step later — however, until you upload them, some of your migrated rules will have a `partially translated` status. If you upload them now, you don't have to wait on the page for them to be processed — a notification will appear when processing is complete.

7. Click **Translate** to start the rule translation process. You don't need to stay on this page. A notification will appear when the process is complete. 

8. When migration is complete, click the notification or return to the **Get started** page then click **View translated rules** to open the **Translated rules** page. 


## The Translated rules page

This section describes the **Translated rules** page's interface and explains how the data that appears here is derived. 

When you upload a new batch of rules, they are assigned a name and number, for example `SIEM rule migration 1`, or `SIEM rule migration 2`. Use the **Migrations** dropdown menu in the upper right to select which batch appears. 

::::{image} ../../../images/security-siem-migration-processed-rules.png
:alt: The translated rules page
:width: 850px
:screenshot:
::::

The table's fields are as follows:

* **Name:** The names of Elastic authored rules cannot be edited until after rule installation. To edit the name of a custom translated rule, click the name and select **Edit**.
* **Status:** The rule's translation status.
* **Risk Score:** For Elastic authored rules, risk scores are predefined. For custom translated rules, risk scores are defined as follows:
  * If the source rule has a field comparable to Elastic's risk score, we use that value.
  * Otherwise, if the source rule has a field comparable to Elastic's rule severity field, we base the risk score on that value according to these [guidelines](/solutions/security/detect-and-alert/create-detection-rule.md#custom-highlighted-esql-fields).
  * Otherwise, a default value is assigned.
* **Rule severity:** For Elastic authored rules, severity scores are predefined. For custom translated rules, risk scores are based on the source rule's severity field. Splunk severity scores are translated to Elastic rule severity scores as follows:

  | Splunk severity | Elastic rule severity |
  | ------- | ----------- |
  | 1 (Info)     | Low      |
  | 2 (Low)      | Low      |
  | 3 (Medium)   | Medium   |
  | 4 (High)     | High     |
  | 5 (Critical) | Critical |

* **Author:** Shows one of two possible values: `Elastic`, or `Custom`. Elastic authored rules are created by Elastic and update automatically. Custom rules are translated by the SIEM migration tool or your team, and do not update automatically.
* **Integrations:** Shows the number of Elastic integrations that must be installed to provide data for the rule to run successfully.
* **Actions:** Allows you to click **Install** to add a rule to Elastic. Installed rules must also be enabled before they will run. To install rules in bulk, select the check box at the top of the table before clicking **Install**.

## Finalize translated rules

Once you're on the **Translated rules** page, to install any rules that were partially translated or not translated, you will need to edit them. Optionally, you can also edit custom rules that were successfully translated to finetune them. 

:::{note}
You cannot edit Elastic authored rules using this interface, but after they are installed you can edit them from the [**Rules**](/solutions/security/detect-and-alert/about-detection-rules.md) page. 
:::
  
### Edit a custom rule

Click the rule's name to open the rule's details flyout to the **Translation** tab, which shows the source rule alongside the translated — or partially translated — Elastic version. You can update any part of the rule. When finished, click **Save**.

::::{image} ../../../images/security-siem-migration-edit-rule.png
:alt: The rule details flyout
:width: 850px
:screenshot:
::::

::::{note}
If you haven't yet ingested your data, you will likely encounter `Unknown index` or `Unknown column` errors while editing. You can ignore these and add your data later.
::::

### View rule details

The rule details flyout which appears when you click on a rule's name in the **Translate rules** table has two other tabs, **Overview** and **Summary**. The **Overview** tab displays information such as the rule's severity, risk score, rule type, and how frequently it runs. The **Summary** tab explains the logic behind how the rule was translated, such as why specific {{esql}} commands were used, or why a source rule was mapped to a particular Elastic authored rule.

