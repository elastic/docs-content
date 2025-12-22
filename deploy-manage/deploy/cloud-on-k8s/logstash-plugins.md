---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-logstash-plugins.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Logstash plugins [k8s-logstash-plugins]

The power of {{ls}} is in the plugins--[inputs](logstash-docs-md://lsr/input-plugins.md), [outputs](logstash-docs-md://lsr/output-plugins.md), [filters](logstash-docs-md://lsr/filter-plugins.md), and [codecs](logstash-docs-md://lsr/codec-plugins.md).

In {{ls}} on ECK, you can use the same plugins that you use for other {{ls}} instances—including Elastic-supported, community-supported, and custom plugins. However, you may have other factors to consider, such as how you configure your {{k8s}} resources, how you specify additional resources, and how you scale your {{ls}} installation.

In this section, we’ll cover:

* [Providing additional resources for plugins (read-only and writable storage)](#k8s-plugin-resources)
* [Scaling {{ls}} on ECK](#k8s-logstash-working-with-plugins-scaling)
* [Plugin-specific considerations](#k8s-logstash-working-with-plugin-considerations)
* [Adding custom plugins](#k8s-logstash-working-with-custom-plugins)

## Providing additional resources for plugins [k8s-plugin-resources]

The plugins in your pipeline can impact how you can configure your {{k8s}} resources, including the need to specify additional resources in your manifest. The most common resources you need to allow for are:

* Read-only assets, such as private keys, translate dictionaries, or JDBC drivers
* [Writable storage](#k8s-logstash-working-with-plugins-writable) to save application state

### Read-only assets [k8s-logstash-working-with-plugins-ro]

Many plugins require or allow read-only assets in order to work correctly. These may be ConfigMaps or Secrets files that have a 1 MiB limit, or larger assets such as JDBC drivers, that need to be stored in a PersistentVolume.

#### ConfigMaps and Secrets (1 MiB max) [k8s-logstash-working-with-plugins-small-ro]

Each instance of a `ConfigMap` or `Secret` has a [maximum size](https://kubernetes.io/docs/concepts/configuration/configmap/#:~:text=The%20data%20stored%20in%20a,separate%20database%20or%20file%20service) of 1 MiB (mebibyte). For larger read-only assets, check out [Larger read-only assets (1 MiB+)](#k8s-logstash-working-with-plugins-large-ro).

In the plugin documentation, look for configurations that call for a `path` or an `array` of `paths`.

**Sensitive assets, such as private keys**

Some plugins need access to private keys or certificates in order to access an external resource. Make the keys or certificates available to the {{ls}} resource in your manifest.

::::{tip}
These settings are typically identified by an `ssl_` prefix, such as `ssl_key`, `ssl_keystore_path`, `ssl_certificate`, for example.
::::


To use these in your manifest, create a Secret representing the asset, a Volume in your `podTemplate.spec` containing that Secret, and then mount that Volume with a VolumeMount in the `podTemplateSpec.container` section of your {{ls}} resource.

First, create your secrets.

```bash
kubectl create secret generic logstash-crt --from-file=logstash.crt
kubectl create secret generic logstash-key --from-file=logstash.key
```

Then, create your Logstash resource.

```yaml
spec:
  podTemplate:
    spec:
      volumes:
        - name: logstash-ssl-crt
          secret:
            secretName: logstash-crt
        - name: logstash-ssl-key
          secret:
            secretName: logstash-key
      containers:
        - name: logstash
          volumeMounts:
            - name: logstash-ssl-key
              mountPath: "/usr/share/logstash/data/logstash.key"
              readOnly: true
            - name: logstash-ssl-crt
              mountPath: "/usr/share/logstash/data/logstash.crt"
              readOnly: true
  pipelines:
    - pipeline.id: main
      config.string: |
        input {
          http {
            port => 8443
            ssl_certificate => "/usr/share/logstash/data/logstash.crt"
            ssl_key => "/usr/share/logstash/data/logstash.key"
          }
        }
```

**Static read-only files**

Some plugins require or allow access to small static read-only files. You can use these for a variety of reasons. Examples include adding custom `grok` patterns for [`logstash-filter-grok`](logstash-docs-md://lsr/plugins-filters-grok.md) to use for lookup, source code for [`logstash-filter-ruby`], a dictionary for [`logstash-filter-translate`](logstash-docs-md://lsr/plugins-filters-translate.md) or the location of a SQL statement for [`logstash-input-jdbc`](logstash-docs-md://lsr/plugins-inputs-jdbc.md). Make these files available to the {{ls}} resource in your manifest.

::::{tip}
In the plugin documentation, these plugin settings are typically identified by `path` or an `array` of `paths`.
::::


To use these in your manifest, create a ConfigMap or Secret representing the asset, a Volume in your `podTemplate.spec` containing the ConfigMap or Secret, and mount that Volume with a VolumeMount in your `podTemplateSpec.container` section of your {{ls}} resource.

This example illustrates configuring a ConfigMap from a ruby source file, and including it in a [`logstash-filter-ruby`](logstash-docs-md://lsr/plugins-filters-ruby.md) plugin.

First, create the ConfigMap.

```bash
kubectl create configmap ruby --from-file=drop_some.rb
```

Then, create your Logstash resource.

```yaml
spec:
  podTemplate:
    spec:
      volumes:
        - name: ruby_drop
          configMap:
            name: ruby
      containers:
        - name: logstash
          volumeMounts:
            - name: ruby_drop
              mountPath: "/usr/share/logstash/data/drop_percentage.rb"
              readOnly: true
  pipelines:
    - pipeline.id: main
      config.string: |
        input {
          beats {
            port => 5044
          }
        }
        filter {
          ruby {
            path => "/usr/share/logstash/data/drop_percentage.rb"
            script_params => { "percentage" => 0.9 }
          }
        }
```



### Larger read-only assets (1 MiB+) [k8s-logstash-working-with-plugins-large-ro]

Some plugins require or allow access to static read-only files that exceed the 1 MiB (mebibyte) limit imposed by ConfigMap and Secret. For example, you may need JAR files to load drivers when using a JDBC or JMS plugin, or a large [`logstash-filter-translate`](logstash-docs-md://lsr/plugins-filters-translate.md) dictionary.

You can add files using:

* **[PersistentVolume populated by an initContainer](#k8s-logstash-ic).** Add a volumeClaimTemplate and a volumeMount to your {{ls}} resource and upload data to that volume, either using an `initContainer`, or direct upload if your Kubernetes provider supports it. You can use the default `logstash-data` volumeClaimTemplate , or a custom one depending on your storage needs.
* **[Custom Docker image](#k8s-logstash-custom-images).** Use a custom docker image that includes the static content that your Logstash pods will need.

Check out [Custom configuration files and plugins](custom-configuration-files-plugins.md) for more details on which option might be most suitable for you.

#### Add files using PersistentVolume populated by an initContainer [k8s-logstash-ic]

This example creates a volumeClaimTemplate called `workdir`, with volumeMounts referring to this mounted to the main container and an initContainer. The initContainer initiates a  download of a PostgreSQL JDBC driver JAR file, and stored it the volumeMount, which is then used in the JDBC input in the pipeline configuration.

```yaml
spec:
  podTemplate:
    spec:
      initContainers:
      - name: download-postgres
        command: ["/bin/sh"]
        args: ["-c", "curl -o /data/postgresql.jar -L https://jdbc.postgresql.org/download/postgresql-42.6.0.jar"]
        volumeMounts:
          - name: workdir
            mountPath: /data
      containers:
        - name: logstash
          volumeMounts:
            - name: workdir
              mountPath: /usr/share/logstash/jars <1>
  volumeClaimTemplates:
    - metadata:
        name: workdir
      spec:
        accessModes:
          - ReadWriteOnce
        resources:
          requests:
            storage: 50Mi
  pipelines:
    - pipeline.id: main
      config.string: |
        input {
          jdbc {
             jdbc_driver_library => "/usr/share/logstash/jars/postgresql.jar"
             jdbc_driver_class => "org.postgresql.Driver"
             <2>
          }
        }
```

1. Should match the `mountPath` of the `container`
2. Remainder of plugin configuration goes here



#### Add files using a custom Docker image [k8s-logstash-custom-images]

This example downloads the same `postgres` JDBC driver, and adds it to the {{ls}} classpath in the Docker image.

First, create a Dockerfile based on the {{ls}} Docker image. Download the JDBC driver, and save it alongside the other JAR files in the {{ls}} classpath:

```shell subs=true
FROM docker.elastic.co/logstash/logstash:{{version.stack}}
RUN curl -o /usr/share/logstash/logstash-core/lib/jars/postgresql.jar -L https://jdbc.postgresql.org/download/postgresql-42.6.0.jar <1>
```

1. Placing the JAR file in the `/usr/share/logstash/logstash-core/lib/jars` folder adds it to the {{ls}} classpath.


After you build and deploy the custom image, include it in the {{ls}} manifest. Check out [*Create custom images*](create-custom-images.md) for more details.

```yaml
  count: 1
  version: {version} <1>
  image: <CUSTOM_IMAGE>
  pipelines:
    - pipeline.id: main
      config.string: |
        input {
          jdbc {
              <2>
             jdbc_driver_class => "org.postgresql.Driver"
              <3>
          }
        }
```

1. The correct version is required as ECK reasons about available APIs and capabilities based on the version field.
2. Note that when you place the JAR file on the {{ls}} classpath, you do not need to specify the `jdbc_driver_library` location in the plugin configuration.
3. Remainder of plugin configuration goes here




### Writable storage [k8s-logstash-working-with-plugins-writable]

Some {{ls}} plugins need access to writable storage. This could be for checkpointing to keep track of events already processed, a place to temporarily write events before sending a batch of events, or just to actually write events to disk in the case of [`logstash-output-file`](logstash-docs-md://lsr/plugins-outputs-file.md).

{{ls}} on ECK by default supplies a small 1.5 GiB (gibibyte) default persistent volume to each pod. This volume is called `logstash-data` and is located at `/usr/logstash/data`, and is typically the default location for most plugin use cases. This volume is stable across restarts of {{ls}} pods and is suitable for many use cases.

::::{note}
When plugins use writable storage, each plugin must store its data a dedicated folder or file to avoid overwriting data.
::::


#### Checkpointing [k8s-logstash-working-with-plugins-writable-checkpointing]

Some {{ls}} plugins need to write "checkpoints" to local storage in order to keep track of events that have already been processed. Plugins that retrieve data from external sources need to do this if the external source does not provide any mechanism to track state internally.

Not all external data sources have mechanisms to track state internally, and {{ls}} checkpoints can help persist data.

In the plugin documentation, look for configurations that call for a `path` with a settings like `sincedb`, `sincedb_path`, `sequence_path`, or `last_run_metadata_path`. Check out specific plugin documentation in the [Logstash Reference](logstash://reference/index.md) for details.

```yaml
spec:
  pipelines:
    - pipeline.id: main
      config.string: |
        input {
          jdbc {
             jdbc_driver_library => "/usr/share/logstash/jars/postgresql.jar"
             jdbc_driver_class => "org.postgresql.Driver"
             last_metadata_path => "/usr/share/logstash/data/main/logstash_jdbc_last_run <1>
          }
        }
```

1. If you are using more than one plugin of the same type, specify a unique location for each plugin to use.


If the default `logstash-data` volume is insufficient for your needs, see the volume section for details on how to add additional volumes.


#### Writable staging or temporary data [k8s-logstash-working-with-plugins-writable-temp]

Some {{ls}} plugins write data to a staging directory or file before processing for input, or outputting to their final destination. Often these staging folders can be persisted across restarts to avoid duplicating processing of data.

In the plugin documentation, look for  names such as `tmp_directory`, `temporary_directory`, `staging_directory`.

To persist data across pod restarts, set this value to point to the default `logstash-data` volume or your own PersistentVolumeClaim.

```yaml
spec:
  pipelines:
    - pipeline.id: main
      config.string: |
        output {
          s3 {
             id => "main_s3_output"
             temporary_directory => "/usr/share/logstash/data/main/main_s3_output<1>
          }
        }
```

1. If you are using more than one plugin of the same type, specify a unique location for each plugin to use.





## Scaling {{ls}} on ECK [k8s-logstash-working-with-plugins-scaling]

::::{important}
The use of autoscalers, such as the HorizontalPodAutoscaler or the VerticalPodAutoscaler, with {{ls}} on ECK is not yet supported.
::::


{{ls}} scalability is highly dependent on the plugins in your pipelines. Some plugins can restrict how you can scale out your Logstash deployment, based on the way that the plugins gather or enrich data.

Plugin categories that require special considerations are:

* [Filter plugins: aggregating filters](#k8s-logstash-agg-filters)
* [Input plugins: events pushed to {{ls}}](#k8s-logstash-inputs-data-pushed)
* [Input plugins: {{ls}} maintains state](#k8s-logstash-inputs-local-checkpoints)
* [Input plugins: external source stores state](#k8s-logstash-inputs-external-state)

If the pipeline *does not* contain any plugins from these categories, you can increase the number of {{ls}} instances by setting the `count` property in the {{ls}} resource:

```yaml subs=true
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  count: 3
```

::::{admonition} Horizontal scaling for {{ls}} plugins
* Not all {{ls}} deployments can be scaled horizontally by increasing the number of {{ls}} Pods defined in the {{ls}} resource. Depending on the types of plugins in a {{ls}} installation, increasing the number of pods may cause data duplication, data loss, incorrect data, or may waste resources with pods unable to be utilized correctly.
* The ability of a {{ls}} installation to scale horizontally is bound by its most restrictive plugin(s). Even if all pipelines are using [`logstash-input-elastic_agent`](logstash-docs-md://lsr/plugins-inputs-elastic_agent.md) or [`logstash-input-beats`](logstash-docs-md://lsr/plugins-inputs-beats.md) which should enable full horizontal scaling, introducing a more restrictive input or filter plugin forces the restrictions for pod scaling associated with that plugin.

::::


### Filter plugins: aggregating filters [k8s-logstash-agg-filters]

{{ls}} installations that use aggregating filters should be treated with particular care:

* They **must** specify `pipeline.workers=1` for any pipelines that use them.
* The number of pods cannot be scaled above 1.

Examples of aggregating filters include [`logstash-filter-aggregate`](logstash-docs-md://lsr/plugins-filters-aggregate.md), [`logstash-filter-csv`](logstash-docs-md://lsr/plugins-filters-csv.md) when `autodetect_column_names` set to `true`, and any [`logstash-filter-ruby`](logstash-docs-md://lsr/plugins-filters-ruby.md) implementations that perform aggregations.


### Input plugins: events pushed to {{ls}} [k8s-logstash-inputs-data-pushed]

{{ls}} installations with inputs that enable {{ls}} to receive data should be able to scale freely and have load spread across them horizontally. These plugins include [`logstash-input-beats`](logstash-docs-md://lsr/plugins-inputs-beats.md), [`logstash-input-elastic_agent`](logstash-docs-md://lsr/plugins-inputs-elastic_agent.md),  [`logstash-input-tcp`](logstash-docs-md://lsr/plugins-inputs-tcp.md), and [`logstash-input-http`](logstash-docs-md://lsr/plugins-inputs-http.md).


### Input plugins: {{ls}} maintains state [k8s-logstash-inputs-local-checkpoints]

{{ls}} installations that use input plugins that retrieve data from an external source, and **maintain local checkpoint state**, or would require some level of co-ordination between nodes to split up work can specify `pipeline.workers` freely, but should keep the pod count at 1 for each {{ls}} installation.

Note that plugins that retrieve data from external sources, and require some level of coordination between nodes to split up work, are not good candidates for scaling horizontally, and would likely produce some data duplication.

Input plugins that include configuration settings such as  `sincedb`, `checkpoint` or `sql_last_run_metadata` may fall into this category.

Examples of these plugins include [`logstash-input-jdbc`](logstash-docs-md://lsr/plugins-inputs-jdbc.md) (which has no automatic way to split queries across {{ls}} instances), [`logstash-input-s3`](logstash-docs-md://lsr/plugins-inputs-s3.md) (which has no way to split which buckets to read across {{ls}} instances), or [`logstash-input-file`](logstash-docs-md://lsr/plugins-inputs-file.md).


### Input plugins: external source stores state [k8s-logstash-inputs-external-state]

{{ls}} installations that use input plugins that retrieve data from an external source, and **rely on the external source to store state** can scale based on the parameters of the external source.

For example, a {{ls}} installation that uses a [`logstash-input-kafka`](logstash-docs-md://lsr/plugins-inputs-kafka.md) plugin to retrieve data can scale the number of pods up to the number of partitions used, as a partition can have at most one consumer belonging to the same consumer group. Any pods created beyond that threshold cannot be scheduled to receive data.

Examples of these plugins include [`logstash-input-kafka`](logstash-docs-md://lsr/plugins-inputs-kafka.md), [`logstash-input-azure_event_hubs`](logstash-docs-md://lsr/plugins-inputs-azure_event_hubs.md), and [`logstash-input-kinesis`](logstash-docs-md://lsr/plugins-inputs-kinesis.md).



## Plugin-specific considerations [k8s-logstash-working-with-plugin-considerations]

Some plugins have additional requirements and guidelines for optimal performance in a {{ls}} ECK environment.

* [{{ls}} integration plugin](#k8s-logstash-plugin-considerations-ls-integration)
* [{{es}} output plugin](#k8s-logstash-plugin-considerations-es-output)
* [Elastic_integration filter plugin](#k8s-logstash-plugin-considerations-integration-filter)
* [Elastic Agent input and Beats input plugins](#k8s-logstash-plugin-considerations-agent-beats)

::::{tip}
Use these guidelines *in addition* to the general guidelines provided in [Scaling {{ls}} on ECK](#k8s-logstash-working-with-plugins-scaling).
::::


### {{ls}} integration plugin [k8s-logstash-plugin-considerations-ls-integration]

When your pipeline uses the [`Logstash integration`](logstash-docs-md://lsr/plugins-integrations-logstash.md) plugin, add `keepalive=>false` to the [logstash-output](logstash-docs-md://lsr/plugins-outputs-logstash.md) definition to ensure that load balancing works correctly rather than keeping affinity to the same pod.


### {{es}} output plugin [k8s-logstash-plugin-considerations-es-output]

The [`elasticsearch output`](logstash-docs-md://lsr/plugins-outputs-elasticsearch.md) plugin requires certain roles to be configured in order to enable {{ls}} to communicate with {{es}}.

You can customize roles in {{es}}. Check out [creating custom roles](../../users-roles/cluster-or-deployment-auth/native.md)

```yaml
kind: Secret
apiVersion: v1
metadata:
  name: my-roles-secret
stringData:
  roles.yml: |-
    eck_logstash_user_role:
      "cluster": ["monitor", "manage_ilm", "read_ilm", "manage_logstash_pipelines", "manage_index_templates", "cluster:admin/ingest/pipeline/get"],
      "indices": [
        {
          "names": [ "logstash", "logstash-*", "ecs-logstash", "ecs-logstash-*", "logs-*", "metrics-*", "synthetics-*", "traces-*" ],
          "privileges": ["manage", "write", "create_index", "read", "view_index_metadata"]
        }
      ]
```


### Elastic_integration filter plugin [k8s-logstash-plugin-considerations-integration-filter]

The [`elastic_integration filter`](logstash-docs-md://lsr/plugins-filters-elastic_integration.md) plugin allows the use of [`ElasticsearchRef`](configuration-logstash.md#k8s-logstash-esref) and environment variables.

```json
  elastic_integration {
            pipeline_name => "logstash-pipeline"
            hosts => [ "${ECK_ES_HOSTS}" ]
            username => "${ECK_ES_USER}"
            password => "${ECK_ES_PASSWORD}"
            ssl_certificate_authorities => "${ECK_ES_SSL_CERTIFICATE_AUTHORITY}"
          }
```

The Elastic_integration filter requires certain roles to be configured on the {{es}} cluster to enable {{ls}} to read ingest pipelines.

```yaml
# Sample role definition
kind: Secret
apiVersion: v1
metadata:
  name: my-roles-secret
stringData:
  roles.yml: |-
    eck_logstash_user_role:
      cluster: [ "monitor", "manage_index_templates", "read_pipeline"]
```


### Elastic Agent input and Beats input plugins [k8s-logstash-plugin-considerations-agent-beats]

When you use the [Elastic Agent input](logstash-docs-md://lsr/plugins-inputs-elastic_agent.md) or the [Beats input](logstash-docs-md://lsr/plugins-inputs-beats.md), set the [`ttl`](beats://reference/filebeat/logstash-output.md#_ttl) value on the Agent or Beat to ensure that load is distributed appropriately.



## Adding custom plugins [k8s-logstash-working-with-custom-plugins]

If you need plugins in addition to those included in the standard {{ls}} distribution, you can add them. Create a custom Docker image that includes the installed plugins, using the `bin/logstash-plugin install` utility to add more plugins to the image so that they can be used by {{ls}} pods.

This sample Dockerfile installs the [`logstash-filter-tld`](logstash-docs-md://lsr/plugins-filters-tld.md) plugin to the official {{ls}} Docker image:

```shell subs=true
FROM docker.elastic.co/logstash/logstash:{{version.stack}}
RUN bin/logstash-plugin install logstash-filter-tld
```

Then after building and deploying the custom image (refer to [*Create custom images*](create-custom-images.md) for more details), include it in the {{ls}} manifest:

```shell subs=true
spec:
  count: 1
  version: {{version.stack}} <1>
  image: <CUSTOM_IMAGE>
```

1. The correct version is required as ECK reasons about available APIs and capabilities based on the version field.
