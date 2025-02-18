---
navigation_title: Air gapped environments
applies:
  eck: all
mapped_urls:
  - https://www.elastic.co/guide/en/elastic-stack/current/air-gapped-install.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-air-gapped.html
---

# Air gapped install

% What needs to be done: Refine

% GitHub issue: https://github.com/elastic/docs-projects/issues/309

% Scope notes: Curate and merget the content to have a proper guide for air gapped installations. Similar to ECE activity

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/stack-docs/elastic-stack/air-gapped-install.md

% already removed
% - [ ] ./raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-air-gapped.md

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):

$$$air-gapped-install$$$

$$$k8s-container-registry-override$$$

$$$k8s-eck-diag-air-gapped$$$

% There are two concepts and areas to explore here:
% ECK installation on air-gapped. This has no complexity as it's all a matter of docker registry and docker images.
% Managing deployments on an ECK running on air-gapped is something not really covered in the official ECK book and partly covered in stack-docs

% In this doc we will focus on ECK operator installation in air gapped environments, and we will link to Manage Deployments -> Air gapped (doesn't exist yet) for the content and examples about the rest.

% from fleet air-gapped
% Kibana is able to reach the Elastic Package Registry to download package metadata and content.
% Elastic Agents are able to download binaries during upgrades from the Elastic Artifact Registry.

% what about Elasticsearch requirements for example for GeoIP database, etc?

Pending to determine what to do with this:
* Syncing container images for ECK and all other {{stack}} components over to a locally-accessible container repository.
* Modifying the ECK helm chart configuration so that ECK is aware that it is supposed to use your offline container repository instead of the public Elastic repository.
* Optionally, disabling ECK telemetry collection in the ECK helm chart. This configuration propagates to all other Elastic components, such as {{kib}}.
* Building your custom deployment container image for the {{artifact-registry}}.
* Building your custom deployment container image for the Elastic Endpoint Artifact Repository.

# Running in air-gapped environments [k8s-air-gapped]

The ECK operator can be run in an air-gapped environment without access to the open internet when it is configured not to pull container images from `docker.elastic.co`.

By default ECK does not require you to specify the container image for each Elastic Stack application you deploy.

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: 8.16.1
  # image: docker.elastic.co/elasticsearch/elasticsearch:8.16.1 <1>
  nodeSets:
  - name: default
    count: 1
  # podTemplate:
  #   spec:
  #     imagePullSecrets: <2>
  #     - name: private-registry-credentials-secret
```

1. The ECK operator will set this value by default. You can explicitly set it to your mirrored container image when running in an air-gapped environment
2. You can provide credentials to your private container registry by setting the `imagePullSecrets` field through the `spec.podTemplate` section of your Elastic resource specification, check [how to customize the Elastic resources Pods](../../../deploy-manage/deploy/cloud-on-k8s/customize-pods.md) and [how to setup a Secret containing your registry credentials](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/).


ECK will automatically set the correct container image for each application. When running in an air-gapped or offline environment you will have to mirror the official Elastic container images in a private container image registry. To make use of your mirrored images you can either set the image for each application explicitly as shown in the preceding example or more conveniently override the default container registry as explained in the next section.


## Use a mirrored image of the ECK operator [k8s-use-mirrored-operator-image]

To deploy the ECK operator in an air-gapped environment, you first have to mirror the operator image itself from `docker.elastic.co` to a private container registry, for example `my.registry`.

Once the ECK operator image is copied internally, replace the original image name `docker.elastic.co/eck/eck-operator:2.16.1` with the private name of the image, for example `my.registry/eck/eck-operator:2.16.1`, in the [operator manifests](../../../deploy-manage/deploy/cloud-on-k8s/install-using-yaml-manifest-quickstart.md). When using [Helm charts](../../../deploy-manage/deploy/cloud-on-k8s/install-using-helm-chart.md), replace the `image.repository` Helm value with, for example, `my.registry/eck/eck-operator`.


## Override the default container registry [k8s-container-registry-override]

When creating custom resources (Elasticsearch, Kibana, APM Server, Beats, Elastic Agent, Elastic Maps Server, and Logstash), the operator defaults to using container images pulled from the `docker.elastic.co` registry. If you are in an environment where external network access is restricted, you can configure the operator to use a different default container registry by starting the operator with the `--container-registry` command-line flag. Check [*Configure ECK*](../../../deploy-manage/deploy/cloud-on-k8s/configure-eck.md) for more information on how to configure the operator using command-line flags and environment variables.

The operator expects container images to be located at specific repositories in the default container registry. Make sure that your container images are stored in the right repositories and are tagged correctly with the Stack version number. For example, if your private registry is `my.registry` and you wish to deploy components from Stack version 8.16.1, the following image names should exist:

* `my.registry/elasticsearch/elasticsearch:8.16.1`
* `my.registry/kibana/kibana:8.16.1`
* `my.registry/apm/apm-server:8.16.1`


## Use a global container repository [k8s-container-repository-override]

If you cannot follow the default Elastic image repositories naming scheme, you can configure the operator to use a different container repository by starting the operator with the `--container-repository` command-line flag. Check [*Configure ECK*](../../../deploy-manage/deploy/cloud-on-k8s/configure-eck.md) for more information on how to configure the operator using command-line flags and environment variables.

For example, if your private registry is `my.registry` and all Elastic images are located under the `elastic` repository, the following image names should exist:

* `my.registry/elastic/elasticsearch:8.16.1`
* `my.registry/elastic/kibana:8.16.1`
* `my.registry/elastic/apm-server:8.16.1`


## ECK Diagnostics in air-gapped environments [k8s-eck-diag-air-gapped]

The [eck-diagnostics tool](../../../troubleshoot/deployments/cloud-on-k8s/run-eck-diagnostics.md) optionally runs diagnostics for Elastic Stack applications in a separate container that is deployed into the Kubernetes cluster.

In air-gapped environments with no access to the `docker.elastic.co` registry, you should copy the latest support-diagnostics container image to your internal image registry and then run the tool with the additional flag `--diagnostic-image <custom-support-diagnostics-image-name>`. To find out which support diagnostics container image matches your version of eck-diagnostics run the tool once without arguments and it will print the default image in use.


% FROM THE OTHER CONTENT (ELASTIC-STACK):

### 2. Kubernetes & OpenShift Install [air-gapped-kubernetes-and-openshift]

Setting up air-gapped Kubernetes or OpenShift installs of the {{stack}} has some unique concerns, but the general dependencies are the same as in the self-managed install case on a regular Linux machine.


#### 2.1. Elastic Kubernetes Operator (ECK) [air-gapped-k8s-os-elastic-kubernetes-operator]

The Elastic Kubernetes operator is an additional component in the Kubernetes OpenShift install that, essentially, does a lot of the work in installing, configuring, and updating deployments of the {{stack}}. For details, refer to the [{{eck}} install instructions](../../../deploy-manage/deploy/cloud-on-k8s/air-gapped-install.md).

The main requirements are:

* Syncing container images for ECK and all other {{stack}} components over to a locally-accessible container repository.
* Modifying the ECK helm chart configuration so that ECK is aware that it is supposed to use your offline container repository instead of the public Elastic repository.
* Optionally, disabling ECK telemetry collection in the ECK helm chart. This configuration propagates to all other Elastic components, such as {{kib}}.
* Building your custom deployment container image for the {{artifact-registry}}.
* Building your custom deployment container image for the Elastic Endpoint Artifact Repository.


#### 2.2. Elastic Package Registry [air-gapped-k8s-os-elastic-package-registry]

The container image can be downloaded from the official Elastic Docker repository, as described in the {{fleet}} and {{elastic-agent}} [air-gapped environments](https://www.elastic.co/guide/en/fleet/current/air-gapped.html) documentation.

This container would, ideally, run as a Kubernetes deployment. Refer to [Appendix C - EPR Kubernetes Deployment](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-epr-kubernetes-example) for examples.


#### 2.3. {{artifact-registry}} [air-gapped-k8s-os-elastic-artifact-registry]

A custom container would need to be created following similar instructions to setting up a web server in the [self-managed install case](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-artifact-registry). For example, a container file using an NGINX base image could be used to run a build similar to the example described in [Appendix B - {{artifact-registry}}](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-artifact-registry-example).


#### 2.4. Elastic Endpoint Artifact Repository [air-gapped-k8s-os-elastic-endpoint-artifact-repository]

Just like the {{artifact-registry}}. A custom container needs to be created following similar instructions to setting up a web server for the [self-managed install case](../../../deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-artifact-registry).


#### 2.5. Ironbank Secure Images for Elastic [air-gapped-k8s-os-ironbank-secure-images]

Besides the public [Elastic container repository](https://www.docker.elastic.co), most {{stack}} container images are also available in Platform One’s [Iron Bank](https://ironbank.dso.mil/repomap?vendorFilters=Elastic&page=1&sort=1).



