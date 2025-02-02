# Security [k8s-security]

All Elastic Stack resources deployed by the ECK operator are secured by default. The operator sets up basic authentication and TLS to encrypt network traffic to, from, and within your Elasticsearch cluster.

## Authentication [k8s-authentication]

To access Elastic resources, the operator manages a default user named `elastic` with the `superuser` role. Its password is stored in a `Secret` named `<name>-elastic-user`.

```sh
> kubectl get secret hulk-es-elastic-user -o go-template='{{.data.elastic | base64decode }}'
42xyz42citsale42xyz42
```

::::{note} 
Beware of copying this Secret as-is into a different namespace. Check [Common Problems: Owner References](../../../troubleshoot/deployments/cloud-on-k8s/common-problems.md#k8s-common-problems-owner-refs) for more information.
::::



