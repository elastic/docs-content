---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/repository-gcs.html
applies_to:
  deployment:
    self:
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

The repository must authenticate the requests it makes to the Google Cloud Storage service. It is common for Google client libraries to employ a strategy named [application default credentials](https://cloud.google.com/docs/authentication/production#providing_credentials_to_your_application). However, that strategy is only **partially supported** by Elasticsearch. The repository operates under the Elasticsearch process, which runs with the security manager enabled. The security manager obstructs the "automatic" credential discovery when the environment variable `GOOGLE_APPLICATION_CREDENTIALS` is used to point to a local file on disk. It can, however, retrieve the service account that is attached to the resource that is running Elasticsearch, or fall back to the default service account that Compute Engine, Kubernetes Engine or App Engine provide. Alternatively, you must configure [service account](#repository-gcs-using-service-account) credentials if you are using an environment that does not support automatic credential discovery.


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
%  NOTCONSOLE

To provide this file to the repository, it must be stored in the [Elasticsearch keystore](../../security/secure-settings.md). You must add a `file` setting with the name `gcs.client.NAME.credentials_file` using the `add-file` subcommand. `NAME` is the name of the client configuration for the repository. The implicit client name is `default`, but a different client name can be specified in the repository settings with the `client` key.

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
%  TEST[skip:we don’t have gcs setup while testing this]

The `credentials_file` settings are [reloadable](../../security/secure-settings.md#reloadable-secure-settings). You can define these settings before the node is started, or call the [Nodes reload secure settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings) after the settings are defined to apply them to a running node.

After you reload the settings, the internal `gcs` clients, which are used to transfer the snapshot contents, utilize the latest settings from the keystore.

::::{note}
Snapshot or restore jobs that are in progress are not preempted by a **reload** of the client’s `credentials_file` settings. They complete using the client as it was built when the operation started.
::::




## Client settings [repository-gcs-client]

The client used to connect to Google Cloud Storage has a number of settings available. Client setting names are of the form `gcs.client.CLIENT_NAME.SETTING_NAME` and are specified inside `elasticsearch.yml`. The default client name looked up by a `gcs` repository is called `default`, but can be customized with the repository setting `client`.

For example:

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
%  TEST[skip:we don’t have gcs setup while testing this]

Some settings are sensitive and must be stored in the [Elasticsearch keystore](../../security/secure-settings.md). This is the case for the service account file:

```sh
bin/elasticsearch-keystore add-file gcs.client.default.credentials_file /path/service-account.json
```

The following are the available client settings. Those that must be stored in the keystore are marked as `Secure`.

`credentials_file` ([Secure](/deploy-manage/security/secure-settings.md), [reloadable](../../security/secure-settings.md#reloadable-secure-settings))
:   The service account file that is used to authenticate to the Google Cloud Storage service.

`endpoint`
:   The Google Cloud Storage service endpoint to connect to. This will be automatically determined by the Google Cloud Storage client but can be specified explicitly.

`connect_timeout`
:   The timeout to establish a connection to the Google Cloud Storage service. The value should specify the unit. For example, a value of `5s` specifies a 5 second timeout. The value of `-1` corresponds to an infinite timeout. The default value is 20 seconds.

`read_timeout`
:   The timeout to read data from an established connection. The value should specify the unit. For example, a value of `5s` specifies a 5 second timeout. The value of `-1` corresponds to an infinite timeout. The default value is 20 seconds.

`application_name`
:   Name used by the client when it uses the Google Cloud Storage service. Setting a custom name can be useful to authenticate your cluster when requests statistics are logged in the Google Cloud Platform. Default to `repository-gcs`

`project_id`
:   The Google Cloud project id. This will be automatically inferred from the credentials file but can be specified explicitly. For example, it can be used to switch between projects when the same credentials are usable for both the production and the development projects.

`proxy.host`
:   Host name of a proxy to connect to the Google Cloud Storage through.

`proxy.port`
:   Port of a proxy to connect to the Google Cloud Storage through.

`proxy.type`
:   Proxy type for the client. Supported values are `direct` (no proxy), `http`, and `socks`. Defaults to `direct`.


## Repository settings [repository-gcs-repository]

The `gcs` repository type supports a number of settings to customize how data is stored in Google Cloud Storage.

These can be specified when creating the repository. For example:

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
%  TEST[skip:we don’t have gcs set up while testing this]

The following settings are supported:

`bucket`
:   The name of the bucket to be used for snapshots. (Mandatory)

`client`
:   The name of the client to use to connect to Google Cloud Storage. Defaults to `default`.

`base_path`
:   Specifies the path within bucket to repository data. Defaults to the root of the bucket.

    ::::{note}
    Don’t set `base_path` when configuring a snapshot repository for {{ECE}}. {{ECE}} automatically generates the `base_path` for each deployment so that multiple deployments may share the same bucket.
    ::::


`chunk_size`
:   Big files can be broken down into multiple smaller blobs in the blob store during snapshotting. It is not recommended to change this value from its default unless there is an explicit reason for limiting the size of blobs in the repository. Setting a value lower than the default can result in an increased number of API calls to the Google Cloud Storage Service during snapshot create as well as restore operations compared to using the default value and thus make both operations slower as well as more costly. Specify the chunk size as a value and unit, for example: `10MB`, `5KB`, `500B`. Defaults to the maximum size of a blob in the Google Cloud Storage Service which is `5TB`.

`compress`
:   When set to `true` metadata files are stored in compressed format. This setting doesn’t affect index files that are already compressed by default. Defaults to `true`.

`max_restore_bytes_per_sec`
:   (Optional, [byte value](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#byte-units)) Maximum snapshot restore rate per node. Defaults to unlimited. Note that restores are also throttled through [recovery settings](elasticsearch://reference/elasticsearch/configuration-reference/index-recovery-settings.md).

`max_snapshot_bytes_per_sec`
:   (Optional, [byte value](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#byte-units)) Maximum snapshot creation rate per node. Defaults to `40mb` per second. Note that if the [recovery settings for managed services](elasticsearch://reference/elasticsearch/configuration-reference/index-recovery-settings.md#recovery-settings-for-managed-services) are set, then it defaults to unlimited, and the rate is additionally throttled through [recovery settings](elasticsearch://reference/elasticsearch/configuration-reference/index-recovery-settings.md).

`readonly`
:   (Optional, Boolean) If `true`, the repository is read-only. The cluster can retrieve and restore snapshots from the repository but not write to the repository or create snapshots in it.

    Only a cluster with write access can create snapshots in the repository. All other clusters connected to the repository should have the `readonly` parameter set to `true`.

    If `false`, the cluster can write to the repository and create snapshots in it. Defaults to `false`.

    ::::{important}
    If you register the same snapshot repository with multiple clusters, only one cluster should have write access to the repository. Having multiple clusters write to the repository at the same time risks corrupting the contents of the repository.

    ::::


`application_name`
:   [6.3.0] Name used by the client when it uses the Google Cloud Storage service.

### Recommended bucket permission [repository-gcs-bucket-permission]

The service account used to access the bucket must have the "Writer" access to the bucket:

1. Connect to the [Google Cloud Platform Console](https://console.cloud.google.com/).
2. Select your project.
3. Go to the [Storage Browser](https://console.cloud.google.com/storage/browser).
4. Select the bucket and "Edit bucket permission".
5. The service account must be configured as a "User" with "Writer" access.



## Linearizable register implementation [repository-gcs-linearizable-registers]

The linearizable register implementation for GCS repositories is based on GCS’s support for strongly consistent preconditions on put-blob operations. To perform a compare-and-exchange operation on a register, {{es}} retrieves the register blob and its current generation, and then uploads the updated blob using the observed generation as its precondition. The precondition ensures that the generation has not changed in the meantime.
