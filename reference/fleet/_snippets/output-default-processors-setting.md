This setting turns off some or all of the default processors that {{agent}} uses to add host, cloud, Docker, and {{k8s}} metadata to events. It applies to the data sent to this output, including {{agent}} monitoring data if this is the monitoring output. Turning off a processor removes the fields it adds, so check that the dashboards, alerts, and other features you use don't rely on those fields.

The setting accepts these options:

* `enabled`: Turns all four processors on or off at once. Set to `false` to turn them all off.
* `add_host_metadata`, `add_cloud_metadata`, `add_docker_metadata`, and `add_kubernetes_metadata`: Turn the individual processors on or off. Set a processor to `false` to turn it off. The processors you don't list stay on.

Individual processor settings take precedence over `enabled`. For example, to keep only cloud metadata, set `enabled` to `false` and `add_cloud_metadata` to `true`.

This example turns off the processors that add Docker and {{k8s}} metadata:

```yaml
default_processors:
  add_docker_metadata: false
  add_kubernetes_metadata: false
```

**Default:** All four processors are on.
