---
navigation_title: Manage Integrations Server 
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-manage-integrations-server.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Manage Integrations Server in {{ece}} [ece-manage-integrations-server]

For deployments that are version 8.0 and later, you have the option to add a combined [Application Performance Monitoring (APM) Server](/solutions/observability/apm/index.md) and [Fleet Server](/reference/fleet/index.md) to your deployment. APM allows you to monitor software services and applications in real time, turning that data into documents stored in the {{es}} cluster. Fleet allows you to centrally manage Elastic Agents on many hosts.

As part of provisioning, the APM Server and Fleet Server are already configured to work with {{es}} and {{kib}}. At the end of provisioning, you are shown the secret token to configure communication between the APM Server and the backend [APM Agents](/reference/apm-agents/index.md). The APM Agents get deployed within your services and applications.

From the deployment **Integrations Server** page you can also:

* Get the URL to complete the APM agent configuration.
* Use the `elastic` credentials to go to the APM area of {{kib}}. Step by step instructions to configure a variety of agents are available right in {{kib}}. After that, you can use the pre-built, dedicated dashboards and the APM tab to visualize the data that is sent back from the APM Agents.
* Use the `elastic` credentials to go to the Fleet area of {{kib}}. Step by step instructions to download and install Elastic Agent on your hosts are available right in {{kib}}. After that, you can manage enrolled Elastic Agents on the **Agents** tab, and the data shipped back from those Elastic Agents on the **Data streams** tab.
* Access the Integrations Server logs and metrics.
* Stop and restart your Integrations Server.
* Upgrade your Integrations Server version if it is out of sync with your {{es}} cluster.
* Fully remove the Integrations Server, delete it from the disk, and stop the charges.

::::{important}
The APM secret token can no longer be reset from the {{ece}} UI. Check [Secret token](/solutions/observability/apm/secret-token.md) for instructions on managing a secret token. Note that resetting the token disrupts your APM service and restarts the server. When the server restarts, you’ll need to update all of your agents with the new token.
::::

## Routing to Fleet Server [ece-integrations-server-fleet-routing]

Because Fleet Server and APM Server live on the same instance, an additional part is added to the Fleet Server hostname to help distinguish between the traffic to each. If you have not configured support for deployment aliases, your certificate may not be configured to expect this extra part.

Data is routed to APM using the same hostname `<<apm-id>>.<<your-domain>>`, but two new endpoints are introduced:

* `<<deployment-id>>.apm.<<your-domain>>` as an alternate endpoint for APM
* `<<deployment-id>>.fleet.<<your-domain>>` is the *only* way of routing data to Fleet Server

::::{note}
New certificates must be generated for both these endpoints. Check [Enable custom endpoint aliases](../../../deploy-manage/deploy/cloud-enterprise/enable-custom-endpoint-aliases.md) for more details.
::::

## Using the API to manage Integrations Server [ece_using_the_api_to_manage_integrations_server]

To manage Integrations Server through the API you need to include an Integrations Server payload when creating or updating a deployment. Check [Enable Integrations Server through the API](../../../deploy-manage/deploy/cloud-enterprise/ece-integrations-server-api-example.md) for an example.

Check [Switch from APM to Integrations Server payload](../../../deploy-manage/deploy/cloud-enterprise/switch-from-apm-to-integrations-server-payload.md) for an example of how to switch from APM & Fleet Server to Integrations Server.


