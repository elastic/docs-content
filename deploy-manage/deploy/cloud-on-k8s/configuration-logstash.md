---
applies:
  eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-logstash-configuration.html
---

# Configuration [k8s-logstash-configuration]

## Upgrade the Logstash specification [k8s-logstash-upgrade-specification]

You can upgrade the Logstash version or change settings by editing the YAML specification. ECK applies the changes by performing a rolling restart of Logstash Pods.


## Logstash configuration [k8s-logstash-configuring-logstash]

Define the Logstash configuration (the ECK equivalent to `logstash.yml`) in the `spec.config` section:

```yaml
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: quickstart
spec:
  version: 8.16.1
  count: 1
  elasticsearchRefs:
  - name: quickstart
    clusterName: qs
  config: <1>
    pipeline.workers: 4
    log.level: debug
```

1. Customize Logstash configuration using `logstash.yml` settings here


Alternatively, you can provide the configuration through a Secret specified in the `spec.configRef` section. The Secret must have a `logstash.yml` entry with your settings:

```yaml
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: quickstart
spec:
  version: 8.16.1
  count: 1
  elasticsearchRefs:
  - name: quickstart
    clusterName: qs
  configRef:
    secretName: quickstart-config
---
apiVersion: v1
kind: Secret
metadata:
  name: quickstart-config
stringData:
  logstash.yml: |-
    pipeline.workers: 4
    log.level: debug
```


## Configuring Logstash pipelines [k8s-logstash-pipelines]

Define Logstash pipelines in the `spec.pipelines` section (the ECK equivalent to `pipelines.yml`):

```yaml
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: quickstart
spec:
  version: 8.16.1
  count: 1
  elasticsearchRefs:
    - clusterName: qs
      name: quickstart
  pipelines:
    - pipeline.id: main
      config.string: |
        input {
          beats {
            port => 5044
          }
        }
        output {
          elasticsearch {
            hosts => [ "${QS_ES_HOSTS}" ]
            user => "${QS_ES_USER}"
            password => "${QS_ES_PASSWORD}"
            ssl_certificate_authorities => "${QS_ES_SSL_CERTIFICATE_AUTHORITY}"
          }
        }
```

Alternatively, you can provide the pipelines configuration through a Secret specified in the `spec.pipelinesRef` field. The Secret must have a `pipelines.yml` entry with your configuration:

```yaml
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: quickstart
spec:
  version: 8.16.1
  count: 1
  elasticsearchRefs:
    - clusterName: qs
      name: quickstart
  pipelinesRef:
    secretName: quickstart-pipeline
---
apiVersion: v1
kind: Secret
metadata:
  name: quickstart-pipeline
stringData:
  pipelines.yml: |-
    - pipeline.id: main
      config.string: |
        input {
          beats {
            port => 5044
          }
        }
        output {
          elasticsearch {
            hosts => [ "${QS_ES_HOSTS}" ]
            user => "${QS_ES_USER}"
            password => "${QS_ES_PASSWORD}"
            ssl_certificate_authorities => "${QS_ES_SSL_CERTIFICATE_AUTHORITY}"
          }
        }
```

Logstash on ECK supports all options present in `pipelines.yml`, including settings to update the number of workers, and the size of the batch that the pipeline will process. This also includes using `path.config` to point to volumes mounted on the Logstash container:

```yaml
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: quickstart
spec:
  version: 8.16.1
  count: 1
  elasticsearchRefs:
    - clusterName: qs
      name: quickstart
  pipelines:
    - pipeline.id: main
      config.string: |
        input {
          beats {
            port => 5044
          }
        }
        output {
          elasticsearch {
            hosts => [ "${QS_ES_HOSTS}" ]
            user => "${QS_ES_USER}"
            password => "${QS_ES_PASSWORD}"
            ssl_certificate_authorities => "${QS_ES_SSL_CERTIFICATE_AUTHORITY}"
          }
        }
```

::::{note}
Logstash persistent queues (PQs) and dead letter queues (DLQs) are not currently managed by the Logstash operator, and using them will require you to create and manage your own Volumes and VolumeMounts
::::



## Defining data volumes for Logstash [k8s-logstash-volumes]

[2.9.0]

::::{warning}
Volume support for Logstash is a breaking change to earlier versions of ECK and requires you to recreate your Logstash resources.
::::



## Specifying the volume claim settings [k8s-volume-claim-settings]

A PersistentVolume called `logstash-data` is created by default. It maps to `/usr/share/logstash/data` for persistent storage, which is typically used for storage from plugins.

By default, the `logstash-data` volume claim is a `1.5Gi` volume, using the standard StorageClass of your Kubernetes cluster. You can override the default by adding a `spec.volumeClaimTemplate` section named `logstash-data`.

