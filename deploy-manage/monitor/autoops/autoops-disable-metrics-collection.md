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

AutoOps collects data from your self-managed cluster with the help of {{agent}} and analyzes related metrics to diagnose issues and provide performance recommendations. 

If you don't want the agent to access certain types of data, you can disable the collection of related metrics by editing your configuration file as described in the following section.

## Edit your AutoOps configuration file

To disable the collection of certain types of data from your environment, delete the lines related to that data from your `autoops_es.yml` file.

Complete the following steps:

1. On your host machine, open the `autoops_es.yml` file. The default location is ``.
2. In the `autoops_es.yml` file, locate the metric or module related to the data that you want AutoOps to stop collecting. 
3. Delete the related lines from the file. For example,
    * to disable the collection of task-related data, delete the `tasks_management` line 
    * to disable the collection of template-related data, delete the `Templates` module 
    The following code demonstrates these examples:

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
                # --- DELETE THIS LINE ---
                - tasks_management
            # --- DELETE THIS MODULE ---
            # Templates
            - module: autoops_es
              hosts: ${env:AUTOOPS_ES_URL}
              period: 24h
              metricsets:
                - cat_template
                - component_template
                - index_template
    ```
4. Save your changes to the `autoops_es.yml` file.
5. Restart {{agent}} so that the new settings can take effect.\
    In most systemd-based Linux environments, you can use the following command to restart the agent:
    ```bash
    sudo systemctl restart elastic-agent
    ```