---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-best-practices-data.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
products:
  - id: cloud-hosted
---

% scope: the scope of this page is just a brief introduction to prod guidance at {{stack}} level, links to ES and KIB,
# Production guidance

Running the {{stack}} in production requires careful planning to ensure resilience, performance, and scalability. This section outlines best practices and recommendations for optimizing {{es}} and {{kib}} in production environments.

You’ll learn how to design highly available and resilient deployments, implement best practices for managing workloads, and apply performance optimizations to handle scaling demands efficiently.

For {{es}}, this includes strategies for fault tolerance, data replication, and workload distribution to maintain stability under load. For {{kib}}, you’ll explore how to deploy multiple {{kib}} instances within the same environment and make informed decisions about scaling horizontally or vertically based on the task manager metrics, which provide insights into background task execution and resource consumption.

By following this guidance, you can ensure your {{stack}} deployment is robust, efficient, and prepared for production-scale workloads.

For detailed, component-specific guidance, refer to:
* [](./production-guidance/elasticsearch-in-production-environments.md)
* [](./production-guidance/kibana-in-production-environments.md)

## Deployment types

Production guidelines and concepts described in this section apply to all [deployment types](/deploy-manage/deploy.md#choosing-your-deployment-type)—including {{ech}}, {{ece}}, {{eck}}, and self-managed clusters—**except** {{serverless-full}}.

However, certain parts may be relevant only to self-managed clusters, as orchestration systems automate some of the configurations discussed here. Check the [badges](/get-started/versioning-availability.md#availability-of-features) on each document or section to confirm whether the content applies to your deployment type.

::::{note}
**{{serverless-full}}** projects are fully managed and automatically scaled by Elastic. Your project’s performance and general data retention are controlled by the [Search AI Lake settings](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-ai-lake-settings).
::::

## Other Elastic products

If you are looking for production guidance for Elastic products other than {{es}} or {{kib}}, check out the following resources:

* [High availability on ECE orchestrator](/deploy-manage/deploy/cloud-enterprise/ece-ha.md)
* [APM scalability and performance](/troubleshoot/observability/apm/processing-performance.md)
* [Fleet server scalability](/reference/fleet/fleet-server-scalability.md)
* [Deploying and scaling Logstash](logstash://reference/deploying-scaling-logstash.md)
