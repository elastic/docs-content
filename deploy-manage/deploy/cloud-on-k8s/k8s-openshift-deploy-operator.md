---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-openshift-deploy-the-operator.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Deploy the operator [k8s-openshift-deploy-the-operator]

This page shows the installation steps to deploy ECK in Openshift:

1. Apply the manifests the same way as described in [](./install-using-yaml-manifest-quickstart.md) document:

   ```shell subs=true
   oc create -f https://download.elastic.co/downloads/eck/{{version.eck}}/crds.yaml
   oc apply -f https://download.elastic.co/downloads/eck/{{version.eck}}/operator.yaml
   ```

2. [Optional] If the Software Defined Network is configured with the `ovs-multitenant` plug-in, you must allow the `elastic-system` namespace to access other Pods and Services in the cluster:

   ```shell
   oc adm pod-network make-projects-global elastic-system
   ```

3. Create a namespace to hold the Elastic resources ({{eck_resources_list}}):
   ::::{note}
   A namespace other than the default namespaces (default, kube-\*, openshift-\*, etc) is required such that default [Security Context Constraint](https://docs.openshift.com/container-platform/4.12/authentication/managing-security-context-constraints.html) (SCC) permissions are applied automatically. Elastic resources will not work properly in any of the default namespaces.
   ::::

   ```sh
   oc new-project elastic # creates the elastic project
   ```

4. [Optional] Allow another user or a group of users to manage the Elastic resources:

   ```shell
   oc adm policy add-role-to-user elastic-operator developer -n elastic
   ```

   In this example the user `developer` is allowed to manage Elastic resources in the namespace `elastic`.