---
applies:
  eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-logstash-configuration-examples.html
---

# Configuration examples [k8s-logstash-configuration-examples]

This section contains manifests that illustrate common use cases, and can be your starting point in exploring Logstash deployed with ECK. These manifests are self-contained and work out-of-the-box on any non-secured Kubernetes cluster. They all contain a three-node Elasticsearch cluster and a single Kibana instance.

::::{warning}
The examples in this section are for illustration purposes only. They should not be considered production-ready. Some of these examples use the `node.store.allow_mmap: false` setting on {{es}} which has performance implications and should be tuned for production workloads, as described in [Virtual memory](virtual-memory.md).
::::


## Single pipeline defined in CRD [k8s-logstash-configuration-single-pipeline-crd]

```sh
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/2.16/config/recipes/logstash/logstash-eck.yaml
```

Deploys Logstash with a single pipeline defined in the CRD


## Single Pipeline defined in Secret [k8s-logstash-configuration-single-pipeline-secret]

```sh
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/2.16/config/recipes/logstash/logstash-pipeline-as-secret.yaml
```

Deploys Logstash with a single pipeline defined in a secret, referenced by a `pipelineRef`


## Pipeline configuration in mounted volume [k8s-logstash-configuration-pipeline-volume]

```sh
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/2.16/config/recipes/logstash/logstash-pipeline-as-volume.yaml
```

Deploys Logstash with a single pipeline defined in a secret, mounted as a volume, and referenced by `path.config`


## Writing to a custom Elasticsearch index [k8s-logstash-configuration-custom-index]

```sh
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/2.16/config/recipes/logstash/logstash-es-role.yaml
```

Deploys Logstash and Elasticsearch, and creates an updated version of the `eck_logstash_user_role` to write to a user specified index.


## Creating persistent volumes for PQ and DLQ [k8s-logstash-configuration-pq-dlq]

```sh
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/2.16/config/recipes/logstash/logstash-volumes.yaml
```

Deploys Logstash, Beats and Elasticsearch. Logstash is configured with two pipelines:

* a main pipeline for reading from the {{beats}} instance, which will send to the DLQ if it is unable to write to Elasticsearch
* a second pipeline, that will read from the DLQ. In addition, persistent queues are set up. This example shows how to configure persistent volumes outside of the default `logstash-data` persistent volume.


## Elasticsearch and Kibana Stack Monitoring [k8s-logstash-configuration-stack-monitoring]

```sh
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/2.16/config/recipes/logstash/logstash-monitored.yaml
```

Deploys an Elasticsearch and Kibana monitoring cluster, and a Logstash that will send its monitoring information to this cluster. You can view the stack monitoring information in the monitoring cluster’s Kibana


## Multiple pipelines/multiple Elasticsearch clusters [k8s-logstash-configuration-multiple-pipelines]

```sh
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/2.16/config/recipes/logstash/logstash-multi.yaml
```

Deploys Elasticsearch in prod and qa configurations, running in separate namespaces. Logstash is configured with a multiple pipeline→pipeline configuration, with a source pipeline routing to `prod` and `qa` pipelines.
