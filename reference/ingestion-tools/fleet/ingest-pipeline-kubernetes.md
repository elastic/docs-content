---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/ingest-pipeline-kubernetes.html
---

# Using a custom ingest pipeline with the Kubernetes Integration [ingest-pipeline-kubernetes]

This tutorial explains how to add a custom ingest pipeline to a {{k8s}} Integration in order to add specific metadata fields for deployments and cronjobs of pods.

Custom pipelines can be used to add custom data processing, like adding fields, obfuscating sensitive information, and more.

## Metadata enrichment for Kubernetes [_metadata_enrichment_for_kubernetes]

The [{{k8s}} Integration](integration-docs://docs/reference/kubernetes.md) is used to collect logs and metrics from Kubernetes clusters with {{agent}}. During the collection, the integration enhances the collected information with extra useful information that users can correlate with different Kubernetes assets. This additional information added on top of collected data, such as labels, annotations, ancestor names of Kubernetes assets, and others, are called metadata.

The [{{k8s}} Provider](/reference/ingestion-tools/fleet/kubernetes-provider.md) offers the `add_resource_metadata` option to configure the metadata enrichment options.

For {{agent}} versions >[8.10.4], the default configuration for metadata enrichment is `add_resource_metadata.deployment=false` and `add_resource_metadata.cronjob=false`. This means that pods that are created from replicasets that belong to specific deployments would not be enriched with `kubernetes.deployment.name`. Additionally, pods that are created from jobs that belong to specific cronjobs, would not be enriched with `kubernetes.cronjob.name`.

**Kubernetes Integration Policy > Collect Kubernetes metrics from Kube-state-metrics > Kubernetes Pod Metrics**

:::{image} images/add_resource_metadata.png
:alt: Configure add_resource_metadata
:class: screenshot
:::

Example: Enabling the enrichment through `add_resource_metadata` in a Managed {{agent}} Policy.

:::{note}
Enabling deployment and cronjob metadata enrichment leads to an increase of Elastic Agent’s memory consumption. Elastic Agent uses a local cache in order to keep records of the Kubernetes assets from being discovered.
:::

## Add deployment and cronjob for {{k8s}} pods through ingest pipelines [_add_deployment_and_cronjob_for_k8s_pods_through_ingest_pipelines]

As an alternative to keeping the feature enabled and using more memory resources for {{agent}}, users can make use of ingest pipelines to add the missing fields of `kubernetes.deployment.name` and `kubernetes.cronjob.name`.

Navigate to `state_pod` datastream under: **Kubernetes Integration Policy > Collect Kubernetes metrics from Kube-state-metrics > Kubernetes Pod Metrics**.

Create the following custom ingest pipeline with two processors:

:::{image} images/ingest_pipeline_custom_k8s.png
:alt: Custom ingest pipeline
:class: screenshot
:::

### Processor for deployment [_processor_for_deployment]

:::{image} images/gsub_deployment.png
:alt: Gsub Processor for deployment
:class: screenshot
:::


### Processor for cronjob [_processor_for_cronjob]

:::{image} images/gsub_cronjob.png
:alt: Gsub Processor for cronjob
:class: screenshot
:::

The final `metrics-kubernetes.state_pod@custom` ingest pipeline:

```json
[
  {
    "gsub": {
      "field": "kubernetes.replicaset.name",
      "pattern": "(?:.(?!-))+$",
      "replacement": "",
      "target_field": "kubernetes.deployment.name",
      "ignore_missing": true,
      "ignore_failure": true
    }
  },
  {
    "gsub": {
      "field": "kubernetes.job.name",
      "pattern": "(?:.(?!-))+$",
      "replacement": "",
      "target_field": "kubernetes.cronjob.name",
      "ignore_missing": true,
      "ignore_failure": true
    }
  }
]
```

:::{note}
The ingest pipeline does not check for the actual existence of a deployment and cronjob ancestor, it only adds the specific values.
:::
