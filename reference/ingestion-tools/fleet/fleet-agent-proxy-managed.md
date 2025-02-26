---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-agent-proxy-managed.html
---

# Fleet managed Elastic Agent connectivity using a proxy server [fleet-agent-proxy-managed]

Proxy settings in the {{agent}} policy override proxy settings specified by environment variables. This means you can specify proxy settings for {{agent}} that are different from host or system-level environment settings.

This page describes where a proxy server is allowed in your deployment and how to configure proxy settings for {{agent}} and {{fleet}}. The steps for deploying the proxy server itself are beyond the scope of this article.

{{agents}} generally egress two sets of connections, one for Control plane traffic to the {{fleet-server}}, the other Data plane traffic to an output such as {{es}}. In a similar fashion operators would place {{agent}} behind a proxy server, and proxy the control and data plane traffic to their final destinations.

{{fleet}} central management enables you to define your proxy servers and then configure an output or the {{fleet-server}} to be reachable through any of these proxies. This also enables you to modify the proxy server details if needed without having to re-install {{agents}}.

:::{image} images/agent-proxy-server-managed-deployment.png
:alt: Image showing connections between {{fleet}} managed {agent}
:::

In this scenario Fleet Server and Elasticsearch are deployed in {{ecloud}} and reachable on port 443.

## Configuring proxy servers in {{fleet}} for managed agents [fleet-agent-proxy-server-managed-agents]

These steps describe how to set up {{fleet}} components to use a proxy.

1. **Globally add proxy server details to {{fleet}}.**

    1. In {{fleet}}, open the **Settings** tab.
    2. Select **Add proxy**. The **Add proxy** or **Edit proxy** flyout opens.

        :::{image} images/elastic-agent-proxy-edit-proxy.png
        :alt: Screen capture of the Edit Proxy UI in Fleet
        :::

    3. Add a name for the proxy (in this example `Proxy-A`) and specify the Proxy URL.
    4. Add any other optional settings.
    5. Select **Save and apply settings**. The proxy information is saved and that proxy is ready for other components in {{fleet}} to reference.

2. **Attach the proxy to a {{fleet-server}}.**

    If the control plane traffic to/from the Fleet Server needs to also go through the proxy server, the proxy created needs to also be added to the definition of that Fleet Server.

    1. In {{fleet}}, open the **Settings** tab.
    2. In the list of **Fleet Server Hosts**, choose a host and select the edit button to configure it.
    3. In the **Proxy** section dropdown list, select the proxy that you configured.

        :::{image} images/elastic-agent-proxy-edit-fleet-server.png
        :alt: Screen capture of the Edit Fleet Server UI
        :::

        In this example, All the {{agents}} in a policy that uses this {{fleet-server}} will now connect to the {{fleet-server}} through the proxy server defined in `Proxy-A`.


    :::::{admonition}
    ::::{warning}
    Any invalid changes to the {{fleet-server}} definition that may cause connectivity issues between the {{agents}} and the {{fleet-server}} will cause them to disconnect. The only remedy would be to re-install the affected agents. This is because the connectivity to the {{fleet-server}} ensures policy updates reach the agents. If a policy with an invalid host address reaches the agent it will no longer be able to connect and therefore won’t receive any other updates from the {{fleet-server}} (including the corrected setting). In this regard, adding a proxy server that is not reachable by the agents will break connectivity to the {{fleet-server}}.
    ::::


    :::::

3. **Attach the proxy to the output**

    Similarly, if the data plane traffic to an output is to traverse via a proxy, that proxy definition would need to be added to the output defined in the Fleet.

    1. In {{fleet}}, open the **Settings** tab.
    2. In the list of **Outputs**, choose an output and select the edit button to configure it.
    3. In the **Proxy** section dropdown list, select the proxy that you configured.

        :::{image} images/elastic-agent-proxy-edit-output.png
        :alt: Screen capture of the Edit output UI in Fleet
        :::

        In this example, All the {{agents}} in a policy that is configured to write to the chosen output will now write to that output through the proxy server defined in `Proxy-A`.


    :::::{admonition}
    ::::{warning}
    If agents are unable to reach the configured proxy server, they will not be able to write data to the output that has the proxy server configured. When changing the proxy of an output, please ensure that the affected agents all have connectivity to the proxy itself.
    ::::


    :::::

4. **Attach the proxy to the agent download source**

    Likewise, if the download traffic to or from the artifact registry needs to go through the proxy server, that proxy definition also needs to be added to the agent binary source defined in {{Fleet}}.

    1. In {{fleet}}, open the **Settings** tab.
    2. In the **Agent Binary Download** list, choose an agent binary source and select the edit button to configure it.
    3. In the **Proxy** section dropdown list, select the proxy that you configured.

        :::{image} images/elastic-agent-proxy-edit-agent-binary-source.png
        :alt: Screen capture of the Edit agent binary source UI in Fleet
        :::

        In this example, all of the {{agents}} enrolled in a policy that is configured to download from the chosen agent download source will now download from that agent download source through the proxy server defined in `Proxy-A`.


    :::::{admonition}
    ::::{warning}
    If agents are unable to reach the configured proxy server, they will not be able to download binaries from the agent download source that has the proxy server configured. When changing the proxy of an agent binary source, please ensure that the affected agents all have connectivity to the proxy itself.
    ::::


    :::::

