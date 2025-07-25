---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-network-policies.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s_prerequisites.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Kubernetes network policies [k8s-network-policies]

Kubernetes [network policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) allow you to isolate pods by restricting incoming and outgoing network connections to a trusted set of sources and destinations.

This section describes how to use network policies to isolate the ECK operator and the {{stack}} applications to a set of namespaces to implement a form of soft multi-tenancy. Soft multi-tenancy is a term used to describe a scenario where a group of trusted users (different teams within an organization, for example) share a single resource such as a Kubernetes cluster.

Note that network policies alone are not sufficient for security. You should complement them with strict RBAC policies, resource quotas, node taints, and other available security mechanisms to ensure that tenants cannot access, modify, or disrupt resources belonging to each other.

:::{tip}
{{eck}} also supports [IP filtering](/deploy-manage/security/ip-filtering-basic.md).
:::

::::{note}
There are several efforts to support multi-tenancy on Kubernetes, including the [official working group for multi-tenancy](https://github.com/kubernetes-sigs/multi-tenancy) and community extensions such as [loft](https://loft.sh) and [kiosk](https://github.com/kiosk-sh/kiosk), that can make configuration and management easier. You might need to employ network policies such the ones described in this section to have fine-grained control over {{stack}} applications deployed by your tenants.
::::

The following sections assume that the operator is installed in the `elastic-system` namespace with the [`namespaces` configuration](../deploy/cloud-on-k8s/configure-eck.md) set to `team-a,team-b`. Each namespace is expected to be labelled as follows:

```sh
kubectl label namespace elastic-system eck.k8s.elastic.co/operator-name=elastic-operator
kubectl label namespace team-a eck.k8s.elastic.co/tenant=team-a
kubectl label namespace team-b eck.k8s.elastic.co/tenant=team-b
```

## Prerequisites [k8s_prerequisites]

To set up the network policies correctly you must know the operator Pod selector and the Kubernetes API server IP. They may vary depending on your environment and how the operator has been installed.

### Operator Pod selector [k8s_operator_pod_selector]

The operator Pod label depends on how the operator has been installed. Check the following table to know which label name is used in the network policies.

| Installation method | Pod selector |
| --- | --- |
| YAML manifests | `control-plane: elastic-operator`<br> |
| Helm Charts | `app.kubernetes.io/name: elastic-operator`<br> |

::::{note}
The examples in this section assume that the ECK operator has been installed using the Helm chart.
::::

### Kubernetes API server IP [k8s_kubernetes_api_server_ip]

Run `kubectl get endpoints kubernetes -n default` to obtain the API server IP address for your cluster.

::::{note}
The following examples assume that the Kubernetes API server IP address is `10.0.0.1`.
::::

## Isolating the operator [k8s-network-policies-operator-isolation]

The minimal set of permissions required are as follows:

|     |     |
| --- | --- |
| Egress (outgoing) | • TCP port 443 of the Kubernetes API server.<br>• UDP port 53 for DNS lookup.<br>• TCP port 9200 of {{es}} nodes on managed namespace.<br> |
| Ingress (incoming) | • TCP port 9443 for webhook requests from the Kubernetes API server.<br> |

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: elastic-operator
  namespace: elastic-system
spec:
  egress:
  - ports:
    - port: 53
      protocol: UDP
  - ports:
    - port: 443
      protocol: TCP
    to:
    - ipBlock:
        cidr: 10.0.0.1/32
  - ports:
    - port: 9200
      protocol: TCP
    to:
    - namespaceSelector:
        matchExpressions:
        - key: eck.k8s.elastic.co/tenant
          operator: In
          values:
          - team-a
          - team-b
      podSelector:
        matchLabels:
          common.k8s.elastic.co/type: elasticsearch
  ingress:
  - from:
    - ipBlock:
        cidr: 10.0.0.1/32
    ports:
    - port: 9443
      protocol: TCP
  podSelector:
    matchLabels:
      app.kubernetes.io/name: elastic-operator
```


## Isolating {{es}} [k8s-network-policies-elasticsearch-isolation]

|     |     |
| --- | --- |
| Egress (outgoing) | • TCP port 9300 to other {{es}} nodes in the namespace (transport port).<br>• UDP port 53 for DNS lookup.<br> |
| Ingress (incoming) | • TCP port 9200 from the operator and other pods in the namespace.<br>• TCP port 9300 from other {{es}} nodes in the namespace (transport port).<br> |

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: eck-elasticsearch
  namespace: team-a
spec:
  egress:
  - ports:
    - port: 9300
      protocol: TCP
    to:
    - namespaceSelector:
        matchLabels:
          eck.k8s.elastic.co/tenant: team-a
      podSelector:
        matchLabels:
          common.k8s.elastic.co/type: elasticsearch
  - ports:
    - port: 53
      protocol: UDP
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          eck.k8s.elastic.co/operator-name: elastic-operator
      podSelector:
        matchLabels:
          app.kubernetes.io/name: elastic-operator
    - namespaceSelector:
        matchLabels:
          eck.k8s.elastic.co/tenant: team-a
    # [Optional] Allow ingress controller pods from the ingress-nginx namespace.
    #- namespaceSelector:
    #    matchLabels:
    #      name: ingress-nginx
    ports:
    - port: 9200
      protocol: TCP
  - from:
    - namespaceSelector:
        matchLabels:
          eck.k8s.elastic.co/tenant: team-a
      podSelector:
        matchLabels:
          common.k8s.elastic.co/type: elasticsearch
    ports:
    - port: 9300
      protocol: TCP
  podSelector:
    matchLabels:
      common.k8s.elastic.co/type: elasticsearch
```


## Isolating {{kib}} [k8s-network-policies-kibana-isolation]

|     |     |
| --- | --- |
| Egress (outgoing) | • TCP port 9200 to {{es}} nodes in the namespace.<br>• UDP port 53 for DNS lookup.<br> |
| Ingress (incoming) | • TCP port 5601 from other pods in the namespace.<br> |

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: eck-kibana
  namespace: team-a
spec:
  egress:
  - ports:
    - port: 9200
      protocol: TCP
    to:
    - namespaceSelector:
        matchLabels:
          eck.k8s.elastic.co/tenant: team-a
      podSelector:
        matchLabels:
          common.k8s.elastic.co/type: elasticsearch
          # [Optional] Restrict to a single Elasticsearch cluster named hulk.
          # elasticsearch.k8s.elastic.co/cluster-name=hulk
  - ports:
    - port: 53
      protocol: UDP
    # [Optional] If Agent is deployed, this is to allow Kibana to access the Elastic Package Registry (https://epr.elastic.co).
    # - port: 443
    #   protocol: TCP
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          eck.k8s.elastic.co/tenant: team-a
    # [Optional] Allow ingress controller pods from the ingress-nginx namespace.
    #- namespaceSelector:
    #    matchLabels:
    #      name: ingress-nginx
    ports:
    - port: 5601
      protocol: TCP
  podSelector:
    matchLabels:
      common.k8s.elastic.co/type: kibana
```


## Isolating APM Server [k8s-network-policies-apm-server-isolation]

|     |     |
| --- | --- |
| Egress (outgoing) | • TCP port 9200 to {{es}} nodes in the namespace.<br>• TCP port 5601 to {{kib}} instances in the namespace.<br>• UDP port 53 for DNS lookup.<br> |
| Ingress (incoming) | • TCP port 8200 from other pods in the namespace.<br> |

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: eck-apm-server
  namespace: team-a
spec:
  egress:
  - ports:
    - port: 9200
      protocol: TCP
    to:
    - namespaceSelector:
        matchLabels:
          eck.k8s.elastic.co/tenant: team-a
      podSelector:
        matchLabels:
          common.k8s.elastic.co/type: elasticsearch
  - ports:
    - port: 5601
      protocol: TCP
    to:
    - namespaceSelector:
        matchLabels:
          eck.k8s.elastic.co/tenant: team-a
      podSelector:
        matchLabels:
          common.k8s.elastic.co/type: kibana
  - ports:
    - port: 53
      protocol: UDP
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          eck.k8s.elastic.co/tenant: team-a
    # [Optional] Allow ingress controller pods from the ingress-nginx namespace.
    #- namespaceSelector:
    #    matchLabels:
    #      name: ingress-nginx
    ports:
    - port: 8200
      protocol: TCP
  podSelector:
    matchLabels:
      common.k8s.elastic.co/type: apm-server
```

## Isolating Beats [k8s-network-policies-beats-isolation]

::::{note}
Some {{beats}} may require additional access rules than what is listed here. For example, {{heartbeat}} will require a rule to allow access to the endpoint it is monitoring.
::::


|     |     |
| --- | --- |
| Egress (outgoing) | • TCP port 9200 to {{es}} nodes in the namespace.<br>• TCP port 5601 to {{kib}} instances in the namespace.<br>• UDP port 53 for DNS lookup.<br> |

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: eck-beats
  namespace: team-a
spec:
  egress:
  - ports:
    - port: 9200
      protocol: TCP
    to:
    - namespaceSelector:
        matchLabels:
          eck.k8s.elastic.co/tenant: team-a
      podSelector:
        matchLabels:
          common.k8s.elastic.co/type: elasticsearch
  - ports:
    - port: 5601
      protocol: TCP
    to:
    - namespaceSelector:
        matchLabels:
          eck.k8s.elastic.co/tenant: team-a
      podSelector:
        matchLabels:
          common.k8s.elastic.co/type: kibana
  - ports:
    - port: 53
      protocol: UDP
  podSelector:
    matchLabels:
      common.k8s.elastic.co/type: beat
```


## Isolating Elastic Agent and Fleet [k8s-network-policies-agent-isolation]

::::{note}
Some {{agent}} policies may require additional access rules other than those listed here.
::::


|     |     |
| --- | --- |
| Egress (outgoing) | • TCP port 9200 to {{es}} nodes in the namespace.<br>• TCP port 5601 to {{kib}} instances in the namespace.<br>• TCP port 8220 to {{fleet}} instances in the namespace.<br>• UDP port 53 for DNS lookup.<br> |

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: eck-agent
  namespace: team-a
spec:
  egress:
    - ports:
        - port: 8220
          protocol: TCP
      to:
        - namespaceSelector:
            matchLabels:
              eck.k8s.elastic.co/tenant: team-a
          podSelector:
            matchLabels:
              common.k8s.elastic.co/type: agent
    - ports:
        - port: 5601
          protocol: TCP
      to:
        - namespaceSelector:
            matchLabels:
              eck.k8s.elastic.co/tenant: team-a
          podSelector:
            matchLabels:
              common.k8s.elastic.co/type: kibana
    - ports:
        - port: 9200
          protocol: TCP
      to:
        - namespaceSelector:
            matchLabels:
              eck.k8s.elastic.co/tenant: team-a
          podSelector:
            matchLabels:
              common.k8s.elastic.co/type: elasticsearch
    - ports:
        - port: 53
          protocol: UDP
    - ports:
        - port: 443
          protocol: TCP
      to:
        - ipBlock:
            cidr: 10.0.0.1/32
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              eck.k8s.elastic.co/tenant: team-a
      ports:
        - port: 8220
          protocol: TCP
  podSelector:
    matchLabels:
      common.k8s.elastic.co/type: agent
```

## Isolating Logstash [k8s-network-policies-logstash-isolation]

::::{note}
{{ls}} may require additional access rules than those listed here, depending on plugin usage.
::::


|     |     |
| --- | --- |
| Egress (outgoing) | • TCP port 9200 to {{es}} nodes in the namespace.<br>• UDP port 53 for DNS lookup.<br> |

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: eck-logstash
  namespace: team-a
spec:
  egress:
  - ports:
    - port: 9200
      protocol: TCP
    to:
    - namespaceSelector:
        matchLabels:
          eck.k8s.elastic.co/tenant: team-a
      podSelector:
        matchLabels:
          common.k8s.elastic.co/type: elasticsearch
  - ports:
    - port: 53
      protocol: UDP
  podSelector:
    matchLabels:
      common.k8s.elastic.co/type: logstash
```

## Isolating Enterprise Search [k8s-network-policies-enterprise-search-isolation]

Enterprise Search is not available in {{stack}} versions 9.0 and later. For an example of Enterprise Search isolation using network policies in previous {{stack}} versions, refer to the [previous ECK documentation](https://www.elastic.co/guide/en/cloud-on-k8s/2.16/k8s_prerequisites.html#k8s-network-policies-enterprise-search-isolation).
