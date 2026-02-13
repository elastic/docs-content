---
navigation_title: Configure memory
applies_to:
  deployment:
    self: all
products:
  - id: kibana
---

# Configure {{kib}} memory

{{kib}} has a default memory limit that scales based on total memory available. In some scenarios, such as large reporting jobs, detection rules, managing alerting workflows, or working with SLOs, it may make sense to tweak memory limits to meet more specific performance requirements.

## Limit memory usage [memory]

A limit can be defined by setting `--max-old-space-size` in the `node.options` config file found inside the `kibana/config` folder or any other folder configured with the environment variable `KBN_PATH_CONF`. For example, in the Debian-based system, the folder is `/etc/kibana`.

The option accepts a limit in MB:

```js
--max-old-space-size=2048
```

::::{note}
In orchestrated environments like {{ech}}, {{ece}}, or {{eck}}, you should not override Kibana’s default memory limit using `--max-old-space-size`. Instead, set the desired {{kib}} memory size at the deployment level. This automatically adjusts the container’s memory allocation and ensures more consistent and predictable performance.
::::
