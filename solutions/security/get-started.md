---
navigation_title: Get started
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/getting-started.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
---

# Get started with {{elastic-sec}} [getting-started]

Create a project or deployment, bring in your data, and start detecting threats.

::::::{stepper}
:::::{step} Create a project or deployment

If you already have a deployment, go to the next step. If it's self-managed, first check the requirements in the tab for self-managed deployments below.

$$$create-sec-serverless-project$$$
::::{tab-set}

:::{tab-item} {{serverless-full}}
{{sec-serverless}} is the quickest way to start, because Elastic manages the underlying {{es}} cluster and {{kib}} instances for you.

There are two options to create serverless projects:
- If you're a new user, [sign up for a free 14-day trial](https://cloud.elastic.co/serverless-registration). For more information about {{ecloud}} trials, check out [Trial information](/deploy-manage/deploy/elastic-cloud/create-an-organization.md#general-sign-up-trial-what-is-included-in-my-trial).
- If you're an existing customer, [log in to {{ecloud}}](https://cloud.elastic.co/login) and do the following:
  1. Select **Create project** from the **Serverless projects** panel.
  2. Select **Next** from the **Security** panel.
  3. Name your project and select your feature tier. For more information about tiers, refer to [pricing](https://www.elastic.co/pricing/serverless-security). If you select the EASE tier, follow [Elastic AI SOC Engine with {{sec-serverless}}](/solutions/security/ai/ease/ease-intro.md) instead of the rest of this page.
  4. Select a cloud provider and region.
  5. Select **Create project**. It takes a few minutes to create your project.
  6. Once the project is ready, select **Continue** to open the **Get started** page. You might need to log in to {{ecloud}} again.
:::

:::{tab-item} {{ech}}
[Create an {{ech}} deployment](/deploy-manage/deploy/elastic-cloud/create-an-elastic-cloud-hosted-deployment.md). Elastic provisions {{fleet-server}} automatically when you create the deployment, and detections need no extra configuration.
:::

:::{tab-item} Self-managed
1. [Deploy a self-managed cluster](/deploy-manage/deploy/self-managed.md).
2. [Deploy {{fleet-server}}](/reference/fleet/add-fleet-server-on-prem.md) so you can enroll {{agent}} on your hosts.
3. Meet the detection requirements: HTTPS between {{es}} and {{kib}}, an encryption key in `kibana.yml`, and security turned on in {{es}}. Refer to [Turn on detections](/solutions/security/detect-and-alert/turn-on-detections.md).
:::

::::

To compare all options, refer to [deployment types](/deploy-manage/deploy.md#choosing-your-deployment-type).
:::::

:::::{step} Bring in data

Which integrations you add depends on whether this is a new deployment or a migration from an existing SIEM.

::::{tab-set}
:group: setup-path

:::{tab-item} New deployment
:sync: new-deployment
At the top of the **Get started** page, select **Set up Security**, then go to **Ingest your data** → **Add data with integrations**. Select a recommended integration, or browse by category.

:::{image} /solutions/images/security-gs-ingest-data.png
:alt: Ingest data
:screenshot:
:::
:::

:::{tab-item} Migrate from an existing SIEM
:sync: migrate
Automatic Migration translates your rules from Splunk, QRadar, or Microsoft Sentinel, then shows which integrations supply the data those rules need. Supported source platforms depend on your version. Automatic Migration requires an LLM connector, and either a Security Complete project or an Enterprise subscription.

1. At the top of the **Get started** page, select **Automatic migration**.
2. Upload and translate your rules. For the full procedure, refer to [Migrate to {{elastic-sec}} with Automatic Migration](/solutions/security/get-started/automatic-migration.md).
3. After at least one rules migration completes, the **Add SIEM data with Integrations** card lists the integrations that your translated rules need. Add those integrations.
:::

::::

After you add an integration, [verify that your data reaches {{elastic-sec}}](/solutions/security/get-started/ingest-data-to-elastic-security.md#security-ingest-verify). To decide between managed and {{agent}} integrations, or to bring in data from a source that has no integration, refer to [Ingest data to {{elastic-sec}}](/solutions/security/get-started/ingest-data-to-elastic-security.md).
:::::

:::::{step} Install detection rules

::::{tab-set}
:group: setup-path

:::{tab-item} New deployment
:sync: new-deployment
On the **Get started** page, go to **Configure rules and alerts** → **Enable rules**, then select **Add Elastic rules**. Start with the prebuilt rules whose `Data Source` tags match your integrations, so every rule you enable has data to run against. For a method to build your first rule set, refer to [Choosing which rules to enable](/solutions/security/detect-and-alert/install-prebuilt-rules.md#choosing-rules-to-enable).
:::

:::{tab-item} Migrate from an existing SIEM
:sync: migrate
Install and enable your translated rules from the **Translated rules** page. Rules with a `Partially translated` or `Not translated` status need edits before you can install them. Refer to [Finalize translated rules](/solutions/security/get-started/automatic-migration.md#finalize-translated-rules-and-view-rule-details).

To cover data sources that your translated rules don't use, also add Elastic prebuilt rules as described in the **New deployment** tab.
:::

::::

:::{note}
If you ingest alerts from another security tool, such as CrowdStrike or Microsoft Sentinel, also install and enable its promotion rule, such as [CrowdStrike External Alerts](detection-rules://rules/promotions/crowdstrike_external_alerts.md), or the general [External Alerts](detection-rules://rules/promotions/external_alerts.md) rule. Promotion rules turn the tool's alerts into {{elastic-sec}} alerts.
:::

:::::

:::::{step} Verify rules and review alerts

Alerts appear only after an enabled rule finds matching data, so the **Alerts** page can be empty at first, especially in an environment with little suspicious activity. To confirm that your rules are running, check the **Last response** column on the **{{siem-rules-ui}}** page.

::::{tab-set}
:group: setup-path

:::{tab-item} New deployment
:sync: new-deployment
On the **Get started** page, go to **Configure rules and alerts** → **View alerts**, then select **View alerts** to open the **Alerts** page. From there, you can triage and investigate alerts. Refer to [Manage detection alerts](/solutions/security/detect-and-alert/manage-detection-alerts.md).
:::

:::{tab-item} Migrate from an existing SIEM
:sync: migrate
On the **Get started** page, go to **Configure rules and alerts** → **View alerts**, then select **View alerts** to open the **Alerts** page. From there, you can triage and investigate alerts. Refer to [Manage detection alerts](/solutions/security/detect-and-alert/manage-detection-alerts.md).

To check your translated rules, filter the **{{siem-rules-ui}}** page by the `Migrated from <vendor>` tag, such as `Migrated from Splunk`. Automatic Migration adds this tag to the custom rules it creates. Rules that it matched to Elastic prebuilt rules don't have the tag.

If a translated rule's **Last response** shows a warning that it can't find matching indices, the rule needs data that you haven't ingested yet. Add the integrations from the **Add SIEM data with Integrations** card. The warning clears when matching data arrives.
:::

::::
:::::

::::::

## Related resources 

Use these resources to learn more about {{elastic-sec}} or get started in a different way.

* Learn what {{elastic-sec}} covers and how its parts fit together in the [{{elastic-sec}} overview](/solutions/security.md).
* Follow a [quickstart](/solutions/security/get-started/quickstarts.md) for a guided walkthrough of SIEM detection, endpoint protection, or cloud security posture management.
* Migrate your detection rules and dashboards from another SIEM using [Automatic Migration](../security/get-started/automatic-migration.md). Supported SIEMs and asset types depend on your version.
* Check out the numerous [Security integrations](https://www.elastic.co/integrations/data-integrations?solution=security) available to collect and process your data.  
* Get started with [AI-assisted operations](../security/ai.md). 
* Learn how to use {{es}} Query Language ({{esql}}) for [security use cases](/solutions/security/esql-for-security.md). 
* View our [release notes](../../release-notes/elastic-security/index.md) for the latest updates. 