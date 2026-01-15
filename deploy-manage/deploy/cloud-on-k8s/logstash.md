---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-logstash.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Logstash [k8s-logstash]

This section describes how to configure and deploy {{ls}} with ECK.

* [Quickstart](quickstart-logstash.md)
* [Configuration](configuration-logstash.md)

    * [Logstash configuration](configuration-logstash.md#k8s-logstash-configuring-logstash)
    * [Configuring Logstash pipelines](configuration-logstash.md#k8s-logstash-pipelines)
    * [Defining data volumes for Logstash](configuration-logstash.md#k8s-logstash-volumes)
    * [Using {{es}} in Logstash pipelines](configuration-logstash.md#k8s-logstash-pipelines-es)
    * [Expose services](configuration-logstash.md#k8s-logstash-expose-services)

* [Securing Logstash API](securing-logstash-api.md)
* [{{ls}} plugins](logstash-plugins.md)

    * [Providing additional resources for plugins](logstash-plugins.md#k8s-plugin-resources)
    * [Scaling {{ls}} on ECK](logstash-plugins.md#k8s-logstash-working-with-plugins-scaling)
    * [Plugin-specific considerations](logstash-plugins.md#k8s-logstash-working-with-plugin-considerations)
    * [Adding custom plugins](logstash-plugins.md#k8s-logstash-working-with-custom-plugins)

* [Configuration examples](configuration-examples-logstash.md)
* [Update Strategy](update-strategy-logstash.md)
* [Advanced configuration](advanced-configuration-logstash.md)

    * [Setting JVM options](advanced-configuration-logstash.md#k8s-logstash-jvm-options)
    * [Setting keystore](advanced-configuration-logstash.md#k8s-logstash-keystore)


::::{note}
Running {{ls}} on ECK is compatible only with {{ls}} 8.7+.
::::
