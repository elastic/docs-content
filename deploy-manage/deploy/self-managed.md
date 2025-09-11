---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/dependencies-versions.html
  - https://www.elastic.co/guide/en/elastic-stack/current/installing-stack-demo-self.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
---

# Self-managed cluster

If you want to install Elastic on your own premises without the assistance of an [orchestrator](/deploy-manage/deploy.md#about-orchestration), then you can deploy a self-managed cluster. If you deploy a self-managed cluster, then you have complete control and responsibility over every aspect of your Elastic deployment.

To quickly set up {{es}} and {{kib}} in Docker for local development or testing, jump to [](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md).

:::{admonition} Simplify the deployment process
Self-managed clusters are useful for local development, and for exploring Elastic features. However, Elastic offers several deployment options that can simplify the process of deploying and managing multi-node deployments, especially in production. They also allow you to deploy and manage multiple deployments from a single surface.

Managed by Elastic:
* [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md)
* [{{ech}}](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md)

Self-hosted options:
* [{{eck}}](/deploy-manage/deploy/cloud-on-k8s.md)
* [{{ece}}](/deploy-manage/deploy/cloud-enterprise.md)

For a comparison of these deployment options, refer to [Choosing your deployment type](/deploy-manage/deploy.md#choosing-your-deployment-type) and [](/deploy-manage/deploy/deployment-comparison.md).
:::

:::{admonition} Use cloud services in your self-managed cluster with Cloud Connect
If you need to run Elastic on your own infrastructure, use [Cloud Connect](/deploy-manage/cloud-connect.md). Cloud connect enables you to use Elastic-managed cloud services in your self-managed cluster without having to install and manage their infrastructure yourself.

This way, you can get faster access to new cloud features while still meeting your infrastructure requirements.
:::

## Installation order

:::{include} /deploy-manage/deploy/_snippets/installation-order.md
:::

## Section overview

This section focuses on deploying {{es}} and {{kib}} without an orchestrator.

Depending on your use case, you might need to deploy other components, such as APM, Fleet, or Logstash.
Deploying those components is not covered in this section. [Learn more about optional components](/get-started/the-stack.md).

This section covers the following tasks:

### Deploying Elasticsearch

Learn how to install and configure {{es}}. {{es}} is the distributed search and analytics engine, scalable data store, and vector database at the heart of all Elastic solutions.

* [](/deploy-manage/deploy/self-managed/installing-elasticsearch.md)
  * [](/deploy-manage/deploy/self-managed/important-system-configuration.md): Prepare your environment for an {{es}} installation.
  * [](/deploy-manage/deploy/self-managed/installing-elasticsearch.md#installation-methods): Install and run {{es}} using one of our install packages or container images.
  * [](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md): Quickly set up {{es}} and {{kib}} in Docker for local development or testing.
* [](/deploy-manage/deploy/self-managed/configure-elasticsearch.md): Learn how to make configuration changes to {{es}}
  * [](/deploy-manage/deploy/self-managed/important-settings-configuration.md): Learn about key settings required for production environments.
  * [](/deploy-manage/deploy/self-managed/plugins.md): Learn about how to extend {{es}} functionality with plugins.

    :::{note}
    For a complete list of settings that you can apply to your {{es}} cluster, refer to the [{{es}} configuration reference](elasticsearch://reference/elasticsearch/configuration-reference/index.md).
    :::

### Deploying Kibana

After you deploy {{es}}, you can install {{kib}}. {{kib}} provides the user interface for all Elastic solutions. It’s a powerful tool for [visualizing and analyzing](/explore-analyze/index.md) your data, and for managing and monitoring the {{stack}}. Although {{kib}} is not required to use {{es}}, it's required for most [use cases](/solutions/index.md).

* [](/deploy-manage/deploy/self-managed/install-kibana.md): Install {{kib}} using one of our install packages or container images, and enroll {{kib}} with your {{es}} cluster.
* [](/deploy-manage/deploy/self-managed/configure-kibana.md): Learn how to make configuration changes to {{kib}}.
* [](/deploy-manage/deploy/self-managed/access-kibana.md): Learn how to access {{kib}} using a web browser.

### Installing in air gapped environments

Some components of the {{stack}} require additional configuration and local dependencies in order to deploy in environments without internet access.

Refer to [](/deploy-manage/deploy/self-managed/air-gapped-install.md) to learn how to install {{es}}, {{kib}}, and optional components in an environment without internet access.

### Tools and APIs

Review a list of all of the resources that you can use to interact with your self-managed cluster, including tools, APIs, client libraries, and more.

[](/deploy-manage/deploy/self-managed/tools-apis.md).

## Other important sections

Review these other sections for critical information about securing and managing your self-managed cluster.

### Secure and control access

Learn how to secure your Elastic environment to restrict access to only authorized parties, and allow communication between your environment and external parties.

* [](/deploy-manage/security.md): Learn about security features that prevent bad actors from tampering with your data, and encrypt communications to, from, and within your cluster.
* [Users and roles](/deploy-manage/users-roles/cluster-or-deployment-auth.md): Set up authentication and authorization for your cluster, and learn about the underlying security technologies that {{es}} uses to authenticate and authorize requests internally and across services.
* [](/deploy-manage/manage-spaces.md): Learn how to organize content in {{kib}}, and restrict access to this content to specific users.
* [](/deploy-manage/api-keys.md): Authenticate and authorize programmatic access to your deployments and {{es}} resources.
* [](/deploy-manage/manage-connectors.md): Manage connection information between Elastic and third-party systems.
* [](/deploy-manage/remote-clusters/remote-clusters-self-managed.md): Enable communication between {{es}} clusters to support [cross-cluster replication](/deploy-manage/tools/cross-cluster-replication.md) and [cross-cluster search](/solutions/search/cross-cluster-search.md).

### Administer and maintain

Monitor the performance of your Elastic environment, administer your license, set up backup and resilience tools, and maintain the health of your environment.

* [](/deploy-manage/tools.md): Learn about the tools available to safeguard data, ensure continuous availability, and maintain resilience in your {{es}} environment.
* [](/deploy-manage/monitor.md): View health and performance data for Elastic components, and receive recommendations and insights.
* [](/deploy-manage/license.md): Learn how to manage your Elastic license.
* [](/deploy-manage/maintenance/start-stop-services.md): Learn how to isolate or deactivate parts of your Elastic environment to perform maintenance, or restart parts of Elastic.
* [](/deploy-manage/maintenance/add-and-remove-elasticsearch-nodes.md): Learn how to add nodes to a cluster or remove them from a cluster to change the size and capacity of {{es}}.

### Upgrade

You can [upgrade your Elastic environment](/deploy-manage/upgrade.md) to gain access to the latest features.

### Design guidance

Learn how to design a production-ready Elastic environment.

* [](/deploy-manage/production-guidance.md): Review tips and guidance that you can use to design a production environment that matches your workloads, policies, and deployment needs.
* [](/deploy-manage/reference-architectures.md): Explore blueprints for deploying clusters tailored to different use cases.

### Architectural information

In the [](/deploy-manage/distributed-architecture.md) section, learn about the architecture of {{es}} and {{kib}}, and how Elastic stores and retrieves data and executes tasks in clusters with multiple nodes.