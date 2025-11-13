---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configure-gcp-snapshotting.html
applies_to:
  deployment:
    ece:
products:
  - id: cloud-enterprise
navigation_title: Google Cloud Storage
---

# Configure a Google Cloud Storage snapshot repository in {{ece}}

Snapshots to Google Cloud Storage (GCS) are supported using an [advanced repository configuration](cloud-enterprise.md) and service account credentials that can administer your GCS bucket.

## Set up your service account credentials [ece_set_up_your_service_account_credentials]

You’ll need to have an existing Google Cloud account and have the appropriate permissions to generate credentials:

1. Create [service account credentials](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) in your Google Cloud project where {{ece}} is running.

    The service account should be [granted the role of `storage.admin`](https://cloud.google.com/iam/docs/granting-roles-to-service-accounts) so that {{es}} clusters can read, write, and list the bucket objects.

2. Save the service account key in JSON file format. You are going to use it later to configure your {{es}} deployment for snapshotting.


## Add the GCS repository [ece_add_the_gcs_repository]

Add your Google Cloud Storage bucket as a repository to the platform:

1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. Go to **Platform > Repositories** and add the following snapshot repository configuration under the advanced mode:

    Repository GCS (check: [supported settings](/deploy-manage/tools/snapshot-and-restore/google-cloud-storage-repository.md#repository-gcs-repository))

    ```json
    {
      "type": "gcs",
      "settings": {
        "bucket": "acme-snapshot-repo",
        "bucket": "acme-snapshots"
      }
    }
    ```


Snapshots are stored in the bucket you provide. Use the repository name you define here to configure your {{es}} clusters for snapshotting to this repository.


## Configure your deployment for GCS snapshots [ece_configure_your_deployment_for_gcs_snapshots]

To save deployment snapshots to the custom GCS repository:

1. Add a [secure setting](../../security/secure-settings.md) named `gcs.client.acme-snapshots.credentials_file` as a JSON block. Make sure that the client name is the same one you provided when configuring the snapshot repository.

    :::{image} /deploy-manage/images/cloud-enterprise-ece-secure-settings.png
    :alt: GCS client secret configuration
    :::

    ::::{note}
    The contents within *credentials_file* must be the exact contents of your GCS credentials file.
    ::::

2. Configure your deployment to [snapshot to the GCS repository](cloud-enterprise.md).

After you enable snapshots, snapshotting will begin within 30 minutes (the default snapshot interval).

