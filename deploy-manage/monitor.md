---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/monitor-elasticsearch-cluster.html
  - https://www.elastic.co/guide/en/cloud/current/ec-monitoring.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
---

# Monitoring

Keeping on top of the health of your cluster or deployment, as well as your orchestrator, is an important part of maintenance. It also helps you to identify and troubleshoot issues. When you move to [production](/deploy-manage/production-guidance.md), detecting and resolving issues when they arise is a key component of keeping your deployment highly available.

Depending on your deployment type, you can use a variety of solutions for monitoring your Elastic components.

## Monitoring your cluster or deployment

Depending on your deployment type and context, you have several options for monitoring your cluster or deployment.

### AutoOps (recommended)

```{applies_to}
deployment:
  ech:
```

:::{include} /deploy-manage/monitor/_snippets/autoops.md
:::

### Stack monitoring

```{applies_to}
deployment:
  ech:
  ece:
  eck:
  self:
```

:::{include} /deploy-manage/monitor/_snippets/stack-monitoring-def.md
:::

In {{ece}} and {{ech}}, Elastic manages the installation and configuration of the monitoring agent for you, simplifying the stack monitoring setup process.

:::{include} /deploy-manage/monitor/_snippets/stack-monitoring-prod.md
:::

### Cluster health and performance metrics

```{applies_to}
deployment:
  ece:
  ech:
```

{{ece}} and {{ech}} provide out of the box tools for monitoring the health of your deployment and resolving health issues when they arise: 

* [Cluster health information](/deploy-manage/monitor/cloud-health-perf.md#ec-es-cluster-health), including [health warnings](/deploy-manage/monitor/cloud-health-perf.md#ec-es-health-warnings)
* A [JVM memory pressure indicator](/deploy-manage/monitor/ec-memory-pressure.md)

{{ech}} only:
* [Cluster performance information](/deploy-manage/monitor/access-performance-metrics-on-elastic-cloud.md)
* [Preconfigured logs and metrics](/deploy-manage/monitor/cloud-health-perf.md#ec-es-health-preconfigured)

{{ece}} only:
* [Platform monitoring](/deploy-manage/monitor/orchestrators/ece-platform-monitoring.md), including logs, metrics, and proxy logs

:::{tip}
Out of the box logs and metrics tools, including ECH preconfigured logs and metrics and ECE platform monitoring logs and metrics, are useful for providing information in a non-production environment. In a production environment, it’s important set up either AutoOps or stack monitoring to retain the logs and metrics that can be used to troubleshoot any health issues in your deployments. In the event of that you need to [contact our support team](/troubleshoot/index.md#contact-us), they can use the retained data to help diagnose any problems that you may encounter.
:::

To learn more about the health and performance tools in {{ecloud}}, refer to [](/deploy-manage/monitor/cloud-health-perf.md).

## Monitoring your orchestrator
```{applies_to}
deployment:
  ece:
  eck:
```

TODO

## Logging

TODO

% * [*Elasticsearch application logging*](../../../deploy-manage/monitor/logging-configuration/update-elasticsearch-logging-levels.md)

