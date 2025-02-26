---
applies_to:
  deployment:
    ess: ga
mapped_urls:
  - https://www.elastic.co/guide/en/cloud/current/index.html
  - https://www.elastic.co/guide/en/cloud/current/ec-getting-started.html
  - https://www.elastic.co/guide/en/cloud/current/ec-faq-getting-started.html
  - https://www.elastic.co/guide/en/cloud/current/ec-about.html
---

# Elastic Cloud Hosted

% What needs to be done: Refine

% GitHub issue: https://github.com/elastic/docs-projects/issues/338

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/cloud/cloud/ec-getting-started.md
% - [ ] ./raw-migrated-files/cloud/cloud/ec-prepare-production.md
%      Notes: link roundup is good but the plan for prod content is not needed here
% - [ ] ./raw-migrated-files/cloud/cloud/ec-faq-getting-started.md
%      Notes: extract what we can from faq
% - [ ] ./raw-migrated-files/cloud/cloud/ec-about.md
%      Notes: redirect only
% - [ ] ./raw-migrated-files/cloud/cloud-heroku/ech-configure.md

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):

$$$faq-aws-difference$$$

$$$faq-aws$$$

$$$faq-config$$$

$$$faq-elastic$$$

$$$faq-full-stack$$$

$$$faq-limit$$$

$$$faq-subscriptions$$$

$$$faq-trial$$$

$$$faq-vs-aws$$$

$$$faq-what$$$

$$$faq-where$$$

$$$faq-x-pack$$$

**{{ech}} is the Elastic Stack, managed through {{ecloud}} deployments.**

It is also formerly known as Elasticsearch Service.

{{ech}} allows you to manage one or more instances of the Elastic Stack through **deployments**. These deployments are hosted on {{ecloud}}, through the cloud provider and regions of your choice, and are tied to your organization account.

A **hosted deployment** helps you manage an Elasticsearch cluster and instances of other Elastic products, like Kibana or APM instances, in one place. Spin up, scale, upgrade, and delete your Elastic Stack products without having to manage each one separately. In a deployment, everything works together.

::::{note}
{{ech}} is one of the two deployment options available on {{ecloud}}. [Depending on your needs](../elastic-cloud.md), you can also run [Elastic Cloud Serverless projects](/deploy-manage/deploy/elastic-cloud/serverless.md).
::::


**Hardware profiles to optimize deployments for your usage.**

You can optimize the configuration and performance of a deployment by selecting a **hardware profile** that matches your usage.

*Hardware profiles* are presets that provide a unique blend of storage, memory and vCPU for each component of a deployment. They support a specific purpose, such as a hot-warm architecture that helps you manage your data storage retention.

You can use these presets, or start from them to get the unique configuration you need. They can vary slightly from one cloud provider or region to another to align with the available virtual hardware.

**Solutions to help you make the most out of your data in each deployment.**

Building a rich search experience, gaining actionable insight into your environment, or protecting your systems and endpoints? You can implement each of these major use cases, and more, with the solutions that are pre-built in each Elastic deployment.

:::{image} ../../../images/cloud-ec-stack-components.png
:alt: Elastic Stack components and solutions with Enterprise Search
:width: 75%
:::

:::{important}
Enterprise Search is not available in {{stack}} 9.0+.
:::

These solutions help you accomplish your use cases: Ingest data into the deployment and set up specific capabilities of the Elastic Stack.

Of course, you can choose to follow your own path and use Elastic components available in your deployment to ingest, visualize, and analyze your data independently from solutions.


## How to operate {{ech}}? [ec_how_to_operate_elasticsearch_service]

**Where to start?**

* Learn the basics of {{es}}, the {{stack}}, and its solutions in [Get started](/get-started/index.md).
* Sign up using your preferred method:

    * [Sign Up for a Trial](/deploy-manage/deploy/elastic-cloud/create-an-organization.md) - Sign up, check what your free trial includes and when we require a credit card.
    * [Sign Up from Marketplace](/deploy-manage/deploy/elastic-cloud/subscribe-from-marketplace.md) - Consolidate billing portals by signing up through one of the available marketplaces.

