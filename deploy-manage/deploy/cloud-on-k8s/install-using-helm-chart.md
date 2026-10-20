---
navigation_title: Helm chart
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-install-helm.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Install ECK using a Helm chart [k8s-install-helm]

You can install ECK using a Helm chart from the following sources:

* The Elastic Helm repository
* {applies_to}`eck: ga 3.6+` The {{container-registry}}

::::::{tab-set}
:group: eck-helm-source

::::{tab-item} Helm repository
:sync: helm-repository

Starting from ECK 1.3.0, the chart is available from the Elastic Helm repository. Add the repository to your Helm repository list:

```sh
helm repo add elastic https://helm.elastic.co
helm repo update
```

:::{note}
The minimum supported version of Helm for this method is {{eck_helm_minimum_version}}.
:::

::::

::::{tab-item} Elastic Container Registry
:sync: oci-registry

{applies_to}`eck: ga 3.6+`

The chart is available as an Open Container Initiative (OCI) artifact in the {{container-registry}} at `docker.elastic.co/eck-charts`.

To use this type of artifact, you do not add a Helm repository. Instead, refer to each chart with an `oci://` URL, as the examples on this page show.

You must specify the chart version with the `--version` option. For the `eck-operator` and `eck-operator-crds` charts, the chart version is the ECK version.

:::{note}
The minimum supported version of Helm for this method is {{eck_helm_oci_minimum_version}}.
:::

::::

::::::

## Installation options

The Elastic Operator Helm chart supports two main installation methods:

* Cluster-wide (global) installation – Installs both the operator and all its Custom Resource Definitions (CRDs) in a single step.
* Restricted installation – Separates the installation of the CRDs from the operator, allowing multiple operator instances to coexist in the same cluster while managing different sets of namespaces.

A restricted installation is required if you plan to run multiple operators in the same cluster or if the operator cannot have cluster-wide permissions.

### Cluster-wide (global) installation [k8s-install-helm-global]

This is the default mode of installation and is equivalent to [installing ECK using the stand-alone YAML manifests](./install-using-yaml-manifest-quickstart.md).

::::{tab-set}
:group: eck-helm-source

:::{tab-item} Helm repository
:sync: helm-repository

```sh
helm install elastic-operator elastic/eck-operator -n elastic-system --create-namespace
```

:::

:::{tab-item} Elastic Container Registry
:sync: oci-registry

```sh subs=true
helm install elastic-operator oci://docker.elastic.co/eck-charts/eck-operator --version {{version.eck}} -n elastic-system --create-namespace
```

:::

::::

### Restricted installation [k8s-install-helm-restricted]

This mode avoids installing any cluster-scoped resources and restricts the operator to manage only a set of pre-defined namespaces.

Since CRDs are global resources, they still need to be installed by an administrator. This can be achieved by:

::::{tab-set}
:group: eck-helm-source

:::{tab-item} Helm repository
:sync: helm-repository

```sh
helm install elastic-operator-crds elastic/eck-operator-crds
```

:::

:::{tab-item} Elastic Container Registry
:sync: oci-registry

```sh subs=true
helm install elastic-operator-crds oci://docker.elastic.co/eck-charts/eck-operator-crds --version {{version.eck}}
```

:::

::::

The operator can be installed by any user who has full access to the set of namespaces they wish to manage. The following example installs the operator to `elastic-system` namespace and configures it to manage only `namespace-a` and `namespace-b`:

::::{tab-set}
:group: eck-helm-source

:::{tab-item} Helm repository
:sync: helm-repository

```sh
helm install elastic-operator elastic/eck-operator -n elastic-system --create-namespace \
  --set=installCRDs=false \
  --set=managedNamespaces='{namespace-a, namespace-b}' \
  --set=createClusterScopedResources=false \
  --set=webhook.enabled=false \
  --set=config.validateStorageClass=false
```

:::

:::{tab-item} Elastic Container Registry
:sync: oci-registry

```sh subs=true
helm install elastic-operator oci://docker.elastic.co/eck-charts/eck-operator --version {{version.eck}} -n elastic-system --create-namespace \
  --set=installCRDs=false \
  --set=managedNamespaces='{namespace-a, namespace-b}' \
  --set=createClusterScopedResources=false \
  --set=webhook.enabled=false \
  --set=config.validateStorageClass=false
```

:::

::::

The previous example disabled the validation webhook along with all other cluster-wide resources. If you need to enable the validation webhook in a restricted environment, see [](./webhook-namespace-selectors.md). To understand what the validation webhook does, refer to [](./configure-validating-webhook.md).

::::{tip}
:applies_to: eck: ga 3.5

Instead of a static list of namespaces, the operator can also select the namespaces to manage dynamically, based on their labels. Refer to [](./dynamic-namespace-handling.md) for details. Note that this feature requires cluster-wide permissions and is therefore not compatible with the restricted installation mode.
::::

#### Using a profile file [k8s-install-helm-profiles]

As an alternative to setting each `--set` option manually, you can install the operator with a pre-defined profile from the `eck-operator` chart. A profile is a values file that sets all the options for a specific installation type. Profile files are in the root of the chart directory and are prefixed with `profile-`. For example, the restricted configuration from the previous example is defined in the `profile-restricted.yaml` file, and can be used as follows:

::::{tab-set}
:group: eck-helm-source

