---
navigation_title: Advanced configuration
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-maps-advanced-configuration.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Advanced configuration for Elastic Maps Server on {{eck}} [k8s-maps-advanced-configuration]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


If you already looked at the [{{es}} on ECK](elasticsearch-configuration.md) documentation, some of these concepts might sound familiar to you. The resource definitions in ECK share the same philosophy when you want to:

* Customize the Pod configuration
* Customize the product configuration
* Manage HTTP settings

## Elastic Maps Server configuration [k8s-maps-configuration]

You can add any valid Elastic Maps Server setting as documented on the [product](/explore-analyze/visualize/maps/maps-connect-to-ems.md#elastic-maps-server-configuration) page to the `spec.config` section.

The following example demonstrates how to set the log level to `debug`:

```yaml subs=true
apiVersion: maps.k8s.elastic.co/v1alpha1
kind: ElasticMapsServer
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  count: 1
  config:
     logging.level: debug
```

Alternatively, settings can be provided through a Secret specified in the `configRef` element:

```yaml subs=true
apiVersion: maps.k8s.elastic.co/v1alpha1
kind: ElasticMapsServer
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  configRef:
    secretName: maps-config
---
apiVersion: v1
kind: Secret
metadata:
  name: maps-config
stringData:
  elastic-maps-server.yml: |-
    logging.level: debug
```

Refer to [Set compute resources for {{kib}}, Elastic Maps Server, APM Server and Logstash](manage-compute-resources.md#k8s-compute-resources-kibana-and-apm) for adjusting compute resources for Elastic Maps Server.


## Scale out an Elastic Maps Server deployment [k8s-maps-scaling]

To deploy more than one instance of maps, all the instances must mount the data volume containing the basemap read only. When this is the case, scaling out is just a matter of increasing the `count` attribute.


