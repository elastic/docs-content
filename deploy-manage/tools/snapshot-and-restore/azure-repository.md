---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/repository-azure.html
applies_to:
  deployment:
    self:
---

# Azure repository [repository-azure]

You can use [Azure Blob storage](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction) as a repository for [Snapshot and restore](../snapshot-and-restore.md).

## Setup [repository-azure-usage]

To enable Azure repositories, first configure an Azure repository client by specifying one or more settings of the form `azure.client.CLIENT_NAME.SETTING_NAME`. By default, `azure` repositories use a client named `default`, but you may specify a different client name when registering each repository.

The only mandatory Azure repository client setting is `account`, which is a [secure setting](../../security/secure-settings.md) defined in the [{{es}} keystore](../../security/secure-settings.md). To provide this setting, use the `elasticsearch-keystore` tool on each node:

```sh
bin/elasticsearch-keystore add azure.client.default.account
```

If you adjust this setting after a node has started, call the [Nodes reload secure settings API](../../security/secure-settings.md) to reload the new value.

You may define more than one client by setting their `account` values. For instance, to set the `default` client and another client called `secondary`, run the following commands on each node:

```sh
bin/elasticsearch-keystore add azure.client.default.account
bin/elasticsearch-keystore add azure.client.secondary.account
```

The `key` and `sas_token` settings are also secure settings and can be set using commands like the following:

```sh
bin/elasticsearch-keystore add azure.client.default.key
bin/elasticsearch-keystore add azure.client.secondary.sas_token
```

Other Azure repository client settings must be set in `elasticsearch.yml` before the node starts. For example:

```yaml
azure.client.default.timeout: 10s
azure.client.default.max_retries: 7
azure.client.default.endpoint_suffix: core.chinacloudapi.cn
azure.client.secondary.timeout: 30s
```

In this example, the client side timeout is `10s` per try for repositories which use the `default` client, with `7` retries before failing and an endpoint suffix of `core.chinacloudapi.cn`. Repositories which use the `secondary` client will have a timeout of `30s` per try, but will use the default endpoint and will fail after the default number of retries.