5. **Configure the {{agent}} policy**

    You can now configure the {{agent}} policy to use the {{fleet-server}} and the outputs that are reachable through a proxy server.

    * If the policy is configured with a {{fleet-server}} that has a proxy attached to it, all the control plane traffic from the agents in that policy will reach the {{fleet-server}} through that proxy.
    * Similarly, if the output definition has a proxy attached to it, all the agents in that policy will write (data plane) to the output through the proxy.

6. **Enroll the {{agents}}**

    Now that {{fleet}} is configured, all policy downloads will update the agent with the latest configured proxies. When the agent is first installed it needs to communicate with {{fleet}} (through {{fleet-server}}) in order to download its first policy configuration.



### Set the proxy for retrieving agent policies from {{fleet}} [cli-proxy-settings]

If there is a proxy between {{agent}} and {{fleet}}, specify proxy settings on the command line when you install {{agent}} and enroll in {{fleet}}. The settings you specify at the command line are added to the `fleet.yml` file installed on the system where the {{agent}} is running.

::::{note}
If the initial agent communication with {{fleet}} (i.e control plane) needs to traverse the proxy server, then the agent needs to be configured to do so using the `–proxy-url` command line flag which is applied during the agent installation. Once connectivity to {{fleet}} is established, proxy server details can be managed through the UI.
::::


::::{note}
If {{kib}} is behind a proxy server, you’ll still need to [configure {{kib}} settings](/reference/ingestion-tools/fleet/epr-proxy-setting.md) to access the package registry.
::::


The `enroll` and `install` commands accept the following flags:

| CLI flag | Description |
| --- | --- |
| `--proxy-url <url>` | URL of the proxy server. The value may be either a complete URL or a`host[:port]`, in which case the `http` scheme is assumed.  The URL accepts optionalusername and password settings for authenticating with the proxy. For example:`http://<username>:<password>@<proxy host>/`. |
| `--proxy-disabled` | If specified, all proxy settings, including the `HTTP_PROXY` and `HTTPS_PROXY`environment variables, are ignored. |
| `--proxy-header <header name>=<value>` | Additional header to send to the proxy during CONNECT requests. Use the`--proxy-header` flag multiple times to add additional headers. You can usethis setting to pass keys/tokens required for authenticating with the proxy. |

For example:

```sh
elastic-agent install --url="https://10.0.1.6:8220" --enrollment-token=TOKEN --proxy-url="http://10.0.1.7:3128" --fleet-server-es-ca="/usr/local/share/ca-certificates/es-ca.crt" --certificate-authorities="/usr/local/share/ca-certificates/fleet-ca.crt"
```

The command in the previous example adds the following settings to the `fleet.yml` policy on the host where {{agent}} is installed:

```yaml
fleet:
  enabled: true
  access_api_key: API-KEY
  hosts:
  - https://10.0.1.6:8220
  ssl:
    verification_mode: ""
    certificate_authorities:
    - /usr/local/share/ca-certificates/es-ca.crt
    renegotiation: never
  timeout: 10m0s
  proxy_url: http://10.0.1.7:3128
  reporting:
    threshold: 10000
    check_frequency_sec: 30
  agent:
    id: ""
```

::::{note}
When {{agent}} runs, the `fleet.yml` file gets encrypted and renamed to `fleet.enc`.
::::



## {{agent}} connectivity using a secure proxy gateway [fleet-agent-proxy-server-secure-gateway]

Many secure proxy gateways are configured to perform mutual TLS and expect all connections to present their certificate. In these instances the Client (in this case the Elastic Agent) would need to present a certificate and key to the Server (the secure proxy). In return the client expects to see a certificate authority chain from the server to ensure it is also communicating to a trusted entity.

:::{image} images/elastic-agent-proxy-gateway-secure.png
:alt: Image showing data flow between the proxy server and the Certificate Authority
:::

If mTLs is a requirement when connecting to your proxy server, then you have the option to add the Client certificate and Client certificate key to the proxy. Once configured, all the Elastic Agents in a policy that connect to this secure proxy (via an output or fleet server), will use the nominated certificates to establish connections to the proxy server.

It should be noted that the user can define a local path to the certificate and key as in many common scenarios the certificate and key will be unique for each Elastic Agent.

Equally important is the Certificate Authority that the agents need to use to validate the certificate they are receiving from the secure proxy server. This can also be added when creating the proxy definition in the Fleet settings.

:::{image} images/elastic-agent-edit-proxy-secure-settings.png
:alt: Screen capture of the Edit Proxy UI
:::

::::{note}
Currently {{agents}} will not present a certificate for Control Plane traffic to the {{fleet-server}}. Some proxy servers are setup to mandate that the client setting up a connection presents a certificate to them before allowing that client to connect. This issue will be resolved by [issue #2248](https://github.com/elastic/elastic-agent/issues/2248). Our recommendation is to avoid adding a secure proxy as such in a {{fleet-server}} configuration flyout.
::::


::::{note}
In case {{kib}} is behind a proxy server or is otherwise unable to access the {{package-registry}} to download package metadata and content, refer to [Set the proxy URL of the {{package-registry}}](/reference/ingestion-tools/fleet/epr-proxy-setting.md).
::::