* [Create a deployment](/deploy-manage/deploy/elastic-cloud/create-an-elastic-cloud-hosted-deployment.md) - Get up and running very quickly. Select your desired configuration and let Elastic deploy Elasticsearch, Kibana, and the Elastic products that you need for you. In a deployment, everything works together, everything runs on hardware that is optimized for your use case.
* [Connect your data to your deployment](/manage-data/ingest.md) - Ingest and index the data you want, from a variety of sources, and take action on it.

**Adjust the capacity and capabilities of your deployments for production**

There are a few things that can help you make sure that your production deployments remain available, healthy, and ready to handle your data in a scalable way over time, with the expected level of performance. Check [](/deploy-manage/production-guidance/plan-for-production-elastic-cloud.md).

**Secure your environment**

Control which users and services can access your deployments by [securing your environment](/deploy-manage/security/secure-your-cluster-deployment.md). [Add authentication mechanisms](/deploy-manage/users-roles.md), configure [traffic filtering](/deploy-manage/security/traffic-filtering.md) for private link, encrypt your deployment data and snapshots at rest [with your own key](/deploy-manage/security/encrypt-deployment-with-customer-managed-encryption-key.md), [manage trust](/deploy-manage/remote-clusters.md) with {{es}} clusters from other environments, and more.

**Monitor your deployments and keep them healthy**

{{ech}} provides several ways to monitor your deployments, anticipate and prevent issues, or fix them when they occur. Check [Monitoring your deployment](/deploy-manage/monitor.md) to get more details.

## More about {{ech}} [ec-about]

Find more information about {{ech}} on the following pages:

