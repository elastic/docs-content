---
mapped_urls:
  - https://www.elastic.co/guide/en/serverless/current/project-and-management-settings.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-manage-project.html

applies_to:
  serverless:
---

# Project settings

$$$elasticsearch-manage-project-search-power-settings$$$

{{serverless-full}} projects are fully managed and automatically scaled by Elastic. You have the option of {{es-serverless}}, {{observability}}, or {{elastic-sec}} for your project.

Your project’s performance and general data retention are controlled by the **Search AI Lake settings**. To manage these settings:

1. Navigate to [cloud.elastic.co](https://cloud.elastic.co/).
2. Log in to your Elastic Cloud account.
3. Select your project from the **Serverless projects** panel and click **Manage**.

Additionally, there are [features and add-ons](#project-features-add-ons) available for security that you can configure.

## Search AI Lake settings [elasticsearch-manage-project-search-ai-lake-settings]

Once ingested, your data is stored in cost-efficient, general storage. A cache layer is available on top of the general storage for recent and frequently queried data that provides faster search speed. Data in this cache layer is considered **search-ready**.

Together, these data storage layers form your project’s **Search AI Lake**.

The total volume of search-ready data is the sum of the following:

1. The volume of non-time series project data
2. The volume of time series project data included in the Search Boost Window

::::{note}
Time series data refers to any document in standard indices or data streams that includes the `@timestamp` field. This field must be present for data to be subject to the Search Boost Window setting.

::::

Each project type offers different settings that let you adjust the performance and volume of search-ready data, as well as the features available in your projects.

The documentation in this section describes shared capabilities that are available in multiple solutions. These settings allow you to tune your project settings not all functionality as you would have with a self-managed deployment.
$$$elasticsearch-manage-project-search-power-settings$$$

| Setting | Description | Project Type |
| :--- | :--- | :--- |
| **Search Power** | Search Power controls the speed of searches against your data. With Search Power, you can improve search performance by adding more resources for querying, or you can reduce provisioned resources to cut costs. Choose from three Search Power settings:<br><br>**On-demand:** Autoscales based on data and search load, with a lower minimum baseline for resource use. This flexibility results in more variable query latency and reduced maximum throughput.<br><br>**Performant:** Delivers consistently low latency and autoscales to accommodate moderately high query throughput.<br><br>**High-throughput:** Optimized for high-throughput scenarios, autoscaling to maintain query latency even at very high query volumes.<br> | Elasticsearch |
| **Search Boost Window** | Non-time series data is always considered search-ready. The **Search Boost Window** determines the volume of time series project data that will be considered search-ready.<br><br>Increasing the window results in a bigger portion of time series project data included in the total search-ready data volume.<br> | Elasticsearch |
| **Data Retention** | Data retention policies determine how long your project data is retained.<br>In {{serverless-full}} data retention policies are configured through [data streams](../../../manage-data/lifecycle/data-stream.md) and you can specify different retention periods for specific data streams in your project.<br><br> {{elastic-sec}} has to additional configuration settings that can be configured to managed your data retention.<br><br>**Maximum data retention period**<br><br>When enabled, this setting determines the maximum length of time that data can be retained in any data streams of this project.<br><br>Editing this setting replaces the data retention set for all data streams of the project that have a longer data retention defined. Data older than the new maximum retention period that you set is permanently deleted.<br><br> **Default data retention period**<br><br>When enabled, this setting determines the default retention period that is automatically applied to all data streams in your project that do not have a custom retention period already set.<br> |Elasticsearch<br>Observability<br>Security  |
| **Project features** | Controls [feature tiers and add-on options](../../../deploy-manage/deploy/elastic-cloud/project-settings.md#project-features-add-ons) for your {{elastic-sec}} project. | Security |

## Project features and add-ons [project-features-add-ons]

```yaml {applies_to}
serverless:
  security:
```

For {{elastic-sec}} projects, edit the **Project features** to select a feature tier and enable add-on options for specific use cases.

| Feature tier | Description and add-ons |
| :--- | :--- |
| **Security Analytics Essentials** | Standard security analytics, detections, investigations, and collaborations. Allows these add-ons:<br><br>* **Endpoint Protection Essentials**: endpoint protections with {{elastic-defend}}.<br>* **Cloud Protection Essentials**: Cloud native security features.<br> |
| **Security Analytics Complete** | Everything in **Security Analytics Essentials*** plus advanced features such as entity analytics, threat intelligence, and more. Allows these add-ons:<br><br>* **Endpoint Protection Complete**: Everything in **Endpoint Protection Essentials** plus advanced endpoint detection and response features.<br>* **Cloud Protection Complete**: Everything in **Cloud Protection Essentials** plus advanced cloud security features.<br> |

### Downgrading the feature tier [elasticsearch-manage-project-downgrading-the-feature-tier]

When you downgrade your Security project features selection from **Security Analytics Complete** to **Security Analytics Essentials**, the following features become unavailable:

* All Entity Analytics features
* The ability to use certain entity analytics-related integration packages, such as:
  * Data Exfiltration detection
  * Lateral Movement detection
  * Living off the Land Attack detection
* Intelligence Indicators page
* External rule action connectors
* Case connectors
* Endpoint response actions history
* Endpoint host isolation exceptions
* AI Assistant
* Attack discovery

And, the following data may be permanently deleted:

* AI Assistant conversation history
* AI Assistant settings
* Entity Analytics user and host risk scores
* Entity Analytics asset criticality information
* Detection rule external connector settings
* Detection rule response action settings
