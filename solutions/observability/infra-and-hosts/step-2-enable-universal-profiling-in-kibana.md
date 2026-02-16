---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/profiling-self-managed-enable-kibana.html
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: observability
---

# Step 2: Enable Universal Profiling in Kibana [profiling-self-managed-enable-kibana]

Configure {{kib}} to enable the Universal Profiling plugin with the following configuration:

```yaml
xpack.profiling.enabled: true
```

Refer to the steps for your platform to deploy update the configuration.


## ECE [_ece]

Install the 8.12.0 stackpack or higher. Refer to [ECE manage elastic stack](/deploy-manage/deploy/cloud-enterprise/manage-elastic-stack-versions.md) for more information.

In ECE, you don’t need to perform any additional steps to enable the Universal Profiling plugin in Kibana.


## Self-managed Elastic stack [_self_managed_elastic_stack]

1. Edit the Kibana YAML configuration file, usually named [`kibana.yml`](/deploy-manage/stack-settings.md) by adding previous configuration line.
2. Restart Kibana to reload the configuration.


## Kubernetes [_kubernetes]

If you’re using ECK, add the previous configuration line to the `kibana.k8s.elastic.co/v1` CRD, placing it under the `spec.config` key. Refer to the [ECK documentation](/deploy-manage/deploy/cloud-on-k8s/k8s-kibana-advanced-configuration.md#k8s-kibana-configuration) for more on configuring {{kib}}.

If you’re not using ECK, edit the `secret` or `configMap` holding the [`kibana.yml`](/deploy-manage/stack-settings.md) configuration file. Add the previously mentioned config line, and then perform a rolling restart of the Kibana deployment to reload the configuration.

Continue to [Step 3: Set up Universal Profiling in {{kib}}](step-3-set-up-universal-profiling-in-kibana.md).