:::{tab-item} Helm repository
:sync: helm-repository

To get the profile files, download and extract the chart with the `helm pull` command. The command extracts the chart to the `eck-operator` directory. You can also find the profile files in the Helm cache directory or in the [ECK source repository](https://github.com/elastic/cloud-on-k8s/tree/{{version.eck | M.M}}/deploy/eck-operator).

```sh
helm pull elastic/eck-operator --untar
helm install elastic-operator elastic/eck-operator -n elastic-system --create-namespace \
  --values="eck-operator/profile-restricted.yaml" \
  --set=managedNamespaces='{namespace-a, namespace-b}'
```

:::

:::{tab-item} Elastic Container Registry
:sync: oci-registry

To get the profile files, download and extract the chart with the `helm pull` command. The command extracts the chart to the `eck-operator` directory. You can also find the profile files in the [ECK source repository](https://github.com/elastic/cloud-on-k8s/tree/{{version.eck | M.M}}/deploy/eck-operator).

```sh subs=true
helm pull oci://docker.elastic.co/eck-charts/eck-operator --version {{version.eck}} --untar
helm install elastic-operator oci://docker.elastic.co/eck-charts/eck-operator --version {{version.eck}} -n elastic-system --create-namespace \
  --values="eck-operator/profile-restricted.yaml" \
  --set=managedNamespaces='{namespace-a, namespace-b}'
```

:::

::::

## View available configuration options [k8s-install-helm-show-values]

You can view all configurable values of the operator Helm chart by running the following:

::::{tab-set}
:group: eck-helm-source

:::{tab-item} Helm repository
:sync: helm-repository

```sh
helm show values elastic/eck-operator
```

:::

:::{tab-item} Elastic Container Registry
:sync: oci-registry

```sh subs=true
helm show values oci://docker.elastic.co/eck-charts/eck-operator --version {{version.eck}}
```

:::

::::

## Migrate an existing installation to Helm [k8s-migrate-to-helm]

::::{warning}
Migrating an existing installation to Helm is essentially an upgrade operation and any [caveats associated with normal operator upgrades](../../upgrade/orchestrator/upgrade-cloud-on-k8s.md#k8s-beta-to-ga-rolling-restart) are applicable. Check the [upgrade documentation](../../upgrade/orchestrator/upgrade-cloud-on-k8s.md#k8s-ga-upgrade) before proceeding.
::::

You can migrate an existing operator installation to Helm by adding the `meta.helm.sh/release-name`, `meta.helm.sh/release-namespace` annotations and the `app.kubernetes.io/managed-by` label to all the resources you want to be adopted by Helm. You *must* do this for the Elastic Custom Resource Definitions (CRD) because deleting them would trigger the deletion of all deployed Elastic applications as well. All other resources are optional and can be deleted.

::::{note}
A shell script is available in the [ECK source repository](https://github.com/elastic/cloud-on-k8s/blob/{{version.eck | M.M}}/deploy/helm-migrate.sh) to demonstrate how to migrate from version 1.7.1 to Helm. You can modify it to suit your own environment.
::::

For example, an ECK 1.2.1 installation deployed using [YAML manifests](/deploy-manage/deploy/cloud-on-k8s/install-using-yaml-manifest-quickstart.md) can be migrated to Helm as follows:

1. Annotate and label all the ECK CRDs with the appropriate Helm annotations and labels. CRDs need to be preserved to retain any existing Elastic applications deployed using the operator.

    ```sh
    for CRD in $(kubectl get crds --no-headers -o custom-columns=NAME:.metadata.name | grep k8s.elastic.co); do
        kubectl annotate crd "$CRD" meta.helm.sh/release-name="$RELEASE_NAME"
        kubectl annotate crd "$CRD" meta.helm.sh/release-namespace="$RELEASE_NAMESPACE"
        kubectl label crd "$CRD" app.kubernetes.io/managed-by=Helm
    done
    ```

2. Uninstall the current ECK operator. You can do this by taking the `operator.yaml` file you used to install the operator and running `kubectl delete -f operator.yaml`. Alternatively, you could delete each resource individually.

    ```sh
    kubectl delete -n elastic-system \
        serviceaccount/elastic-operator \
        secret/elastic-webhook-server-cert \
        clusterrole.rbac.authorization.k8s.io/elastic-operator \
        clusterrole.rbac.authorization.k8s.io/elastic-operator-view \
        clusterrole.rbac.authorization.k8s.io/elastic-operator-edit \
        clusterrolebinding.rbac.authorization.k8s.io/elastic-operator \
        service/elastic-webhook-server \
        configmap/elastic-operator \ <1>
        statefulset.apps/elastic-operator \
        validatingwebhookconfiguration.admissionregistration.k8s.io/elastic-webhook.k8s.elastic.co
    ```

    1. If you have previously customized the operator configuration in this ConfigMap, you will have to repeat the configuration once the operator has been reinstalled in the next step.

3. Install the ECK operator using the Helm chart as described in [Install ECK using the Helm chart](./install-using-helm-chart.md).

## Next steps

* For ECK configuration settings, refer to [](/deploy-manage/deploy/cloud-on-k8s/configure.md).
* To continue with the installation of {{es}} and {{kib}} go to [](/deploy-manage/deploy/cloud-on-k8s/manage-deployments.md).
