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

New to {{elastic-sec}}? Follow the instructions in this topic to get started. Then, review the rest of the Get Started section to learn how to use the UI, review requirements, and discover more about our security features.

::::::{{stepper}}
:::::{{step}} Choose your deployment type   

Elastic provides several self-managed and Elastic-managed options. For simplicity and speed, we recommend [](./elastic-security-serverless.md), which enables you to run {{elastic-sec}} in a fully managed environment so you don’t have to manage the underlying {{es}} cluster and {{kib}} instances. 

::::{dropdown} Create an Elastic Security Serverless project

There are two options to create serverless projects:
- If you're a new user, [sign up for a free 14-day trial](https://cloud.elastic.co/serverless-registration). For more information about {{ecloud}} trials, check out [Trial information](/deploy-manage/deploy/elastic-cloud/create-an-organization.md#general-sign-up-trial-what-is-included-in-my-trial).
- If you're an existing customer, [log in to {{ecloud}}](https://cloud.elastic.co/login) and follow [these instructions](./get-started/create-security-project.md) on how to create a serverless project.  

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
If you have data from a source that doesn't yet have an integration, you can use [Automatic Import](/solutions/security/get-started/automatic-import.md) to create one using AI.   
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

