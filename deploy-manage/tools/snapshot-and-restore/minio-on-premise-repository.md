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

::::{important}
Avoid running MinIO directly on ECE hosts. Sharing infrastructure can lead to resource contention, especially disk I/O, and may affect the performance and stability of your Elastic workloads. It also complicates upgrades, troubleshooting, and supportability.

If you're evaluating MinIO in a test system, do not place MinIO containers on the same hosts as ECE proxies, as both services use the same port.
::::

## Deploy MinIO

This section provides guidance and recommendations for deploying MinIO. It does not include installation steps. As MinIO is a third-party product, its deployment, configuration, and maintenance are outside the scope of Elastic support.

For installation instructions, refer to the official [MinIO documentation](https://min.io/docs/).

The performance and reliability of MinIO depend on its configuration and the underlying infrastructure. Consider the following best practices:

* For production use, deploy MinIO in a [Multi-Node Multi-Drive](https://min.io/docs/minio/linux/operations/install-deploy-manage/deploy-minio-multi-node-multi-drive.html#minio-mnmd) configuration.
* Use a single MinIO endpoint with the ECE installation, to simplify repository configuration.
* Secure access to the MinIO endpoint with TLS.

After deployment, make sure you collect the following values:

* MinIO Access Key
* MinIO Secret Key
* MinIO endpoint URL

::::{tip}
MinIO may report multiple endpoint URLs. Be sure to select the one reachable from your {{es}} containers running on ECE allocator hosts.
::::

### Testing and evaluation

Use the [MinIO Quickstart Guide](https://charts.min.io/) or the [container deployment guide](https://min.io/docs/minio/container/index.html) to spin up a simple standalone MinIO container. Use `-v` to map persistent storage when using the `docker` or `podman` options.

### Production environments

Set up MinIO across multiple nodes and drives to ensure high availability, performance, and scalability, following the recommendations in the [MinIO documentation](https://min.io/docs/minio/linux/operations/install-deploy-manage/deploy-minio-multi-node-multi-drive.html).

You can use Docker Compose, Kubernetes, or another orchestration tool of your choice.

## Create the S3 bucket [ece-minio-create-s3-bucket]

After installing MinIO you will need to create a bucket to store your deployments' snapshots. Use the MinIO browser or an S3 client application to create an S3 bucket to store your snapshots.

::::{tip}
Don’t forget to make the bucket name DNS-friendly, for example no underscores or uppercase letters. For more details, read the [bucket restrictions](https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html).
::::

## {{ece}} configuration [ece-install-with-minio]

This section describes the configuration changes required to use MinIO storage within ECE to make periodic snapshots of your deployments. The required steps include:

* Configuring the repository at ECE level
* Associating it with your deployments
* Applying specific YAML settings to the deployments

### Prerequisites

Before integrating ECE with MinIO, ensure you have the following details from your MinIO deployment:

* MinIO Access Key
* MinIO Secret Key
* MinIO endpoint URL
* S3 bucket name

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

For additional considerations on performance, reliability, and troubleshooting when using MinIO as a snapshot repository, refer to [Using MinIO with {{es}}](/deploy-manage/tools/snapshot-and-restore/s3-repository.md#using-minio-with-elasticsearch).
