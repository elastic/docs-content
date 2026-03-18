---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/repository-gcs.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
---

# Google Cloud Storage repository [repository-gcs]

You can use the [Google Cloud Storage](https://cloud.google.com/storage/) service as a repository for [Snapshot/Restore](../snapshot-and-restore.md).

## Getting started [repository-gcs-usage]

This repository type uses the [Google Cloud Java Client for Storage](https://github.com/GoogleCloudPlatform/google-cloud-java/tree/master/google-cloud-clients/google-cloud-storage) to connect to the Storage service. If you are using [Google Cloud Storage](https://cloud.google.com/storage/) for the first time, you must connect to the [Google Cloud Platform Console](https://console.cloud.google.com/) and create a new project. After your project is created, you must enable the Cloud Storage Service for your project.

### Creating a bucket [repository-gcs-creating-bucket]

The Google Cloud Storage service uses the concept of a [bucket](https://cloud.google.com/storage/docs/key-terms) as a container for all the data. Buckets are usually created using the [Google Cloud Platform Console](https://console.cloud.google.com/). This repository type does not automatically create buckets.

To create a new bucket:

1. Connect to the [Google Cloud Platform Console](https://console.cloud.google.com/).
2. Select your project.
3. Go to the [Storage Browser](https://console.cloud.google.com/storage/browser).
4. Click the **Create Bucket** button.
5. Enter the name of the new bucket.
6. Select a storage class.
7. Select a location.
8. Click the **Create** button.

For more detailed instructions, see the [Google Cloud documentation](https://cloud.google.com/storage/docs/quickstart-console#create_a_bucket).


### Service authentication [repository-gcs-service-authentication]

The repository must authenticate the requests it makes to the Google Cloud Storage service. It is common for Google client libraries to employ a strategy named [application default credentials](https://cloud.google.com/docs/authentication/production#providing_credentials_to_your_application). However, that strategy is only **partially supported** by {{es}}. The repository operates under the {{es}} process, which runs with the security manager enabled. The security manager obstructs the "automatic" credential discovery when the environment variable `GOOGLE_APPLICATION_CREDENTIALS` is used to point to a local file on disk. It can, however, retrieve the service account that is attached to the resource that is running {{es}}, or fall back to the default service account that Compute Engine, Kubernetes Engine or App Engine provide. Alternatively, you must configure [service account](#repository-gcs-using-service-account) credentials if you are using an environment that does not support automatic credential discovery.


### Using a service account [repository-gcs-using-service-account]

You have to obtain and provide [service account credentials](https://cloud.google.com/iam/docs/overview#service_account) manually.

For detailed information about generating JSON service account files, see the [Google Cloud documentation](https://cloud.google.com/storage/docs/authentication?hl=en#service_accounts). Note that the PKCS12 format is not supported by this repository type.

Here is a summary of the steps:

1. Connect to the [Google Cloud Platform Console](https://console.cloud.google.com/).
2. Select your project.
3. Select the [Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts) tab.
4. Click **Create service account**.
5. After the account is created, select it and go to **Keys**.
6. Select **Add Key** and then **Create new key**.
7. Select Key Type **JSON** as P12 is unsupported.

A JSON service account file looks like this:

```js
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "service-account-for-your-repository@your-project-id.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-bucket@your-project-id.iam.gserviceaccount.com"
}
```

To provide this file to the repository, it must be stored in the [{{es}} keystore](../../security/secure-settings.md). You must add a `file` setting with the name `gcs.client.NAME.credentials_file` using the `add-file` subcommand. `NAME` is the name of the client configuration for the repository. The implicit client name is `default`, but a different client name can be specified in the repository settings with the `client` key.

::::{note}
Passing the file path via the GOOGLE_APPLICATION_CREDENTIALS environment variable is **not** supported.
::::


For example, if you added a `gcs.client.my_alternate_client.credentials_file` setting in the keystore, you can configure a repository to use those credentials like this:

```console
PUT _snapshot/my_gcs_repository
{
  "type": "gcs",
  "settings": {
    "bucket": "my_bucket",
    "client": "my_alternate_client"
  }
}
```

The `credentials_file` settings are [reloadable](../../security/secure-settings.md#reloadable-secure-settings). You can define these settings before the node is started, or call the [Nodes reload secure settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings) after the settings are defined to apply them to a running node.

After you reload the settings, the internal `gcs` clients, which are used to transfer the snapshot contents, utilize the latest settings from the keystore.

::::{note}
Snapshot or restore jobs that are in progress are not preempted by a **reload** of the client's `credentials_file` settings. They complete using the client as it was built when the operation started.
::::




## Client settings [repository-gcs-client]

The client used to connect to Google Cloud Storage has a number of settings available. Client setting names are of the form `gcs.client.CLIENT_NAME.SETTING_NAME` and are specified inside [`elasticsearch.yml`](/deploy-manage/stack-settings.md). The default client name looked up by a `gcs` repository is called `default`, but can be customized with the repository setting `client`.

Available client settings include `credentials_file`, `endpoint`, `connect_timeout`, `read_timeout`, `application_name`, `project_id`, and proxy configuration.

For a complete list of all GCS client settings, refer to [GCS repository client settings](elasticsearch://reference/elasticsearch/configuration-reference/gcs-repository-settings.md#repository-gcs-client-settings).


## Repository settings [repository-gcs-repository]

The `gcs` repository type supports a number of settings to customize how data is stored in Google Cloud Storage. These can be specified when creating the repository. For example:

```console
PUT _snapshot/my_gcs_repository
{
  "type": "gcs",
  "settings": {
    "bucket": "my_other_bucket",
    "base_path": "dev"
  }
}
```

Available repository settings include the target `bucket`, `base_path`, `chunk_size`, `compress`, and throughput throttling (`max_restore_bytes_per_sec`, `max_snapshot_bytes_per_sec`).

For a complete list of all GCS repository settings, refer to [GCS repository settings](elasticsearch://reference/elasticsearch/configuration-reference/gcs-repository-settings.md#repository-gcs-repository-settings).

### Recommended bucket permission [repository-gcs-bucket-permission]

The service account used to access the bucket must have the "Writer" access to the bucket:

1. Connect to the [Google Cloud Platform Console](https://console.cloud.google.com/).
2. Select your project.
3. Go to the [Storage Browser](https://console.cloud.google.com/storage/browser).
4. Select the bucket and "Edit bucket permission".
5. The service account must be configured as a "User" with "Writer" access.



## Linearizable register implementation [repository-gcs-linearizable-registers]

The linearizable register implementation for GCS repositories is based on GCS's support for strongly consistent preconditions on put-blob operations. To perform a compare-and-exchange operation on a register, {{es}} retrieves the register blob and its current generation, and then uploads the updated blob using the observed generation as its precondition. The precondition ensures that the generation has not changed in the meantime.
