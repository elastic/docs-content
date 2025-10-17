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

:::::{{stepper}}
::::{{step}} Install the Elastic Stack  

To use {{elastic-sec}}, at minimum, you'll need to install {{es}} and {{kib}}—the core components of the {{stack}}. Elastic provides several self-managed or Elastic-managed installation options. For simplicity and speed, we recommend one of our [{{ecloud}}](/deploy-manage/deploy/elastic-cloud.md) options—either {{ech}} or {{serverless-full}}. However, if you prefer to install Elastic on your own infrastructure, you can deploy a [self-managed cluster](/deploy-manage/deploy/self-managed.md). Check out our [deployment types](/deploy-manage/deploy.md#choosing-your-deployment-type) to learn more. 
::::

::::{{step}} Ingest your data 


After you've deployed {{elastic-sec}}, the next step is to get data into the product before you can search, analyze, or use any visualization tools. The easiest way to get data into {{elastic-sec}} is through one of our [Security integrations](https://www.elastic.co/integrations/data-integrations?solution=security)—pre-packaged collections of assets that allows you to easily collect, store, and visualize any data from any source. You can add an integration directly from the **Get Started** page within the **Ingest your data** section. Choose from one of our recommended integrations, or select another tab to browse by category. Elastic also provides different [ingestion tools](../../manage-data/ingest/tools.md) to meet your infrastructure needs. 

:::{{tip}}
If you have data from a source that doesn't yet have an integration, you can use our [Automatic Import tool](/solutions/security/get-started/automatic-import.md). 
:::
::::

::::{{step}} Get started with your use case 
Not sure where to start exploring {{elastic-sec}} 
or which features may be relevant to you? Continue to the next topic to view our [quickstart guides](../security/get-started/quickstarts.md), each of which is tailored to a specific use case and helps you complete a core task so you can get up and running. 
::::

:::::

## Related resources 

Use these resources to learn more about {{elastic-sec}} or get started in a different way.

* Migrate your SIEM rules from Splunk's Search Processing Language (SPL) to Elasticsearch Query Language ({{esql}}) using [Automatic Migration](../security/get-started/automatic-migration.md). 
* Check out the numerous [Security integrations](https://www.elastic.co/integrations/data-integrations?solution=security) available to collect and process your data.  
* Get started with [AI for Security](../security/ai.md). 
* View our [release notes](../../release-notes/elastic-security/index.md) for the latest updates. 

