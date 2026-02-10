---
navigation_title: AWS S3 repository
applies_to:
  deployment:
    ece:
navigation_title: AWS S3
---

# Configure an AWS S3 snapshot repository in {{ece}} [ece-aws-custom-repository]

This guide focuses on registering an AWS S3 snapshot repository at the {{ece}} (ECE) platform level. Platform-level repositories can be assigned to deployments and are used by ECE to automatically manage snapshots through the `found-snapshots` repository.

If you have custom requirements or deployment-specific use cases that are independent of the ECE-managed automation, you can also register snapshot repositories directly at the deployment level. To do that, follow the [{{ech}} guide for AWS S3](/deploy-manage/tools/snapshot-and-restore/ec-aws-custom-repository.md), which is also applicable to {{ece}} deployments.

## Add the AWS S3 repository

To add the repository:

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

## Configure your deployment to use the repository

After adding the snapshot repository, [configure your deployment to use it](./cloud-enterprise.md#ece-manage-repositories-clusters). Once configured, snapshots run automatically according to the scheduled interval. You can update this schedule from the **Snapshots** section in the **{{es}}** menu of your deployment page.