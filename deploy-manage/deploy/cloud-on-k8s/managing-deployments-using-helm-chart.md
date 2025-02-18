---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-stack-helm-chart.html
---

# Managing deployments using a Helm chart [k8s-stack-helm-chart]

Starting from ECK 2.4.0, a Helm chart is available for managing Elastic Stack resources using the ECK Operator. It is available from the Elastic Helm repository and can be added to your Helm repository list by running the following command:

```sh
helm repo add elastic https://helm.elastic.co
helm repo update
```

::::{note} 
The minimum supported version of Helm is 3.2.0.
::::



## Installing Elasticsearch and Kibana using the eck-stack Helm Chart [k8s-install-elasticsearch-kibana-helm] 

Similar to the [quickstart](elasticsearch-deployment-quickstart.md), the following section describes how to setup an Elasticsearch cluster with a simple Kibana instance managed by ECK, and how to customize a deployment using the eck-stack Helm chart’s values.

```sh
# Install an eck-managed Elasticsearch and Kibana using the default values, which deploys the quickstart examples.
helm install es-kb-quickstart elastic/eck-stack -n elastic-stack --create-namespace
```


### Customizing Kibana and Elasticsearch using the eck-stack Helm Chart’s example values [k8s-eck-stack-helm-customize] 

There are example Helm values files for installing and managing a more advanced Elasticsearch and/or Kibana [in the project repository](https://github.com/elastic/cloud-on-k8s/tree/2.16/deploy/eck-stack/examples).

To use one or more of these example configurations, use the `--values` Helm option, as seen in the following section.

```sh
# Install an eck-managed Elasticsearch and Kibana using the Elasticsearch node roles example with hot, warm, and cold data tiers, and the Kibana example customizing the http service.
helm install es-quickstart elastic/eck-stack -n elastic-stack --create-namespace \
    --values https://raw.githubusercontent.com/elastic/cloud-on-k8s/2.16/deploy/eck-stack/examples/elasticsearch/hot-warm-cold.yaml \
    --values https://raw.githubusercontent.com/elastic/cloud-on-k8s/2.16/deploy/eck-stack/examples/kibana/http-configuration.yaml
```


## Installing Fleet Server with Elastic Agents along with Elasticsearch and Kibana using the eck-stack Helm Chart [k8s-install-fleet-agent-elasticsearch-kibana-helm] 

The following section builds upon the previous section, and allows installing Fleet Server, and Fleet-managed Elastic Agents along with Elasticsearch and Kibana.

```sh
# Install an eck-managed Elasticsearch, Kibana, Fleet Server, and managed Elastic Agents using custom values.
helm install eck-stack-with-fleet elastic/eck-stack \
    --values https://raw.githubusercontent.com/elastic/cloud-on-k8s/2.16/deploy/eck-stack/examples/agent/fleet-agents.yaml -n elastic-stack
```


## Installing Logstash along with Elasticsearch, Kibana and Beats using the eck-stack Helm Chart [k8s-install-logstash-elasticsearch-kibana-helm] 

The following section builds upon the previous sections, and allows installing Logstash along with Elasticsearch, Kibana and Beats.

```sh
# Install an eck-managed Elasticsearch, Kibana, Beats and Logstash using custom values.
helm install eck-stack-with-logstash elastic/eck-stack \
    --values https://raw.githubusercontent.com/elastic/cloud-on-k8s/2.16/deploy/eck-stack/examples/logstash/basic-eck.yaml -n elastic-stack
```


## Installing a standalone Elastic APM Server along with Elasticsearch and Kibana using the eck-stack Helm Chart [k8s-install-apm-server-elasticsearch-kibana-helm] 

The following section builds upon the previous sections, and allows installing a standalone Elastic APM Server along with Elasticsearch and Kibana.

```sh
# Install an eck-managed Elasticsearch, Kibana, and standalone APM Server using custom values.
helm install eck-stack-with-apm-server elastic/eck-stack \
    --values https://raw.githubusercontent.com/elastic/cloud-on-k8s/2.16/deploy/eck-stack/examples/apm-server/basic.yaml -n elastic-stack
```

### Installing individual components of the Elastic Stack using the Helm Charts [k8s-eck-stack-individual-components] 

You can install individual components in one of two ways using the provided Helm Charts.

1. Using Helm values
2. Using the individual Helm Charts directly

**Using Helm values to install only Elasticsearch**

```sh
helm install es-quickstart elastic/eck-stack -n elastic-stack --create-namespace --set=eck-kibana.enabled=false
```

**Using the eck-elasticsearch Helm Chart directly to install only Elasticsearch**

```sh
helm install es-quickstart elastic/eck-elasticsearch -n elastic-stack --create-namespace
```


### Adding Ingress to the Elastic stack using the Helm Charts [k8s-eck-stack-ingress] 

Both Elasticsearch and Kibana support Ingress, which can be enabled using the following options:

```sh
helm install es-quickstart elastic/eck-elasticsearch -n elastic-stack --create-namespace --set=ingress.enabled=true --set=ingress.hosts[0].host=elasticsearch.example.com --set=ingress.hosts[0].path="/"
```

