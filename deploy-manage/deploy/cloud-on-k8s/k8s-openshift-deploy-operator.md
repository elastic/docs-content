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

::::{note}
These instructions do not apply if the operator is installed from the OpenShift software catalog or when using Operator Lifecycle Manager (OLM). However, creating resources outside of the installation namespace, as mentioned in step 3, is always advised.
::::

This page shows the installation steps to deploy ECK in Openshift:

1. Apply the manifests the same way as described in [](./install-using-yaml-manifest-quickstart.md) document:

   ```shell subs=true
   oc create -f https://download.elastic.co/downloads/eck/{{version.eck}}/crds.yaml
   oc apply -f https://download.elastic.co/downloads/eck/{{version.eck}}/operator.yaml
   ```

2. [Optional] Only if your cluster still uses the OpenShift SDN network plug-in with the `ovs-multitenant` mode, you must allow the `elastic-system` namespace to access other Pods and Services in the cluster. Clusters that use the default OVN-Kubernetes network plug-in don't need this step:

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
   oc adm policy add-role-to-user elastic-operator-edit developer -n elastic
   ```

   In this example the user `developer` is allowed to manage Elastic resources in the namespace `elastic`. Use `elastic-operator-view` to grant read-only access. Users that already have the built-in `edit` or `admin` role in the namespace can manage Elastic resources without this step.