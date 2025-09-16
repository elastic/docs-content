---
applies_to:
  serverless:
  stack:
---
# How to use the documentation

Our documentation is organized to guide you through your journey with Elastic, from learning the basics to deploying and managing complex solutions.

Here is a detailed breakdown of the documentation structure:

* [**Elastic fundamentals**](/get-started/index.md): Understand the basics about the deployment options, platform, solutions, and features of the documentation.  
* [**Solutions and use cases**](/solutions/index.md): Learn use cases, evaluate, and implement Elastic's solutions: Observability, Search, and Security.  
* [**Manage data**](/manage-data/index.md): Learn about data store primitives, ingestion and enrichment, managing the data lifecycle, and migrating data.  
* [**Explore and analyze**](/explore-analyze/index.md): Get value from data through querying, visualization, machine learning, and alerting.  
* [**Deploy and manage**](/deploy-manage/index.md): Deploy and manage production-ready clusters. Covers deployment options and maintenance tasks.  
* [**Manage your Cloud account**](/cloud-account/index.md): A dedicated section for user-facing cloud account tasks like resetting passwords.  
* [**Troubleshoot**](/troubleshoot/index.md): Identify and resolve problems.  
* [**Extend and contribute**](/extend/index.md): How to contribute to or integrate with Elastic, from open source to plugins to integrations.  
* [**Release notes**](/release-notes/index.md): Contains release notes and changelogs for each new release.  
* [**Reference**](/reference/index.md): Reference material for core tasks and manuals for other Elastic products.

## Applicability badges

Because you can deploy Elastic products in different ways (like on {{ecloud}} or in your own data center) and have different versions, not all documentation applies to every user. To help you quickly see if a topic is relevant to your situation, we use **applicability badges**.

These badges appear at the top of a page or section and tell you which products, deployment models, and versions the content applies to. They also indicate the maturity level of a feature, such as **beta**, **technical preview**, or **generally available (GA)**. This system ensures that you can identify content specific to your environment and version.

:::{tip}
A **Stack** badge indicates that a page applies to [{{stack}}](/get-started/the-stack.md) components across all deployment options except {{serverless-full}}. If a page applies to all deployment options, it will have **{{serverless-short}}** and Stack badges.
:::

## Page options

On each documentation page, you'll find several links that allow you to interact with the content:

* **View as Markdown**: This link shows you the raw Markdown source code for the page you're viewing. This can be helpful if you want to reuse the source or feed the document to AI.  
* **Edit this page**: Selecting this link will take you directly to the page's source file in its GitHub repository. From there, you can propose edits, which our team will review.  
* **Report an issue**: If you've found a problem, like a typo, a technical error, or confusing content, but don't want to edit the page yourself, use this link. It will open a new issue in our GitHub repository, pre-filled with information about the page you were on, so you can describe the problem in detail.

## Versioned documentation

Starting with Elastic Stack 9.0, Elastic no longer publishes separate documentation sets for each minor release. Instead, all changes in the 9.x series are included in a single, continuously updated documentation set.

This approach helps:

* Reduce duplicate pages.  
* Show the full history and context of a feature.  
* Simplify search and navigation.

We clearly mark content added or changed in a specific version using availability badges. The availability badges appear in page headers, section headers, and inline.

### Elastic Stack example

{applies_to}`stack: ga 9.1.0`

This means the feature is:

* Generally Available (GA) in the [{{stack}}](/get-started/the-stack.md) across all deployment options except {{serverless-full}}
* Introduced in version 9.1.0

:::{tip}
If a page applies to all deployment options including {{serverless-full}}, it will have both {{serverless-short}} and Stack badges.
:::

### Serverless example

{applies_to}`serverless: ga` {applies_to}`security: beta`

This means the feature is:

* Generally Available for {{es-serverless}} projects  
* Beta for {{sec-serverless}} projects

### Elastic Cloud Enterprise example

{applies_to}`ece: deprecated 4.1.0`

This means the feature is:

* Available on Elastic Cloud Enterprise  
* Deprecated starting in version 4.1.0

