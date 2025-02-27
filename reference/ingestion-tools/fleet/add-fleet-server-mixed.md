---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/add-fleet-server-mixed.html
---

# Deploy Fleet Server on-premises and Elasticsearch on Cloud [add-fleet-server-mixed]

To use {{fleet}} for central management, a [{{fleet-server}}](/reference/ingestion-tools/fleet/fleet-server.md) must be running and accessible to your hosts.

Another approach is to deploy a cluster of {{fleet-server}}s on-premises and connect them back to {{ecloud}} with access to {{es}} and {{kib}}. In this [deployment model](/reference/ingestion-tools/fleet/deployment-models.md), you are responsible for high-availability, fault-tolerance, and lifecycle management of {{fleet-server}}.

This approach might be right for you if you would like to limit the control plane traffic out of your data center. For example, you might take this approach if you are a managed service provider or a larger enterprise that segregates its networks.

This approach might *not* be right for you if you don’t want to manage the life cycle of an extra compute resource in your environment for {{fleet-server}} to reside on.

:::{image} images/fleet-server-on-prem-es-cloud.png
:alt: {{fleet-server}} on-premise and {{es}} on Cloud deployment model
:::

To deploy a self-managed {{fleet-server}} on-premises to work with an {{ech}} deployment, you need to:

