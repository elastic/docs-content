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

New to {{elastic-sec}}? Start with what it protects and how its parts fit together, then follow the steps to deploy it and bring in your data.

## What {{elastic-sec}} protects [security-what-it-protects]

{{elastic-sec}} covers four areas. You can use them together or start with one:

| Area | What it does | Start here |
|---|---|---|
| SIEM detection and response | Collects security data from across your environment, detects threats with rules and {{ml}}, and helps you investigate and respond. | [Detect and respond to threats with SIEM](/solutions/security/get-started/get-started-detect-with-siem.md) |
| Endpoint protection | Prevents and detects malware, ransomware, and malicious behavior on Windows, macOS, and Linux hosts with {{elastic-defend}}. | [Protect your hosts with endpoint security](/solutions/security/get-started/get-started-endpoint-security.md) |
| Cloud posture | Checks your cloud and Kubernetes configurations against security benchmarks, and scans cloud workloads for vulnerabilities. | [Secure your cloud assets with cloud security posture management](/solutions/security/get-started/get-started-cloud-security.md) |
| Cloud workload protection | Detects and blocks threats on cloud VMs and Kubernetes containers while they run. | [Cloud workload protection for VMs](/solutions/security/cloud/cloud-workload-protection-for-vms.md) |

For a full list of use cases and core concepts, refer to the [{{elastic-sec}} overview](/solutions/security.md).

Which areas you can use depends on your deployment and license:

- {applies_to}`serverless: ga` In {{sec-serverless}}, the Security Analytics feature tiers include SIEM detection and response, with optional add-ons for endpoint protection and cloud protection. The Elastic AI SOC Engine (EASE) tier adds AI-powered threat hunting and alert triage to a third-party SIEM. Refer to [Serverless feature tiers](/solutions/security/security-serverless-feature-tiers.md).
- {applies_to}`stack: ga` In {{stack}} deployments, the features you can use depend on your [subscription](https://www.elastic.co/pricing).

## How a SIEM comes together [security-siem-pieces]

There's no single step that installs a SIEM. A working SIEM needs three things:

1. **Data collection:** [{{agent}}](/reference/fleet/index.md), managed with {{fleet}}, collects data from your hosts. {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+, preview 9.0-9.4` On {{ecloud}}, [{{managed-integrations}}](/manage-data/ingest/managed-integrations/managed-integrations.md) can also collect data from cloud sources without an agent.
2. **Data sources:** Integrations bring in the logs, alerts, and findings that {{elastic-sec}} analyzes. Refer to [Ingest data to {{elastic-sec}}](/solutions/security/get-started/ingest-data-to-elastic-security.md).
3. **Detection rules:** Rules search your data and create alerts. [Turn on detections](/solutions/security/detect-and-alert/turn-on-detections.md), then [install Elastic's prebuilt rules](/solutions/security/detect-and-alert/install-prebuilt-rules.md). Refer to [Detections and alerts](/solutions/security/detect-and-alert.md).

## Coming from another SIEM [security-coming-from-siem]

If you're moving from Splunk, QRadar, or Microsoft Sentinel, [Automatic Migration](/solutions/security/get-started/automatic-migration.md) can translate your existing rules, and Splunk dashboards, into {{elastic-sec}}. Supported sources and assets vary by version.

## Get started in three steps [security-get-started-steps]

::::::{{stepper}}
:::::{{step}} Choose your deployment type   

Elastic provides several self-managed and Elastic-managed options. For simplicity and speed, we recommend {{sec-serverless}}, which enables you to run {{elastic-sec}} in a fully managed environment so you don’t have to manage the underlying {{es}} cluster and {{kib}} instances. 

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
  6. Once the project is ready, select **Continue** to open the **Get started** page (you might need to log in to Elastic Cloud again).   From here, you can learn more about Elastic Security features and start setting up your workspace.  

:::{note}
You need the `admin` predefined role or an equivalent custom role to create projects. For more information, refer to [User roles and privileges](https://www.elastic.co/docs/deploy-manage/users-roles/cloud-organization/user-roles).
:::

After you've created your project, you're ready to move on to the next step.
::::

Alternatively, if you prefer a self-managed deployment, you can create a [local development installation](https://www.elastic.co/docs/deploy-manage/deploy/self-managed/local-development-installation-quickstart) in Docker:
    
```sh
curl -fsSL https://elastic.co/start-local | sh
```

Check out the complete list of [deployment types](/deploy-manage/deploy.md#choosing-your-deployment-type) to learn more.

:::::

::::{{step}} Ingest your data 


After you've deployed {{elastic-sec}}, the next step is to get data into the product before you can search, analyze, or use any visualization tools. The easiest way to get data into {{elastic-sec}} is through one of our hundreds of ready-made integrations. You can add an integration directly from the **Get Started** page within the **Ingest your data** section:
1. At the top of the page, click **Set up Security**. 
2. In the Ingest your data section, click **Add data with integrations**. 
3. Choose from one of our recommended integrations, or select another tab to browse by category. 
:::{image} /solutions/images/security-gs-ingest-data.png
:alt: Ingest data
:screenshot:
:::

Elastic also provides different [ingestion methods](/manage-data/ingest.md) to meet your infrastructure needs. 

:::{{tip}}
If you have data from a source that doesn't yet have an integration, you can use [Automatic Import](/explore-analyze/ai-features/automatic-import.md) to create one using AI.   
:::
::::

::::{{step}} Get started with your use case 
Not sure where to start exploring {{elastic-sec}} 
or which features may be relevant to you? Continue to the next topic to view our [quickstart guides](../security/get-started/quickstarts.md), each of which is tailored to a specific use case and helps you complete a core task so you can get up and running. 
::::

::::::

## Related resources 

Use these resources to learn more about {{elastic-sec}} or get started in a different way.

* Migrate your SIEM rules from Splunk's Search Processing Language (SPL) to Elasticsearch Query Language ({{esql}}) using [Automatic Migration](../security/get-started/automatic-migration.md). 
* Check out the numerous [Security integrations](https://www.elastic.co/integrations/data-integrations?solution=security) available to collect and process your data.  
* Get started with [AI for Security](../security/ai.md). 
* Learn how to use {{es}} Query Language ({{esql}}) for [security use cases](/solutions/security/esql-for-security.md). 
* View our [release notes](../../release-notes/elastic-security/index.md) for the latest updates. 