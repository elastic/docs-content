---
navigation_title: add_cloud_metadata
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/add-cloud-metadata-processor.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Add cloud metadata [add-cloud-metadata-processor]


::::{tip}
Inputs that collect logs and metrics use this processor by default, so you do not need to configure it explicitly.
::::


The `add_cloud_metadata` processor enriches each event with instance metadata from the machine’s hosting provider. At startup the processor queries a list of hosting providers and caches the instance metadata.

The following providers are supported:

* Amazon Web Services (AWS)
* Digital Ocean
* Google Compute Engine (GCE)
* [Tencent Cloud](https://www.qcloud.com/?lang=en) (QCloud)
* Alibaba Cloud (ECS)
* Huawei Cloud (ECS)
* Azure Virtual Machine
* Openstack Nova

The Alibaba Cloud and Tencent providers are disabled by default, because they require to access a remote host. Use the `providers` setting to select a list of default providers to query.


## Example [_example_2]

This configuration enables the processor:

```yaml
  - add_cloud_metadata: ~
```

The metadata that is added to events varies by hosting provider. For examples, refer to [Provider-specific metadata examples](#provider-specific-examples).


## Configuration settings [_configuration_settings]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that they process the raw event data rather than the final event sent to {{es}}. For related limitations, refer to [What are some limitations of using processors?](/reference/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `timeout` | No | `3s` | Maximum amount of time to wait for a successful response when detecting the hosting provider. If a timeout occurs, no instance metadata is added to the events. This makes it possible to enable this processor for all your deployments (in the cloud or on-premise). |
| `providers` | No |  | List of provider names to use. If `providers` is not configured, all providers that do not access a remote endpoint are enabled by default. The list of providers may alternatively be configured with the environment variable `BEATS_ADD_CLOUD_METADATA_PROVIDERS`, by setting it to a comma-separated list of provider names.<br><br>The list of supported provider names includes:<br><br>* `alibaba` or `ecs` for the Alibaba Cloud provider (disabled by default).<br>* `azure` for Azure Virtual Machine (enabled by default).<br>* `digitalocean` for Digital Ocean (enabled by default).<br>* `aws` or `ec2` for Amazon Web Services (enabled by default).<br>* `gcp` for Google Compute Engine (enabled by default).<br>* `openstack` or `nova` for Openstack Nova (enabled by default).<br>* `openstack-ssl` or `nova-ssl` for Openstack Nova when SSL metadata APIs are enabled (enabled by default).<br>* `tencent` or `qcloud` for Tencent Cloud (disabled by default).<br>* `huawei` for Huawei Cloud (enabled by default).<br> |
| `overwrite` | No | `false` | Whether to overwrite existing cloud fields. If `true`, the processor overwrites existing `cloud.*` fields. |

The `add_cloud_metadata` processor supports SSL options to configure the http client used to query cloud metadata.

For more information, refer to [SSL/TLS](/reference/fleet/elastic-agent-ssl-configuration.md), specifically the settings under [Table 7, Common configuration options](/reference/fleet/elastic-agent-ssl-configuration.md#common-ssl-options) and [Table 8, Client configuration options](/reference/fleet/elastic-agent-ssl-configuration.md#client-ssl-options).


### Control Azure credential selection

After the Azure provider detects an Azure VM, the processor automatically makes a best-effort Azure Resource Manager lookup for the AKS cluster name and ID. These fields are optional, but the processor attempts the lookup even when the VM is not an AKS node. Because inputs that collect logs and metrics enable this processor by default, the lookup can occur without an explicit processor configuration.

If `TENANT_ID`, `CLIENT_ID`, and `CLIENT_SECRET` are all present, the processor uses an explicit client secret. Otherwise, it uses the Azure SDK for Go `DefaultAzureCredential` chain. Depending on the {{agent}} version, development-focused credentials in the bundled default chain may start Azure CLI, Azure Developer CLI, or Azure PowerShell on Windows. `AzurePowerShellCredential` is in the chain in {{agent}} 9.1.8 and later 9.1 releases, 9.2.2 and later 9.2 releases, and all 9.3 and later releases; when included, it invokes PowerShell with an encoded command.

{applies_to}`stack: ga 9.1.3+` {applies_to}`serverless: ga` In production, you can exclude development credentials by setting `AZURE_TOKEN_CREDENTIALS=prod` in the {{agent}} process environment and restarting {{agent}}. This setting retains `EnvironmentCredential`, `WorkloadIdentityCredential`, and `ManagedIdentityCredential`. For details, refer to Microsoft's guidance on [excluding a credential type category](https://learn.microsoft.com/en-us/azure/developer/go/sdk/authentication/credential-chains#exclude-a-credential-type-category). On Windows, follow the [Windows service environment procedure](/reference/fleet/host-proxy-env-vars.md#where-to-set-proxy-env-vars) to set the variable and restart {{agent}}.

::::{note}
{applies_to}`stack: ga 9.1.3+` {applies_to}`serverless: ga` `AZURE_TOKEN_CREDENTIALS` applies process-wide to components that use `DefaultAzureCredential`. It does not disable Azure metadata collection or the AKS lookup, and a retained credential can still make Azure Resource Manager requests. Excluding `azure` from the processor's `providers` setting is broader because it also removes basic Azure VM metadata.
::::


## Provider-specific metadata examples [provider-specific-examples]

The following sections show examples for each of the supported providers.


### AWS [_aws]

```json
{
  "cloud": {
    "account.id": "123456789012",
    "availability_zone": "us-east-1c",
    "instance.id": "i-4e123456",
    "machine.type": "t2.medium",
    "image.id": "ami-abcd1234",
    "provider": "aws",
    "region": "us-east-1"
  }
}
```


### Digital Ocean [_digital_ocean]

```json
{
  "cloud": {
    "instance.id": "1234567",
    "provider": "digitalocean",
    "region": "nyc2"
  }
}
```


### GCP [_gcp]

```json
{
  "cloud": {
    "availability_zone": "us-east1-b",
    "instance.id": "1234556778987654321",
    "machine.type": "f1-micro",
    "project.id": "my-dev",
    "provider": "gcp"
  }
}
```


### Tencent Cloud [_tencent_cloud]

```json
{
  "cloud": {
    "availability_zone": "gz-azone2",
    "instance.id": "ins-qcloudv5",
    "provider": "qcloud",
    "region": "china-south-gz"
  }
}
```


### Huawei Cloud [_huawei_cloud]

```json
{
  "cloud": {
    "availability_zone": "cn-east-2b",
    "instance.id": "37da9890-8289-4c58-ba34-a8271c4a8216",
    "provider": "huawei",
    "region": "cn-east-2"
  }
}
```


### Alibaba Cloud [_alibaba_cloud]

This metadata is only available when VPC is selected as the network type of the ECS instance.

```json
{
  "cloud": {
    "availability_zone": "cn-shenzhen",
    "instance.id": "i-wz9g2hqiikg0aliyun2b",
    "provider": "ecs",
    "region": "cn-shenzhen-a"
  }
}
```


### Azure Virtual Machine [_azure_virtual_machine]

```json
{
  "cloud": {
    "provider": "azure",
    "instance.id": "04ab04c3-63de-4709-a9f9-9ab8c0411d5e",
    "instance.name": "test-az-vm",
    "machine.type": "Standard_D3_v2",
    "region": "eastus2"
  }
}
```


### Openstack Nova [_openstack_nova]

```json
{
  "cloud": {
    "instance.name": "test-998d932195.mycloud.tld",
    "instance.id": "i-00011a84",
    "availability_zone": "xxxx-az-c",
    "provider": "openstack",
    "machine.type": "m2.large"
  }
}
```

