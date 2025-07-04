---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configuring-minio.html
applies_to:
  deployment:
    ece:
products:
  - id: cloud-enterprise
---

# MinIO self-managed repository [ece-configuring-minio]

[MinIO](https://min.io/docs/minio/container/index.html) is a popular, open-source object storage server compatible with the Amazon AWS S3 API. As an [S3 compatible service](/deploy-manage/tools/snapshot-and-restore/s3-repository.md#repository-s3-compatible-services), MinIO is supported for use as a snapshot repository in {{ece}} (ECE).

This guide walks you through integrating MinIO with ECE to store your {{es}} snapshots.

## Deploy MinIO

This section provides guidance and recommendations for deploying MinIO. It does not include detailed installation steps, as MinIO is a third-party product. For full installation instructions, refer to the official [MinIO documentation](https://min.io/docs/).

### Create a test environment [ece-minio-test]

We recommend following either the [MinIO Quickstart Guide](https://charts.min.io/) or the [MinIO for containers guide](https://min.io/docs/minio/container/index.html) to create a simple MinIO standalone installation for your initial evaluation and development.

Be sure to use the `docker` or `podman` `-v` option to map persistent storage to the container.

### Production environment prerequisites [ece-minio-requirements]

Installing MinIO for production requires a high-availability configuration where MinIO is running in [Distributed mode](https://min.io/docs/minio/linux/operations/install-deploy-manage/deploy-minio-multi-node-multi-drive.html#minio-mnmd).

As mentioned in the MinIO documentation, you will need to have 4-16 MinIO drive mounts. There is no hard limit on the number of MinIO nodes. It might be convenient to place the MinIO node containers on your ECE hosts to ensure you have a suitable level of availability, but those cannot be located on the same hosts as ECE proxies since they both listen on the same port.

::::{note}
Although you can run MinIO containers in your ECE allocator hosts, we recommend deploying MinIO in separate hosts.
::::

The following illustration is a sample architecture for a [large ECE installation](../../deploy/cloud-enterprise/deploy-large-installation.md). Note that there is at least one MinIO container in *each* availability zone.

:::{image} /deploy-manage/images/cloud-enterprise-ece-minio-large-arch.png
:alt: Architecture diagram
:name: img-ece-minio-large-arch
:::

There are a number of different ways of orchestrating the MinIO deployment (Docker Compose, Kubernetes, and so on). We suggest you use the method most familiar to you.

We recommend:

* Using a single MinIO endpoint with the {{ece}} installation, to simplify repository management.
* Securing access to the MinIO endpoint with TLS.

### Air-gapped installations [ece-minio-offline-installation]

If you are installing MinIO offline, the process is very similar to the [offline installation of {{ece}}](../../deploy/cloud-enterprise/air-gapped-install.md). There are two options:

* Use a private Docker repository and [install the MinIO images in the private repository](https://docs.docker.com/registry/deploying/).
* Download the MinIO images from an internet-connected machine, then use docker save to bundle the images into tar files. Copy the TAR files to the target hosts and use `docker load` to install.

Gather the following after your installation:

* MinIO AccessKey
* MinIO SecretKey
* Endpoint URL

::::{tip}
MinIO might report various Endpoint URLs, be sure to choose the one that will be routable from your {{es}} Docker containers.
::::

## Create the S3 bucket [ece-minio-create-s3-bucket]

After installing MinIO you will need to create a bucket to store your deployments' snapshots. Use the MinIO browser or an S3 client application to create an S3 bucket to store your snapshots.

::::{tip}
Don’t forget to make the bucket name DNS-friendly, for example no underscores or uppercase letters. For more details, read the [bucket restrictions](https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html).
::::

## {{ece}} configuration [ece-install-with-minio]

This section describes the configuration changes required to use MinIO storage within ECE to make periodic snapshots of your {{es}} deployments. The required steps include:

* Configuring the repository at ECE level
* Associating it with your deployments
* Applying specific YAML settings to the deployments

### Add the repository to {{ece}} [ece-add-repository]

You must add the new repository at ECE platform level before it can be used by your {{es}} deployments.

1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Repositories**.
3. Select **Add Repository**.
4. From the **Repository Type** drop-down list, select **Advanced**.
5. In the **Configuration** text area, provide the repository JSON. You must specify the bucket, access_key, secret_key, endpoint, and protocol.

    ```json
      {
         "type": "s3",
          "settings": {
             "bucket": "ece-backup",
             "access_key": "<your MinIO AccessKey>",
             "secret_key": "<your MinIO SecretKey>",
             "endpoint": "<your MinIO endpoint URL>:9000",
             "path_style_access": "true",
             "protocol": "http"
          }
      }
    ```

6. Select **Save** to submit your configuration.

### Associate repository with deployments

Once the MinIO repository is created at the ECE platform level, you can associate it with your {{es}} deployments in two ways:

* For new deployments, select the repository from the **Snapshot repository** drop-down list while [creating the deployment](/deploy-manage/deploy/cloud-enterprise/create-deployment.md).

* For existing deployments, associate the repository by following the instructions in [Manage {{es}} clusters repositories](/deploy-manage/tools/snapshot-and-restore/cloud-enterprise.md#ece-manage-repositories-clusters).

### Additional settings for {{es}} [ece-6.x-settings]

After selecting the repository, you also need to configure your [{{es}} user settings YAML](/deploy-manage/deploy/cloud-enterprise/edit-stack-settings-elasticsearch.md) to specify the endpoint and protocol. For example:

```
s3.client.default.endpoint: "<your MinIO endpoint>:9000"
s3.client.default.protocol: http
```

Refer to the [{{es}} S3 plugin details](/deploy-manage/tools/snapshot-and-restore/s3-repository.md) for more information.

#### Add S3 repository plugin (only for {{es}} 7.x)

For {{es}} clusters in version 7.x you must add the S3 repository plugin to your cluster. Refer to [Managing plugins for ECE](elasticsearch://reference/elasticsearch-plugins/plugin-management.md#managing-plugins-for-ece) for more details.

::::{note}
For versions 8.0 and later, {{es}} has built-in support for AWS S3 repositories; no repository plugin is needed.
::::

## Verify snapshots [ece-minio-verify-snapshot]

The cluster should make periodic snapshots when the repository is set up and associated to it. You can check this in the **Elasticsearch > Snapshots** section of the deployment page in the [Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).

As an extra verification step, you can [restore snapshots across clusters](/deploy-manage/tools/snapshot-and-restore/ece-restore-across-clusters.md).

Refer to [work with snapshots](../snapshot-and-restore.md) for more information around {{es}} snapshot and restore.