---
navigation_title: Configure memory
applies_to:
  deployment:
    self: all
products:
  - id: kibana
---

# Configure {{kib}} memory

{{kib}} has a default memory limit that scales based on total memory available.

The default limit is sufficient for core {{kib}} functionality. In some scenarios, such as large reporting jobs, detection rules, managing alerting workflows, or working with SLOs, we recommend increasing memory limits to at least 2 GB to meet more specific performance requirements.

For Platinum and Enterprise users, we recommend at least 2 GB of memory for each {{kib}} instance to avoid service interruptions when using advanced features.

## Limit memory usage [memory]

A limit can be defined by setting `--max-old-space-size` in the `node.options` config file found inside the `kibana/config` folder or any other folder configured with the environment variable `KBN_PATH_CONF`. For example, in the Debian-based system, the folder is `/etc/kibana`.

The option accepts a limit in MB:

```js
--max-old-space-size=2048
```

::::{note}
Starting in {{kib}} version 9.4.0, containers set the default Node.js heap to 75% of available memory, up to a maximum of 4096 MB. Previously, this was set to 50% regardless of the environment.

In orchestrated environments like {{ech}}, {{ece}}, you should not override Kibana’s default memory limit using `--max-old-space-size`. Instead, set the desired {{kib}} memory size at the deployment level. This automatically adjusts the container’s memory allocation and ensures more consistent and predictable performance.

In {{eck}}, the {{kib}} memory size is not automatically adjusted, but the default memory size logic applies. You can override the default memory settings if they do not meet your requirements. Review [ECK - Manage compute resources](../deploy/cloud-on-k8s/manage-compute-resources.md#k8s-compute-resources-kibana-and-apm) for more guidance.
::::
