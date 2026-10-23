---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-custom-images.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Create custom images [k8s-custom-images]

You can create your own custom application images ({{eck_resources_list}}) instead of using the base images provided by Elastic. You might want to do this to have a canonical image with all the necessary plugins pre-loaded rather than [installing them through an init container](/deploy-manage/plugins-and-custom-configuration-files/cloud-on-k8s/init-containers-for-plugin-downloads.md) each time a Pod starts.  You must use the official image as the base for custom images. For example, if you want to create an {{es}} {{version.stack}} image with the [ICU Analysis Plugin](elasticsearch://reference/elasticsearch-plugins/analysis-icu.md), you can do the following:

1. Create a `Dockerfile` containing:

    ```sh subs=true
    FROM docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}}
    RUN bin/elasticsearch-plugin install --batch analysis-icu
    ```

2. Build the image with:

    ```sh subs=true
    docker build --tag elasticsearch-icu:{{version.stack}} .
    ```


There are various hosting options for your images. If you use Google Kubernetes Engine, you can store your custom images in [Artifact Registry](https://cloud.google.com/artifact-registry/docs/overview). Before you push an image, [create a Docker repository and configure authentication](https://cloud.google.com/artifact-registry/docs/docker/store-docker-container-images). Make sure that your cluster has [permission to pull images from the repository](https://cloud.google.com/artifact-registry/docs/integrate-gke).

```sh subs=true
docker tag elasticsearch-icu:{{version.stack}} ${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/elasticsearch-icu:{{version.stack}}
docker push ${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/elasticsearch-icu:{{version.stack}}
```

Configure your {{es}} specification to use the newly pushed image, for example:

```yaml subs=true
spec:
  version: {{version.stack}}
  image: ${LOCATION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/elasticsearch-icu:{{version.stack}}
```

::::{note}
Providing the correct version is always required as ECK reasons about APIs and capabilities available to it based on the version field.
::::


The steps are similar for [Azure Kubernetes Service](https://docs.microsoft.com/en-us/azure/aks/tutorial-kubernetes-prepare-acr) and [AWS Elastic Container Registry](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-basics.html#use-ecr).

If your custom images follow the naming convention adopted by the official images, and you only want to use your custom images, you can also simply [override the container registry](air-gapped-install.md#k8s-container-registry-override).

For more information, check the following references:

* [{{es}} documentation on building a custom Docker image](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-configure.md#_c_customized_image)
* [Google Artifact Registry](https://cloud.google.com/artifact-registry/docs/overview)
* [Azure Container Registry](https://docs.microsoft.com/en-us/azure/container-registry/)
* [Amazon Elastic Container Registry](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)
* [OpenShift Container Platform registry](https://docs.openshift.com/container-platform/4.12/registry/index.html)