* [Subscription Levels](/deploy-manage/license.md)
* [Version Policy](/deploy-manage/deploy/elastic-cloud/available-stack-versions.md)
* [{{ech}} Hardware](asciidocalypse://docs/cloud/docs/reference/cloud-hosted/hardware.md)
* [{{ech}} Regions](asciidocalypse://docs/cloud/docs/reference/cloud-hosted/regions.md)
* [Service Status](/deploy-manage/cloud-organization/service-status.md)
* [Getting help](/troubleshoot/index.md)
* [Restrictions and known problems](/deploy-manage/deploy/elastic-cloud/restrictions-known-problems.md)

:::{dropdown} {{ech}} FAQ

$$$ec-faq-getting-started$$$

This frequently-asked-questions list helps you with common questions while you get {{ech}} up and running for the first time. For questions about {{ech}} configuration options or billing, check the [Technical FAQ](/deploy-manage/index.md) and the [Billing FAQ](/deploy-manage/cloud-organization/billing/billing-faq.md).

* [What is {{ech}}?](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-what)
* [Is {{ech}}, formerly known as Elasticsearch Service, the same as Amazon’s {{es}} Service?](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-aws-difference)
* [Can I run the full Elastic Stack in {{ech}}?](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-full-stack)
* [Can I try {{ech}} for free?](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-trial)
* [What if I need to change the size of my {{es}} cluster at a later time?](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-config)
* [Do you offer support subscriptions?](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-subscriptions)
* [Where are deployments hosted?](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-where)
* [What is the difference between {{ech}} and the Amazon {{es}} Service?](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-vs-aws)
* [Can I use {{ech}} on platforms other than AWS?](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-aws)
* [Do you offer Elastic’s commercial products?](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-elastic)
* [Is my {{es}} cluster protected by X-Pack?](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-x-pack)
* [Is there a limit on the number of documents or indexes I can have in my cluster?](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md#faq-limit)

$$$faq-what$$$**What is {{ech}}?**
:   {{ech}} is hosted and managed {{es}} and {{kib}} brought to you by the creators of {{es}}. {{ech}} is part of Elastic Cloud and ships with features that you can only get from the company behind {{es}}, {{kib}}, {{beats}}, and {{ls}}. {{es}} is a full text search engine that suits a range of uses, from search on websites to big data analytics and more.

$$$faq-aws-difference$$$**Is {{ech}}, formerly known as Elasticsearch Service, the same as Amazon’s {{es}} Service?**
:   {{ech}} is not the same as the Amazon {{es}} service. To learn more about the differences, check our [AWS {{es}} Service](https://www.elastic.co/aws-elasticsearch-service) comparison.

$$$faq-full-stack$$$**Can I run the full Elastic Stack in {{ech}}?**
:   Many of the products that are part of the Elastic Stack are readily available in {{ech}}, including {{es}}, {{kib}}, plugins, and features such as monitoring and security. Use other Elastic Stack products directly with {{ech}}. For example, both Logstash and Beats can send their data to {{ech}}. What is run is determined by the [subscription level](https://www.elastic.co/cloud/as-a-service/subscriptions).

$$$faq-trial$$$**Can I try {{ech}} for free?**
:   Yes, sign up for a 14-day free trial. The trial starts the moment a cluster is created. During the free trial period get access to a deployment to explore Elastic solutions for Search, Observability, Security, or the latest version of the Elastic Stack.


$$$faq-config$$$**What if I need to change the size of my {{es}} cluster at a later time?**
:   Scale your clusters both up and down from the user console, whenever you like. The resizing of the cluster is transparently done in the background, and highly available clusters are resized without any downtime. If you scale your cluster down, make sure that the downsized cluster can handle your {{es}} memory requirements. Read more about sizing and memory in [Sizing {{es}}](https://www.elastic.co/blog/found-sizing-elasticsearch).

$$$faq-subscriptions$$$**Do you offer support?**
:   Yes, all subscription levels for {{ech}} include support, handled by email or through the Elastic Support Portal. Different subscription levels include different levels of support. For the Standard subscription level, there is no service-level agreement (SLA) on support response times. Gold and Platinum subscription levels include an SLA on response times to tickets and dedicated resources. To learn more, check [Getting Help](/troubleshoot/index.md).

$$$faq-where$$$**Where are deployments hosted?**
:   We host our {{es}} clusters on Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft Azure. Check out which [regions we support](https://www.elastic.co/guide/en/cloud/current/ec-reference-regions.html) and what [hardware we use](https://www.elastic.co/guide/en/cloud/current/ec-reference-hardware.html). New data centers are added all the time.

$$$faq-vs-aws$$$**What is the difference between {{ech}} and the Amazon {{es}} Service?**
:   {{ech}} is the only hosted and managed {{es}} service built, managed, and supported by the company behind {{es}}, {{kib}}, {{beats}}, and {{ls}}. With {{ech}}, you always get the latest versions of the software. Our service is built on best practices and years of experience hosting and managing thousands of {{es}} clusters in the Cloud and on premise. For more information, check the following Amazon and Elastic {{es}} Service [comparison page](https://www.elastic.co/aws-elasticsearch-service).

    Please note that there is no formal partnership between Elastic and Amazon Web Services (AWS), and Elastic does not provide any support on the AWS {{es}} Service.


$$$faq-aws$$$**Can I use {{ech}} on platforms other than AWS?**
:   Yes, create deployments on the Google Cloud Platform and Microsoft Azure.

$$$faq-elastic$$$**Do you offer Elastic’s commercial products?**
:   Yes, all {{ech}} customers have access to basic authentication, role-based access control, and monitoring.

    {{ecloud}} Gold, Platinum and Enterprise customers get complete access to all the capabilities in X-Pack:

    * Security
    * Alerting
    * Monitoring
    * Reporting
    * Graph Analysis & Visualization

    [Contact us](https://www.elastic.co/cloud/contact) to learn more.


$$$faq-x-pack$$$**Is my Elasticsearch cluster protected by X-Pack?**
:   Yes, X-Pack security features offer the full power to protect your {{ech}} deployment with basic authentication and role-based access control.

$$$faq-limit$$$**Is there a limit on the number of documents or indexes I can have in my cluster?**
:   No. We do not enforce any artificial limit on the number of indexes or documents you can store in your cluster.

    That said, there is a limit to how many indexes Elasticsearch can cope with. Every shard of every index is a separate Lucene index, which in turn comprises several files. A process cannot have an unlimited number of open files. Also, every shard has its associated control structures in memory. So, while we will let you make as many indexes as you want, there are limiting factors. Our larger plans provide your processes with more dedicated memory and CPU-shares, so they are capable of handling more indexes. The number of indexes or documents you can fit in a given plan therefore depends on their structure and use.

:::