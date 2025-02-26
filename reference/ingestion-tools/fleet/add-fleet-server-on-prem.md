---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/add-fleet-server-on-prem.html
---

# Deploy on-premises and self-managed [add-fleet-server-on-prem]

To use {{fleet}} for central management, a [{{fleet-server}}](/reference/ingestion-tools/fleet/fleet-server.md) must be running and accessible to your hosts.

You can deploy {{fleet-server}} on-premises and manage it yourself. In this [deployment model](/reference/ingestion-tools/fleet/deployment-models.md), you are responsible for high-availability, fault-tolerance, and lifecycle management of {{fleet-server}}.

This approach might be right for you if you would like to limit the control plane traffic out of your data center or have requirements for fully air-gapped operations. For example, you might take this approach if you need to satisfy data governance requirements or you want agents to only have access to a private segmented network.

This approach might *not* be right for you if you don’t want to manage the life cycle of your Elastic environment and instead would like that to be handled by Elastic.

When using this approach, it’s recommended that you provision multiple instances of the {{fleet-server}} and use a load balancer to better scale the deployment. You also have the option to use your organization’s certificate to establish a secure connection from {{fleet-server}} to {{es}}.

:::{image} images/fleet-server-on-prem-deployment.png
:alt: {{fleet-server}} on-premises deployment model
:::

To deploy a self-managed {{fleet-server}}, you need to:

