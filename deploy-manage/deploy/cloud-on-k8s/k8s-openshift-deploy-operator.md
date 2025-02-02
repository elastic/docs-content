---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-openshift-deploy-the-operator.html
---

# Deploy the operator [k8s-openshift-deploy-the-operator]

1. Apply the all-in-one template, as described in the [quickstart](deploy-an-orchestrator.md).

    ```shell
    oc create -f https://download.elastic.co/downloads/eck/2.16.1/crds.yaml
    oc apply -f https://download.elastic.co/downloads/eck/2.16.1/operator.yaml
    ```

2. [Optional] If the Software Defined Network is configured with the `ovs-multitenant` plug-in, you must allow the `elastic-system` namespace to access other Pods and Services in the cluster:

    ```shell
    oc adm pod-network make-projects-global elastic-system
    ```

3. Create a namespace to hold the Elastic resources (Elasticsearch, Kibana, APM Server, Enterprise Search, Beats, Elastic Agent, Elastic Maps Server, and Logstash):

    ::::{note} 
    A namespace other than the default namespaces (default, kube-**, openshift-**, etc) is required such that default [Security Context Constraint](https://docs.openshift.com/container-platform/4.12/authentication/managing-security-context-constraints.md) (SCC) permissions are applied automatically. Elastic resources will not work properly in any of the default namespaces.
    ::::


```shell
oc new-project elastic # creates the elastic project
```

1. [Optional] Allow another user or a group of users to manage the Elastic resources:

    ```shell
    oc adm policy add-role-to-user elastic-operator developer -n elastic
    ```

    In this example the user `developer` is allowed to manage Elastic resources in the namespace `elastic`.


