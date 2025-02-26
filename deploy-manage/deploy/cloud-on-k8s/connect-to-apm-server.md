---
applies_to:
  deployment:
    eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-apm-connecting.html
---

# Connect to the APM Server [k8s-apm-connecting]

This section covers the following topics:

* [APM Server service](#k8s-apm-service)
* [APM Server secret token](#k8s-apm-secret-token)
* [APM Server API keys](#k8s-apm-api-keys)

## APM Server service [k8s-apm-service]

The APM Server is exposed with a Service. For information on accessing it, check [How to access Elastic Stack services](accessing-services.md).

To retrieve the list of all the APM Services, use the following command:

```sh
kubectl get service --selector='common.k8s.elastic.co/type=apm-server'
```

```sh
NAME                             TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
apm-server-quickstart-apm-http   ClusterIP   10.0.1.252   <none>        8200/TCP   154m
```


## APM Server secret token [k8s-apm-secret-token]

The operator generates an authorization token that agents must send to authenticate themselves to the APM Server.

This token is stored in a secret named `{{APM-server-name}}-apm-token` and can be retrieved with the following command:

```sh
kubectl get secret/apm-server-quickstart-apm-token -o go-template='{{index .data "secret-token" | base64decode}}'
```

For more information, check [APM Server Reference](https://www.elastic.co/guide/en/apm/server/current/index.html).


## APM Server API keys [k8s-apm-api-keys]

If you want to configure API keys to authorize requests to the APM Server, instead of using the APM Server CLI, you have to create API keys using the Elasticsearch  [create API key API](https://www.elastic.co/guide/en/elasticsearch/reference/7.14/security-api-create-api-key.html), check the [APM Server documentation](/solutions/observability/apps/api-keys.md).