* Satisfy all [compatibility requirements](#add-fleet-server-mixed-compatibility) and [prerequisites](#add-fleet-server-mixed-prereq)
* Create a [{{fleet-server}} policy](#fleet-server-create-policy)
* [Add {{fleet-server}}](#fleet-server-add-server) by installing an {{agent}} and enrolling it in an agent policy containing the {{fleet-server}} integration


## Compatibility [add-fleet-server-mixed-compatibility]

{{fleet-server}} is compatible with the following Elastic products:

* {{stack}} 7.13 or later

    * For version compatibility, {{es}} must be at the same or a later version than {{fleet-server}}, and {{fleet-server}} needs to be at the same or a later version than {{agent}} (not including patch releases).
    * {{kib}} should be on the same minor version as {es}

* {{ece}} 2.9 or later—​allows you to use a hosted {{fleet-server}} on {{ecloud}}.

    * Requires additional wildcard domains and certificates (which normally only cover `*.cname`, not `*.*.cname`). This enables us to provide the URL for {{fleet-server}} of `https://.fleet.`.
    * The deployment template must contain an {{integrations-server}} node.

    For more information about hosting {{fleet-server}} on {{ece}}, refer to [Manage your {{integrations-server}}](/deploy-manage/deploy/cloud-enterprise/manage-integrations-server.md).



## Prerequisites [add-fleet-server-mixed-prereq]

Before deploying, you need to:

* Obtain or generate a Cerfiticate Authority (CA) certificate.
* Ensure components have access to the default ports needed for communication.


### CA certificate [add-fleet-server-mixed-cert-prereq]

Before setting up {{fleet-server}} using this approach, you will need a CA certificate to configure Transport Layer Security (TLS) to encrypt traffic between the {{fleet-server}}s and the {{stack}}.

If your organization already uses the {{stack}}, you may already have a CA certificate. If you do not have a CA certificate, you can read more about generating one in [Configure SSL/TLS for self-managed {{fleet-server}}s](/reference/ingestion-tools/fleet/secure-connections.md).

::::{note}
This is not required when testing and iterating using the **Quick start** option, but should always be used for production deployments.
::::



### Default port assignments [default-port-assignments-mixed]

When {{es}} or {{fleet-server}} are deployed, components communicate over well-defined, pre-allocated ports. You may need to allow access to these ports. See the following table for default port assignments:

| Component communication | Default port |
| --- | --- |
| Elastic Agent → {{fleet-server}} | 8220 |
| Elastic Agent → {{es}} | 443 |
| Elastic Agent → Logstash | 5044 |
| Elastic Agent → {{kib}} ({{fleet}}) | 443 |
| {{fleet-server}} → {{kib}} ({{fleet}}) | 443 |
| {{fleet-server}} → {{es}} | 443 |

::::{note}
If you do not specify the port for {{es}} as 443, the {{agent}} defaults to 9200.
::::



## Create a {{fleet-server}} policy [fleet-server-create-policy]

First, create a {{fleet-server}} policy. The {{fleet-server}} policy manages and configures the {{agent}} running on the {{fleet-server}} host to launch a {{fleet-server}} process.

To create a {{fleet-server}} policy:

1. In {{fleet}}, open the **Agent policies** tab.
2. Click on the **Create agent policy** button, then:

    1. Provide a meaningful name for the policy that will help you identify this {{fleet-server}} (or cluster) in the future.
    2. Ensure you select *Collect system logs and metrics* so the compute system hosting this {{fleet-server}} can be monitored. (This is not required, but is highly recommended.)

3. After creating the {{fleet-server}} policy, navigate to the policy itself and click **Add integration**.
4. Search for and select the **{{fleet-server}}** integration.
5. Then click **Add {{fleet-server}}**.
6. Configure the {{fleet-server}}:

    1. Expand **Change default**. Because you are deploying this {{fleet-server}} on-premises, you need to enter the *Host* address and *Port* number, `8220`. (In our example the {{fleet-server}} will be installed on the host `10.128.0.46`.)
    2. It’s recommended that you also enter the *Max agents* you intend to support with this {{fleet-server}}. This can also be modified at a later stage. This will allow the {{fleet-server}} to handle the load and frequency of updates being sent to the agent and ensure a smooth operation in a bursty environment.



## Add {{fleet-server}}s [fleet-server-add-server]

Now that the policy exists, you can add {{fleet-server}}s.

A {{fleet-server}} is an {{agent}} that is enrolled in a {{fleet-server}} policy. The policy configures the agent to operate in a special mode to serve as a {{fleet-server}} in your deployment.

To add a {{fleet-server}}:

1. In {{fleet}}, open the **Agents** tab.
2. Click **Add {{fleet-server}}**.
3. This will open in-product instructions for adding a {{fleet-server}} using one of two options. Choose **Advanced**.

    :::{image} images/add-fleet-server-advanced.png
    :alt: In-product instructions for adding a {{fleet-server}} in advanced mode
    :class: screenshot
    :::

4. Follow the in-product instructions to add a {{fleet-server}}.

    1. Select the agent policy that you created for this deployment.
    2. Choose **Production** as your deployment mode.

        Production mode is the fully secured mode where TLS certificates ensure a secure communication between {{fleet-server}} and {{es}}.

    3. Open the **{{fleet-server}} Hosts** dropdown and select **Add new {{fleet-server}} Hosts**. Specify one or more host URLs your {{agent}}s will use to connect to {{fleet-server}}. For example, `https://192.0.2.1:8220`, where `192.0.2.1` is the host IP where you will install {{fleet-server}}.
    4. A **Service Token** is required so the {{fleet-server}} can write data to the connected {{es}} instance. Click **Generate service token** and copy the generated token.
    5. Copy the installation instructions provided in {{kib}}, which include some of the known deployment parameters.
    6. Replace the value of the `--certificate-authorities` parameter with your [CA certificate](#add-fleet-server-mixed-prereq).

5. If installation is successful, a confirmation indicates that {{fleet-server}} is set up and connected.

After {{fleet-server}} is installed and enrolled in {{fleet}}, the newly created {{fleet-server}} policy is applied. You can see this on the {{fleet-server}} policy page.

The {{fleet-server}} agent will also show up on the main {{fleet}} page as another agent whose life-cycle can be managed (like other agents in the deployment).

You can update your {{fleet-server}} configuration in {{kib}} at any time by going to: **Management** → **{{fleet}}** → **Settings**. From there you can:

* Update the {{fleet-server}} host URL.
* Configure additional outputs where agents will send data.
* Specify the location from where agents will download binaries.
* Specify proxy URLs to use for {{fleet-server}} or {{agent}} outputs.


## Next steps [fleet-server-install-agents]

Now you’re ready to add {{agent}}s to your host systems. To learn how, see [Install {{fleet}}-managed {{agent}}s](/reference/ingestion-tools/fleet/install-fleet-managed-elastic-agent.md).

::::{note}
For on-premises deployments, you can dedicate a policy to all the agents in the network boundary and configure that policy to include a specific {{fleet-server}} (or a cluster of {{fleet-server}}s).

Read more in [Add a {{fleet-server}} to a policy](/reference/ingestion-tools/fleet/agent-policy.md#add-fleet-server-to-policy).

::::
