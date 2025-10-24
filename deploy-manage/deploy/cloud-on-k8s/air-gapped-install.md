---
navigation_title: Air-gapped environments
mapped_pages:
  - https://www.elastic.co/guide/en/elastic-stack/current/air-gapped-install.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-air-gapped.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Running in air-gapped environments [k8s-air-gapped]

The ECK operator can be run in an air-gapped environment without access to the open internet when configured to avoid pulling container images from `docker.elastic.co`.

:::{note}
To deploy ECK in Google Distributed Hosted Cloud refer to [](./eck-gdch.md).
:::

By default ECK does not require you to specify the container image for each {{stack}} application you deploy.

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  # image: docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}} // <1>
  nodeSets:
  - name: default
    count: 1
  # podTemplate:
  #   spec:
  #     imagePullSecrets: // <2>
  #     - name: private-registry-credentials-secret
```

1. The ECK operator will set this value by default. You can explicitly set it to your mirrored container image when running in an air-gapped environment
2. You can provide credentials to your private container registry by setting the `imagePullSecrets` field through the `spec.podTemplate` section of your Elastic resource specification, check [how to customize the Elastic resources Pods](../../../deploy-manage/deploy/cloud-on-k8s/customize-pods.md) and [how to setup a Secret containing your registry credentials](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/).


ECK will automatically set the correct container image for each application. When running in an air-gapped or offline environment you will have to mirror the official Elastic container images in a private container image registry. To make use of your mirrored images you can either set the image for each application explicitly as shown in the preceding example or more conveniently override the default container registry as explained in the next section.


## Use a mirrored image of the ECK operator [k8s-use-mirrored-operator-image]

To deploy the ECK operator in an air-gapped environment, you first have to mirror the operator image itself from `docker.elastic.co` to a private container registry, for example `my.registry`.

Once the ECK operator image is copied internally, replace the original image name with the private name of the image in the [operator manifests](../../../deploy-manage/deploy/cloud-on-k8s/install-using-yaml-manifest-quickstart.md). For example:

Before:
```text subs=true
docker.elastic.co/eck/eck-operator:{{version.eck}}
```

After:
```text subs=true
my.registry/eck/eck-operator:{{version.eck}}
```

When using [Helm charts](../../../deploy-manage/deploy/cloud-on-k8s/install-using-helm-chart.md), replace the `image.repository` Helm value with, for example, `my.registry/eck/eck-operator`.


## Override the default container registry [k8s-container-registry-override]

When creating custom resources ({{eck_resources_list}}), the operator defaults to using container images pulled from the `docker.elastic.co` registry. If you are in an environment where external network access is restricted, you can configure the operator to use a different default container registry by starting the operator with the `--container-registry` command-line flag. Check [*Configure ECK*](../../../deploy-manage/deploy/cloud-on-k8s/configure-eck.md) for more information on how to configure the operator using command-line flags and environment variables.

The operator expects container images to be located at specific repositories in the default container registry. Make sure that your container images are stored in the right repositories and are tagged correctly with the Stack version number. For example, if your private registry is `my.registry` and you wish to deploy components from Stack version {{version.stack}}, the following image names should exist:

* my.registry/elasticsearch/elasticsearch:{{version.stack}}
* my.registry/kibana/kibana:{{version.stack}}
* my.registry/apm/apm-server:{{version.stack}}


## Use a global container repository [k8s-container-repository-override]

If you cannot follow the default Elastic image repositories naming scheme, you can configure the operator to use a different container repository by starting the operator with the `--container-repository` command-line flag. Check [*Configure ECK*](../../../deploy-manage/deploy/cloud-on-k8s/configure-eck.md) for more information on how to configure the operator using command-line flags and environment variables.

For example, if your private registry is `my.registry` and all Elastic images are located under the `elastic` repository, the following image names should exist:

* my.registry/elastic/elasticsearch:{{version.stack}}
* my.registry/elastic/kibana:{{version.stack}}
* my.registry/elastic/apm-server:{{version.stack}}


## ECK Diagnostics in air-gapped environments [k8s-eck-diag-air-gapped]

The [eck-diagnostics tool](../../../troubleshoot/deployments/cloud-on-k8s/run-eck-diagnostics.md) optionally runs diagnostics for {{stack}} applications in a separate container that is deployed into the Kubernetes cluster.

In air-gapped environments with no access to the `docker.elastic.co` registry, you should copy the latest support-diagnostics container image to your internal image registry and then run the tool with the additional flag `--diagnostic-image <custom-support-diagnostics-image-name>`. To find out which support diagnostics container image matches your version of eck-diagnostics, run the tool once without arguments and it will print the default image in use.
