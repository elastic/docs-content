---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/setup.html
  - https://www.elastic.co/guide/en/cloud/current/ec-faq-technical.html
  - https://www.elastic.co/guide/en/elastic-stack/current/index.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-administering-deployments.html
  - https://www.elastic.co/guide/en/kibana/current/management.html
products:
  - id: kibana
  - id: cloud-hosted
  - id: cloud-enterprise
description: Deploy and manage your Elastic environment. Learn how to design resilient
  clusters, secure access, monitor performance, and maintain your Elastic Stack
  components across different deployment options.
---

# Deploy and manage

To get started with Elastic, you need to choose a deployment method and deploy {{stack}} components.

In this section, you'll learn about how to deploy and manage all aspects of your Elastic environment. You'll learn how to design resilient, highly available clusters and deployments, and how to maintain and scale your environment to grow with your use case.

This section focuses on deploying and managing the core components of the {{stack}}: {{es}} and {{kib}}. It also documents deploying and managing supporting orchestration technologies. However, depending on your use case, you might need to deploy other components. [Learn more](/get-started/the-stack.md).

:::{tip}
To get started quickly, you can set up a [local development and testing environment](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md), or sign up for a [Serverless](https://cloud.elastic.co/serverless-registration) or [Hosted](https://cloud.elastic.co/registration) trial in {{ecloud}}.
:::

## Design and deploy

Learn how to design and deploy a production-ready Elastic environment.

* [](/deploy-manage/deploy.md): Understand your deployment options and choose the approach that best fits your needs.

  If you already know how you want to deploy, you can jump to the documentation for your preferred deployment method:
  * [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md)
  * [{{ech}}](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md)
  * [{{ece}}](/deploy-manage/deploy/cloud-enterprise.md)
  * [{{eck}}](/deploy-manage/deploy/cloud-on-k8s.md)
  * [Self-managed](/deploy-manage/deploy/self-managed.md)

* [](/deploy-manage/distributed-architecture.md): Learn about the architecture of {{es}} and {{kib}}, and how Elastic stores and retrieves data and executes tasks in clusters with multiple nodes.
* [](/deploy-manage/production-guidance.md): Review tips and guidance that you can use to design a production environment that matches your workloads, policies, and deployment needs.
* [](/deploy-manage/reference-architectures.md): Explore blueprints for deploying clusters tailored to different use cases.
* [](/deploy-manage/tools.md): Learn about the tools available to safeguard data, ensure continuous availability, and maintain resilience in your {{es}} environment.
* [](/deploy-manage/autoscaling.md): Learn how to configure your [orchestrated](/deploy-manage/deploy.md#about-orchestration) deployment to scale based on policies and cluster signals. Applies to {{ech}}, {{ece}}, and {{eck}} deployments.
* [](/deploy-manage/cloud-connect.md): Learn how to use {{ecloud}} services in your self-hosted environment.

:::{admonition} Serverless does it for you
If you deploy an {{serverless-full}} project, then you don't need to learn about Elastic architecture, production design, resilience, or scaling concepts. Serverless automatically scales and backs up your cluster for you, and is ready for production out of the box.
:::

## Secure and control access

Learn how to secure your Elastic environment to restrict access to only authorized parties, and allow communication between your environment and external parties.

* [](/deploy-manage/security.md): Learn about security features that prevent bad actors from tampering with your data, and encrypt communications to, from, and within your cluster.
* [](/deploy-manage/users-roles.md): Manage user authentication and authorization at the level of your Cloud organization, your orchestrator, or your deployment or cluster.
* [](/deploy-manage/manage-spaces.md): Learn how to organize content in {{kib}}, and restrict access to this content to specific users.
* [](/deploy-manage/api-keys.md): Authenticate and authorize programmatic access to your deployments and {{es}} resources.
* [](/deploy-manage/manage-connectors.md): Manage connection information between Elastic and third-party systems.
* [](/deploy-manage/remote-clusters.md): Enable communication between {{es}} clusters to support [cross-cluster replication](/deploy-manage/tools/cross-cluster-replication.md) and [cross-cluster search](/solutions/search/cross-cluster-search.md).

## Administer and maintain

Monitor the performance of your Elastic environment, administer your organization and license, and maintain the health of your environment.

* [](/deploy-manage/monitor.md): View health and performance data for Elastic components, and receive recommendations and insights.
* [](/deploy-manage/cloud-organization.md): Administer your {{ecloud}} organization, including billing, organizational contacts, and service monitoring.
* [](/deploy-manage/license.md): Learn how to manage your Elastic license or subscription.
* [](/deploy-manage/maintenance.md): Learn how to isolate or deactivate parts of your Elastic environment to perform maintenance, or restart parts of Elastic.
* [](/deploy-manage/uninstall.md): Uninstall one or more Elastic components.

## Upgrade

You can [upgrade your Elastic environment](/deploy-manage/upgrade.md) to gain access to the latest features. Learn how to upgrade your cluster or deployment to the latest {{stack}} version, or upgrade your {{ece}} orchestrator or {{eck}} operator to the latest version.

