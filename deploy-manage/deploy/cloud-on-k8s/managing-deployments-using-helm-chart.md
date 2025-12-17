---
navigation_title: Elastic Stack Helm chart
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-stack-helm-chart.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# {{stack}} Helm chart [k8s-stack-helm-chart]

Starting from ECK 2.4.0, a Helm chart is available for managing {{stack}} resources using the ECK Operator. It is available from the Elastic Helm repository and can be added to your Helm repository list by running the following command:

```sh
helm repo add elastic https://helm.elastic.co
helm repo update
```

::::{note}
The minimum supported version of Helm is {{eck_helm_minimum_version}}.
::::

The {{stack}} (`eck-stack`) Helm chart is built on top of individual charts such as `eck-elasticsearch` and `eck-kibana`. For more details on its structure and dependencies, refer to the [chart repository](https://github.com/elastic/cloud-on-k8s/tree/main/deploy/eck-stack/).

The chart enables you to deploy the core components ({{es}} and {{kib}}) together, along with other {{stack}} applications if needed, under the same chart release. The following sections guide you through the installation process for multiple use cases. Choose the command that best fits your setup.

::::{tip}
All the provided examples deploy the applications in a namespace named `elastic-stack`. Consider adapting the commands to your use case.
::::

## {{es}} and {{kib}} [k8s-install-elasticsearch-kibana-helm]

Similar to the quickstart examples for {{es}} and {{kib}}, this section describes how to setup an {{es}} cluster with a simple {{kib}} instance managed by ECK, and how to customize a deployment using the eck-stack Helm chart’s values.

```sh
# Install an eck-managed Elasticsearch and Kibana using the default values, which deploys the quickstart examples.
helm install es-kb-quickstart elastic/eck-stack -n elastic-stack --create-namespace
```

### Customize {{es}} and {{kib}} installation with example values [k8s-eck-stack-helm-customize]

You can find example Helm values files for deploying and managing more advanced {{es}} and {{kib}} setups [in the project repository](https://github.com/elastic/cloud-on-k8s/tree/{{version.eck | M.M}}/deploy/eck-stack/examples).

To use one or more of these example configurations, use the `--values` Helm option, as seen in the following section.

```sh subs=true
# Install an eck-managed Elasticsearch and Kibana using the Elasticsearch node roles example with hot, warm, and cold data tiers, and the Kibana example customizing the http service.
helm install es-quickstart elastic/eck-stack -n elastic-stack --create-namespace \
    --values https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/deploy/eck-stack/examples/elasticsearch/hot-warm-cold.yaml \
    --values https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/deploy/eck-stack/examples/kibana/http-configuration.yaml
```

## Fleet Server with Elastic Agents along with {{es}} and {{kib}} [k8s-install-fleet-agent-elasticsearch-kibana-helm]

The following section builds upon the previous section, and allows installing Fleet Server, and Fleet-managed Elastic Agents along with {{es}} and {{kib}}.

```sh subs=true
# Install an eck-managed Elasticsearch, Kibana, Fleet Server, and managed Elastic Agents using custom values.
helm install eck-stack-with-fleet elastic/eck-stack \
    --values https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/deploy/eck-stack/examples/agent/fleet-agents.yaml -n elastic-stack
```

## Logstash along with {{es}}, {{kib}} and Beats [k8s-install-logstash-elasticsearch-kibana-helm]

The following section builds upon the previous sections, and allows installing Logstash along with {{es}}, {{kib}} and Beats.

```sh subs=true
# Install an eck-managed Elasticsearch, Kibana, Beats and Logstash using custom values.
helm install eck-stack-with-logstash elastic/eck-stack \
    --values https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/deploy/eck-stack/examples/logstash/basic-eck.yaml -n elastic-stack
```

## Standalone Elastic APM Server along with {{es}} and {{kib}} [k8s-install-apm-server-elasticsearch-kibana-helm]

The following section builds upon the previous sections, and allows installing a standalone Elastic APM Server along with {{es}} and {{kib}}.

```sh subs=true
# Install an eck-managed Elasticsearch, Kibana, and standalone APM Server using custom values.
helm install eck-stack-with-apm-server elastic/eck-stack \
    --values https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/deploy/eck-stack/examples/apm-server/basic.yaml -n elastic-stack
```

## Enterprise Search server along with {{es}} and {{kib}} [k8s-install-enterprise-search-elasticsearch-kibana-helm]

Enterprise Search is not available in {{stack}} versions 9.0 and later. For an example deployment of {{es}} version 8.x, {{kib}} 8.x, and an 8.x Enterprise Search server using the Helm chart, refer to the [previous ECK documentation](https://www.elastic.co/guide/en/cloud-on-k8s/2.16/k8s-stack-helm-chart.html).

## Install individual components of the {{stack}} [k8s-eck-stack-individual-components]

You can install individual components in one of two ways using the provided Helm charts:

* Using Helm values with the `eck-stack` chart to include only the components you need
* Using the individual Helm charts directly, without using the `eck-stack` chart

The following examples show how to install only {{es}} using each approach.

### Using Helm values to install only {{es}}

This example installs only {{es}} by deploying the `eck-stack` chart and excluding {{kib}}. By default, the chart deploys both {{es}} and {{kib}}.

```sh
helm install es-quickstart elastic/eck-stack -n elastic-stack --create-namespace --set=eck-kibana.enabled=false
```

### Using the eck-elasticsearch Helm chart directly to install only {{es}} [individual-chart]

This example installs {{es}} by deploying the `eck-elasticsearch` chart on its own.

```sh
helm install es-quickstart elastic/eck-elasticsearch -n elastic-stack --create-namespace
```

## Upgrade or change {{stack}} configuration with Helm [k8s-upgrade-modify-helm]

Whether you want to upgrade your {{stack}} components to a new version or modify the configuration of your existing installation (known as a `release`), you use the [`helm upgrade`](https://helm.sh/docs/helm/helm_upgrade/) command. The key principle is to use the same options and values you used during installation, along with any changes you want to apply.

The `helm upgrade` command requires the following arguments:
- The name of the release to update, which must match the name used with `helm install`.
- The chart name, which must be the same chart used during installation.

::::{important}
When using `helm upgrade`, you must include all the options and values from your original installation command (for example, custom values files and `--set` options). Helm does not retain your previous configuration, so omitting them causes values to revert to their default settings.
::::

By default, `helm upgrade` uses the latest available version of the chart unless the `--version` option is specified. Refer to [View chart versions](#show-versions) to list the available chart versions or the version associated with an installed release.

::::{admonition} Chart version vs {{stack}} component version
There is an important distinction between the Helm chart version and the {{stack}} component version:

- **Chart version**: The version of the Helm chart itself (for example, `eck-stack` version 0.17.0). You can specify this using the `--version` flag in your Helm `install` or `upgrade` commands.
- **Component version**: The version of a {{stack}} component (for example, {{es}} 8.15.0 or {{kib}} 8.15.0). You can specify this in your values file or by using `--set` parameters.

Each chart version defines default {{stack}} component versions. Unless explicitly overridden, installing or upgrading the chart deploys those default versions.

% When available we can tell users how to check the default {{stack}} version associated with each chart release. That's not feasible today and users are a bit blind on this regard.
::::

All examples in this section assume that your release was installed using the `eck-stack` Helm chart. Adapt the examples if you deployed the [individual charts](#individual-chart) directly.

### Upgrade to the latest version of the chart

To upgrade an installed release named `es-kb-quickstart` to the latest version of the Helm chart, do the following:

```sh
helm repo update <1>
helm upgrade es-kb-quickstart elastic/eck-stack -n elastic-stack
```
1. Refresh the local chart cache.

By default, upgrading the Helm chart also upgrades the {{stack}} components to the versions associated with that chart version. To override this behavior, you can explicitly set the {{stack}} component versions to use, as shown in the following section.

### Upgrade to specific {{stack}} version

If for example you want to upgrade the {{stack}} components to a newer version that is not the default for the Helm chart, you can explicitly set the component versions using Helm values or `--set` options.

The following examples show both ways to upgrade the release to the latest available version of the Helm chart and all {{stack}} components to version {{version.stack}}.

::::{note}
To avoid the Helm chart to be upgraded to the latest release you can use `--version` option on the Helm upgrade command. To know the chart version associated with your installed release, refer to [check chart versions](#show-versions).
::::

#### Using the `--set` option

Use `--set` options to override the component versions directly from the command line:

```sh
helm repo update <1>
helm upgrade es-kb-quickstart elastic/eck-stack -n elastic-stack \
  --set eck-elasticsearch.version={{version.stack}} \ <2>
  --set eck-kibana.version={{version.stack}}
```
1. Refresh the local chart cache.
2. Specify versions for all the components you deploy. Components without an explicitly defined version continue to use the default versions provided by the chart.

#### Using a values file

If you already use a values file for this release, update it to include the following settings. Otherwise, create a new values file (for example, `custom-values.yaml`) with the following content:

```yaml subs=true
eck-elasticsearch: <1>
  version: {{version.stack}}
eck-kibana:
  version: {{version.stack}}
```
1. Specify versions for all the components you deploy. Components without an explicitly defined version continue to use the default versions provided by the chart.

Then upgrade the release using the values file:

```sh
helm repo update <1>
helm upgrade es-kb-quickstart elastic/eck-stack -n elastic-stack -f custom-values.yaml
```
1. Refresh the local chart cache.

### Apply configuration changes

To apply configuration changes to an existing release, run `helm upgrade` with the complete configuration you want the release to use. This includes both the current configuration and any new changes.

For example, if you installed the [quickstart release](#k8s-install-elasticsearch-kibana-helm) and want to scale the {{es}} cluster to three nodes and expose the {{kib}} service using a LoadBalancer, do the following:

1. Create a values file with the desired configuration, and save it as `custom-values.yaml`:

```yaml
eck-elasticsearch:
  nodeSets:
  - name: default
    count: 3

eck-kibana:
  http:
    service:
      spec:
        # This deploys a load balancer in a cloud service provider, where supported.
        type: LoadBalancer
```

2. Apply the configuration using `helm upgrade`:

```sh
helm upgrade es-kb-quickstart elastic/eck-stack \
  -n elastic-stack \
  -f custom-values.yaml
```

::::{warning}
The previous example also upgrades the {{stack}} components if a newer Helm chart version is available. To avoid this, [identify the chart version](#show-versions) currently used by your release and include the `--version` option when running `helm upgrade`.
::::

## Adding Ingress to the {{stack}} [k8s-eck-stack-ingress]

:::{admonition} Support scope for Ingress Controllers
[Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) is a standard Kubernetes concept. While ECK-managed workloads can be publicly exposed using ingress resources, and we provide [example configurations](/deploy-manage/deploy/cloud-on-k8s/recipes.md), setting up an Ingress controller requires in-house Kubernetes expertise.

If ingress configuration is challenging or unsupported in your environment, consider using standard `LoadBalancer` services as a simpler alternative.
:::


Both {{es}} and {{kib}} support [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/), which can be enabled using the following options:

**If an individual chart is used (not eck-stack)**

The following command installs an {{es}} cluster using the `eck-elasticsearch` chart and configures an ingress resource:

```sh
helm install es-quickstart elastic/eck-elasticsearch -n elastic-stack --create-namespace \
  --set=ingress.enabled=true --set=ingress.hosts[0].host=elasticsearch.example.com --set=ingress.hosts[0].path="/"
```

**If eck-stack chart is used**

The following command deploys the basic {{es}} and {{kib}} example with ingress resources for both components:

```sh
helm install es-kb-quickstart elastic/eck-stack -n elastic-stack --create-namespace \
  --set=eck-elasticsearch.ingress.enabled=true --set=eck-elasticsearch.ingress.hosts[0].host=elasticsearch.example.com --set=eck-elasticsearch.ingress.hosts[0].path="/" \
  --set=eck-kibana.ingress.enabled=true --set=eck-kibana.ingress.hosts[0].host=kibana.example.com --set=eck-kibana.ingress.hosts[0].path="/"
```

For illustration purposes, the ingress objects created by the previous command look similar to the following:

```yaml
# Source: eck-stack/charts/eck-elasticsearch/templates/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: elasticsearch
  labels:
    ...
spec:
  rules:
  - host: "elasticsearch.example.com"
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: elasticsearch-es-http
            port:
              number: 9200
---
# Source: eck-stack/charts/eck-kibana/templates/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: es-kb-quickstart-eck-kibana
  labels:
    ...
spec:
  rules:
  - host: "kibana.example.com"
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: es-kb-quickstart-eck-kibana-kb-http
            port:
              number: 5601
```

## View available configuration options [k8s-install-helm-show-values-stack]

You can view all configurable values of the {{stack}} helm chart of the individual charts by running the following:

```sh
helm show values elastic/eck-stack
helm show values elastic/eck-elasticsearch
helm show values elastic/eck-kibana
helm show values elastic/eck-agent
helm show values elastic/eck-beats
helm show values elastic/eck-apm-server
helm show values elastic/eck-fleet-server
helm show values elastic/eck-logstash
```

## View available chart versions [show-versions]

To view the available versions of a Helm chart, update the local chart cache and use the `helm repo search` command with `--versions` option:

```sh
helm repo update
helm repo search elastic/eck-stack --versions <1>
```
1. Applicable to `eck-stack` or the [individual charts](#k8s-eck-stack-individual-components)

To view the version associated with an installed release, check the **CHART** column of the `helm list` command output. For example:

```sh
$ helm list -n elastic-stack
NAME            	NAMESPACE    	REVISION	UPDATED                             	STATUS  	CHART                   	APP VERSION
es-kb-quickstart	elastic-stack	2       	2025-12-17 11:24:06.156007 +0100 CET	deployed	eck-stack-0.17.0
```