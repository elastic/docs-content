---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/repository-azure.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
---

# Azure repository [repository-azure]

You can use [Azure Blob storage](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction) as a repository for [Snapshot and restore](../snapshot-and-restore.md).

{{es}} uses an internal client module to connect to Azure Blob storage, referred to in this document as the *Azure client* or the *Azure repository client*. Clients are configured through a combination of [secure settings](../../security/secure-settings.md) defined in the {{es}} keystore, and [standard settings](/deploy-manage/stack-settings.md) defined in the `elasticsearch.yml` configuration file.

## Setup [repository-azure-usage]

To enable Azure repositories, first configure an Azure repository client by specifying one or more settings of the form `azure.client.CLIENT_NAME.SETTING_NAME`. By default, `azure` repositories use a client named `default`, but you may specify a different client name when registering each repository.

The only mandatory setting for an Azure repository client is `account`, which is a [secure setting](../../security/secure-settings.md) defined in the {{es}} keystore. To provide this setting, use the `elasticsearch-keystore` tool on each node:

```sh
bin/elasticsearch-keystore add azure.client.default.account
```

If you adjust this setting after a node has started, call the [Nodes reload secure settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings) to reload the new value.

You may define more than one client by setting their `account` values. For example, to set the `default` client and another client called `secondary`, run the following commands on each node:

```sh
bin/elasticsearch-keystore add azure.client.default.account
bin/elasticsearch-keystore add azure.client.secondary.account
```

The `key` and `sas_token` settings are also secure settings and can be set using commands like the following:

```sh
bin/elasticsearch-keystore add azure.client.default.key
bin/elasticsearch-keystore add azure.client.secondary.sas_token
```

Other Azure repository client settings must be set in [`elasticsearch.yml`](/deploy-manage/stack-settings.md) before the node starts. For example:

```yaml
azure.client.default.timeout: 10s
azure.client.default.max_retries: 7
azure.client.default.endpoint_suffix: core.chinacloudapi.cn
azure.client.secondary.timeout: 30s
```

In this example, the client side timeout is `10s` per try for repositories which use the `default` client, with `7` retries before failing and an endpoint suffix of `core.chinacloudapi.cn`. Repositories which use the `secondary` client will have a timeout of `30s` per try, but will use the default endpoint and will fail after the default number of retries.

Once an Azure repository client is configured correctly, register an Azure repository as follows, providing the client name using the `client` [repository setting](elasticsearch://reference/elasticsearch/configuration-reference/azure-repository-settings.md#repository-azure-repository-settings):

```console
PUT _snapshot/my_backup
{
  "type": "azure",
  "settings": {
    "client": "secondary"
  }
}
```

If you are using the `default` client, you may omit the `client` repository setting:

```console
PUT _snapshot/my_backup
{
  "type": "azure"
}
```

::::{note}
In progress snapshot or restore jobs will not be preempted by a **reload** of the storage secure settings. They will complete using the client as it was built when the operation started.
::::



## Client settings [repository-azure-client-settings]

Available client settings include the Azure `account` name, authentication credentials (`key` or `sas_token`), `endpoint_suffix`, `timeout`, `max_retries`, and proxy configuration.

For a complete list of all Azure client settings, refer to [Azure repository client settings](elasticsearch://reference/elasticsearch/configuration-reference/azure-repository-settings.md#repository-azure-client-settings).

::::{admonition} Obtaining credentials from the environment
:class: note

:name: repository-azure-default-credentials

If you specify neither the `key` nor the `sas_token` settings for a client then {{es}} will attempt to automatically obtain credentials from the environment in which it is running using mechanisms built into the Azure SDK. This is ideal for when running {{es}} on the Azure platform.

When running {{es}} on an [Azure Virtual Machine](https://azure.microsoft.com/en-gb/products/virtual-machines), you should use [Azure Managed Identity](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview) to provide credentials to {{es}}. To use Azure Managed Identity, assign a suitably authorized identity to the Azure Virtual Machine on which {{es}} is running.

When running {{es}} in [Azure Kubernetes Service](https://azure.microsoft.com/en-gb/products/kubernetes-service), for instance using [{{eck}}](cloud-on-k8s.md#k8s-azure-workload-identity), you should use [Azure Workload Identity](https://azure.github.io/azure-workload-identity/docs/introduction.html) to provide credentials to {{es}}. To use Azure Workload Identity, mount the `azure-identity-token` volume as a subdirectory of the [{{es}} config directory](../../deploy/self-managed/configure-elasticsearch.md#config-files-location) and set the `AZURE_FEDERATED_TOKEN_FILE` environment variable to point to a file called `azure-identity-token` within the mounted volume.

The Azure SDK has several other mechanisms to automatically obtain credentials from its environment, but the two methods described above are the only ones that are tested and supported for use in {{es}}.

::::



## Repository settings [repository-azure-repository-settings]

The Azure repository supports a number of settings to customize how data is stored, which may be specified when creating the repository.

Available repository settings include the target `container`, `base_path`, `chunk_size`, `compress`, throughput throttling (`max_restore_bytes_per_sec`, `max_snapshot_bytes_per_sec`), `location_mode`, and batch delete tuning.

For a complete list of all Azure repository settings, refer to [Azure repository settings](elasticsearch://reference/elasticsearch/configuration-reference/azure-repository-settings.md#repository-azure-repository-settings).


## Repository validation rules [repository-azure-validation]

According to the [containers naming guide](https://docs.microsoft.com/en-us/rest/api/storageservices/Naming-and-Referencing-Containers—Blobs—and-Metadata), a container name must be a valid DNS name, conforming to the following naming rules:

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

The linearizable register implementation for Azure repositories is based on Azure's support for strongly consistent leases. Each lease may only be held by a single node at any time. The node presents its lease when performing a read or write operation on a protected blob. Lease-protected operations fail if the lease is invalid or expired. To perform a compare-and-exchange operation on a register, {{es}} first obtains a lease on the blob, then reads the blob contents under the lease, and finally uploads the updated blob under the same lease. This process ensures that the read and write operations happen atomically.
