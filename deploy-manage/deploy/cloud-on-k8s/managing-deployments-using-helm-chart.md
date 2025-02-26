---
navigation_title: Elastic Stack Helm chart
applies_to:
  deployment:
    eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-stack-helm-chart.html
---

# Elastic Stack Helm chart [k8s-stack-helm-chart]

Starting from ECK 2.4.0, a Helm chart is available for managing Elastic Stack resources using the ECK Operator. It is available from the Elastic Helm repository and can be added to your Helm repository list by running the following command:

```sh
helm repo add elastic https://helm.elastic.co
helm repo update
```

::::{note} 
The minimum supported version of Helm is 3.2.0.
::::

The Elastic Stack (`eck-stack`) Helm chart is built on top of individual charts such as `eck-elasticsearch` and `eck-kibana`. For more details on its structure and dependencies, refer to the [chart repository](https://github.com/elastic/cloud-on-k8s/tree/main/deploy/eck-stack/).

The chart enables you to deploy the core components ({{es}} and {{kib}}) together, along with other {{stack}} applications if needed, under the same chart release. The following sections guide you through the installation process for multiple use cases. Choose the command that best fits your setup.

::::{tip}
All the provided examples deploy the applications in a namespace named `elastic-stack`. Consider adapting the commands to your use case.
::::

## Elasticsearch and Kibana [k8s-install-elasticsearch-kibana-helm] 

Similar to the quickstart examples for {{es}} and {{kib}}, this section describes how to setup an {{es}} cluster with a simple {{kib}} instance managed by ECK, and how to customize a deployment using the eck-stack Helm chart’s values.

```sh
# Install an eck-managed Elasticsearch and Kibana using the default values, which deploys the quickstart examples.
helm install es-kb-quickstart elastic/eck-stack -n elastic-stack --create-namespace
```

### Customize Elasticsearch and Kibana installation with example values [k8s-eck-stack-helm-customize] 

You can find example Helm values files for deploying and managing more advanced Elasticsearch and Kibana setups [in the project repository](https://github.com/elastic/cloud-on-k8s/tree/2.16/deploy/eck-stack/examples).

To use one or more of these example configurations, use the `--values` Helm option, as seen in the following section.

```sh
# Install an eck-managed Elasticsearch and Kibana using the Elasticsearch node roles example with hot, warm, and cold data tiers, and the Kibana example customizing the http service.
helm install es-quickstart elastic/eck-stack -n elastic-stack --create-namespace \
    --values https://raw.githubusercontent.com/elastic/cloud-on-k8s/2.16/deploy/eck-stack/examples/elasticsearch/hot-warm-cold.yaml \
    --values https://raw.githubusercontent.com/elastic/cloud-on-k8s/2.16/deploy/eck-stack/examples/kibana/http-configuration.yaml
```

## Fleet Server with Elastic Agents along with Elasticsearch and Kibana [k8s-install-fleet-agent-elasticsearch-kibana-helm] 

The following section builds upon the previous section, and allows installing Fleet Server, and Fleet-managed Elastic Agents along with Elasticsearch and Kibana.

```sh
# Install an eck-managed Elasticsearch, Kibana, Fleet Server, and managed Elastic Agents using custom values.
helm install eck-stack-with-fleet elastic/eck-stack \
    --values https://raw.githubusercontent.com/elastic/cloud-on-k8s/2.16/deploy/eck-stack/examples/agent/fleet-agents.yaml -n elastic-stack
```

## Logstash along with Elasticsearch, Kibana and Beats [k8s-install-logstash-elasticsearch-kibana-helm] 

The following section builds upon the previous sections, and allows installing Logstash along with Elasticsearch, Kibana and Beats.

```sh
# Install an eck-managed Elasticsearch, Kibana, Beats and Logstash using custom values.
helm install eck-stack-with-logstash elastic/eck-stack \
    --values https://raw.githubusercontent.com/elastic/cloud-on-k8s/2.16/deploy/eck-stack/examples/logstash/basic-eck.yaml -n elastic-stack
```

## Standalone Elastic APM Server along with Elasticsearch and Kibana [k8s-install-apm-server-elasticsearch-kibana-helm] 

The following section builds upon the previous sections, and allows installing a standalone Elastic APM Server along with Elasticsearch and Kibana.

```sh
# Install an eck-managed Elasticsearch, Kibana, and standalone APM Server using custom values.
helm install eck-stack-with-apm-server elastic/eck-stack \
    --values https://raw.githubusercontent.com/elastic/cloud-on-k8s/2.16/deploy/eck-stack/examples/apm-server/basic.yaml -n elastic-stack
```

## Install individual components of the Elastic Stack [k8s-eck-stack-individual-components] 

You can install individual components in one of two ways using the provided Helm Charts.

1. Using Helm values
2. Using the individual Helm Charts directly (not the `eck-stack` helm chart)

**Using Helm values to install only Elasticsearch**

```sh
helm install es-quickstart elastic/eck-stack -n elastic-stack --create-namespace --set=eck-kibana.enabled=false
```

**Using the eck-elasticsearch Helm Chart directly to install only Elasticsearch**

```sh
helm install es-quickstart elastic/eck-elasticsearch -n elastic-stack --create-namespace
```

## Adding Ingress to the Elastic stack [k8s-eck-stack-ingress] 

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

For illustration purposes, the ingress objects created by the previous command will look similar to the following:

```yaml
# Source: eck-stack/charts/eck-elasticsearch/templates/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: elasticsearch
  labels:
    helm.sh/chart: eck-elasticsearch-0.14.1
    app.kubernetes.io/name: eck-elasticsearch
    app.kubernetes.io/instance: es-kb-quickstart
    app.kubernetes.io/managed-by: Helm
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
    helm.sh/chart: eck-kibana-0.14.1
    app.kubernetes.io/name: eck-kibana
    app.kubernetes.io/instance: es-kb-quickstart
    app.kubernetes.io/managed-by: Helm
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

You can view all configurable values of the Elastic Stack helm chart of the individual charts by running the following:

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