Once an Azure repository client is configured correctly, register an Azure repository as follows, providing the client name using the `client` [repository setting](#repository-azure-repository-settings):

```console
PUT _snapshot/my_backup
{
  "type": "azure",
  "settings": {
    "client": "secondary"
  }
}
```
%  TEST[skip:we don’t have azure setup while testing this]

If you are using the `default` client, you may omit the `client` repository setting:

```console
PUT _snapshot/my_backup
{
  "type": "azure"
}
```
%  TEST[skip:we don’t have azure setup while testing this]

::::{note}
In progress snapshot or restore jobs will not be preempted by a **reload** of the storage secure settings. They will complete using the client as it was built when the operation started.
::::



## Client settings [repository-azure-client-settings]

The following list describes the available client settings. Those that must be stored in the keystore are marked as ([Secure](/deploy-manage/security/secure-settings.md), [reloadable](../../security/secure-settings.md#reloadable-secure-settings)); the other settings must be stored in the `elasticsearch.yml` file. The default `CLIENT_NAME` is `default` but you may configure a client with a different name and specify that client by name when registering a repository.

`azure.client.CLIENT_NAME.account` ([Secure](/deploy-manage/security/secure-settings.md), [reloadable](../../security/secure-settings.md#reloadable-secure-settings))
:   The Azure account name, which is used by the repository’s internal Azure client. This setting is required for all clients.

`azure.client.CLIENT_NAME.endpoint_suffix`
:   The Azure endpoint suffix to connect to. The default value is `core.windows.net`.

`azure.client.CLIENT_NAME.key` ([Secure](/deploy-manage/security/secure-settings.md), [reloadable](../../security/secure-settings.md#reloadable-secure-settings))
:   The Azure secret key, which is used by the repository’s internal Azure client. Alternatively, use `sas_token`.

`azure.client.CLIENT_NAME.max_retries`
:   The number of retries to use when an Azure request fails. This setting helps control the exponential backoff policy. It specifies the number of retries that must occur before the snapshot fails. The default value is `3`. The initial backoff period is defined by Azure SDK as `30s`. Thus there is `30s` of wait time before retrying after a first timeout or failure. The maximum backoff period is defined by Azure SDK as `90s`.

`azure.client.CLIENT_NAME.proxy.host`
:   The host name of a proxy to connect to Azure through. By default, no proxy is used.

`azure.client.CLIENT_NAME.proxy.port`
:   The port of a proxy to connect to Azure through. By default, no proxy is used.

`azure.client.CLIENT_NAME.proxy.type`
:   Register a proxy type for the client. Supported values are `direct`, `http`, and `socks`. For example: `azure.client.default.proxy.type: http`. When `proxy.type` is set to `http` or `socks`, `proxy.host` and `proxy.port` must also be provided. The default value is `direct`.

`azure.client.CLIENT_NAME.sas_token` ([Secure](/deploy-manage/security/secure-settings.md), [reloadable](../../security/secure-settings.md#reloadable-secure-settings))
:   A shared access signatures (SAS) token, which the repository’s internal Azure client uses for authentication. The SAS token must have read (r), write (w), list (l), and delete (d) permissions for the repository base path and all its contents. These permissions must be granted for the blob service (b) and apply to resource types service (s), container (c), and object (o). Alternatively, use `key`.

`azure.client.CLIENT_NAME.timeout`
:   The client side timeout for any single request to Azure, as a [time unit](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#time-units). For example, a value of `5s` specifies a 5 second timeout. There is no default value, which means that {{es}} uses the [default value](https://azure.github.io/azure-storage-java/com/microsoft/azure/storage/RequestOptions.html#setTimeoutIntervalInMs(java.lang.Integer)) set by the Azure client.

`azure.client.CLIENT_NAME.endpoint`
:   The Azure endpoint to connect to. It must include the protocol used to connect to Azure.

`azure.client.CLIENT_NAME.secondary_endpoint`
:   The Azure secondary endpoint to connect to. It must include the protocol used to connect to Azure.

::::{admonition} Obtaining credentials from the environment
:class: note

:name: repository-azure-default-credentials

If you specify neither the `key` nor the `sas_token` settings for a client then {{es}} will attempt to automatically obtain credentials from the environment in which it is running using mechanisms built into the Azure SDK. This is ideal for when running {{es}} on the Azure platform.

When running {{es}} on an [Azure Virtual Machine](https://azure.microsoft.com/en-gb/products/virtual-machines), you should use [Azure Managed Identity](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview) to provide credentials to {{es}}. To use Azure Managed Identity, assign a suitably authorized identity to the Azure Virtual Machine on which {{es}} is running.

When running {{es}} in [Azure Kubernetes Service](https://azure.microsoft.com/en-gb/products/kubernetes-service), for instance using [{{eck}}](cloud-on-k8s.md#k8s-azure-workload-identity), you should use [Azure Workload Identity](https://azure.github.io/azure-workload-identity/docs/introduction.html) to provide credentials to {{es}}. To use Azure Workload Identity, mount the `azure-identity-token` volume as a subdirectory of the [{{es}} config directory](../../deploy/self-managed/configure-elasticsearch.md#config-files-location) and set the `AZURE_FEDERATED_TOKEN_FILE` environment variable to point to a file called `azure-identity-token` within the mounted volume.

The Azure SDK has several other mechanisms to automatically obtain credentials from its environment, but the two methods described above are the only ones that are tested and supported for use in {{es}}.

::::



## Repository settings [repository-azure-repository-settings]

The Azure repository supports the following settings, which may be specified when registering an Azure repository as follows:

```console
PUT _snapshot/my_backup
{
  "type": "azure",
  "settings": {
    "client": "secondary",
    "container": "my_container",
    "base_path": "snapshots_prefix"
  }
}
```
%  TEST[skip:we don’t have azure setup while testing this]

`client`
:   The name of the Azure repository client to use. Defaults to `default`.

`container`
:   Container name. You must create the azure container before creating the repository. Defaults to `elasticsearch-snapshots`.

`base_path`
:   Specifies the path within container to repository data. Defaults to empty (root directory).

    ::::{note}
    Don’t set `base_path` when configuring a snapshot repository for {{ECE}}. {{ECE}} automatically generates the `base_path` for each deployment so that multiple deployments may share the same bucket.
    ::::


`chunk_size`
:   Big files can be broken down into multiple smaller blobs in the blob store during snapshotting. It is not recommended to change this value from its default unless there is an explicit reason for limiting the size of blobs in the repository. Setting a value lower than the default can result in an increased number of API calls to the Azure blob store during snapshot create as well as restore operations compared to using the default value and thus make both operations slower as well as more costly. Specify the chunk size as a [byte unit](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#byte-units), for example: `10MB`, `5KB`, `500B`. Defaults to the maximum size of a blob in the Azure blob store which is `5TB`.

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


`location_mode`
:   `primary_only` or `secondary_only`. Defaults to `primary_only`. Note that if you set it to `secondary_only`, it will force `readonly` to true.

`delete_objects_max_size`
:   (integer) Sets the maxmimum batch size, betewen 1 and 256, used for `BlobBatch` requests. Defaults to 256 which is the maximum number supported by the [Azure blob batch API](https://learn.microsoft.com/en-us/rest/api/storageservices/blob-batch#remarks).

`max_concurrent_batch_deletes`
:   (integer) Sets the maximum number of concurrent batch delete requests that will be submitted for any individual bulk delete with `BlobBatch`. Note that the effective number of concurrent deletes is further limited by the Azure client connection and event loop thread limits. Defaults to 10, minimum is 1, maximum is 100.


## Repository validation rules [repository-azure-validation]

According to the [containers naming guide](https://docs.microsoft.com/en-us/rest/api/storageservices/Naming-and-Referencing-Containers—​Blobs—​and-Metadata), a container name must be a valid DNS name, conforming to the following naming rules:

* Container names must start with a letter or number, and can contain only letters, numbers, and the dash (-) character.
* Every dash (-) character must be immediately preceded and followed by a letter or number; consecutive dashes are not permitted in container names.
* All letters in a container name must be lowercase.
* Container names must be from 3 through 63 characters long.

::::{admonition} Supported Azure Storage Account types
:class: important

The Azure repository type works with all Standard storage accounts

* Standard Locally Redundant Storage - `Standard_LRS`
* Standard Zone-Redundant Storage - `Standard_ZRS`
* Standard Geo-Redundant Storage - `Standard_GRS`
* Standard Read Access Geo-Redundant Storage - `Standard_RAGRS`

[Premium Locally Redundant Storage](https://azure.microsoft.com/en-gb/documentation/articles/storage-premium-storage) (`Premium_LRS`) is **not supported** as it is only usable as VM disk storage, not as general storage.

::::



## Linearizable register implementation [repository-azure-linearizable-registers]

The linearizable register implementation for Azure repositories is based on Azure’s support for strongly consistent leases. Each lease may only be held by a single node at any time. The node presents its lease when performing a read or write operation on a protected blob. Lease-protected operations fail if the lease is invalid or expired. To perform a compare-and-exchange operation on a register, {{es}} first obtains a lease on the blob, then reads the blob contents under the lease, and finally uploads the updated blob under the same lease. This process ensures that the read and write operations happen atomically.
