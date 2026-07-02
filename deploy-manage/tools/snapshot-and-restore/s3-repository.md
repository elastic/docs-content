---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/repository-s3.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
---

# S3 repository [repository-s3]

You can use AWS S3 as a repository for [Snapshot/Restore](../snapshot-and-restore.md).

::::{note}
If you are looking for a hosted solution of {{es}} on AWS, visit [https://www.elastic.co/cloud/](https://www.elastic.co/cloud/).
::::

See [this video](https://www.youtube.com/watch?v=ACqfyzWf-xs) for a walkthrough of connecting an AWS S3 repository.

## Getting started [repository-s3-usage]

To register an S3 repository, specify the type as `s3` when creating the repository. The only mandatory [repository setting](#repository-s3-repository) is the bucket name:

```console
PUT _snapshot/my_s3_repository
{
  "type": "s3",
  "settings": {
    "bucket": "my-bucket"
  }
}
```

[Client settings](#repository-s3-client) describe how repositories select an S3 client and how authentication is configured. The `PUT` request above only specifies the `s3` type and `bucket`, so it implicitly uses the `default` client, which, by default, also attempts to resolve credentials automatically from the environment if no explicit settings are provided. Client configuration is covered in the following section.

## Client settings [repository-s3-client]

{{es}} communicates with S3 through an S3 client. Clients are configured through a combination of [secure settings](/deploy-manage/security/secure-settings.md) in the {{es}} keystore, and [standard settings](/deploy-manage/stack-settings.md) in `elasticsearch.yml`. Settings use the prefix `s3.client.CLIENT_NAME` plus a suffix such as `access_key`. The full set of client settings is listed under [S3 repository client settings](elasticsearch://reference/elasticsearch/configuration-reference/s3-repository-settings.md#repository-s3-client-settings).

You can define several clients, each with its own settings, using the form `s3.client.CLIENT_NAME.SETTING_NAME`. When the environment is compatible, {{es}} also creates a client named `default`, and `s3` repositories use that client unless the repository [setting `client`](#repository-s3-repository) selects another name.

`default` can use automatic credential discovery when available:

* On an EC2 instance, the [EC2 Instance Metadata Service (IMDS)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html) can provide temporary credentials for the [instance IAM role](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html).
* In an Amazon ECS task, {{es}} can use temporary [task IAM role](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html) credentials.
* On Kubernetes, you can use [service account-based authentication](#iam-kubernetes-service-accounts) with the right setup in the node or pod.

If you do not want to rely on automatic credentials discovery, add explicit keys for a client in the [{{es}} keystore](/deploy-manage/security/secure-settings.md). A typical choice for the built-in `default` client is:

* `s3.client.default.access_key`
* `s3.client.default.secret_key`
* `s3.client.default.session_token` (optional)

S3 client settings cover authentication, region and endpoint selection, proxy/network configuration, and connection or retry tuning.
For a complete list of all S3 client settings, refer to [S3 repository client settings](elasticsearch://reference/elasticsearch/configuration-reference/s3-repository-settings.md#repository-s3-client-settings).

## Repository settings [repository-s3-repository]

The `s3` repository type supports a number of settings to customize how data is stored in S3. These can be specified when creating the repository. For example:

```console
PUT _snapshot/my_s3_repository
{
  "type": "s3",
  "settings": {
    "bucket": "my-bucket",
    "client": "default" <1>
  }
}
```

1. `client` must refer to a configured S3 client. If omitted, the `default` client is used.

Available repository settings define storage placement, snapshot data handling, storage and encryption behavior, throughput limits, and multipart upload tuning.
For a complete list of all S3 repository settings, refer to [S3 repository settings](elasticsearch://reference/elasticsearch/configuration-reference/s3-repository-settings.md#repository-s3-repository-settings).


## S3 storage classes [repository-s3-storage-classes]

Amazon S3 supports a variety of  *storage classes*, each of which offers different operational characteristics. For instance, some classes cost less per byte stored per month, but cost more per request, and other classes may vary in terms of their availability guarantees.

You can specify the storage class that {{es}} uses to store data objects with the `storage_class` repository setting. 

{applies_to}`stack: ga 9.5` You can also specify the storage class for objects with the `data_storage_class` and `metadata_storage_class` settings. For {{es}} versions 9.5 and later, we recommended you specify the `data_storage_class` and `metadata_storage_class` settings instead of the `storage_class` setting. To learn about the differences between these settings, refer to the [{{es}} configuration reference](elasticsearch://reference/elasticsearch/configuration-reference/s3-repository-settings.md#repository-s3-repository-settings).

Changing the `storage_class`, `data_storage_class`, or `metadata_storage_class` setting on an existing repository only affects the storage class for newly created objects, resulting in a mixed usage of storage classes.

You may use an S3 Lifecycle Policy to adjust the storage class of existing objects in your repository, but you must not transition objects to an unsupported class such as the Glacier classes, and you must not expire objects. If you use a Glacier storage class, or another unsupported storage class, or object expiry, then you may permanently lose access to your repository contents.

You may use the `intelligent_tiering` storage class to automatically manage the class of objects, but you must not enable the optional Archive Access or Deep Archive Access tiers. If you use these tiers then you may permanently lose access to your repository contents.

For more information about S3 storage classes, see [AWS Storage Classes Guide](https://docs.aws.amazon.com/AmazonS3/latest/dev/storage-class-intro.html).


## Recommended S3 permissions [repository-s3-permissions]

In order to restrict the {{es}} snapshot process to the minimum required resources, we recommend using Amazon IAM in conjunction with pre-existing S3 buckets. Here is an example policy which will allow the snapshot access to an S3 bucket named "snaps.example.com". This may be configured through the AWS IAM console, by creating a Custom Policy, and using a Policy Document similar to this (changing snaps.example.com to your bucket name).

```js
{
  "Statement": [
    {
      "Action": [
        "s3:ListBucket",
        "s3:GetBucketLocation",
        "s3:ListBucketMultipartUploads",
        "s3:ListBucketVersions"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::snaps.example.com"
      ]
    },
    {
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:AbortMultipartUpload",
        "s3:ListMultipartUploadParts"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::snaps.example.com/*"
      ]
    }
  ],
  "Version": "2012-10-17"
}
```

You may further restrict the permissions by specifying a prefix within the bucket, in this example, named "foo".

```js
{
  "Statement": [
    {
      "Action": [
        "s3:ListBucket",
        "s3:GetBucketLocation",
        "s3:ListBucketMultipartUploads",
        "s3:ListBucketVersions"
      ],
      "Condition": {
        "StringLike": {
          "s3:prefix": [
            "foo/*"
          ]
        }
      },
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::snaps.example.com"
      ]
    },
    {
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:AbortMultipartUpload",
        "s3:ListMultipartUploadParts"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::snaps.example.com/foo/*"
      ]
    }
  ],
  "Version": "2012-10-17"
}
```

The bucket needs to exist to register a repository for snapshots. If you did not create the bucket then the repository registration will fail.

You can also impose similar restrictions using a [bucket policy](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html).

Do not impose any additional restrictions on access to your bucket, for instance by using stricter `Condition` clauses than the ones documented above. Overly-restrictive access policies can prevent {{es}} snapshots from working correctly.

#### Using IAM roles for Kubernetes service accounts for authentication [iam-kubernetes-service-accounts]

If you want to use [Kubernetes service accounts](https://aws.amazon.com/blogs/opensource/introducing-fine-grained-iam-roles-service-accounts/) for authentication, you need to add a symlink to the `$AWS_WEB_IDENTITY_TOKEN_FILE` environment variable (which should be automatically set by a Kubernetes pod) in the S3 repository config directory, so the repository can have the read access for the service account (a repository can't read any files outside its config directory). For example:

```bash
mkdir -p "${ES_PATH_CONF}/repository-s3"
ln -s $AWS_WEB_IDENTITY_TOKEN_FILE "${ES_PATH_CONF}/repository-s3/aws-web-identity-token-file"
```

::::{important}
The symlink must be created on all data and master eligible nodes and be readable by the `elasticsearch` user. By default, {{es}} runs as user `elasticsearch` using uid:gid `1000:0`.
::::


If the symlink exists, it will be used by default by all S3 repositories that don't have explicit `client` credentials.


#### Using EKS Pod Identity for authentication [eks-pod-identity]

If you want to use [EKS Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html) for authentication, you need to make the injected token readable by the S3 repository. EKS injects a token file into the pod and sets the `AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE` environment variable to point at it, but that file lives outside the S3 repository config directory and a repository can't read any files outside its config directory. Add a symlink to the token inside the config directory, then point `AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE` (or the `aws.containerAuthorizationTokenFile` system property) at the symlink so the AWS SDK reads the token through it. For example:

```bash
mkdir -p "${ES_PATH_CONF}/repository-s3"
ln -s $AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE "${ES_PATH_CONF}/repository-s3/eks-pod-identity-token"
export AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE="${ES_PATH_CONF}/repository-s3/eks-pod-identity-token"
```

::::{important}
The symlink must be created on all data and master eligible nodes and be readable by the `elasticsearch` user. By default, {{es}} runs as user `elasticsearch` using uid:gid `1000:0`.
::::


{{es}} does not override `AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE` or `aws.containerAuthorizationTokenFile` itself, so the symlink and the repointed value must be in place before the node starts. Once configured, the token is used by default by all S3 repositories that don't have explicit `client` credentials, and it is re-read automatically when EKS rotates it.


## AWS VPC bandwidth settings [repository-s3-aws-vpc]

AWS instances resolve S3 endpoints to a public IP. If the {{es}} instances reside in a private subnet in an AWS VPC then all traffic to S3 will go through the VPC's NAT instance. If your VPC's NAT instance is a smaller instance size (e.g. a t2.micro) or is handling a high volume of network traffic your bandwidth to S3 may be limited by that NAT instance's networking bandwidth limitations. Instead we recommend creating a [VPC endpoint](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-endpoints.html) that enables connecting to S3 in instances that reside in a private subnet in an AWS VPC. This will eliminate any limitations imposed by the network bandwidth of your VPC's NAT instance.

Instances residing in a public subnet in an AWS VPC will connect to S3 via the VPC's internet gateway and not be bandwidth limited by the VPC's NAT instance.

## Replicating objects [repository-s3-replicating-objects]

AWS S3 supports [replication of objects](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html), both within a single region and across regions. However, this replication is not compatible with {{es}} snapshots.

The objects that {{es}} writes to the repository refer to other objects in the repository. {{es}} writes objects in a very specific order to ensure that each object only refers to objects which already exist. Likewise, {{es}} only deletes an object from the repository after it becomes unreferenced by all other objects. AWS S3 replication will apply operations to the replica repository in a different order from the order in which {{es}} applies them to the primary repository, which can cause some objects in replica repositories to refer to other objects that do not exist. This is an invalid state. It may not be possible to recover any data from a repository if it is in this state.

To replicate a repository's contents elsewhere, follow the [repository backup](/deploy-manage/tools/snapshot-and-restore/self-managed.md#snapshots-repository-backup) process. In particular, you may use the point-in-time restore capability of [AWS S3 backups](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html) to restore a backup of a snapshot repository to an earlier point in time.

## S3-compatible services [repository-s3-compatible-services]

Some storage systems offer an S3-compatible API, and the `s3` repository type allows you to use these systems in place of AWS S3. To do so, set the `s3.client.CLIENT_NAME.endpoint` setting to the storage system's endpoint URL. For example, `https://172.17.0.2` or `https://172.17.0.2:9000`.

By default {{es}} communicates with your storage system using HTTPS, and validates the repository's certificate chain using the JVM-wide truststore. Ensure that the JVM-wide truststore includes an entry for your repository. If you wish to use unsecured HTTP communication instead of HTTPS, set `s3.client.CLIENT_NAME.endpoint` to a URL which starts with `http://`.

The `s3` repository type requires your storage API to be _fully_ compatible with AWS S3. This means it must exactly conform to every aspect of the documented behavior of AWS S3: it must support all the same API endpoints, with all the same parameters, return the same errors in case of failures, and offer consistency, performance, and reliability at least as good as AWS S3 even when accessed concurrently by multiple {{es}} nodes. Some storage products, including some from very well-known storage vendors, claim to offer a S3-compatible API but in fact only support a subset of the features of AWS S3. Others offer an API which matches that of AWS S3 but with different behavior, especially when accessed concurrently. Such storage products are not fully S3-compatible. Using a storage product which is not fully S3-compatible puts your snapshot data at risk. If you are using such a system for your snapshots, consider using a [shared filesystem repository](shared-file-system-repository.md) based on a standardized protocol such as NFS to access your storage system instead.

Ensure that your storage supplier offers a full compatibility guarantee, and work with them to address any incompatibilities you encounter. Don't report {{es}} issues involving storage systems which claim to be S3-compatible unless you can demonstrate that the same issue exists when using a genuine AWS S3 repository.

You can perform some basic checks of the suitability of your storage system using the [repository analysis API]({{es-apis}}operation/operation-snapshot-repository-analyze). If this API does not complete successfully, or indicates poor performance, then your storage system is not fully compatible with AWS S3 and therefore unsuitable for use as a snapshot repository. However, a successful response from this API does not guarantee full compatibility. When upgrading, always verify that your storage passes repository analysis in the upgraded version before upgrading any production clusters.

$$$using-minio-with-elasticsearch$$$
::::{admonition} Using MinIO with {{es}}
[MinIO](https://minio.io) is an example of a storage system that provides an S3-compatible API. The `s3` repository type allows {{es}} to work with MinIO-backed repositories as well as repositories stored on AWS S3. The {{es}} test suite includes some checks which aim to detect deviations in behavior between MinIO and AWS S3. Elastic will report directly to the MinIO project any deviations in behavior found by these checks. If you are running a version of MinIO whose behavior deviates from that of AWS S3 then you must upgrade your MinIO installation. If in doubt, please contact the MinIO support team for further information.

The performance, reliability, and durability of a MinIO-backed repository depend on the properties of the underlying infrastructure and on the details of your MinIO configuration. You must design your storage infrastructure and configure MinIO in a way that ensures your MinIO-backed repository has performance, reliability, and durability characteristics which match AWS S3 in order for it to be fully S3-compatible. If you need assistance with your MinIO configuration, please contact the MinIO support team.
::::

### Investigating incompatibilities

Most storage systems can be configured to log the details of their interaction with {{es}}. If you are investigating a suspected incompatibility with AWS S3, it is usually simplest to collect these logs from your storage system and provide them to the supplier of your storage system for further analysis. Contact the supplier of your storage system for advice on how to configure it to log requests sufficiently verbosely for this troubleshooting.

If the incompatibility is not clear from the logs emitted by the storage system, you can enable more granular logging:

::::::{applies-switch}

:::::{applies-item} { "stack": "ga 9.1+" }

::::{warning}
In {{es}} versions **9.1.0 to 9.1.8**, and **9.2.0 to 9.2.2**, it is not possible to obtain more detailed logs from the AWS Java SDK. Use the logs from the storage system itself, or upgrade to a later version of {{es}}.
::::

Configure {{es}} to log every request it makes to the S3 API by [setting the logging level](/deploy-manage/monitor/logging-configuration/update-elasticsearch-logging-levels.md) of the `software.amazon.awssdk.request` logger to `DEBUG`:

```console
PUT /_cluster/settings
{
  "persistent": {
    "logger.software.amazon.awssdk.request": "DEBUG"
  }
}
```

To prevent leaking sensitive information such as credentials and keys in logs, {{es}} rejects configuring this logger at high verbosity unless [insecure network trace logging](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#http-rest-request-tracer) is enabled. To do so, you must explicitly enable it on each node by setting the system property `es.insecure_network_trace_enabled` to `true`.

Collect the {{es}} logs covering the time period of the failed analysis from all nodes in your cluster and share them with the supplier of your storage system along with the analysis response so they can use them to determine the problem. Refer to [Logging with the AWS S3 SDK for Java 2.x](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/logging-slf4j.html) for further information, including details about other loggers that can be used to obtain even more verbose logs. When configuring other loggers, note that {{es}} configures the AWS Java SDK to use the `ApacheHttpClient` synchronous HTTP client.

:::::

:::::{applies-item} { "stack": "ga =9.0" }
Configure {{es}} to log every request it makes to the S3 API by [setting the logging level](/deploy-manage/monitor/logging-configuration/update-elasticsearch-logging-levels.md) of the `com.amazonaws.request` logger to `DEBUG`:

```console
PUT /_cluster/settings
{
  "persistent": {
    "logger.com.amazonaws.request": "DEBUG"
  }
}
```

To prevent leaking sensitive information such as credentials and keys in logs, {{es}} rejects configuring this logger at high verbosity unless [insecure network trace logging](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#http-rest-request-tracer) is activated. To do so, you must explicitly configure it on each node by setting the system property `es.insecure_network_trace_enabled` to `true`.

Collect the {{es}} logs covering the time period of the failed analysis from all nodes in your cluster and share them with the supplier of your storage system along with the analysis response so they can use them to determine the problem. Refer to [Logging AWS SDK for Java Calls](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/java-dg-logging.html) for further information, including details about other loggers that can be used to obtain even more verbose logs.
:::::

::::::

When you have finished collecting the logs needed by your supplier, set the logger settings back to `null` to return to the default logging configuration and deactivate insecure network trace logging again. Refer to [Logger](elasticsearch://reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-logger) and [Cluster update settings]({{es-apis}}operation/operation-cluster-put-settings) for more information.


## Linearizable register implementation [repository-s3-linearizable-registers]

### Conditional writes
```{applies_to}
stack: ga 9.3
```

From 9.3.0 onwards the linearizable register implementation for S3 repositories is based on [S3's conditional writes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html) using the `If-None-Match` and `If-Match` request headers.

If your storage does not support conditional writes then it is not fully S3-compatible. In this case {{es}} can fall back to using the multipart upload APIs for its linearizable registers, as long as these APIs have strongly consistent semantics as described below. Future versions of {{es}} may remove this lenient behavior and require your storage to support conditional writes. Contact the supplier of your storage for further information about conditional writes and the strong consistency of your storage's multipart upload APIs.

### Multipart uploads

```{applies_to}
stack: deprecated 9.3
```

In versions before 9.3.0, or if your storage does not support conditional writes, the linearizable register implementation for S3 repositories is based on the strongly consistent semantics of the multipart upload APIs. {{es}} first creates a multipart upload to indicate its intention to perform a linearizable register operation. {{es}} then lists and cancels all other multipart uploads for the same register. {{es}} then attempts to complete the upload. If the upload completes successfully then the compare-and-exchange operation was atomic.
