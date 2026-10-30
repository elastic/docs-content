---
navigation_title: Migrate
description: Migrate Splunk, QRadar, and Microsoft Sentinel rules and dashboards to Elastic Security with Automatic Migration. Review, fix, and install translated rules, including from Agent Builder chat.
applies_to:
  stack: preview =9.0, ga 9.1+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Migrate to {{elastic-sec}} with Automatic Migration

Move your detection rules and dashboards from Microsoft Sentinel, Splunk, or QRadar to {{elastic-sec}} without rebuilding them by hand. Automatic Migration translates them into {{elastic-sec}} rules and dashboards that you can review and edit. It supports the following asset types:

* {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview` Microsoft Sentinel rules
* {applies_to}`stack: ga 9.4+, preview 9.2-9.3` {applies_to}`serverless: ga` Splunk Classic dashboards (v1.1)
* {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` Splunk Dashboard Studio dashboards
* {applies_to}`stack: preview =9.0, ga 9.1+` {applies_to}`serverless: ga` Splunk rules
* {applies_to}`stack: ga 9.4+, preview 9.3` {applies_to}`serverless: ga` QRadar rules

The following table summarizes which assets Automatic Migration can and cannot translate:

| Source platform | Asset type | Supported |
| --- | --- | --- |
| Splunk | Rules (saved searches) | Yes |
| Splunk | Classic dashboards (v1.1) | Yes |
| Splunk | Dashboard Studio dashboards | Yes |
| QRadar | Rules | Yes |
| QRadar | Dashboards | No |
| Microsoft Sentinel | Rules | Yes |

For rule migrations, if comparable Elastic-authored rules exist, Automatic Migration simplifies onboarding by mapping your rules to them. Otherwise, it creates custom rules and dashboards on the fly so you can verify and edit them instead of writing them from scratch.

You can ingest your data before migrating your assets, or migrate your assets first in which case the tool recommends which data sources you need to power your migrated rules.

::::{applies-switch}

:::{applies-item} { "stack": "ga 9.4+", "serverless": "ga" }
**Requirements**

* Minimum [{{kib}} privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for these **Security** features:

  - `All` for **SIEM migrations**
  - At least `Read` for **Rules**
* A working [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md).
* {{stack}} users: an [Enterprise](https://www.elastic.co/pricing) subscription.
* {{Stack}} users: {{ml}} must be enabled.
* {{serverless-short}} users: a [Security Complete](/deploy-manage/deploy/elastic-cloud/project-settings.md) subscription.
* {{ecloud}} users: {{ml}} must be enabled. We recommend a minimum size of 4GB of RAM per {{ml}} zone.
* {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` To use [{{agent-builder}}](#siem-migration-agent-builder):

  - At least `Read` [privileges](/explore-analyze/ai-features/agent-builder/permissions.md#kib-privileges) for **Agent Builder**.
  - {{agent-builder}} as the [chat experience](/solutions/security/ai/set-up-ai-features.md#set-up-ai-chat) in your space. Otherwise, **Add to chat** doesn't appear.
  - To use **Add to chat**, the [`agentBuilder:experimentalFeatures`](/explore-analyze/ai-features/agent-builder/get-started.md#enable-experimental-features-optional) and [`agentBuilder:apiDiscovery`](/explore-analyze/ai-features/agent-builder/tools/builtin-tools-reference.md#api-discovery) advanced settings turned on in your space.
  - To install rules from chat, `All` privileges for **Rules**.
:::

:::{applies-item} { "stack": "ga 9.3", "serverless": "ga" }
**Requirements**

* `All` [{{kib}} privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for the **Security > SIEM migrations** {{kib}} feature and at least `Read` privileges for the **Security > Rules, Alerts, and Exceptions** {{kib}} feature.
* A working [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md).
* {{stack}} users: an [Enterprise](https://www.elastic.co/pricing) subscription.
* {{Stack}} users: {{ml}} must be enabled.
* {{serverless-short}} users: a [Security Complete](/deploy-manage/deploy/elastic-cloud/project-settings.md) subscription.
* {{ecloud}} users: {{ml}} must be enabled. We recommend a minimum size of 4GB of RAM per {{ml}} zone.
:::

:::{applies-item} stack: ga 9.0-9.2
**Requirements**

* `All` [{{kib}} privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for the **Security > SIEM migrations** {{kib}} feature.
* A working [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md).
* {{stack}} users: an [Enterprise](https://www.elastic.co/pricing) subscription.
* {{Stack}} users: {{ml}} must be enabled.
* {{serverless-short}} users: a [Security Complete](/deploy-manage/deploy/elastic-cloud/project-settings.md) subscription.
* {{ecloud}} users: {{ml}} must be enabled. We recommend a minimum size of 4GB of RAM per {{ml}} zone.

:::

::::

::::{admonition} Splunk dashboard migration limitations
Only supports `visualization`, `chart`, `table`, and `single value (Metric)` Splunk dashboard panels, not `map`, `event`, or `html` panels. You can still migrate a dashboard that contains unsupported panels, but those panels appear as `Unsupported` in migrated dashboards.
::::

## Get started with Automatic Migration

1. Find **Get started** in the navigation menu or use the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Under **Configure AI provider**, select a configured model or [add a new one](/explore-analyze/ai-features/llm-guides/llm-connectors.md). For information on how different models perform, refer to the [LLM performance matrix](/solutions/security/ai/large-language-model-performance-matrix.md).
3. Next, under **Migrate rules & dashboards**, select either **Translate your existing SIEM rules to Elastic** or **Migrate your existing SIEM dashboards to Elastic**, then click **Upload**. The upload flyout appears. 
4. Select the migration source and follow the instructions on the flyout to export your assets.

   :::{image} /solutions/images/security-siem-migration-1.png
   :alt: the Upload SIEM rules flyout with migration source dropdown
   :width: 700px
   :screenshot:
   :::


   ::::{note}
   The provided queries download a default selection of assets. For QRadar exports, we do not recommend changing the query. For Splunk, as long as you export your results as JSON, you can use a different query. For example, the following custom query would download rules related to just the `splunksysmonsecurity` app:

   ```
   | rest /servicesNS/-/-/saved/searches
   | search action.correlationsearch.enabled = "1" OR (eai:acl.app = "Splunk_Security_Essentials" AND is_scheduled=1)
   | where disabled=0
   | table id, title, search, description, action.escu.eli5, action.correlationsearch.annotations, alert.severity
   ```

   For rule migration, we recommend against downloading all searches (for example with `| rest /servicesNS/-/-/saved/searches`) because much of the data would be irrelevant to asset migration.
   ::::

5. Select your JSON file and click **Upload**. If the file is large, you can separate it into multiple parts and upload them individually to avoid exceeding your LLM's context window.

6. After you upload your assets, Automatic Migration detects whether they use any macros, lookups, reference sets, watchlists, or MITRE mappings. If so, follow the instructions which appear to export and upload them. Alternatively, you can complete this step later—however, some of your migrated assets will have a `partially translated` status. If you upload them now, you don't have to stay on this page—a notification appears when processing is complete.

7. Click **Translate** to start the rule translation process. The **Start rules migration** popup appears.

8. Use the dropdown menu to select which AI connector to use. For rule migrations, the **Match to Elastic prebuilt rules** option (on by default) converts any migrated rules that are similar to an Elastic prebuilt rule to that prebuilt rule (this uses fewer tokens). When the option is off, each rule is converted into a new custom rule. 

9. Click **Translate**. A name for the migration is automatically created, and you can track its progress on this page. The **More actions** ({icon}`boxes_vertical`) button lets you rename or delete the migration. 

   ::::{image} /solutions/images/security-siem-migration-rule-status-more-actions.png
   :alt: The rule migration status view
   :width: 850px
   :screenshot:
   ::::

   You don't need to stay on this page. A notification appears when the migration is complete.


10. Use the **Add SIEM data with Integrations** section to set up data ingestion from third-party sources. If at least one rules migration has completed, the **Recommended** tab shows integrations that provide the data needed by your translated rules. These include both Elastic-managed integrations and any applicable custom integrations you made using [automatic import](/explore-analyze/ai-features/automatic-import.md).

   ::::{image} /solutions/images/security-siem-migration-integrations-panel.png
   :alt: The add integrations panel.
   :width: 850px
   :screenshot:
   ::::

11. When migration is complete, click the notification or return to the **Get started** page then click **View translated rules** or **View translated dashboards** to open the [**Translated rules**](#the-translated-rules-page) page  or the [**Translated dashboards**](#the-translated-dashboards-page) page. 


## The Translated rules page

This section describes the **Translated rules** page's interface and the data it displays. Use the **Migrations** dropdown menu in the upper right to select which migration appears. 

::::{image} /solutions/images/security-siem-migration-processed-rules.png
:alt: The translated rules page
:width: 850px
:screenshot:
::::

The table's fields are as follows:

* **Updated:** The migration date.
* **Name:** The names of Elastic-authored rules cannot be edited until after rule installation. To edit the name of a custom translated rule, click the name and select **Edit**.
* **Status:** The rule's translation status:
  * `Installed`: Already added to Elastic SIEM. Click **View** to manage and enable it.
  * `Translated`: Ready to install. This rule was mapped to an Elastic-authored rule, or translated by Automatic Migration. Click **Install** to install it.
  * `Partially translated`: Part of the query could not be translated. You may need to specify an index pattern for the rule query, upload missing macros or lookups, or fix broken rule syntax. 
    ::::{note}
    To fix partially translated rules that are missing an index pattern, use the **Update missing index pattern** button. This affects all migrated assets that contain the placeholder `[indexPattern]`, not only those currently visible on the table page.
    ::::
  * `Not translated`: None of the original query could be translated.
  * `Failed`: Translation failed. Refer to the error for details.
* **Risk Score:** For Elastic-authored rules, risk scores are predefined. For custom translated rules, risk scores are defined as follows:
  * If the source rule has a field comparable to Elastic's `risk score`, we use that value.
  * Otherwise, if the source rule has a field comparable to Elastic's `rule severity` field, we base the risk score on that value according to [these guidelines](/solutions/security/detect-and-alert/common-rule-settings.md#rule-ui-basic-params).
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

### Finalize translated rules and view rule details

To install any rules that were partially translated or not translated, you must first edit them. Optionally, you can also edit rules that were successfully translated to finetune them.

:::{note}
You cannot edit Elastic-authored rules using this interface, but after they are installed you can [edit them](/solutions/security/detect-and-alert/manage-detection-rules.md) from the **{{siem-rules-ui}}** page.
:::

Click a rule's name to open its details flyout to the **Translation** tab, which shows the source rule alongside the translated — or partially translated — Elastic version. You can update any part of the rule. When finished, click **Save**.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` To have {{agent-builder}} propose and apply a fix for you, refer to [Fix translated rules in chat](#siem-migration-fix-rules-in-chat).

::::{image} /solutions/images/security-siem-migration-edit-rule.png
:alt: The rule details flyout
:width: 850px
:screenshot:
::::

::::{note}
If you haven't yet ingested your data, you may encounter `Unknown index` or `Unknown column` errors. You can ignore these and add your data later.
::::

The rule details flyout has two other tabs, **Overview** and **Summary**. The **Overview** tab displays information such as the rule's severity, risk score, rule type, and how frequently it runs. The **Summary** tab explains the logic behind how the rule was translated, such as why specific {{esql}} commands were used, or why a source rule was mapped to a particular Elastic-authored rule.

## The Translated dashboards page 

This section describes the **Translated dashboards** page's interface and the data it displays. Use the **Migrations** dropdown menu in the upper right to select which migration appears. 

::::{image} /solutions/images/security-siem-migration-processed-dashboards.png
:alt: The translated rules page
:width: 850px
:screenshot:
::::

:::::{admonition} Important information for QRadar "BB" rules

- {applies_to}`stack: preview =9.3`
QRadar Building Block rules can appear in QRadar migrations. You can identify them by their `BB:` prefix. You should not enable these rules, because they will generate noisy alerts. If you do enable them, we recommend you delete them.

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+`
Building block rule logic is included automatically in translated rules. No action is required.

:::::

The table's fields are as follows:

* **Name:** The names of the translated dashboards cannot be edited until after installation. 
* **Updated:** The date when the dashboard was last modified in its source platform.
* **Status:** The dashboard's translation status:
  * `Installed`: Already added to {{elastic-sec}}. Click **View** to manage it.
  * `Translated`: Ready to install. Click **Install** to install it.
  * `Partially translated`: Part of the dashboard could not be translated. Upload any missing macros or lookups, or fix broken syntax. 
  * `Not translated`: None of the original dashboard could be translated.
  * `Failed`: Translation failed. Click the dashboard's name to open the details flyout and view error details.
* **Tags:** The dashboard's tags, which identify its source application, and can be used to identify it on the **Dashboards** page.
* **Actions:** To view an `Installed` dashboard, click **View**. To install a `Translated` dashboard, click **Install**. To reprocess a `Failed` dashboard, click **Reprocess**.

### View dashboard migration details
For an explanation of a dashboard's translation, click its name to open the dashboard details flyout and view an AI chat that explains the reasoning behind each panel's translation. 


### Finalize translated dashboards

Once you're on the **Translated dashboards** page, to install any assets that were partially translated, you need to edit them. Optionally, you can also edit assets that were successfully translated to finetune them. For more information about editing dashboards, refer to [](/explore-analyze/dashboards/open-dashboard.md).

## Manage rule migrations with {{agent-builder}} [siem-migration-agent-builder]

```{applies_to}
serverless:
  security: ga
stack: ga 9.6+
```

Check on your rule migrations, start or stop them, install translated rules, and fix rule translations that need your input, all by chatting with [{{agent-builder}}](/solutions/security/ai/agent-builder/agent-builder.md). The agent asks you to confirm before it changes a migration or a rule. For example prompts, refer to [Security use cases for {{agent-builder}}](/solutions/security/ai/agent-builder/skills-use-cases.md#automatic-migration). To create a migration or upload rules, use the **Get started** page as described in [Get started with Automatic Migration](#get-started-with-automatic-migration).

### Rule problems you can fix in chat [siem-migration-chat-fixes]

The agent can fix translated rules that aren't installed yet. To fix rules with a `Failed` status, reprocess them instead. The agent can't fix rules with a `Not translated` status. Their source rules usually rely on features that Elastic doesn't support. To change a rule after you install it, edit it from the **{{siem-rules-ui}}** page.

| Problem | What the agent does |
| --- | --- |
| The rule matches the wrong prebuilt rule. | Compares up to five Elastic prebuilt rules that cover your source rule's logic, and recommends one. |
| The rule uses the wrong integration, or its index pattern is wrong or missing. | Finds the Elastic integration that provides the rule's data, and rewrites the {{esql}} query to use that integration's index pattern and field names. |
| The {{esql}} query uses the wrong field names. | Corrects the field names. |
| The {{esql}} query has macro or lookup placeholders. | Removes the placeholders if you agree. The rule then no longer applies the logic they held, such as an exclusion list. To keep that logic, upload the missing macros or lookups and reprocess the rule instead. |

:::{note}
If the rule matches a prebuilt rule, changing its integration or query makes it a custom rule. The rule takes the title and description of your source rule and no longer gets updates from Elastic.
:::

### Fix translated rules in chat [siem-migration-fix-rules-in-chat]

To send rules to the agent and fix them in chat:

1. On the **Translated rules** page, open a chat in one of these ways:

   * For one rule, select its name to open the rule details flyout, then select **Add to chat**.
   * For several rules, select them in the table, then select **Add to chat**.
   * For every rule in the migration, clear all selections, then select **Add to chat**.

   A new chat opens with the rules attached.

2. Describe the problem. Include details the agent can't find on its own, such as the integration or index your data comes from.

3. Review the proposed change, then confirm it. The rule's status changes to `Translated`. If you matched it to a prebuilt rule that's already installed, the status changes to `Installed` instead. A note that explains the change appears on the rule's **Summary** tab.

4. Install the rule from the **Translated rules** page, or ask the agent to install it. The agent asks whether to enable the rule.

## Frequently asked questions (FAQ)

**How does Automatic Migration handle assets that can't be exactly translated for various reasons, such as feature parity issues?**

After translation, assets that can't be translated appear with a status of either partially translated (yellow) or not translated (red). A not translated status usually means that the source rule uses features that Elastic doesn't fully support. From there, you can address them individually.

**Are nested macros supported?**

Yes, Automatic Migration can handle nested macros.

**How can we ensure rules stay up to date?**

With the exception of rules that were matched to Elastic-authored rules (which are updated automatically), assets created by Automatic Migration must be maintained by you.

**What index does information about each migration appear in?**

Rule migration data appears in `.kibana-siem-rule-migrations-rules-default`. Dashboard migration data appears in `.kibana-siem-dashboard-migrations-dashboards-default`. You can use [Discover](/explore-analyze/discover.md) to review a variety of metrics, analyze metrics, and more.

**How does Automatic Migration handle Splunk assets which lookup other indices?**

Assets that fall into this category will typically appear with a status of partially translated. You can use the [`LOOKUP JOIN`](elasticsearch://reference/query-languages/esql/esql-lookup-join.md) capability to help in this situation.
