---
navigation_title: AWS S3 repository
applies_to:
  deployment:
    ece:
---

# Configure an AWS S3 snapshot repository in {{ece}} [ece-aws-custom-repository]

To store {{es}} snapshots in AWS S3, you need to configure a snapshot repository in {{ece}} (ECE). This guide explains how to add an Amazon S3 repository using the Cloud UI and provides details on required settings and advanced configurations.

To add a snapshot repository:

1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Repositories**.
3. Select **Add Repository** to add an existing repository.
4. Provide a name for the repository configuration.

    ECE Snapshot Repository names are now required to meet the same standards as S3 buckets. Refer to the official AWS documentation on [Bucket naming rules](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html).

5. Select one of the supported repository types and specify the necessary settings:

    * Amazon S3 configuration:

        All repository options must be specified, as there are no default values.

        Region
        :   The region where the bucket is located.

        Bucket
        :   The name of the bucket to be used for snapshots.

        Access key
        :   The access key to use for authentication.

        Secret key
        :   The secret key to use for authentication.

    * Advanced configuration:

        Used for Microsoft Azure, Google Cloud Platform, or for some Amazon S3 repositories where you need to provide additional configuration parameters not supported by the S3 repository option. Configurations must be specified in a valid JSON format. For example:

        Amazon S3 (check [supported settings](/deploy-manage/tools/snapshot-and-restore/s3-repository.md#repository-s3-repository)):

        ```json
        {
          "type": "s3",
          "settings": {
            "bucket": "my_bucket_name",
            "region": "us-west"
          }
        }
        ```

        ::::{note}
        Don’t set `base_path` when configuring a snapshot repository for {{ECE}}. {{ECE}} automatically generates the `base_path` for each deployment so that multiple deployments may share the same bucket.
        ::::

6. Select **Save**.