---
applies:
  eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-orchestrating-elastic-stack-applications.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-update-deployment.html
---

# Configure deployments [k8s-orchestrating-elastic-stack-applications]

This section provides details around {{kib}} and {{es}} configuration when running on ECK. For general information about how ECK applies configuration changes and the syntax to use in the YAML manifests, refer to [](./update-deployments.md).

* [**{{es}} configuration**](elasticsearch-configuration.md): Review configuration possibilities to tune your {{es}} cluster running on ECK, learn how [nodes orchestration](./nodes-orchestration.md) work, [storage recommendations](./storage-recommendations.md), and more.

* [**{{kib}} configuration**](kibana-configuration.md): Learn how to connect {{kib}} to an {{es}} cluster, apply advanced configuration settings, and tune the HTTP configuration.

Additionally, the following topics apply to both {{es}} and {{kib}}, and in some cases, to other applications supported by ECK:

* [**Access services**](accessing-services.md): Learn how to access to the orchestrated clusters and how to adapt the Kubernetes services to your needs.

* [**Customize Pods**](customize-pods.md): Learn how to adapt the `podTemplate` field to your needs.

* [**Manage compute resources**](manage-compute-resources.md): Important considerations around CPU and memory `requests` and `limits` when running production workloads.

* [**Recipes**](recipes.md): Advanced use cases examples available in our GitHub repository. 

* [**Connect to external Elastic resources**](connect-to-external-elastic-resources.md): Use custom `secrets` for the `elasticsearchRef` and `kibanaRef` parameters.

ECK also facilitates configuration and operation activities with advanced features, such as:

* [**Elastic Stack configuration policies**](elastic-stack-configuration-policies.md): Organize your {{es}} and {{kib}} configuration settings through `StackConfigPolicy` resources that can be referenced within your deployments. This helps to keep your manifests simplified.

## Other sections
% check this other sections with the same section on elasticsearch-configuration to decide what to do
Other sections of the Elastic documentation cover additional topics related to deployments configuration on ECK:

**Security**

% the two pages about HTTP TLS certificate should be merged into one and be placed on Security docs
  * [**HTTP TLS certificates**](/deploy-manage/security/secure-http-communications.md): Use your own SSL/TLS certificates for the HTTP endpoint of {{es}} and {{kib}}.

  * Custom HTTP certificate -> TBD: https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-custom-http-certificate.html

  * SAML authentication -> TBD: https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-saml-authentication.html (this mixes Elasticsearch and Kibana)

  * [Users and roles] -> TBD Link to wherever this ends up: https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-users-and-roles.html

**Monitoring and Logging**

  * [**Stack monitoring**](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-stack-monitoring.html): Use ECK to manage logs and metrics for your deployments.
