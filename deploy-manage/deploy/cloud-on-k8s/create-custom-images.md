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

You can create your own custom application images ({{eck_resources_list}}) instead of using the base images provided by Elastic. You might want to do this to have a canonical image with all the necessary plugins pre-loaded rather than [installing them through an init container](init-containers-for-plugin-downloads.md) each time a Pod starts.  You must use the official image as the base for custom images. For example, if you want to create an {{es}} {{version.stack}} image with the [ICU Analysis Plugin](elasticsearch://reference/elasticsearch-plugins/analysis-icu.md), you can do the following:

1. Create a `Dockerfile` containing:

    ```sh subs=true
    FROM docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}}
    RUN bin/elasticsearch-plugin install --batch analysis-icu
    ```

2. Build the image with:

    ```sh subs=true
    docker build --tag elasticsearch-icu:{{version.stack}}
    ```


There are various hosting options for your images. If you use Google Kubernetes Engine, it is automatically configured to use the Google Container Registry. Check [Using Container Registry with Google Cloud](https://cloud.google.com/container-registry/docs/using-with-google-cloud-platform#google-kubernetes-engine) for more information. To use the image, you can then [push to the registry](https://cloud.google.com/container-registry/docs/pushing-and-pulling#pushing_an_image_to_a_registry) with:

```sh subs=true
docker tag elasticsearch-icu:{{version.stack}} gcr.io/$PROJECT-ID/elasticsearch-icu:{{version.stack}}
docker push gcr.io/$PROJECT-ID/elasticsearch-icu:{{version.stack}}
```

Configure your {{es}} specification to use the newly pushed image, for example:

```yaml subs=true
spec:
  version: {{version.stack}}
  image: gcr.io/$PROJECT-ID/elasticsearch-icu:{{version.stack}}
```

::::{note}
Providing the correct version is always required as ECK reasons about APIs and capabilities available to it based on the version field.
::::


The steps are similar for [Azure Kubernetes Service](https://docs.microsoft.com/en-us/azure/aks/tutorial-kubernetes-prepare-acr) and [AWS Elastic Container Registry](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-basics.html#use-ecr).

If your custom images follow the naming convention adopted by the official images, and you only want to use your custom images, you can also simply [override the container registry](air-gapped-install.md#k8s-container-registry-override).

For more information, check the following references:

* [{{es}} documentation on Using custom Docker images](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-configure.md#_c_customized_image)
* [Google Container Registry](https://cloud.google.com/container-registry/docs/how-to)
* [Azure Container Registry](https://docs.microsoft.com/en-us/azure/container-registry/)
* [Amazon Elastic Container Registry](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)
* [OpenShift Container Platform registry](https://docs.openshift.com/container-platform/4.12/registry/index.html)

