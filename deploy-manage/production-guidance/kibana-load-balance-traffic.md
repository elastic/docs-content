---
navigation_title: High availability and load balancing
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/production.html
applies_to:
  deployment:
    self: all
products:
  - id: kibana
---

# High Availability and load balancing in Kibana

This page provides guidance on scaling {{kib}} by distributing traffic across multiple instances, accessing multiple load-balanced deployments, and configuring high availability with multiple {{es}} nodes.

For scaling considerations related to background tasks, and the alerting framework, refer to [](./kibana-task-manager-scaling-considerations.md), and [](./kibana-alerting-production-considerations.md).

The configurations provided in this section are required only for self-managed deployments. Orchestration systems automatically apply the necessary settings when multiple {{kib}} instances belong to the same deployment.

## Load balancing across multiple {{kib}} instances [load-balancing-kibana]

To run multiple {{kib}} instances connected to the same {{es}} cluster, you need to adjust the configuration. See the [{{kib}} configuration reference](kibana://reference/configuration-reference.md) for details on each setting.

::::{note}
When adding multiple {{kib}} instances to the same deployment in {{ech}}, {{ece}}, or {{eck}}, the orchestrator applies the necessary configuration, requiring no manual setup.
::::

* When using a file appender, the target file must be unique:

  ```yaml
  logging:
    appenders:
      default:
        type: file
        fileName: /unique/path/per/instance
  ```

* These settings must be **the same** for all {{kib}} belonging to the same cluster or deployment:

  ```js
  xpack.security.encryptionKey // decrypting session information
  xpack.security.authc.* // authentication configuration
  xpack.security.session.* // session configuration
  xpack.reporting.encryptionKey // decrypting reports
  xpack.encryptedSavedObjects.encryptionKey // decrypting saved objects
  xpack.encryptedSavedObjects.keyRotation.decryptionOnlyKeys // saved objects encryption key rotation, if any
  ```

  ::::{warning} 
  If the authentication configuration does not match, sessions from unrecognized providers in each {{kib}} instance will be deleted during that instance’s regular session cleanup. Similarly, inconsistencies in session configuration can also lead to undesired session logouts. This also applies to any {{kib}} instances that are backed by the same {{es}} instance and share the same kibana.index, even if they are not behind the same load balancer.
  ::::

* Separate configuration files can be used from the command line by using the `-c` flag:

  ```js
  bin/kibana -c config/instance1.yml
  bin/kibana -c config/instance2.yml
  ```

## Accessing multiple load-balanced {{kib}} deployments [accessing-load-balanced-kibana] 

To access multiple load-balanced {{kib}} deployments from the same browser, explicitly set `xpack.security.cookieName` to the same value across all {{kib}} instances within the same cluster, and use different values for other clusters.

This prevents cookie conflicts between {{kib}} instances, ensuring seamless high availability and maintaining the session active in case of an instance failure.

::::{note}
In this context, a {{kib}} cluster or deployment refers to multiple {{kib}} instances connected to the same {{es}} cluster.
::::

## High availability across multiple {{es}} nodes [high-availability]

{{kib}} can be configured to connect to multiple {{es}} nodes in the same cluster.  In situations where a node becomes unavailable, {{kib}} will transparently connect to an available node and continue operating.  Requests to available hosts will be routed in a round robin fashion (except for Dev Tools which will connect only to the first node available).

In kibana.yml:

```js
elasticsearch.hosts:
  - http://elasticsearch1:9200
  - http://elasticsearch2:9200
```

Related configurations include `elasticsearch.sniffInterval`, `elasticsearch.sniffOnStart`, and `elasticsearch.sniffOnConnectionFault`. These can be used to automatically update the list of hosts as a cluster is resized.  Parameters can be found in the [{{kib}} configuration reference](kibana://reference/configuration-reference/general-settings.md).

::::{note}
This configuration can be useful when there is no load balancer or reverse proxy in front of {{es}}. If a load balancer is in place to distribute traffic among {{es}} instances, {{kib}} should be configured to connect to it instead. 

In [orchestrated deployments](/deploy-manage/deploy.md#about-orchestration), {{kib}} is automatically configured to connect to {{es}} through load-balanced services—such as platform proxies in ECE or ECH, or Kubernetes services in the case of ECK.
::::
