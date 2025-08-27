You can add your own {{kib}} settings to the `spec.config` section.

The following example demonstrates how to set the [`elasticsearch.requestHeadersWhitelist`](kibana://reference/configuration-reference/general-settings.md#elasticsearch-requestheaderswhitelist) configuration option.

```yaml subs=true
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana-sample
spec:
  version: {{version.stack}}
  count: 1
  elasticsearchRef:
    name: "elasticsearch-sample"
  config:
     elasticsearch.requestHeadersWhitelist:
     - authorization
```