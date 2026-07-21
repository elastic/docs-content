---
applies_to:
  deployment:
    self:
    ece:
    eck:
navigation_title: Disable certain types of data collection
products:
  - id: cloud-kubernetes
  - id: cloud-enterprise
---

# Disable certain types of data collection by AutoOps 

When you connect your ECE, ECK, or self-managed {{es}} cluster to AutoOps, {{agent}} collects data from your cluster and sends it to AutoOps to diagnose issues and provide performance recommendations. 

If you don't want the agent to access certain types of data, you can disable the collection of related metrics by editing your configuration file as described in the following section.

:::{warning}
Disable data collection only when necessary, as it limits the insights that AutoOps can provide. For example, disabling the collection of cluster health metrics prevents you from receiving critical warnings and diagnostics about your cluster's health.
:::

## Configure data collection

:::::{tab-set}
:group: autoops-configure-collection

::::{tab-item} Edit configuration file
:sync: configure-collection-other

To disable the collection of certain types of data from your environment, delete the lines related to that data from your `autoops_es.yml` file on the host machine where {{agent}} is installed.

Complete the following steps:

1. On your host machine, open the `autoops_es.yml` file.
2. In the `autoops_es.yml` file, locate the metricset or section related to the data that you want AutoOps to stop collecting. 
3. Delete the related lines from the file.

    ```yaml
    receivers:
      metricbeatreceiver:
        metricbeat:
          modules:
            # Metrics
            - module: autoops_es
              hosts: ${env:AUTOOPS_ES_URL}
              period: 10s
              metricsets:
                - cat_shards
                - cluster_health
                - cluster_settings
                - license
                - node_stats
                - tasks_management <1>
            # Templates
            - module: autoops_es <2>
              hosts: ${env:AUTOOPS_ES_URL}
              period: 24h
              metricsets:
                - cat_template
                - component_template
                - index_template
    ```
    For example, 
    1. to disable the collection of task-related data, delete the `tasks_management` line
    2. to disable the collection of template-related data, delete all the lines in the `Templates` section
4. Save your changes to the `autoops_es.yml` file.
5. Restart {{agent}} for the new settings to take effect.

::::

::::{tab-item} ECK
:sync: configure-collection-eck
```{applies_to}
deployment:
  eck: ga 3.5
```

When using {{eck}}, configure data collection directly in the `AutoOpsAgentPolicy` resource using `spec.config` or `spec.configRef`. At most one of these fields can be set at a time.

Use `spec.config` for inline configuration:

```yaml
apiVersion: autoops.k8s.elastic.co/v1alpha1
kind: AutoOpsAgentPolicy
metadata:
  name: autoops-agent-policy
spec:
  config:
    receivers:
      metricbeatreceiver:
        metricbeat:
          modules:
            - module: autoops_es
              period: 30s
              metricsets: [cluster_health]
```

Or use `spec.configRef` to reference a Kubernetes Secret. The secret must use the key `autoops_es.yml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-autoops-config
stringData:
  autoops_es.yml: |
    receivers:
      metricbeatreceiver:
        metricbeat:
          modules:
            - module: autoops_es
              period: 30s
              metricsets: [cluster_health]
---
apiVersion: autoops.k8s.elastic.co/v1alpha1
kind: AutoOpsAgentPolicy
metadata:
  name: autoops-agent-policy
spec:
  configRef:
    secretName: my-autoops-config
```

When you supply at least one `autoops_es` module, ECK uses it instead of the built-in Metrics and Templates modules, giving you full control over which metricsets are collected and at what interval. Elasticsearch connection details, the OTLP exporter endpoint, and the healthcheck extension are always injected by ECK and cannot be overridden.

::::

:::::