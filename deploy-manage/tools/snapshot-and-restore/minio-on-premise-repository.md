---
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configuring-minio.html
applies_to:
  deployment:
    ece: 
---

# Minio on-premise repository [ece-configuring-minio]

Minio is a popular, open-source distributed object storage server compatible with the Amazon AWS S3 API. You can use it with Elastic Cloud Enterprise installations when you want to store your Elasticsearch snapshots locally.


## Create a test environment [ece-minio-test]

We recommend following the [Minio Quickstart Guide Docker Container instructions](https://docs.minio.io/docs/minio-docker-quickstart-guide) to create a simple Minio standalone installation for your initial evaluation and development.

Be sure to use the `docker -v` option to map persistent storage to the container.


## Production environment prerequisites [ece-minio-requirements]

Installing Minio for production requires a high-availability configuration where Minio is running in [Distributed mode](https://docs.minio.io/docs/distributed-minio-quickstart-guide).

As mentioned in the Minio documentation, you will need to have 4-16 Minio drive mounts. There is no hard limit on the number of Minio nodes. It might be convenient to place the Minio node containers on your ECE hosts to ensure you have a suitable level of availability, but those can not be located on the same hosts as ECE proxies since they both listen on the same port.

The following illustration is a sample architecture for a [large ECE installation](../../deploy/cloud-enterprise/deploy-large-installation-onprem.md). Note that there is at least one MinIO container in *each* availability zone.

There are a number of different ways of orchestrating the Minio deployment (Docker Compose, Kubernetes, and so on). We suggest you use the method most familiar to you.

We recommend:

* Using a single Minio endpoint with the Elastic Cloud Enterprise installation, to simplify repository management.
* Securing access to the Minio endpoint with TLS.

:::{image} ../../../images/cloud-enterprise-ece-minio-large-arch.png
:alt: Architecture diagram
:name: img-ece-minio-large-arch
:::


## Create an offline installation [ece-minio-offline-installation]

If you are installing MinIO offline, the process is very similar to the [offline installation of Elastic Cloud Enterprise](../../deploy/cloud-enterprise/air-gapped-install.md). There are two options:

* Use a private Docker repository and [install the Minio images in the private repository](https://docs.docker.com/registry/deploying/).
* Download the Minio images from an internet-connected machine, then use docker save to bundle the images into tar files. Copy the TAR files to the target hosts and use `docker load` to install.

Gather the following after your installation:

* Minio AccessKey
* Minio SecretKey
* Endpoint URL

::::{tip}
Minio might report various Endpoint URLs, be sure to choose the one that will be routable from your Elasticsearch Docker containers.
::::



## Create the S3 bucket [ece-minio-create-s3-bucket]

How you create the AWS S3 bucket depends on what version of Elasticsearch you are using:

* For version 7.x:

    1. Using the Minio browser or an S3 client application, create an S3 bucket to store your snapshots.
    2. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md) and [add the S3 repository plugin](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch-plugins/cloud-enterprise/ece-add-plugins.md) to your cluster.

* For versions 8.0 and later, {{es}} has built-in support for AWS S3 repositories; no repository plugin is needed. Use the Minio browser or an S3 client application to create an S3 bucket to store your snapshots.

::::{tip}
Don’t forget to make the bucket name DNS-friendly, for example no underscores or uppercase letters. For more details, read the [bucket restrictions](https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.md).
::::



## Elastic Cloud Enterprise configuration [ece-install-with-minio]

You can configure existing deployments, or create new ones, with the following changes to use Minio storage.


### Add the repository to Elastic Cloud Enterprise [ece-add-repository]

You must add the new repository to Elastic Cloud Enterprise before it can be used with your Elasticsearch clusters.

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
             "access_key": "<your Minio AccessKey>",
             "secret_key": "<your Minio SecretKey>",
             "endpoint": "<your Minio endpoint URL>:9000",
             "path_style_access": "true",
             "protocol": "http"
          }
      }
    ```

    :::{image} ../../../images/cloud-enterprise-ece-minio-repository.png
    :alt: Create form
    :name: img-ece-minio-repository
    :::

6. Select **Save** to submit your configuration.

The Minio repository is now available from the drop-down list of repositories when creating deployments.

:::{image} ../../../images/cloud-enterprise-ece-minio-deployment.png
:alt: Create deployment
:name: img-ece-minio-deployment
:::


### Additional settings for 6.x clusters [ece-6.x-settings]

For Elasticsearch versions 6.0 and later, after selecting the repository, you also need to set your **User Settings** YAML to specify the endpoint and protocol. For example:

```
s3.client.default.endpoint: "<your Minio endpoint>:9000"
s3.client.default.protocol: http
```
Check the [Elasticsearch S3 plugin details](https://www.elastic.co/guide/en/elasticsearch/plugins/6.8/repository-s3-client.html) for more information.


## Upgrade from 5.x to 6.x Elasticsearch clusters [ece-upgrade-minio]

The configuration options for the Elasticsearch S3 repository plugin have changed from 5.x to 6.x versions and you must copy the endpoint and protocol values from your repository configuration to your **User Settings** YAML before you upgrade.


## Verify snapshots [ece-minio-verify-snapshot]

The cluster should make a snapshot when the repository is set up. You can check that by going to the **Elasticsearch** and then the **Snapshots** page.

As an extra verification step, you can restore a cluster using the snapshots that have been taken.

1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. Get the plan from your test cluster.

    1. From the **Deployments** page, select your deployment.

        Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

    2. From your deployment menu, go to the **Edit** page then go to the bottom of the page and select **advanced Elasticsearch configuration**.
    3. Copy the JSON format under the **Deployment configuration** heading.

3. Create a new Elasticsearch cluster as your target.
4. On the new cluster, open the advanced cluster configuration editor. In the transient section, add the `restore_snapshot` settings to the plan.

    ```json
      ...
      "transient": {
           "restore_snapshot": {
              "repository_name": "<Minio repository name>",
              "snapshot_name": "latest_success"
           }
      }
    ```

5. Select **Save** to restore from the snapshot. When the plan update is complete, you can check the restored indexes in your target cluster.

More details are available to [work with snapshots](../snapshot-and-restore.md).

