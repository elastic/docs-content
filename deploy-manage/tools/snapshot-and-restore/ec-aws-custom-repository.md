---
applies_to:
  deployment:
    ess: 
---

# Configure a snapshot repository using AWS S3 [ec-aws-custom-repository]

Configure a custom snapshot repository using an S3 storage bucket in your AWS account.


## Prepare an S3 bucket [ec-prepare-aws-bucket]

Create the S3 bucket in your custom AWS account. Make sure to reserve this bucket to backup only one cluster, since AWS allows file overwrite for non-unique titles.

Next, create an IAM user, copy the access key ID and secret, and configure the following user policy. This is important to make sure the access keys, which you will need to provide to your cluster, can only access the intended bucket.

```json
{
  "Version": "policy-language-YYYY-MM-dd",<1>
  "Statement": [
    {
      "Action": [
        "s3:*"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::bucket-name",
        "arn:aws:s3:::bucket-name/*"
      ]
    }
  ]
}
```

1. The version of the policy language syntax rules. For more information, refer to the [AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-reference-policy-checks.md#access-analyzer-reference-policy-checks-error-invalid-version).


For more information on S3 and IAM, refer to AWS' [S3-documentation](http://docs.aws.amazon.com/AmazonS3/latest/dev/Introduction.md) and [IAM-documentation](http://aws.amazon.com/documentation/iam/).

::::{note}
For a full list of settings that are supported for your S3 bucket, refer to [S3 repository](s3-repository.md) in the {{es}} Guide.
::::



## Store your secrets in the keystore [ec-snapshot-secrets-keystore]

You can use the {{es}} keystore to store the credentials to access your AWS account.

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Navigate to the **Security** page of the deployment you wish to configure.
3. Locate **Elasticsearch keystore** and select **Add settings**.
4. With **Type** set to **Single string**, add the following keys and their values:

    * `s3.client.secondary.access_key`
    * `s3.client.secondary.secret_key`

5. Perform a cluster restart to [reload the secure settings](/deploy-manage/security/secure-settings.md#ec-add-secret-values).


## Create the repository [ec-create-aws-repository]

1. Open Kibana and go to **Management** > **Snapshot and Restore**.
2. On the **Repositories** tab, select **Register a repository**.
3. Provide a name for your repository and select type **AWS S3**.
4. Provide the following settings:

    * Client: `secondary`
    * Bucket: `YOUR_S3_BUCKET_NAME`

5. Add any other settings that you wish to configure.
6. Select **Register**.
7. Select **Verify** to confirm that your settings are correct and the deployment can connect to your repository.

Your snapshot repository is now set up using S3! You can use Kibana to manage your snapshots and begin sending Elasticsearch snapshots to your own bucket. For details refer to the [Snapshot and Restore](create-snapshots.md) documentation.