For production workloads, you should define your own volume claim template with the desired storage capacity and (optionally) the Kubernetes [storage class](https://kubernetes.io/docs/concepts/storage/storage-classes/) to associate with the persistent volume. To override this volume claim for `data` usages, the name of this volume claim must be `logstash-data`.

This example updates the default data template to increase the storage to `2Gi` for the {{ls}} data folder:

```yaml
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: logstash
spec:
  # some configuration attributes omitted for brevity here
  volumeClaimTemplates:
    - metadata:
        name: logstash-data # Do not change this name unless you set up a volume mount for the data path.
      spec:
        accessModes:
          - ReadWriteOnce
        resources:
          requests:
            storage: 2Gi
```

The default volume size will likely be insufficient for production workloads, especially when you are using:

* the persistent queue (PQ) feature
* dead letter queues (DLQ), or
* {{ls}} plugins that make heavy use of temporary storage.

Increase the storage capacity, or consider creating separate volumes for these use cases.

You can add separate storage by including an additional `spec.volumeClaimTemplate` along with a corresponding `spec.podTemplate.spec.containers.volumeMount` for each requested volume.

This example shows how to setup separate storage for a PQ:

```yaml
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: logstash
spec:
  # some configuration attributes omitted for brevity here
  volumeClaimTemplates:
    - metadata:
        name: pq <1>
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 10Gi
  podTemplate:
    spec:
      containers:
      - name: logstash
        volumeMounts:
        - mountPath: /usr/share/logstash/pq <2>
          name: pq  <1>
          readOnly: false
  config:
    log.level: info
    queue.type: persisted
    path.queue: /usr/share/logstash/pq <2>
```

1. The `name` values in the `volumeMount` for the container in the `podTemplate` section and the name of the `volumeClaimTemplate` must match.
2. Set the `path.queue` setting in the configuration to match the `mountPath` in the `volumeMount`.


This example shows how to configure {{ls}} with a Dead Letter Queue setup on the main pipeline, and a separate pipeline to read items from the DLQ.

```yaml
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: logstash
spec:
   # some configuration attributes omitted for brevity here
   podTemplate:
    spec:
      containers:
      - name: logstash
        volumeMounts:
        - mountPath: /usr/share/logstash/dlq <2>
          name: dlq  <1>
          readOnly: false
  volumeClaimTemplates:
    - metadata:
        name: dlq <1>
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 10Gi
  pipelines:
    - pipeline.id: beats
      dead_letter_queue.enable: true
      path.dead_letter_queue: /usr/share/logstash/dlq <2>
      config.string: |
        input {
          beats {
            port => 5044
          }
        }
        output {
          elasticsearch {
            hosts => [ "${ECK_ES_HOSTS}" ]
            user => "${ECK_ES_USER}"
            password => "${ECK_ES_PASSWORD}"
            ssl_certificate_authorities => "${ECK_ES_SSL_CERTIFICATE_AUTHORITY}"
          }
        }
    - pipeline.id: dlq_read
      dead_letter_queue.enable: false
      config.string: |
        input {
          dead_letter_queue {
            path => "/usr/share/logstash/dlq" <2>
            commit_offsets => true
            pipeline_id => "beats"
            clean_consumed => true
          }
        }
        filter {
          mutate {
            remove_field => "[geoip][location]"
          }
        }
        output {
          elasticsearch {
            hosts => [ "${ECK_ES_HOSTS}" ]
            user => "${ECK_ES_USER}"
            password => "${ECK_ES_PASSWORD}"
            ssl_certificate_authorities => "${ECK_ES_SSL_CERTIFICATE_AUTHORITY}"
          }
        }
```

1. The `name` values in the `volumeMount` for the container in the `podTemplate` section and the name of the `volumeClaimTemplate` must match.
2. Set the `path.dead_letter_queue` setting in the pipeline config to match the `mountPath` in the `volumeMount` for pipelines that are writing to the Dead Letter Queue, and set the `path` setting of the `dead_letter_queue` plugin for the pipeline that will read from the Dead Letter Queue.



## Updating the volume claim settings [k8s-volume-claim-settings-updates]

If the storage class allows [volume expansion](https://kubernetes.io/blog/2018/07/12/resizing-persistent-volumes-using-kubernetes/), you can increase the storage requests size in `spec.volumeClaimTemplates`. ECK updates the existing PersistentVolumeClaims accordingly, and recreates the StatefulSet automatically.

If the volume driver supports `ExpandInUsePersistentVolumes`, the filesystem is resized online. In this case, you do not need to restart the {{ls}} process or re-create the Pods.

If the volume driver does not support `ExpandInUsePersistentVolumes`, you must manually delete Pods after the resize so that they can be recreated automatically with the expanded filesystem.

Any other changes in the volumeClaimTemplates—​such as changing the storage class or decreasing the volume size—​are not allowed. To make changes such as these, you must fully delete the {{ls}} resource, delete and recreate or resize the volume, and create a new {{ls}} resource.

Before you delete a persistent queue (PQ) volume, ensure that the queue is empty. We recommend setting `queue.drain: true` on the {{ls}} Pods to ensure that the queue is drained when Pods are shutdown. Note that you should also increase the `terminationGracePeriodSeconds` to a large enough value to allow the queue to drain.

This example shows how to configure a {{ls}} resource to drain the queue and increase the termination grace period.

```yaml
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: logstash
spec:
  # some configuration attributes omitted for brevity here
  config:
    queue.drain: true
  podTemplate:
    spec:
      terminationGracePeriodSeconds: 604800
```

::::{note}
A [{{k8s}} known issue](https://github.com/kubernetes/kubernetes/issues/94435): {{k8s}} may not honor `terminationGracePeriodSeconds` settings greater than 600. A queue of a terminated Pod may not be fully drained, even when `queue.drain: true` is set and a high `terminationGracePeriodSeconds` is configured.
::::


::::{note}
In this technical preview, there is currently no way to drain a dead letter queue (DLQ) automatically before {{ls}} shuts down. To manually drain the queue, first stop sending data to it, by either disabling the DLQ feature, or disabling any pipelines that send to a DLQ. Then wait for events to stop flowing through any pipelines reading from the input.
::::



## EmptyDir [k8s-emptydir]

If you are not concerned about data loss, you can use an `emptyDir` volume for Logstash data.

::::{warning}
The use of `emptyDir` in a production environment may cause permanent data loss. Do not use with persistent queues (PQs), dead letter queues (DLQs), or with any plugin that requires persistent storage to keep track of state between restarts of {{ls}}.

Plugins that require persistent storage include any plugin that stores state locally. These plugins typically have a configuration parameter that includes the name `path` or `directory`, not including paths to static content, such as certificates or keystores. Examples include the `sincedb_path` setting for the `file`, `dead_letter_queue` and `s3` inputs, the `last_run_metadata_path` for the `JDBC` input, `aggregate_maps_path` for the `aggregate` filter, and `temporary_directory` for the `s3` output, used to aggregate content before uploading to s3.

::::


```yaml
spec:
  count: 5
  podTemplate:
    spec:
      volumes:
      - name: logstash-data
        emptyDir: {}
```


## Using Elasticsearch in Logstash pipelines [k8s-logstash-pipelines-es]

### `elasticsearchRefs` for establishing a secured connection [k8s-logstash-esref]

The `spec.elasticsearchRefs` section provides a mechanism to help configure Logstash to establish a secured connection to one or more ECK managed Elasticsearch clusters. By default, each `elasticsearchRef` will target all nodes in its referenced Elasticsearch cluster. If you want to direct traffic to specific nodes of your Elasticsearch cluster, refer to [*Traffic Splitting*](requests-routing-to-elasticsearch-nodes.md) for more information and examples.

When you use `elasticsearchRefs` in a Logstash pipeline, the Logstash operator creates the necessary resources from the associated Elasticsearch cluster, and provides environment variables to allow these resources to be accessed from the pipeline configuration. Environment variables are replaced at runtime with the appropriate values. The environment variables have a fixed naming convention:

* `NORMALIZED_CLUSTERNAME_ES_HOSTS`
* `NORMALIZED_CLUSTERNAME_ES_USER`
* `NORMALIZED_CLUSTERNAME_ES_PASSWORD`
* `NORMALIZED_CLUSTERNAME_ES_SSL_CERTIFICATE_AUTHORITY`

where NORMALIZED_CLUSTERNAME is the value taken from the `clusterName` field of the `elasticsearchRef` property, capitalized, with `-` transformed to `_`. That is, `prod-es` would become `PROD_ES`.

::::{note}
* The `clusterName` value should be unique across all referenced {{es}} instances in the same {{ls}} spec.
* The {{ls}} ECK operator creates a user called `eck_logstash_user_role` when an `elasticsearchRef` is specified. This user has the following permissions:

    ```
      "cluster": ["monitor", "manage_ilm", "read_ilm", "manage_logstash_pipelines", "manage_index_templates", "cluster:admin/ingest/pipeline/get",]
      "indices": [
        {
          "names": [ "logstash", "logstash-*", "ecs-logstash", "ecs-logstash-*", "logs-*", "metrics-*", "synthetics-*", "traces-*" ],
          "privileges": ["manage", "write", "create_index", "read", "view_index_metadata"]
        }
    ]
    ```

    You can [update user permissions](../../users-roles/cluster-or-deployment-auth/native.md) to include more indices if the Elasticsearch plugin is expected to use indices other than the default. Check out [Logstash configuration with a custom index](configuration-examples-logstash.md#k8s-logstash-configuration-custom-index) sample configuration that creates a user that writes to a custom index.


::::


This example demonstrates how to create a Logstash deployment that connects to different Elasticsearch instances, one of which is in a separate namespace:

```yaml
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: quickstart
spec:
  version: 8.16.1
  count: 1
  elasticsearchRefs:        <1>
    - clusterName: prod-es  <2>
      name: prod
    - clusterName: qa-es    <3>
      name: qa
      namespace: qa
  pipelines:
    - pipeline.id: main
      config.string: |
        input {
          beats {
            port => 5044
          }
        }
        output {
          elasticsearch {   <4>
            hosts => [ "${PROD_ES_ES_HOSTS}" ]
            user => "${PROD_ES_ES_USER}"
            password => "${PROD_ES_ES_PASSWORD}"
            ssl_certificate_authorities => "${PROD_ES_ES_SSL_CERTIFICATE_AUTHORITY}"
          }
          elasticsearch {   <4>
            hosts => [ "${QA_ES_ES_HOSTS}" ]
            user => "${QA_ES_ES_USER}"
            password => "${QA_ES_ES_PASSWORD}"
            ssl_certificate_authorities => "${QA_ES_ES_SSL_CERTIFICATE_AUTHORITY}"
          }
        }
```

1. Define Elasticsearch references in the CRD. This will create the appropriate Secrets to store certificate details and the rest of the connection information, and create environment variables to allow them to be referred to in Logstash pipeline configurations.
2. This refers to an Elasticsearch cluster residing in the same namespace as the Logstash instances.
3. This refers to an Elasticsearch cluster residing in a different namespace to the Logstash instances.
4. Elasticsearch output definitions - use the environment variables created by the Logstash operator when specifying an `ElasticsearchRef`. Note the use of "normalized" versions of the `clusterName` in the environment variables used to populate the relevant fields.



### Connect to an external Elasticsearch cluster [k8s-logstash-external-es]

Logstash can connect to external Elasticsearch cluster that is not managed by ECK. You can reference a Secret instead of an Elasticsearch cluster in the `elasticsearchRefs` section through the `secretName` attribute:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: external-es-ref
stringData:
  url: https://abcd-42.xyz.elastic-cloud.com:443 <1>
  username: logstash_user <2>
  password: REDACTED <3>
  ca.crt: REDACTED <4>
---
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: quickstart
spec:
  version: 8.16.1
  count: 1
  elasticsearchRefs:
    - clusterName: prod-es
      secretName: external-es-ref <5>
  monitoring:
    metrics:
      elasticsearchRefs:
      - secretName: external-es-ref <5>
    logs:
      elasticsearchRefs:
      - secretName: external-es-ref <5>
```

1. The URL to reach the {{es}} cluster.
2. The username of the user to be authenticated to the {{es}} cluster.
3. The password of the user to be authenticated to the {{es}} cluster.
4. The CA certificate in PEM format to secure communication to the {{es}} cluster (optional).
5. The `secretName` and `name` attributes are mutually exclusive, you have to choose one or the other.


::::{tip}
Always specify the port in the URL when {{ls}} is connecting to an external {{es}} cluster.
::::




## Expose services [k8s-logstash-expose-services]

By default, the {{ls}} operator creates a headless Service for the metrics endpoint to enable metric collection by the Metricbeat sidecar for Stack Monitoring:

```sh
kubectl get service quickstart-ls-api
```

```sh
NAME                TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
quickstart-ls-api   ClusterIP   None         <none>        9600/TCP   48s
```

Additional services can be added in the `spec.services` section of the resource:

```yaml
services:
  - name: beats
    service:
      spec:
        ports:
        - port: 5044
          name: "winlogbeat"
          protocol: TCP
        - port: 5045
          name: "filebeat"
          protocol: TCP
```


## Pod configuration [k8s-logstash-pod-configuration]

You can [customize the {{ls}} Pod](customize-pods.md) using a Pod template, defined in the `spec.podTemplate` section of the configuration.

This example demonstrates how to create a {{ls}} deployment with increased heap size and resource limits.

```yaml
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: logstash-sample
spec:
  version: 8.16.1
  count: 1
  elasticsearchRefs:
    - name: "elasticsearch-sample"
      clusterName: "sample"
  podTemplate:
    spec:
      containers:
      - name: logtash
        env:
        - name: LS_JAVA_OPTS
          value: "-Xmx2g -Xms2g"
        resources:
          requests:
            memory: 1Gi
            cpu: 0.5
          limits:
            memory: 4Gi
            cpu: 2
```

The name of the container in the Pod template must be `logstash`.
