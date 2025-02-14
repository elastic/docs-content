# Manage your Integrations Server [ece-manage-integrations-server]

For deployments that are version 8.0 and later, you have the option to add a combined [Application Performance Monitoring (APM) Server](/solutions/observability/apps/application-performance-monitoring-apm.md) and [Fleet Server](https://www.elastic.co/guide/en/fleet/current/fleet-overview.html) to your deployment. APM allows you to monitor software services and applications in real time, turning that data into documents stored in the Elasticsearch cluster. Fleet allows you to centrally manage Elastic Agents on many hosts.

As part of provisioning, the APM Server and Fleet Server are already configured to work with Elasticsearch and Kibana. At the end of provisioning, you are shown the secret token to configure communication between the APM Server and the backend [APM Agents](https://www.elastic.co/guide/en/apm/agent/index.html). The APM Agents get deployed within your services and applications.

From the deployment **Integrations Server** page you can also:

* Get the URL to complete the APM agent configuration.
* Use the `elastic` credentials to go to the APM area of Kibana. Step by step instructions to configure a variety of agents are available right in Kibana. After that, you can use the pre-built, dedicated dashboards and the APM tab to visualize the data that is sent back from the APM Agents.
* Use the `elastic` credentials to go to the Fleet area of Kibana. Step by step instructions to download and install Elastic Agent on your hosts are available right in Kibana. After that, you can manage enrolled Elastic Agents on the **Agents** tab, and the data shipped back from those Elastic Agents on the **Data streams** tab.
* Access the Integrations Server logs and metrics.
* Stop and restart your Integrations Server.
* Upgrade your Integrations Server version if it is out of sync with your Elasticsearch cluster.
* Fully remove the Integrations Server, delete it from the disk, and stop the charges.

::::{important}
The APM secret token can no longer be reset from the Elastic Cloud Enterprise UI. Check [Secret token](/solutions/observability/apps/secret-token.md) for instructions on managing a secret token. Note that resetting the token disrupts your APM service and restarts the server. When the server restarts, you’ll need to update all of your agents with the new token.
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

To manage Integrations Server through the API you need to include an Integrations Server payload when creating or updating a deployment. Check [Enable Integrations Server through the API](../../../deploy-manage/deploy/cloud-enterprise/manage-integrations-server.md) for an example.

Check [Switch from APM to Integrations Server payload](../../../deploy-manage/deploy/cloud-enterprise/switch-from-apm-to-integrations-server-payload.md) for an example of how to switch from APM & Fleet Server to Integrations Server.


