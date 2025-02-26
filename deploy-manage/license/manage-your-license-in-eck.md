---
navigation_title: "{{eck}}"
applies_to:
  deployment:
    eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-licensing.html
---

# Manage your license in {{eck}} [k8s-licensing]

When you install the default distribution of ECK, you receive a Basic license. Any Elastic stack application you manage through ECK will also be Basic licensed. Go to [https://www.elastic.co/subscriptions](https://www.elastic.co/subscriptions) to check which features are included in the Basic license for free.

::::{important}
ECK is only offered in two licensing tiers: Basic and Enterprise. Similar to the Elastic Stack, customers can download and use ECK with a Basic license for free. Basic license users can obtain support from GitHub or through our [community](https://discuss.elastic.co). A paid Enterprise subscription is required to engage the Elastic support team. For more details, check the [Elastic subscriptions](https://www.elastic.co/subscriptions).
::::


In this section, you are going to learn how to:

* [Start a trial](#k8s-start-trial)
* [Add a license](#k8s-add-license)
* [Update your license](#k8s-update-license)
* [Get usage data](#k8s-get-usage-data)


## Start a trial [k8s-start-trial]

If you want to try the features included in the Enterprise subscription, you can start a 30-day trial. To start a trial, create a Kubernetes secret as shown in this example. Note that it must be in the same namespace as the operator:

```yaml
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: eck-trial-license
  namespace: elastic-system
  labels:
    license.k8s.elastic.co/type: enterprise_trial
  annotations:
    elastic.co/eula: accepted <1>
EOF
```

1. By setting this annotation to `accepted` you are expressing that you have accepted the Elastic EULA which can be found at [https://www.elastic.co/eula](https://www.elastic.co/eula).


::::{note}
You can initiate a trial only if a trial has not been previously activated.
::::


At the end of the trial period, the Platinum and Enterprise features operate in a [degraded mode](https://www.elastic.co/guide/en/elastic-stack-overview/current/license-expiration.html). You can revert to a Basic license, extend the trial, or purchase an Enterprise subscription.


## Add a license [k8s-add-license]

If you have a valid Enterprise subscription or a trial license extension, you will receive a link to download a license as a JSON file.

::::{note}
When downloading the license choose the "Orchestration license" option.
::::


The downloaded JSON file contains the Enterprise orchestration license which enables ECK Enterprise features. Embedded in the orchestration license are also Enterprise stack licenses for recent Elasticsearch versions and Platinum licenses for older Elasticsearch versions that do not support Enterprise licenses.

To add the license to your ECK installation, create a Kubernetes secret of the following form:

```yaml
apiVersion: v1
kind: Secret
metadata:
  labels:
    license.k8s.elastic.co/scope: operator <1>
  name: eck-license
type: Opaque
data:
  license: "JSON license in base64 format"  <2>
```

1. This label is required for ECK to identify your license secret.
2. The license file can have any name.


You can easily create this secret using `kubectl` built-in support for secrets. Note that it must be in the same namespace as the operator:

```shell script
kubectl create secret generic eck-license --from-file=my-license-file.json -n elastic-system
kubectl label secret eck-license "license.k8s.elastic.co/scope"=operator -n elastic-system
```

After you install a license into ECK, the Enterprise features of the operator are available, like Elasticsearch autoscaling and support for Elastic Maps Server. All the Elastic Stack applications you manage with ECK will have Platinum and Enterprise features enabled.  The [`_license`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-license-get) API reports that individual Elasticsearch clusters are running under an Enterprise license, and the [elastic-licensing](#k8s-get-usage-data) ConfigMap contains the current license level of the ECK operator. The applications created before you installed the license are upgraded to Platinum or Enterprise features without interruption of service after a short delay.

::::{note}
The Elasticsearch `_license` API for versions before 8.0.0 reports a Platinum license level for backwards compatibility even if an Enterprise license is installed.
::::



## Update your license [k8s-update-license]

Before your current Enterprise license expires, you will receive a new Enterprise license from Elastic (provided that your subscription is valid).

::::{note}
You can check the expiry date of your license in the [elastic-licensing](#k8s-get-usage-data) ConfigMap. Enterprise licenses are container licenses that include multiple licenses for individual Elasticsearch clusters with shorter expiry. Therefore, you get a different expiry in Kibana or through the Elasticsearch [`_license`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-license-get) API. ECK automatically updates the Elasticsearch cluster licenses until the expiry date of the ECK Enterprise license is reached.
::::


To avoid any unintended downgrade of individual Elasticsearch clusters to a Basic license while installing the new license, we recommend installing the new Enterprise license as a new Kubernetes secret next to your existing Enterprise license. Just replace `eck-license` with a different name in the [Kubernetes secret example](#k8s-add-license). ECK will use the correct license automatically.

Once you have created the new license secret you can safely delete the old license secret.


## Get usage data [k8s-get-usage-data]

The operator periodically writes the total amount of Elastic resources under management to a configmap named `elastic-licensing`, which is in the same namespace as the operator. Here is an example of retrieving the data:

```shell
> kubectl -n elastic-system get configmap elastic-licensing -o json | jq .data
{
  "apm_memory": "0.50GiB",
  "apm_memory_bytes": "536870912",
  "eck_license_expiry_date": "2025-01-01T00:59:59+01:00",
  "eck_license_level": "enterprise",
  "elasticsearch_memory": "18.00GiB",
  "elasticsearch_memory_bytes": "19327352832",
  "enterprise_resource_units": "1",
  "enterprise_search_memory": "4.00GiB",
  "enterprise_search_memory_bytes": "4294967296",
  "kibana_memory": "1.00GiB",
  "kibana_memory_bytes": "1073741824",
  "logstash_memory": "2.00GiB",
  "logstash_memory_bytes": "2147483648",
  "max_enterprise_resource_units": "250",
  "timestamp": "2024-07-26T12:40:42+02:00",
  "total_managed_memory": "25.50GiB",
  "total_managed_memory_bytes": "27380416512"
}
```

If the operator metrics endpoint is enabled with the `--metrics-port` flag (check [*Configure ECK*](../deploy/cloud-on-k8s/configure-eck.md)), license usage data will be included in the reported metrics.

```shell
> curl "$ECK_METRICS_ENDPOINT" | grep elastic_licensing
# HELP elastic_licensing_enterprise_resource_units_max Maximum number of enterprise resource units available
# TYPE elastic_licensing_enterprise_resource_units_max gauge
elastic_licensing_enterprise_resource_units_max{license_level="enterprise"} 250
# HELP elastic_licensing_enterprise_resource_units_total Total enterprise resource units used
# TYPE elastic_licensing_enterprise_resource_units_total gauge
elastic_licensing_enterprise_resource_units_total{license_level="enterprise"} 1
# HELP elastic_licensing_memory_gibibytes_apm Memory used by APM server in GiB
# TYPE elastic_licensing_memory_gibibytes_apm gauge
elastic_licensing_memory_gibibytes_apm{license_level="enterprise"} 0.5
# HELP elastic_licensing_memory_gibibytes_elasticsearch Memory used by Elasticsearch in GiB
# TYPE elastic_licensing_memory_gibibytes_elasticsearch gauge
elastic_licensing_memory_gibibytes_elasticsearch{license_level="enterprise"} 18
# HELP elastic_licensing_memory_gibibytes_kibana Memory used by Kibana in GiB
# TYPE elastic_licensing_memory_gibibytes_kibana gauge
elastic_licensing_memory_gibibytes_kibana{license_level="enterprise"} 1
# HELP elastic_licensing_memory_gibibytes_logstash Memory used by Logstash in GiB
# TYPE elastic_licensing_memory_gibibytes_logstash gauge
elastic_licensing_memory_gibibytes_logstash{license_level="enterprise"} 2
# HELP elastic_licensing_memory_gibibytes_total Total memory used in GiB
# TYPE elastic_licensing_memory_gibibytes_total gauge
elastic_licensing_memory_gibibytes_total{license_level="enterprise"} 25.5
```

::::{note}
Logstash resources managed by ECK will be counted towards ERU usage for informational purposes. Billable consumption depends on license terms on a per customer basis (See [Self Managed Subscription Agreement](https://www.elastic.co/agreements/global/self-managed))
::::


