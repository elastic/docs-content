---
applies:
  eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-beat-troubleshooting.html
---

# Troubleshooting [k8s-beat-troubleshooting]

## Beat Pods are crashing when kibanaRef is specified [k8s-beat-beat-pods-are-crashing-when-kibanaref-is-specified]

When `kibanaRef` is specified, Beat tries to connect to the Kibana instance. If it’s unable to do so, the Beat process exits and the Pod restarts. This may happen when Kibana is not yet up or when a Beat user is not yet created in Elasticsearch. The Pod may restart a few times when it is first deployed. Afterwards, the Beat should run successfully.


## Configuration containing key: null is malformed [k8s-beat-configuration-containing-key-null-is-malformed]

When `kubectl` is used to modify a resource, it calculates the diff between the user applied and the existing configuration. This diff has special  [semantics](https://tools.ietf.org/html/rfc7396#section-1) that forces the removal of keys if they have special values. For example, if the user-applied configuration contains `some_key: null` (or equivalent `some_key: ~`), this is interpreted as an instruction to remove `some_key`. In Beats configurations, this is often a problem when it comes to defining things like [processors](https://www.elastic.co/guide/en/beats/filebeat/current/add-cloud-metadata.html). To avoid this problem:

* Use `some_key: {}` (empty map) or `some_key: []` (empty array) instead of `some_key: null` if doing so does not affect the behaviour. This might not be possible in all cases as some applications distinguish between null values and empty values and behave differently.
* Instead of using `config` to define configuration inline, use `configRef` and store the configuration in a Secret.


## Pod fails to start after update [k8s_pod_fails_to_start_after_update]

If you have configured a Beat to run as a `Deployment` and you are using a `hostPath` volume as the Beats data directory, you might encounter an error similar to the following:

```shell script
ERROR   instance/beat.go:958    Exiting: data path already locked by another beat. Please make sure that multiple beats are not sharing the same data path (path.data).
```

This can happen if the new Pod is scheduled on the same Kubernetes node as the old Pod and is now trying to use the same data directory. Use a [`Recreate`](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-beat-configuration.html#k8s-beat-chose-the-deployment-model) deployment strategy to avoid this problem.


