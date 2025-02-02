# Rotate auto-generated credentials [k8s-rotate-credentials]

When deploying an Elastic Stack application, the operator generates a set of credentials essential for the operation of that application. For example, these generated credentials include the default `elastic` user for Elasticsearch and the security token for APM Server.

To list all auto-generated credentials in a namespace, run the following command:

```sh
kubectl get secret -l eck.k8s.elastic.co/credentials=true
```

You can force the auto-generated credentials to be regenerated with new values by deleting the appropriate Secret. For example, to change the password for the `elastic` user from the [quickstart example](../../../deploy-manage/deploy/cloud-on-k8s/deploy-an-orchestrator.md), use the following command:

```sh
kubectl delete secret quickstart-es-elastic-user
```

::::{warning}
If you are using the `elastic` user credentials in your own applications, they will fail to connect to Elasticsearch and Kibana after you run this command. It is not recommended to use `elastic` user credentials for production use cases. Always [create your own users with restricted roles](../../../deploy-manage/users-roles/cluster-or-deployment-auth/native.md) to access Elasticsearch.
::::


To regenerate all auto-generated credentials in a namespace, run the following command:

```sh
kubectl delete secret -l eck.k8s.elastic.co/credentials=true
```

::::{warning}
This command regenerates auto-generated credentials of **all** Elastic Stack applications in the namespace.
::::
