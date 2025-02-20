---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-upgrading-eck.html
---

# Upgrade Elastic Cloud on Kubernetes [k8s-upgrading-eck]

This page provides instructions on how to upgrade the ECK operator.

For upgrades of Elastic Stack applications like Elasticsearch or Kibana, check [Upgrade the Elastic Stack version](../deployment-or-cluster.md).


## Before you upgrade to ECK 2.16.1 [k8s-ga-upgrade]

The upgrade process results in an update to all the existing managed resources. This potentially triggers a rolling restart of all Elasticsearch and Kibana pods. This [list](#k8s-beta-to-ga-rolling-restart) details the affected target versions that will cause a rolling restart. If you have a large Elasticsearch cluster or multiple Elastic Stack deployments, the rolling restart could cause a performance degradation. When you plan to upgrade ECK for production workloads, take into consideration the time required to upgrade the ECK operator plus the time required to roll all managed workloads and Elasticsearch clusters. Check for more information on how to [control the rolling restarts during the upgrade](#k8s-beta-to-ga-rolling-restart).

Before upgrading, refer to the [release notes](https://www.elastic.co/guide/en/cloud-on-k8s/current/release-notes-2.16.1.html) to make sure that the release does not contain any breaking changes that could affect you. The [release highlights document](https://www.elastic.co/guide/en/cloud-on-k8s/current/release-highlights-2.16.1.html) provides more details and possible workarounds for any breaking changes or known issues in each release.

Note that the release notes and highlights only list the changes since the last release. If during the upgrade you skip any intermediate versions and go for example from 1.0.0 directly to 2.16.1, review the release notes and highlights of each of the skipped releases to understand all the breaking changes you might encounter during and after the upgrade.

::::{warning}
When upgrading always ensure that the version of the CRDs installed in the cluster matches the version of the operator. If you are using Helm, the CRDs are upgraded automatically as part of the Helm chart. If you are using the YAML manifests, you must upgrade the CRDs manually. Running differing versions of the CRDs and the operator is not a supported configuration and can lead to unexpected behavior.
::::



## Upgrade instructions [k8s-upgrade-instructions]


### Upgrading from ECK 1.6 or earlier [k8s_upgrading_from_eck_1_6_or_earlier]

Release 1.7.0 moved the [CustomResourceDefinitions](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/) (CRD) used by ECK to the v1 version. If you upgrade from a previous version of ECK, the new version of the CRDs replaces the existing CRDs. If you cannot remove the current ECK installation because you have production workloads that must not be deleted, the following approach is recommended.

```shell
kubectl replace -f https://download.elastic.co/downloads/eck/2.16.1/crds.yaml
```

::::{note}
If you skipped a release in which new CRDs where introduced, you will get an error message similar to `Error from server (NotFound): error when replacing "config/crds.yaml": customresourcedefinitions.apiextensions.k8s.io ... not found`. To add the missing CRDs run

```shell
kubectl create -f https://download.elastic.co/downloads/eck/2.16.1/crds.yaml
```

::::


Then upgrade the remaining objects with the operator manifest:

```shell
kubectl apply -f https://download.elastic.co/downloads/eck/2.16.1/operator.yaml
```

```shell
helm upgrade elastic-operator elastic/eck-operator-crds -n elastic-system --force
```

Then upgrade the main chart as usual:

```shell
helm upgrade elastic-operator elastic/eck-operator -n elastic-system
```

If you are using ECK through an OLM-managed distribution channel like [operatorhub.io](https://operatorhub.io) or the OpenShift OperatorHub then the CRD version upgrade will be handled by OLM for you and you do not need to take special action.


### Upgrading from ECK 1.9 or earlier [k8s_upgrading_from_eck_1_9_or_earlier]

Operator Lifecycle Manager (OLM) and OpenShift OperatorHub users that run with automatic upgrades enabled, are advised to set the `set-default-security-context` [operator flag](/deploy-manage/deploy/cloud-on-k8s/configure-eck.md) explicitly before upgrading to ECK 2.0 or later. If not set, ECK can fail to [auto-detect](https://github.com/elastic/cloud-on-k8s/issues/5061) the correct security context configuration and Elasticsearch Pods may not be allowed to run.


### Upgrading from ECK 2.0 or later [k8s_upgrading_from_eck_2_0_or_later]

There are no special instructions to follow if you upgrade from any 2.x version to 2.16.1. Use the upgrade method applicable to your installation method of choice.

```shell
kubectl apply -f https://download.elastic.co/downloads/eck/2.16.1/crds.yaml
kubectl apply -f https://download.elastic.co/downloads/eck/2.16.1/operator.yaml
```

```shell
helm upgrade elastic-operator elastic/eck-operator -n elastic-system
```

This will update the ECK installation to the latest binary and update the CRDs and other ECK resources in the cluster.


## Control rolling restarts during the upgrade [k8s-beta-to-ga-rolling-restart]

Upgrading the operator results in a one-time update to existing managed resources in the cluster. This potentially triggers a rolling restart of pods by Kubernetes to apply those changes. The following list contains the ECK operator versions that would cause a rolling restart after they have been installed.

```
1.6, 1.9, 2.0, 2.1, 2.2, 2.4, 2.5, 2.6, 2.7, 2.8, 2.14
```
::::{note}
Stepping over one of these versions, for example, upgrading ECK from 2.6 to 2.9, still triggers a rolling restart.
::::


If you have a very large Elasticsearch cluster or multiple Elastic Stack deployments, this rolling restart might be disruptive or inconvenient. To have more control over when the pods belonging to a particular deployment should be restarted, you can [add an annotation](../../../troubleshoot/deployments/cloud-on-k8s/troubleshooting-methods.md#k8s-exclude-resource) to the corresponding resources to temporarily exclude them from being managed by the operator. When the time is convenient, you can remove the annotation and let the rolling restart go through.

::::{warning}
Once a resource is excluded from being managed by ECK, you will not be able to add/remove nodes, upgrade Stack version, or perform other [orchestration tasks](../../deploy/cloud-on-k8s/configure-deployments.md) by updating the resource manifest. You must remember to remove the exclusion to ensure that your Elastic Stack deployment is continually monitored and managed by the operator.
::::


```shell
ANNOTATION='eck.k8s.elastic.co/managed=false'

# Exclude a single Elasticsearch resource named "quickstart"
kubectl annotate --overwrite elasticsearch quickstart $ANNOTATION

# Exclude all resources in the current namespace
kubectl annotate --overwrite elastic --all $ANNOTATION

# Exclude all resources in all of the namespaces:
for NS in $(kubectl get ns -o=custom-columns='NAME:.metadata.name' --no-headers); do kubectl annotate --overwrite elastic --all $ANNOTATION -n $NS; done
```

Once the operator has been upgraded and you are ready to let the resource become managed again (triggering a rolling restart of pods in the process), remove the annotation.

```shell
RM_ANNOTATION='eck.k8s.elastic.co/managed-'

# Resume management of a single Elasticsearch cluster named "quickstart"
kubectl annotate elasticsearch quickstart $RM_ANNOTATION
```

::::{note}
The ECK source repository contains a [shell script](https://github.com/elastic/cloud-on-k8s/tree/2.16/hack/annotator) to assist with mass addition/deletion of annotations.
::::
