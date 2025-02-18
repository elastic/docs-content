# Working with deployments [ece-stack-getting-started]

::::{note}
Are you just discovering Elastic or are unfamiliar with the core concepts of the Elastic Stack? Would you like to be guided through the very first steps and understand how Elastic can help you? Try one of our [getting started guides](https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/getting-started-guides.html) first.
::::



## Introducing deployments [ece_introducing_deployments]

**The Elastic Stack, managed through {{ecloud}} deployments.**

Elastic Cloud Enterprise allows you to manage one or more instances of the Elastic Stack through **deployments**.

A *deployment* helps you manage an Elasticsearch cluster and instances of other Elastic products, like Kibana or APM instances, in one place. Spin up, scale, upgrade, and delete your Elastic Stack products without having to manage each one separately. In a deployment, everything works together.

**Hardware profiles to optimize deployments for your usage.**

You can optimize the configuration and performance of a deployment by selecting a **hardware profile** that matches your usage.

*Hardware profiles* are presets that provide a unique blend of storage, memory and vCPU for each component of a deployment. They support a specific purpose, such as a hot-warm architecture that helps you manage your data storage retention.

You can use these presets, or start from them to get the unique configuration you need. They can vary slightly from one cloud provider or region to another to align with the available virtual hardware.

All of these profiles are based on *deployment templates*, which are a reusable configuration of Elastic products that you can deploy. With the flexibility of Elastic Cloud Enterprise, you can take it a step further by customizing a deployment template to your own needs.

**Solutions to help you make the most out of your data in each deployment.**

Building a rich search experience, gaining actionable insight into your environment, or protecting your systems and endpoints? You can implement each of these major use cases, and more, with the solutions that are pre-built in each Elastic deployment.

:::{image} ../../../images/cloud-enterprise-ec-stack-components.png
:alt: Elastic Stack components and solutions with Enterprise Search
:::

:::{important}
Enterprise Search is not available in {{stack}} 9.0+.
:::

These solutions help you accomplish your use cases: Ingest data into the deployment and set up specific capabilities of the Elastic Stack.

Of course, you can choose to follow your own path and use Elastic components available in your deployment to ingest, visualize, and analyze your data independently from solutions.


## How to operate Elastic Cloud Enterprise? [ece_how_to_operate_elastic_cloud_enterprise]

**Where to start?**

* Try one of our solutions by following our [getting started guides](https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/getting-started-guides.html).
* [Create a deployment](../../../deploy-manage/deploy/cloud-enterprise/create-deployment.md) - Get up and running very quickly. Select your desired configuration and let Elastic deploy Elasticsearch, Kibana, and the Elastic products that you need for you. In a deployment, everything works together, everything runs on hardware that is optimized for your use case.
* [Connect your data to your deployment](https://www.elastic.co/guide/en/cloud-enterprise/current/ece-cloud-ingest-data.html) - Ingest and index the data you want, from a variety of sources, and take action on it.

**And then?**

Now is the time for you to work with your data. The content of the Elastic Cloud Enterprise section helps you get your environment up and ready to handle your data the way you need. You can always adjust your deployments and their configuration as your usage evolves over time.

To get the most out of the solutions that the Elastic Stack offers, [log in to {{ecloud}}](https://cloud.elastic.co) or [browse the documentation](https://www.elastic.co/docs).
