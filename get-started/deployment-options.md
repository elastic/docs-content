---
navigation_title: Deployment options
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro-deploy.html
products:
  - id: elasticsearch
applies_to:
  serverless:
  stack:
---

# Deployment options?

You can run Elastic on any infrastructure, allowing you to choose the model that best fits your operational needs.

Use this page for a quick overview of your options for deploying Elastic!

Utilize the above control.

## Why your deployment choice matters

Your deployment type significantly impacts the capabilities available across your Elastic environment and the amount of manual work required to set up and maintain it. Some deployment types provide automated orchestration that handles scaling, upgrades, and monitoring across multiple clusters, while others require you to manage these operational tasks manually. 

The choice you make determines how much time you'll spend on infrastructure management versus focusing on using Elastic's features to solve your business problems.

## Quick start options

These are the most common deployment types and their main features:

* **[{{ecloud}}](/deploy-manage/deploy/elastic-cloud.md)**: Get a hosted solution up and running in minutes.
  * **[{{ech}}](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md)**: This offering, managed through [{{ecloud}}](/deploy-manage/deploy/elastic-cloud.md), provides you with a dedicated cluster on your choice of cloud provider (AWS, GCP, or Azure). It offers high control over your cluster's configuration, allowing you to fine-tune nodes, hardware, and versions to meet specific performance and architectural requirements. Sign up for a [14-day free trial](https://cloud.elastic.co/registration).
  * **[{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md)**: This fully managed SaaS offering managed through [{{ecloud}}](/deploy-manage/deploy/elastic-cloud.md) abstracts away all underlying infrastructure, automatically and seamlessly scaling resources to meet your workload demands. It's designed for operational simplicity, with usage-based pricing that allows you to focus on your data without managing clusters. Sign up for a [14-day free trial](https://cloud.elastic.co/serverless-registration).
* **[Local development](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md)**: Get started quickly with {{es}} and {{kib}} in Docker for local development and testing.

## Advanced options

* **[Self-managed](/deploy-manage/deploy/self-managed.md)**: This approach allows you to install, operate, and maintain components of the {{stack}} on your own hardware, whether on-premises or in your private cloud. It provides maximum control over your environment.
* **[{{ece}}](/deploy-manage/deploy/cloud-enterprise.md)**: This Elastic self-managed offering allows you to provision, manage, and monitor components of the {{stack}} at any scale and on any infrastructure, while managing everything from a single console.
* **[{{eck}}](/deploy-manage/deploy/cloud-on-k8s.md)**: This extends Kubernetes by providing an official operator for deploying and managing components of the {{stack}}. It's ideal if you want to run and orchestrate Elastic on your own Kubernetes platform.

:::{tip}
Refer to [Deploy and manage](/deploy-manage/index.md) for detailed information and guidance on selecting the appropriate deployment for your needs.
:::
