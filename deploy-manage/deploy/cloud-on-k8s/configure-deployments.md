---
applies:
  eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-orchestrating-elastic-stack-applications.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-update-deployment.html
---

% the security link needs to be refined to point to the eck related section around security
% same for upgrade link

# Configure deployments [k8s-orchestrating-elastic-stack-applications]

This section provides details around {{kib}} and {{es}} configuration when running on ECK. For general information about how ECK applies configuration changes and the syntax to use in the YAML manifests, refer to [](./update-deployments.md).

* [**{{es}} configuration**](elasticsearch-configuration.md) → Review configuration possibilities to tune your {{es}} cluster running on ECK, learn how [nodes orchestration](./nodes-orchestration.md) work, [storage recommendations](./storage-recommendations.md), and more.

  * [](./requests-routing-to-elasticsearch-nodes.md) → Control the nodes receiving incoming traffic when using multiple `nodeSets` with different [node roles](https://www.elastic.co/guide/en/elasticsearch/reference/current/node-roles-overview.html).

* [**{{kib}} configuration**](kibana-configuration.md) → Learn how to connect {{kib}} to an {{es}} cluster, apply advanced configuration settings, and tune the HTTP configuration.

Additionally, the following topics apply to both {{es}} and {{kib}}, and in some cases, to other applications supported by ECK:

* [**Access services**](accessing-services.md) → Learn how to access to the orchestrated clusters and how to adapt the Kubernetes services to your needs.

* [**TLS certificates**](./tls-certificates.md) → Use your own SSL/TLS certificates for the HTTP endpoint of {{es}} or {{kib}}.

* [**Secure the Elastic Stack**](../../security.md) → Manage users and roles, authentication realms, and more.

* [**Recipes**](recipes.md) → Advanced use cases examples available in our GitHub repository. 

* [**Customize Pods**](customize-pods.md) → Learn how to adapt the `podTemplate` field to your needs.

* [**Manage compute resources**](manage-compute-resources.md) → Important considerations around CPU and memory when running production workloads.

* [**Autoscaling stateless applications**](../../autoscaling/autoscaling-stateless-applications-on-eck.md) → Use [Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) for {{kib}} or other stateless applications.

* [**Connect to external Elastic resources**](connect-to-external-elastic-resources.md) → Use `secrets` with custom settings for `elasticsearchRef` and `kibanaRef` parameters.

ECK also facilitates configuration and operation activities with advanced features, such as:

* [**Elastic Stack configuration policies**](elastic-stack-configuration-policies.md) → Organize your {{es}} and {{kib}} configuration settings through `StackConfigPolicy` resources that can be referenced within your deployments.

* [**Stack monitoring**](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-stack-monitoring.html) → Monitor your deployments smoothly with the help of ECK.

* [**Remote clusters**](/deploy-manage/remote-clusters/eck-remote-clusters.md) → Configure {{es}} remote clusters functionality for Cross Cluster Search (CCS) and Cross Cluster Replication.

* [**Upgrade the Elastic Stack version**](../../upgrade/deployment-or-cluster.md) → Upgrade orchestrated applications on ECK.