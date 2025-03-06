---
applies_to:
  deployment:
    eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-readiness.html
---

# Readiness probe [k8s-readiness]

## Elasticsearch versions before 8.2.0 [k8s_elasticsearch_versions_before_8_2_0]

By default, the readiness probe checks that the Pod responds to HTTP requests within a timeout of three seconds. This is acceptable in most cases. However, when the cluster is under heavy load, you might need to increase the timeout. This allows the Pod to stay in a `Ready` state and be part of the Elasticsearch service even if it is responding slowly. To adjust the timeout, set the `READINESS_PROBE_TIMEOUT` environment variable in the Pod template and update the readiness probe configuration with the new timeout.

This example describes how to increase the API call timeout to ten seconds and the overall check time to twelve seconds:

```yaml
spec:
  version: 8.16.1
  nodeSets:
    - name: default
      count: 1
      podTemplate:
        spec:
          containers:
          - name: elasticsearch
            readinessProbe:
              exec:
                command:
                - bash
                - -c
                - /mnt/elastic-internal/scripts/readiness-probe-script.sh
              failureThreshold: 3
              initialDelaySeconds: 10
              periodSeconds: 12
              successThreshold: 1
              timeoutSeconds: 12
            env:
            - name: READINESS_PROBE_TIMEOUT
              value: "10"
```

Note that this requires restarting the Pods.

## Elasticsearch versions 8.2.0 and later [k8s_elasticsearch_versions_8_2_0_and_later]

% this feature might have disappeared, we will need to investigate this a bit more, as the link below doesn't work anymore but it does for 8.15 for example.

We do not recommend overriding the default readiness probe on Elasticsearch 8.2.0 and later. ECK configures a socket based readiness probe using the Elasticsearch [readiness port feature](elasticsearch://reference/elasticsearch/jvm-settings.md#readiness-tcp-port) which is not influenced by the load on the Elasticsearch cluster.


