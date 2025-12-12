---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-settings.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Fleet settings [fleet-settings]

::::{note}
The settings described here are configurable through the {{fleet}} UI. Refer to [{{fleet}} settings in {{kib}}](kibana://reference/configuration-reference/fleet-settings.md) for a list of settings that you can configure in the [`kibana.yml`](/deploy-manage/stack-settings.md) configuration file.
::::


On the **Settings** tab in **Fleet**, you can configure global settings available to all {{agent}}s enrolled in {{fleet}}. This includes {{fleet-server}} hosts and output settings.


## {{fleet-server}} host settings [fleet-server-hosts-setting]

Select **Edit hosts** and specify the host URLs your {{agent}}s will use to connect to a {{fleet-server}}.

::::{tip}
If the **Edit hosts** option is grayed out, {{fleet-server}} hosts are configured outside of {{fleet}}. For more information, refer to [{{fleet}} settings in {{kib}}](kibana://reference/configuration-reference/fleet-settings.md).
::::


Not sure if {{fleet-server}} is running? Refer to [What is {{fleet-server}}?](/reference/fleet/fleet-server.md).

On self-managed clusters, you must specify one or more URLs.

On {{ecloud}}, this field is populated automatically. If you are using Azure Private Link, GCP Private Service Connect, or AWS PrivateLink and enrolling the {{agent}} with a private link URL, ensure that this setting is configured. Otherwise, {{agent}} will reset to use a default address instead of the private link URL.

::::{note}
If a URL is specified without a port, {{kib}} sets the port to `80` (http) or `443` (https).
::::


By default, {{fleet-server}} is typically exposed on the following ports:

`8220`
:   Default {{fleet-server}} port for self-managed clusters

`443` or `9243`
:   Default {{fleet-server}} port for {{ecloud}}. View the {{fleet}} **Settings** tab to find the actual port that’s used.

::::{important}
The exposed ports must be open for ingress and egress in the firewall and networking rules on the host to allow {{agent}}s to communicate with {{fleet-server}}.
::::


Specify multiple URLs (select **Add row**) to scale out your deployment and provide automatic failover. If multiple URLs exist, {{fleet}} shows the first provided URL for enrollment purposes. Enrolled {{agent}}s will connect to the URLs in round robin order until they connect successfully.

When a {{fleet-server}} is added or removed from the list, all agent policies are updated automatically.

**Examples:**

* `https://192.0.2.1:8220`
* `https://abae718c1276457893b1096929e0f557.fleet.eu-west-1.aws.qa.cld.elstc.co:443`
* `https://[2001:db8::1]:8220`


## Output settings [output-settings]

Add or edit output settings to specify where {{agent}}s send data. {{agent}}s use the default output if you don’t select an output in the agent policy.

::::{tip}
If your [Elastic subscription level](https://www.elastic.co/subscriptions) supports **per integration output assignment**, you can configure {{agent}} to [send data to different outputs for different integration policies](/reference/fleet/integration-level-outputs.md).
::::


::::{note}
The {{ecloud}} internal output is locked and cannot be edited. This output is used for internal routing to reduce external network charges when using the {{ecloud}} agent policy. It also provides visibility for troubleshooting on {{ece}}.
::::


To add or edit an output:

1. Go to **{{fleet}}** > **Settings**.
2. Under **Outputs**, select **Add output** or **Edit**.

    :::{image} images/fleet-add-output-button.png
    :alt: {{fleet}} Add output button
    :::

    The **Add new output** UI opens.

3. Set the output name and type.
4. Specify settings for the output type you selected:

    * [{{es}} output settings](/reference/fleet/es-output-settings.md)
    * [{{ls}} output settings](/reference/fleet/ls-output-settings.md)
    * [Kafka output settings](/reference/fleet/kafka-output-settings.md)
    * [Remote {{es}} output](/reference/fleet/remote-elasticsearch-output.md)

5. Select **Save and apply settings**.

::::{tip}
If the options for editing an output are grayed out, outputs are configured outside of {{fleet}}. For more information, refer to [{{fleet}} settings in {{kib}}](kibana://reference/configuration-reference/fleet-settings.md).
::::

## Agent binary download settings [fleet-agent-binary-download-settings]

{{agent}}s must be able to access the {{artifact-registry}} to download binaries during upgrades. By default {{agent}}s download artifacts from the artifact registry at `https://artifacts.elastic.co/downloads/`.

For {{agent}}s that cannot access the internet, you can specify agent binary download settings, and then configure agents to download their artifacts from the alternate location. For more information about running {{agent}}s in a restricted environment, refer to [Air-gapped environments](/reference/fleet/air-gapped.md).

To add or edit the source of binary downloads:

1. Go to **{{fleet}}** > **Settings**.
2. Under **Agent Binary Download**, select **Add agent binary source** or **Edit**.
3. Set the agent binary source name.
4. For **Host**, specify the address where you are hosting the artifacts repository.
5. (Optional) To make this location the default, select **Make this host the default for all agent policies**. {{agent}}s use the default location if you don’t select a different agent binary source in the agent policy.


### Configure SSL for binary downloads [agent-binary-ssl]
```{applies_to}
  stack: ga 9.1
```

You can optionally secure connections to your binary download source using TLS. These settings correspond to the certificates the agent uses when connecting to the download host.

The following SSL options are available when adding or editing an agent binary source:

| **UI Field**           | **Purpose**                                                                  |
|------------------------|------------------------------------------------------------------------------|
| Certificate authorities | Trusted CAs for verifying the server certificate.                           |
| Certificate             | Client certificate to use for mTLS authentication with the download host.  |
| Certificate key         | Private key associated with the client certificate.                         |


## Proxies [proxy-settings]

You can specify a proxy server to be used in {{fleet-server}}, {{agent}} outputs, or for any agent binary download sources. For full details about proxy configuration refer to [Using a proxy server with {{agent}} and {{fleet}}](/reference/fleet/fleet-agent-proxy-support.md).

## Advanced settings [fleet-advanced-settings]

On the **{{fleet}}** > **Settings** page, you can also configure {{fleet}} to automatically delete unenrolled agents or to display agentless resources for inspection and diagnostics purposes.

### Delete unenrolled agents [delete-unenrolled-agents-setting]

After an {{agent}} has been unenrolled in {{fleet}}, a number of documents about the agent are retained in case the agent needs to be recovered at some point. You can choose to have all data related to an unenrolled agent deleted automatically.

This option can also be enabled by adding the `xpack.fleet.enableDeleteUnenrolledAgents: true` setting to the [{{kib}} settings file](/deploy-manage/stack-settings.md#kib-settings).

To enable automatic deletion of unenrolled agents:

1. Go to **{{fleet}}** > **Settings**.
2. In the **Advanced Settings** section, enable the **Delete unenrolled agents** option.

### Show agentless resources [show-agentless-resources-setting]

```{applies_to}
stack: ga 9.1.6
serverless: ga
```

If you have [agentless integrations](/solutions/security/get-started/agentless-integrations.md) deployed, you can enable the **Show agentless resources** option to display agentless agents and policies in {{fleet}} for inspection and diagnostics purposes. This setting is stored locally, and it's only visible to you.

To display agentless resources in the agent and agent policy lists:

1. Go to **{{fleet}}** > **Settings**.
2. In the **Advanced Settings** section, enable **Show agentless resources**.

You can view and request diagnostics for agentless agents, but you cannot upgrade, unenroll, or reassign them.