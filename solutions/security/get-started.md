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

Deploy {{elastic-sec}}, bring in your data, and start detecting threats. For what {{elastic-sec}} covers and how its parts fit together, refer to the [{{elastic-sec}} overview](/solutions/security.md).

## Set up {{elastic-sec}} [security-get-started-steps]

These steps follow the **Set up Security** checklist on the {{elastic-sec}} **Get started** page. {applies_to}`serverless: ga` If your project uses the EASE feature tier, follow [Elastic AI SOC Engine with {{sec-serverless}}](/solutions/security/ai/ease/ease-intro.md) instead.

{applies_to}`stack: preview =9.0, ga 9.1+` {applies_to}`serverless: ga` If you're migrating from Splunk, QRadar, or Microsoft Sentinel, run [Automatic Migration](/solutions/security/get-started/automatic-migration.md) after you create your deployment. It translates your existing rules and identifies the data sources they need, so you know which integrations to add in step 2.

::::::{stepper}
:::::{step} Create or choose a deployment

{{sec-serverless}} is the quickest way to start, because Elastic manages the underlying {{es}} cluster and {{kib}} instances for you.

$$$create-sec-serverless-project$$$
::::{dropdown} Create an {{sec-serverless}} project
:open:
There are two options to create serverless projects:
- If you're a new user, [sign up for a free 14-day trial](https://cloud.elastic.co/serverless-registration). For more information about {{ecloud}} trials, check out [Trial information](/deploy-manage/deploy/elastic-cloud/create-an-organization.md#general-sign-up-trial-what-is-included-in-my-trial).
- If you're an existing customer, [log in to {{ecloud}}](https://cloud.elastic.co/login) and do the following:
  1. Select **Create project** from the **Serverless projects** panel.
  2. Select **Next** from the **Security** panel.
  3. Name your project and select your feature tier. For more information about tiers, refer to [pricing](https://www.elastic.co/pricing/serverless-security).
  4. Select a cloud provider and region.
  5. Select **Create project**. It takes a few minutes to create your project.
  6. Once the project is ready, select **Continue** to open the **Get started** page. You might need to log in to {{ecloud}} again.

:::{note}
You need the `admin` predefined role or an equivalent custom role to create projects. For more information, refer to [User roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md).
:::
::::

For other deployment types:

- **{{ech}}:** [Create a deployment](/deploy-manage/deploy/elastic-cloud/create-an-elastic-cloud-hosted-deployment.md). Detections need no extra configuration.
- **Self-managed:** [Deploy a self-managed cluster](/deploy-manage/deploy/self-managed.md), then [deploy {{fleet-server}}](/reference/fleet/add-fleet-server-on-prem.md) so you can enroll {{agent}} on your hosts. Before detections can run, you also need HTTPS between {{es}} and {{kib}} and an encryption key in `kibana.yml`. Refer to [Turn on detections](/solutions/security/detect-and-alert/turn-on-detections.md).
- **Existing deployment:** Go to the next step. On a self-managed deployment, check the detection requirements first.

To compare all options, refer to [deployment types](/deploy-manage/deploy.md#choosing-your-deployment-type).
:::::

:::::{step} Bring in data

At the top of the **Get started** page, select **Set up Security**, then go to **Ingest your data** → **Add data with integrations**. Select a recommended integration, or browse by category.

:::{image} /solutions/images/security-gs-ingest-data.png
:alt: Ingest data
:screenshot:
:::

On {{sec-serverless}} and {{ech}}, use a managed integration when one exists for your source, because Elastic runs the collector for you. Otherwise, use an integration that runs on {{agent}}. Refer to [Decide between managed and {{agent}} integrations](/solutions/security/get-started/ingest-data-to-elastic-security.md#security-ingest-collection-methods). After you add an integration, [verify that your data reaches {{elastic-sec}}](/solutions/security/get-started/ingest-data-to-elastic-security.md#security-ingest-verify).

If a source has no integration, you can build one with [Automatic Import](/explore-analyze/ai-features/automatic-import.md). For {{beats}}, {{ls}}, and third-party collectors, refer to [Ingest data to {{elastic-sec}}](/solutions/security/get-started/ingest-data-to-elastic-security.md).
:::::

:::::{step} Install detection rules

On the **Get started** page, go to **Configure rules and alerts** → **Install Elastic rules**. Start with the prebuilt rules whose `Data Source` tags match your integrations, so every rule you enable has data to run against. For a method to build your first rule set, refer to [Choosing which rules to enable](/solutions/security/detect-and-alert/install-prebuilt-rules.md#choosing-rules-to-enable).

If you ran Automatic Migration, install and enable your translated rules from the **Translated rules** page.
:::::

:::::{step} Review alerts

On the **Get started** page, go to **Configure rules and alerts** → **Alert list and details** to open the **Alerts** page. From there, you can triage and investigate alerts. Refer to [Manage detection alerts](/solutions/security/detect-and-alert/manage-detection-alerts.md).
:::::

::::::

## Related resources 

Use these resources to learn more about {{elastic-sec}} or get started in a different way.

* Follow a [quickstart](/solutions/security/get-started/quickstarts.md) for a guided walkthrough of SIEM detection, endpoint protection, or cloud security posture management.
* Migrate your detection rules from Splunk, QRadar, or Microsoft Sentinel, and your Splunk dashboards, using [Automatic Migration](../security/get-started/automatic-migration.md).
* Check out the numerous [Security integrations](https://www.elastic.co/integrations/data-integrations?solution=security) available to collect and process your data.  
* Get started with [AI-assisted operations](../security/ai.md). 
* Learn how to use {{es}} Query Language ({{esql}}) for [security use cases](/solutions/security/esql-for-security.md). 
* View our [release notes](../../release-notes/elastic-security/index.md) for the latest updates. 