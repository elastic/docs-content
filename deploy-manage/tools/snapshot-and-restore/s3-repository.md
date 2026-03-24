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

{{es}} communicates with S3 through a dedicated S3 client module. Clients are configured through a combination of [secure settings](../../security/secure-settings.md) defined in the {{es}} keystore, and [standard settings](/deploy-manage/stack-settings.md) defined in `elasticsearch.yml`. If you don't provide explicit S3 client configuration, {{es}} will try to obtain credentials from the environment it's running in.

## Getting started [repository-s3-usage]

To register an S3 repository, specify the type as `s3` when creating the repository. The only mandatory setting is the bucket name:

```console
PUT _snapshot/my_s3_repository
{
  "type": "s3",
  "settings": {
    "bucket": "my-bucket"
  }
}
```

By default, an S3 repository will attempt to obtain its credentials automatically from the environment. For instance, if {{es}} is running on an AWS EC2 instance then it will attempt to use the [EC2 Instance Metadata Service](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html) to obtain temporary credentials for the [instance IAM role](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html). Likewise, if {{es}} is running in AWS EC2, then it will automatically obtain temporary [ECS IAM Role](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html) credentials for authentication. You can also use [Kubernetes service accounts](#iam-kubernetes-service-accounts) for authentication. To disable this behavior, specify an access key, a secret key, and optionally a session token, in the {{es}} keystore.

## Client settings [repository-s3-client]

The S3 client that you use to connect to S3 has a number of settings available. The settings have the form `s3.client.CLIENT_NAME.SETTING_NAME`. By default, `s3` repositories use a client named `default`, but this can be modified using the [repository setting](#repository-s3-repository) `client`.

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
    "another_setting": "setting-value"
  }
}
```

Available repository settings define storage placement, snapshot data handling, storage and encryption behavior, throughput limits, and multipart upload tuning.
For a complete list of all S3 repository settings, refer to [S3 repository settings](elasticsearch://reference/elasticsearch/configuration-reference/s3-repository-settings.md#repository-s3-repository-settings).


## S3 storage classes [repository-s3-storage-classes]

Amazon S3 supports a variety of  *storage classes*, each of which offers different operational characteristics. For instance, some classes cost less per byte stored per month, but cost more per request, and other classes may vary in terms of their availability guarantees.

You may specify the storage class that {{es}} uses to store data objects with the `storage_class` repository setting.

Changing the `storage_class` setting on an existing repository only affects the storage class for newly created objects, resulting in a mixed usage of storage classes.

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


## AWS VPC bandwidth settings [repository-s3-aws-vpc]

AWS instances resolve S3 endpoints to a public IP. If the {{es}} instances reside in a private subnet in an AWS VPC then all traffic to S3 will go through the VPC's NAT instance. If your VPC's NAT instance is a smaller instance size (e.g. a t2.micro) or is handling a high volume of network traffic your bandwidth to S3 may be limited by that NAT instance's networking bandwidth limitations. Instead we recommend creating a [VPC endpoint](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-endpoints.html) that enables connecting to S3 in instances that reside in a private subnet in an AWS VPC. This will eliminate any limitations imposed by the network bandwidth of your VPC's NAT instance.

Instances residing in a public subnet in an AWS VPC will connect to S3 via the VPC's internet gateway and not be bandwidth limited by the VPC's NAT instance.

## Replicating objects [repository-s3-replicating-objects]

AWS S3 supports [replication of objects](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html), both within a single region and across regions. However, this replication is not compatible with {{es}} snapshots.

The objects that {{es}} writes to the repository refer to other objects in the repository. {{es}} writes objects in a very specific order to ensure that each object only refers to objects which already exist. Likewise, {{es}} only deletes an object from the repository after it becomes unreferenced by all other objects. AWS S3 replication will apply operations to the replica repository in a different order from the order in which {{es}} applies them to the primary repository, which can cause some objects in replica repositories to refer to other objects that do not exist. This is an invalid state. It may not be possible to recover any data from a repository if it is in this state.

To replicate a repository's contents elsewhere, follow the [repository backup](/deploy-manage/tools/snapshot-and-restore/self-managed.md#snapshots-repository-backup) process. In particular, you may use the point-in-time restore capability of [AWS S3 backups](https://docs.aws.amazon.com/aws-backup/latest/devguide/s3-backups.html) to restore a backup of a snapshot repository to an earlier point in time.

## S3-compatible services [repository-s3-compatible-services]

There are a number of storage systems that provide an S3-compatible API, and the `s3` repository type allows you to use these systems in place of AWS S3. To do so, you should set the `s3.client.CLIENT_NAME.endpoint` setting to the system's endpoint. This setting accepts IP addresses and hostnames and may include a port. For example, the endpoint may be `172.17.0.2` or `172.17.0.2:9000`.

By default {{es}} communicates with your storage system using HTTPS, and validates the repository's certificate chain using the JVM-wide truststore. Ensure that the JVM-wide truststore includes an entry for your repository. If you wish to use unsecured HTTP communication instead of HTTPS, set `s3.client.CLIENT_NAME.protocol` to `http`.

There are many systems, including some from very well-known storage vendors, which claim to offer an S3-compatible API despite failing to emulate S3's behavior in full. If you are using such a system for your snapshots, consider using a [shared filesystem repository](shared-file-system-repository.md) based on a standardized protocol such as NFS to access your storage system instead. The `s3` repository type requires full compatibility with S3. In particular it must support the same set of API endpoints, with the same parameters, return the same errors in case of failures, and offer consistency, performance, and reliability at least as good as S3 even when accessed concurrently by multiple nodes. You will need to work with the supplier of your storage system to address any incompatibilities you encounter. Don't report {{es}} issues involving storage systems which claim to be S3-compatible unless you can demonstrate that the same issue exists when using a genuine AWS S3 repository.

You can perform some basic checks of the suitability of your storage system using the [repository analysis API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-repository-analyze). If this API does not complete successfully, or indicates poor performance, then your storage system is not fully compatible with AWS S3 and therefore unsuitable for use as a snapshot repository. However, a successful response from this API does not guarantee full compatibility, so you must also ensure that your storage supplier offers a full compatibility guarantee. When upgrading, always verify that your storage passes repository analysis in the upgraded version before upgrading any production clusters.

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

When you have finished collecting the logs needed by your supplier, set the logger settings back to `null` to return to the default logging configuration and deactivate insecure network trace logging again. Refer to [Logger](elasticsearch://reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-logger) and [Cluster update settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) for more information.


## Linearizable register implementation [repository-s3-linearizable-registers]

### Conditional writes
```{applies_to}
stack: ga 9.3
```

From 9.3.0 onwards the linearizable register implementation for S3 repositories is based on [S3's conditional writes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html) using the `If-None-Match` and `If-Match` request headers.

If your storage does not support conditional writes then it is not fully S3-compatible. However, if this is its only deviation in behavior from AWS S3 then it will work correctly with {{es}} as long as its multipart upload APIs have strongly consistent semantics, as described below. Future versions of {{es}} may remove this lenient behavior and require your storage to support conditional writes. Contact the supplier of your storage for further information about conditional writes and the strong consistency of your storage's multipart upload APIs.

### Multipart uploads

```{applies_to}
stack: deprecated 9.3
```

In versions before 9.3.0, or if your storage does not support conditional writes, the linearizable register implementation for S3 repositories is based on the strongly consistent semantics of the multipart upload APIs. {{es}} first creates a multipart upload to indicate its intention to perform a linearizable register operation. {{es}} then lists and cancels all other multipart uploads for the same register. {{es}} then attempts to complete the upload. If the upload completes successfully then the compare-and-exchange operation was atomic.
