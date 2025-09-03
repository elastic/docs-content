---
navigation_title: Deployment options
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro-deploy.html
products:
  - id: elasticsearch
---

# Deployment options

You can run Elastic on virtually any infrastructure, allowing you to choose the model that best fits your operational needs. 

These are the most common deployment types and their main features:

* **{{serverless-full}}**: This fully managed SaaS offering abstracts away all underlying infrastructure, automatically and seamlessly scaling resources to meet your workload demands. It's designed for operational simplicity, with usage-based pricing that allows you to focus on your data without managing clusters.  
* **{{ech}}**: This managed SaaS offering provides you with a dedicated cluster on your choice of cloud provider (AWS, GCP, or Azure). It offers a high degree of control over your cluster's configuration, allowing you to fine-tune nodes, hardware, and versions to meet specific performance and architectural requirements.  
* **Self-managed**: This approach allows you to install, operate, and maintain the Elastic Stack on your own hardware, whether on-premises or in your private cloud. It provides maximum control over your environment.  
* **{{eck}} (ECK)**: This extends Kubernetes by providing an official operator for deploying and managing Elastic products. It's ideal if you want to run and orchestrate Elastic on your own Kubernetes platform.  
* **{{ece}} (ECE):** This Elastic self-managed offering allows you to provision, manage, and monitor Elasticsearch and Kibana at any scale, on any infrastructure, while managing everything from a single console. It's ideal if you want to use the full Elastic Stack while maintaining control over your data and infrastructure. 

For more information on Deployment modes, refer to [Detailed deployment comparison](/deploy-manage/deploy/deployment-comparison.md).