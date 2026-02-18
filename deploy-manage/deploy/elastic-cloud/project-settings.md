---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/project-and-management-settings.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-manage-project.html
applies_to:
  serverless:
products:
  - id: cloud-serverless
---

# Project settings

Project settings are configurations that apply to your entire project, managed from the {{ecloud}} console. While Elastic [manages many things for you](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md), you can customize the following aspects of your project:

- **[Search AI Lake settings](#elasticsearch-manage-project-search-ai-lake-settings)**: Configure search performance, cache behavior, and data retention.
- **[Project features and add-ons](#project-features-add-ons)**: Select feature tiers and enable add-ons for your project type.
- **[Project tags](#project-tags)**: Add custom metadata to categorize and organize your projects.
- **[Connection aliases](#elasticsearch-manage-project-connection-aliases)**: Use predictable, human-readable URLs for your projects that you can share easily.

To manage these settings:

1. Navigate to [cloud.elastic.co](https://cloud.elastic.co/).
2. Log in to your {{ecloud}} account.
3. Select your project from the **Serverless projects** panel and click **Manage**.

## Requirements

To edit a project's settings, you must be granted the **Admin** or **Editor** [role](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles-table) on the project.

## Search AI Lake settings [elasticsearch-manage-project-search-ai-lake-settings]

$$$elasticsearch-manage-project-search-power-settings$$$

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
| **Search Power** | Search Power controls the speed of searches against your data. With Search Power, you can improve search performance by adding more resources for querying, or you can reduce provisioned resources to cut costs. Choose from three Search Power settings:<br><br>**On-demand:** Autoscales based on data and search load, with a lower minimum baseline for resource use. This flexibility results in more variable query latency and reduced maximum throughput.<br><br>**Performant:** Delivers consistently low latency and autoscales to accommodate moderately high query throughput.<br><br>**High-throughput:** Optimized for high-throughput scenarios, autoscaling to maintain query latency even at very high query volumes.<br> | {{es}} |
| **Search Boost Window** | Non-time series data is always considered search-ready. The **Search Boost Window** determines the volume of time series project data that will be considered search-ready.<br><br>Increasing the window results in a bigger portion of time series project data included in the total search-ready data volume.<br> | {{es}} |
| **Data Retention** | Data retention policies determine how long your project data is retained.<br>In {{serverless-full}} data retention policies are configured through [data streams](../../../manage-data/lifecycle/data-stream.md) and you can [specify different retention periods](../../../manage-data/lifecycle/data-stream/tutorial-update-existing-data-stream.md#set-lifecycle) for specific data streams in your project.<br><br> {{elastic-sec}} has to additional configuration settings that can be configured to manage your data retention.<br><br>**Maximum data retention period**<br><br>When enabled, this setting determines the maximum length of time that data can be retained in any data streams of this project.<br><br>Editing this setting replaces the data retention set for all data streams of the project that have a longer data retention defined. Data older than the new maximum retention period that you set is permanently deleted.<br><br> **Default data retention period**<br><br>When enabled, this setting determines the default retention period that is automatically applied to all data streams in your project that do not have a custom retention period already set.<br> |Elasticsearch<br>Observability<br>Security  |
| **Project features** | Controls [feature tiers and add-on options](../../../deploy-manage/deploy/elastic-cloud/project-settings.md#project-features-add-ons) for your {{elastic-sec}} project. | Security |

## Project features and add-ons [project-features-add-ons]

Project features and add-ons control which capabilities are available in your serverless project and how they are billed. What you can configure depends on your project type: 

* [{{es-serverless}} project features](#es-serverless-project-features)
* [{{sec-serverless}} project features](#sec-serverless-project-features)
* [{{obs-serverless}} project features](#obs-serverless-project-features) 

The [Serverless Plus add-on](#serverless-plus) is included with Security and Observability Complete, and is optional for {{es}} projects.

### {{es-serverless}} project features [es-serverless-project-features]

The only add-on available for {{es}} projects is Serverless Plus. To opt in during the promotional period, start using the features on the relevant project. For more information, refer to [Serverless Plus add-on](#serverless-plus).

### {{sec-serverless}} project features

For {{sec-serverless}} projects, edit the **Project features** to select a feature tier and enable add-on options for specific use cases.

| Feature tier | Description and add-ons |
| :--- | :--- |
| **Elastic AI SOC Engine (EASE)** | A package of AI-powered tools meant to work with and enhance your existing SOC platforms: triage and correlate alerts from any platform using Attack Discovery, get realtime recommendations and assistance from AI Assistant, and share insights with your other tools.  |
| **Security Analytics Essentials** | A suite of security analytics, detections, investigations, and collaboration tools. Does not include AI-powered tools. Allows these add-ons:<br>• **Endpoint Protection Essentials**: endpoint protections with {{elastic-defend}}.<br>• **Cloud Protection Essentials**: Cloud native security features.<br> |
| **Security Analytics Complete** | Everything in **Security Analytics Essentials** and **EASE**, plus advanced features such as entity analytics, threat intelligence, and more. Allows these add-ons:<br><br>• **Endpoint Protection Complete**: Everything in **Endpoint Protection Essentials** plus advanced endpoint detection and response features.<br>• **Cloud Protection Complete**: Everything in **Cloud Protection Essentials** plus advanced cloud security features.<br><br>The [Serverless Plus add-on](#serverless-plus) is included with this tier at no additional charge. |

#### Downgrading the feature tier [elasticsearch-manage-project-downgrading-the-feature-tier]

:::{note}
You cannot downgrade to EASE from any other feature tier. You can upgrade from EASE to other tiers.
:::

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

:::{tip}
For a full feature comparison, upgrading instructions, and more, refer to [{{product.serverless-security}} feature tiers](/solutions/security/security-serverless-feature-tiers.md).
:::

### {{obs-serverless}} project features

For {{obs-serverless}} projects, edit the **Project features** to select a feature tier.

| Feature tier | Description|
| :--- | :--- |
| **Observability Logs Essentials** | Includes everything you need to store and analyze logs at scale.<br> |
| **Observability Complete** | Adds full-stack observability capabilities to monitor cloud-native and hybrid environments.<br><br>The [Serverless Plus add-on](#serverless-plus) is included with this tier at no additional charge. |

:::{tip}
For a full feature comparison, upgrading instructions, and more, refer to [{{obs-serverless}} feature tiers](../../../solutions/observability/observability-serverless-feature-tiers.md).
:::

### Serverless Plus add-on [serverless-plus]

:::{include} ../_snippets/serverless-plus.md
:::

#### Availability [serverless-plus-add-on-availability]

:::{include} ../_snippets/serverless-plus-availability.md
:::

## Project tags

Project tags are custom metadata key-value pairs that allow you to categorize and organize your projects.

While each project is automatically categorized by attributes such as its project type, cloud service provider, and region, you can add your own tags to further categorize your projects. 

For example, you might tag a project with the following types of metadata:

* The team or department that uses it: `dept:finance`, `dept:marketing`, `dept:engineering`
* The environment type: `env:dev`, `env:staging`, or `env:prod`

### Create project tags

1. In {{ecloud}}, select your project from the **Serverless projects** panel and click **Manage**.
2. From the **Overview** page for your project, in the **Tags** section, click **{icon}`plus_in_circle` Add tags**.
3. Add a key and value for your tag, and then click **Add**.
4. When you're finished creating tags, click **Save**.

To remove a tag from a project, reopen the tag management drawer by clicking **{icon}`plus_in_circle`  Add tags**.

### Project tags using the {{serverless-full}} API

You can also manage your project tags through the [{{serverless-full}} API]({{cloud-serverless-apis}}).

#### Add tags

You can manage project tags using the `POST` or `PATCH` project endpoints for your project type:

* {{es}}: [POST]({{cloud-serverless-apis}}/operation/operation-createelasticsearchproject), [PATCH]({{cloud-serverless-apis}}/operation/operation-patchelasticsearchproject)
* Observability: [POST]({{cloud-serverless-apis}}/operation/operation-createobservabilityproject), [PATCH]({{cloud-serverless-apis}}/operation/operation-patchobservabilityproject)
* Security: [POST]({{cloud-serverless-apis}}/operation/operation-createsecurityproject), [PATCH]({{cloud-serverless-apis}}/operation/operation-patchsecurityproject)

Project tags are passed as key-value pairs in the `metadata.tags` property of the request body:

```console
PATCH /api/v1/serverless/projects/elasticsearch/1234 <1>

{
  "metadata": {
    "tags": {
      "dept": "support_eng",
      "env": "staging",
    }
  }
}
```
1. `/api/v1/serverless/projects/{project-type}/{project-id}`

#### Remove tags

To remove a value for a tag, pass a `null` value for that tag:

```console
PATCH /api/v1/serverless/projects/elasticsearch/1234 <1>


{
  "metadata": {
    "tags": {
      "dept": null,
    }
  }
}
```
1. `/api/v1/serverless/projects/{project-type}/{project-id}`

#### Query by tag

After you've added tags to your project, you can query your projects by their tags by adding the desired tags as query parameters:

* [{{es}}]({{cloud-serverless-apis}}/operation/operation-listelasticsearchprojects)
* [Observability]({{cloud-serverless-apis}}/operation/operation-listobservabilityprojects)
* [Security]({{cloud-serverless-apis}}/operation/operation-listsecurityprojects)

```console
GET /api/v1/serverless/projects/{type}?tag[key1]=value1&tag[key2]=value2
```

For example, to query for all {{es}} projects that are staging environments belonging to support_eng: 

```console
GET /api/v1/serverless/projects/elasticsearch?tag[env]=staging&tag[dept]=support_eng
```

## Connection aliases [elasticsearch-manage-project-connection-aliases]

Connection aliases for your projects enable you to have predictable, human-readable URLs that can be shared easily.
The connection alias must be unique for each region, across all accounts.
New projects are assigned a default alias derived from the project name.

### Update a connection alias for a project

To modify the connection alias for a project:

1. From the **Serverless projects** menu, select a project and click **Manage**.
2. Locate **Connection alias**, click **Edit**.
3. Define a new alias. Make sure you choose something meaningful to you.

    ::::{tip}
    Make the alias as unique as possible to avoid collisions. Aliases might have been already claimed by other users for projects in the region.
    ::::

4. Select **Update alias**.

::::{important}
Renaming connection aliases might cause disruptions to applications and services that rely on these endpoints. Ensure that you update any references to the old alias to prevent issues.
::::