* Satisfy all [compatibility requirements](#add-fleet-server-on-prem-compatibility) and [prerequisites](#add-fleet-server-on-prem-prereq).
* [Add a {{fleet-server}}](#add-fleet-server-on-prem-add-server) by installing an {{agent}} and enrolling it in an agent policy containing the {{fleet-server}} integration.

::::{note}
You can install only a single {{agent}} per host, which means you cannot run {{fleet-server}} and another {{agent}} on the same host unless you deploy a containerized {{fleet-server}}.
::::



## Compatibility [add-fleet-server-on-prem-compatibility]

{{fleet-server}} is compatible with the following Elastic products:

* {{stack}} 7.13 or later.

    * For version compatibility, {{es}} must be at the same or a later version than {{fleet-server}}, and {{fleet-server}} needs to be at the same or a later version than {{agent}} (not including patch releases).
    * {{kib}} should be on the same minor version as {{es}}.

* {{ece}} 2.9 or later

    * Requires additional wildcard domains and certificates (which normally only cover `*.cname`, not `*.*.cname`). This enables us to provide the URL for {{fleet-server}} of `https://.fleet.`.
    * The deployment template must contain an {{integrations-server}} node.

    For more information about hosting {{fleet-server}} on {{ece}}, refer to [Manage your {{integrations-server}}](/deploy-manage/deploy/cloud-enterprise/manage-integrations-server.md).



## Prerequisites [add-fleet-server-on-prem-prereq]

Before deploying, you need to:

* Obtain or generate a Cerfiticate Authority (CA) certificate.
* Ensure components have access to the ports needed for communication.


### CA certificate [add-fleet-server-on-prem-cert-prereq]

Before setting up {{fleet-server}} using this approach, you will need a CA certificate to configure Transport Layer Security (TLS) to encrypt traffic between the {{fleet-server}}s and the {{stack}}.

If your organization already uses the {{stack}}, you may already have a CA certificate. If you do not have a CA certificate, you can read more about generating one in [Configure SSL/TLS for self-managed {{fleet-server}}s](/reference/ingestion-tools/fleet/secure-connections.md).

::::{note}
This is not required when testing and iterating using the **Quick start** option, but should always be used for production deployments.
::::



### Default port assignments [default-port-assignments-on-prem]

When {{es}} or {{fleet-server}} are deployed, components communicate over well-defined, pre-allocated ports. You may need to allow access to these ports. Refer to the following table for default port assignments:

| Component communication | Default port |
| --- | --- |
| Elastic Agent → {{fleet-server}} | 8220 |
| Elastic Agent → {{es}} | 9200 |
| Elastic Agent → Logstash | 5044 |
| Elastic Agent → {{kib}} ({{fleet}}) | 5601 |
| {{fleet-server}} → {{kib}} ({{fleet}}) | 5601 |
| {{fleet-server}} → {{es}} | 9200 |

::::{note}
Connectivity to {{kib}} on port 5601 is optional and not required at all times. {{agent}} and {{fleet-server}} may need to connect to {{kib}} if deployed in a container environment where an enrollment token can not be provided during deployment.
::::



## Add {{fleet-server}} [add-fleet-server-on-prem-add-server]

A {{fleet-server}} is an {{agent}} that is enrolled in a {{fleet-server}} policy. The policy configures the agent to operate in a special mode to serve as a {{fleet-server}} in your deployment.

To add a {{fleet-server}}:

1. In {{fleet}}, open the **Agents** tab.
2. Click **Add {{fleet-server}}**.
3. This opens in-product instructions to add a {{fleet-server}} using one of two options: **Quick Start** or **Advanced**.

    * Use **Quick Start** if you want {{fleet}} to generate a {{fleet-server}} policy and enrollment token for you. The {{fleet-server}} policy will include a {{fleet-server}} integration plus a system integration for monitoring {{agent}}. This option generates self-signed certificates and is **not** recommended for production use cases.

        :::{image} images/add-fleet-server.png
        :alt: In-product instructions for adding a {{fleet-server}} in quick start mode
        :class: screenshot
        :::

    * Use **Advanced** if you want to either:

        * **Use your own {{fleet-server}} policy.** {{fleet-server}} policies manage and configure the {{agent}} running on {{fleet-server}} hosts to launch a {{fleet-server}} process. You can create a new {{fleet-server}} policy or select an existing one. Alternatively you can [create a {{fleet-server}} policy without using the UI](/reference/ingestion-tools/fleet/create-policy-no-ui.md), and then select the policy here.
        * **Use your own TLS certificates.** TLS certificates encrypt traffic between {{agent}}s and {{fleet-server}}. To learn how to generate certs, refer to [Configure SSL/TLS for self-managed {{fleet-server}}s](/reference/ingestion-tools/fleet/secure-connections.md).

            ::::{note}
            If you are providing your own certificates:

            * Before running the `install` command, make sure you replace the values in angle brackets.
            * Note that the URL specified by `--url` must match the DNS name used to generate the certificate specified by `--fleet-server-cert`.

            ::::


            :::{image} images/add-fleet-server-advanced.png
            :alt: In-product instructions for adding a {{fleet-server}} in advanced mode
            :class: screenshot
            :::

4. Step through the in-product instructions to configure and install {{fleet-server}}.

    ::::{note}
    * The fields to configure {{fleet-server}} hosts are not available if the hosts are already configured outside of {{fleet}}. For more information, refer to [{{fleet}} settings in {{kib}}](kibana://docs/reference/configuration-reference/fleet-settings.md).
    * When using the **Advanced** option, it’s recommended to generate a unique service token for each {{fleet-server}}. For other ways to generate service tokens, refer to [`elasticsearch-service-tokens`](elasticsearch://docs/reference/elasticsearch/command-line-tools/service-tokens-command.md).
    * If you’ve configured a non-default port for {{fleet-server}} in the {{fleet-server}} integration, you need to include the `--fleet-server-host` and `--fleet-server-port` options in the `elastic-agent install` command. Refer to the [install command documentation](/reference/ingestion-tools/fleet/agent-command-reference.md#elastic-agent-install-command) for details.

    ::::


    At the **Install Fleet Server to a centralized host** step, the `elastic-agent install` command installs an {{agent}} as a managed service and enrolls it in a {{fleet-server}} policy. For more {{fleet-server}} commands, refer to the [{{agent}} command reference](/reference/ingestion-tools/fleet/agent-command-reference.md).

5. If installation is successful, a confirmation indicates that {{fleet-server}} is set up and connected.

After {{fleet-server}} is installed and enrolled in {{fleet}}, the newly created {{fleet-server}} policy is applied. You can see this on the {{fleet-server}} policy page.

The {{fleet-server}} agent also shows up on the main {{fleet}} page as another agent whose life-cycle can be managed (like other agents in the deployment).

You can update your {{fleet-server}} configuration in {{kib}} at any time by going to: **Management** → **{{fleet}}** → **Settings**. From there you can:

* Update the {{fleet-server}} host URL.
* Configure additional outputs where agents should send data.
* Specify the location from where agents should download binaries.
* Specify proxy URLs to use for {{fleet-server}} or {{agent}} outputs.


## Troubleshooting [add-fleet-server-on-prem-troubleshoot]

If you’re unable to add a {{fleet}}-managed agent, click the **Agents** tab and confirm that the agent running {{fleet-server}} is healthy.


## Next steps [add-fleet-server-on-prem-next]

Now you’re ready to add {{agent}}s to your host systems. To learn how, see [Install {{fleet}}-managed {{agent}}s](/reference/ingestion-tools/fleet/install-fleet-managed-elastic-agent.md).

::::{note}
For on-premises deployments, you can dedicate a policy to all the agents in the network boundary and configure that policy to include a specific {{fleet-server}} (or a cluster of {{fleet-server}}s).

Read more in [Add a {{fleet-server}} to a policy](/reference/ingestion-tools/fleet/agent-policy.md#add-fleet-server-to-policy).

::::