:::{tip}
Want to learn more about how availability badges are used? Check the [Elastic Docs syntax guide](https://elastic.github.io/docs-builder/syntax/applies/).
:::

## Accessing previous versions

You can browse documentation for different versions of our products in two ways:

* **Version menu:** On most documentation pages, you'll find a version menu. Clicking this menu allows you to switch to a different version of the documentation for the content you are currently viewing.  
* **All documentation versions page:** For a complete list of all available documentation versions for all Elastic products, you can visit the [All documentation versions](/versions.md) page.

## Find docs for your product version

Find the documentation for your Elastic product versions or releases.

### Elastic Stack product versions

| Product | Version |
| ----- | ----- |
| [Elasticsearch](https://www.elastic.co/docs/release-notes/elasticsearch) | 9.0.0 and later |
| [Kibana](https://www.elastic.co/docs/release-notes/kibana) | 9.0.0 and later |
| [Fleet and Elastic Agent](https://www.elastic.co/docs/release-notes/fleet) | 9.0.0 and later |
| [Logstash](https://www.elastic.co/docs/release-notes/logstash) | 9.0.0 and later |
| [Beats](https://www.elastic.co/docs/release-notes/beats) | 9.0.0 and later |
| [Elastic Observability](https://www.elastic.co/docs/release-notes/observability) | 9.0.0 and later |
| [Elastic APM](https://www.elastic.co/docs/release-notes/apm) | 9.0.0 and later |
| [Elastic Security](https://www.elastic.co/docs/release-notes/security) | 9.0.0 and later |

### Deployment type versions or releases

| Product | Version or release |
| ----- | ----- |
| All [Elastic Cloud Serverless](https://www.elastic.co/docs/release-notes/cloud-serverless) project types | All releases |
| [Elastic Cloud Hosted](https://www.elastic.co/docs/release-notes/cloud-hosted) | All releases for January 2025 and later |
| [Elastic Cloud Enterprise](https://www.elastic.co/docs/release-notes/cloud-enterprise) | 4.0.0 and later |
| [Elastic Cloud on Kubernetes](https://www.elastic.co/docs/release-notes/cloud-on-k8s) | 3.0.0 and later |

### Schema, library, and tool versions

| Product | Version or release |
| ----- | ----- |
| [Elasticsearch Java Client](https://www.elastic.co/docs/release-notes/elasticsearch/clients/java) | 9.0.0 and later |
| [Elasticsearch JavaScript Client](https://www.elastic.co/docs/release-notes/elasticsearch/clients/javascript) | 9.0.0 and later |
| [Elasticsearch .NET Client](https://www.elastic.co/docs/release-notes/elasticsearch/clients/dotnet) | 9.0.0 and later |
| [Elasticsearch PHP Client](https://www.elastic.co/docs/release-notes/elasticsearch/clients/php) | 9.0.0 and later |
| [Elasticsearch Python Client](https://www.elastic.co/docs/release-notes/elasticsearch/clients/python) | 9.0.0 and later |
| [Elasticsearch Ruby Client](https://www.elastic.co/docs/release-notes/elasticsearch/clients/ruby) | 9.0.0 and later |
| [Elastic Common Schema (ECS)](https://www.elastic.co/docs/release-notes/ecs) | 9.0.0 and later |
| [ECS Logging .NET library](https://www.elastic.co/docs/reference/ecs/logging/dotnet) | 8.18.1 and later |
| [ECS Logging Go (Logrus) library](https://www.elastic.co/docs/reference/ecs/logging/go-logrus) | 1.0.0 and later |
| [ECS Logging Go (Zap) library](https://www.elastic.co/docs/reference/ecs/logging/go-zap) | 1.0.3 and later |
| [ECS Logging Go (Zerolog) library](https://www.elastic.co/docs/reference/ecs/logging/go-zerolog) | 0.2.0 and later |
| [ECS Logging Java library](https://www.elastic.co/docs/reference/ecs/logging/java) | 1.x and later |
| [ECS Logging Node.js library](https://www.elastic.co/docs/reference/ecs/logging/nodejs) | 1.5.3 and later |
| [ECS Logging PHP library](https://www.elastic.co/docs/reference/ecs/logging/php) | 2.0.0 and later |
| [ECS Logging Python library](https://www.elastic.co/docs/reference/ecs/logging/python) | 2.2.0 and later |
| [ECS Logging Ruby library](https://www.elastic.co/docs/reference/ecs/logging/ruby) | 1.0.0 and later |
| [Elasticsearch for Apache Hadoop](https://www.elastic.co/docs/release-notes/elasticsearch-hadoop) | 9.0.0 and later |
| [Elasticsearch Curator](https://www.elastic.co/docs/reference/elasticsearch/curator) | 8.0.0 and later |
| [Elastic Cloud Control (ECCTL)](https://www.elastic.co/docs/release-notes/ecctl) | 1.14.0 and later |
| [Elastic Serverless Forwarder for AWS](https://www.elastic.co/docs/reference/aws-forwarder) | 1.20.1 and later |
| [Elastic integrations](https://www.elastic.co/docs/reference/integrations/all_integrations) | All versions |
| [Search UI JavaScript library](https://www.elastic.co/docs/reference/search-ui) | 1.24.0 and later |

### APM agent and tool versions

| Product | Version |
| ----- | ----- |
| [Elastic Distribution of OpenTelemetry Android](https://www.elastic.co/docs/release-notes/edot/sdks/android) | 0.1.0 and later |
| [Elastic Distribution of OpenTelemetry iOS](https://www.elastic.co/docs/release-notes/edot/sdks/ios) | 1.0.0 and later |
| [Elastic Distribution of OpenTelemetry Java](https://www.elastic.co/docs/release-notes/edot/sdks/java) | 1.0.0 and later |
| [Elastic Distribution of OpenTelemetry .NET](https://www.elastic.co/docs/release-notes/edot/sdks/dotnet) | 1.0.0 and later |
| [Elastic Distribution of OpenTelemetry Node.js](https://www.elastic.co/docs/release-notes/edot/sdks/node) | 0.1.0 and later |
| [Elastic Distribution of OpenTelemetry Python](https://www.elastic.co/docs/release-notes/edot/sdks/python) | 0.1.0 and later |
| [Elastic Distribution of OpenTelemetry PHP](https://www.elastic.co/docs/release-notes/edot/sdks/php) | 0.1.0 and later |
| [Elastic APM .NET Agent](https://www.elastic.co/docs/release-notes/apm/agents/dotnet) | 1.0.0 and later |
| [Elastic APM Go Agent](https://www.elastic.co/docs/release-notes/apm/agents/go) | 2.0.0 and later |
| [Elastic APM Java Agent](https://www.elastic.co/docs/release-notes/apm/agents/java) | 1.0.0 and later |
| [Elastic APM Node.js Agent](https://www.elastic.co/docs/release-notes/apm/agents/nodejs) | 4.0.0 and later |
| [Elastic APM PHP Agent](https://www.elastic.co/docs/release-notes/apm/agents/php) | 1.0.0 and later |
| [Elastic APM Python Agent](https://www.elastic.co/docs/release-notes/apm/agents/python) | 6.0.0 and later |
| [Elastic APM Ruby Agent](https://www.elastic.co/docs/release-notes/apm/agents/ruby) | 4.0.0 and later |
| [Elastic APM Real User Monitoring JavaScript Agent](https://www.elastic.co/docs/release-notes/apm/agents/rum-js) | 5.0.0 and later |
| [Elastic APM AWS Lambda extension](https://www.elastic.co/docs/release-notes/apm/aws-lambda/release-notes) | 1.0.0 and later |
| [Elastic APM Attacher for Kubernetes](https://www.elastic.co/docs/reference/apm/k8s-attacher) | 1.1.3 |

## Glossary

To help you understand the terminology used throughout our documentation, we provide a [glossary of common Elastic terms](/reference/glossary/index.md). This is a great resource for new users or anyone looking to clarify the meaning of a specific term.

## How to contribute

We value contributions from our community. For detailed instructions on how to contribute to both the main documentation and the API references, refer to our [contribution guide](https://www.elastic.co/docs/extend/contribute/).