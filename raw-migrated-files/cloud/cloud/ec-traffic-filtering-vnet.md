# Azure Private Link traffic filters [ec-traffic-filtering-vnet]

Traffic filtering, to allow only Azure Private Link connections, is one of the security layers available in {{ecloud}}. It allows you to limit how your deployments can be accessed.

Read more about [Traffic Filtering](../../../deploy-manage/security/traffic-filtering.md) for the general concepts behind traffic filtering in {{ecloud}}.

::::{note}
Azure Private Link filtering is supported only for Azure regions.
::::


Azure Private Link establishes a secure connection between two Azure VNets. The VNets can belong to separate accounts, for example a service provider and their service consumers. Azure routes the Private Link traffic within the Azure data centers and never exposes it to the public internet. In such a configuration, Elastic Cloud is the third-party service provider and the customers are service consumers.

Private Link is a connection between an Azure Private Endpoint and a Azure Private Link Service.


## Azure Private Link Service aliases [ec-private-link-azure-service-aliases]

Private Link Services are set up by Elastic in all supported Azure regions under the following aliases:

::::{dropdown} **Azure Public Regions**
| **Region** | **Azure Private Link Service alias** | **Private hosted zone domain name** |
| --- | --- | --- |
| australiaeast | australiaeast-prod-012-privatelink-service.a0cf0c1a-33ab-4528-81e7-9cb23608f94e.australiaeast.azure.privatelinkservice | privatelink.australiaeast.azure.elastic-cloud.com |
| centralus | centralus-prod-009-privatelink-service.49a041f7-2ad1-4bd2-9898-fba7f7a1ff77.centralus.azure.privatelinkservice | privatelink.centralus.azure.elastic-cloud.com |
| eastus2 | eastus2-prod-002-privatelink-service.64359fdd-7893-4215-9929-ece3287e1371.eastus2.azure.privatelinkservice | privatelink.eastus2.azure.elastic-cloud.com |
| francecentral | francecentral-prod-008-privatelink-service.8ab667fd-e8af-44b2-a347-bd48d109afec.francecentral.azure.privatelinkservice | privatelink.francecentral.azure.elastic-cloud.com |
| japaneast | japaneast-prod-006-privatelink-service.cfcf2172-917a-4260-b002-3e7183e56fd0.japaneast.azure.privatelinkservice | privatelink.japaneast.azure.elastic-cloud.com |
| northeurope | northeurope-prod-005-privatelink-service.163e4238-bdde-4a0b-a812-04650bfa41c4.northeurope.azure.privatelinkservice | privatelink.northeurope.azure.elastic-cloud.com |
| southeastasia | southeastasia-prod-004-privatelink-service.20d67dc0-2a36-40a0-af8d-0e1f997a419d.southeastasia.azure.privatelinkservice | privatelink.southeastasia.azure.elastic-cloud.com |
| uksouth | uksouth-prod-007-privatelink-service.98758729-06f7-438d-baaa-0cb63e737cdf.uksouth.azure.privatelinkservice | privatelink.uksouth.azure.elastic-cloud.com |
| westeurope | westeurope-prod-001-privatelink-service.190cd496-6d79-4ee2-8f23-0667fd5a8ec1.westeurope.azure.privatelinkservice | privatelink.westeurope.azure.elastic-cloud.com |
| westus2 | westus2-prod-003-privatelink-service.b9c176b8-4fe9-41f9-916c-67cacd753ca1.westus2.azure.privatelinkservice | privatelink.westus2.azure.elastic-cloud.com |
| eastus | eastus-prod-010-privatelink-service.b5765cd8-1fc8-45e9-91fc-a9b208369f9a.eastus.azure.privatelinkservice | privatelink.eastus.azure.elastic-cloud.com |
| southcentralus | southcentralus-prod-013-privatelink-service.f8030986-5fb9-4b0e-8463-69604233b07e.southcentralus.azure.privatelinkservice | privatelink.southcentralus.azure.elastic-cloud.com |
| canadacentral | canadacentral-prod-011-privatelink-service.203896f1-da53-4c40-b7db-0ba4e17a1019.canadacentral.azure.privatelinkservice | privatelink.canadacentral.azure.elastic-cloud.com |
| brazilsouth | brazilsouth-prod-014-privatelink-service.05813ca4-cd0f-4692-ad69-a339d023f666.brazilsouth.azure.privatelinkservice | privatelink.brazilsouth.azure.elastic-cloud.com |
| centralindia | centralindia-prod-016-privatelink-service.071806ca-8101-425b-ae86-737935a719d3.centralindia.azure.privatelinkservice | privatelink.centralindia.azure.elastic-cloud.com |
| southafricanorth | southafricanorth-prod-015-privatelink-service.b443098d-6382-42aa-9025-e0cd3ec9c103.southafricanorth.azure.privatelinkservice | privatelink.southafricanorth.azure.elastic-cloud.com |

::::


The process of setting up the Private link connection to your clusters is split between Azure (e.g. by using Azure portal), Elastic Cloud Support, and Elastic Cloud UI. These are the high-level steps:

| Azure portal | Elastic Cloud UI |
| --- | --- |
| 1. Create a private endpoint using Elastic Cloud service alias. |  |
| 2. Create a [DNS record pointing to the private endpoint](https://learn.microsoft.com/en-us/azure/dns/private-dns-privatednszone). |  |
|  | 3. Create an Azure Private Link rule set with the private endpoint **Name** and **ID**. |
|  | 4. Associate the Azure Private Link rule set with your deployments. |
|  | 5. Interact with your deployments over Private Link. |


## Create your private endpoint and DNS entries in Azure [ec-private-link-azure-dns]

1. Create a private endpoint in your VNet using the alias for your region.

    Follow the [Azure instructions](https://docs.microsoft.com/en-us/azure/private-link/create-private-endpoint-portal#create-a-private-endpoint) for details on creating a private endpoint to an endpoint service.

    Use [the service aliases for your region](../../../deploy-manage/security/azure-private-link-traffic-filters.md#ec-private-link-azure-service-aliases). Select the "Connect to an Azure resource by resource ID or alias" option. For example for the region `eastus2` the service alias is `eastus2-prod-002-privatelink-service.64359fdd-7893-4215-9929-ece3287e1371.eastus2.azure.privatelinkservice`

    ::::{note}
    You will notice that the Private Link endpoint is in the `Awaiting Approval` state. We validate and approve the endpoints when you create the ruleset using the Private Link `resource name` and `resource ID`, as described in the next section [Add the Private Link rules to your deployments](../../../deploy-manage/security/azure-private-link-traffic-filters.md#ec-azure-allow-traffic-from-link-id).
    ::::

2. Create a DNS record.

    1. Create a *Private DNS Zone*. Get the private hosted zone domain name in *Azure Private Link Service Alias* for the name of the zone. For example, in *eastus2* use `privatelink.*eastus2*.azure.elastic-cloud.com` as the zone domain name. Using this zone domain name is required to ensure certificate names match.
    2. After creating the *Private DNS Zone*, associate the zone with your VNet by creating a [virtual network link](https://learn.microsoft.com/en-us/azure/dns/private-dns-getstarted-portal).
    3. Then create a DNS A record pointing to the private endpoint. Use `*` as the record name, `A` as the type, and put the private endpoint IP address as the record value.

        Follow the [Azure instructions](https://docs.microsoft.com/en-us/azure/dns/private-dns-getstarted-portal#create-an-additional-dns-record) for details on creating an A record which points to your private endpoint IP address.

        ::::{tip}
        The private endpoint IP address is available through the network interface for the private endpoint.
        ::::



## Add the Private Link rules to your deployments [ec-azure-allow-traffic-from-link-id]

Follow these high-level steps to add Private Link rules to your deployments.

1. [Find your private endpoint resource name](../../../deploy-manage/security/azure-private-link-traffic-filters.md#ec-find-your-resource-name).
2. [Find your private endpoint resource ID](../../../deploy-manage/security/azure-private-link-traffic-filters.md#ec-find-your-resource-id).
3. [Create rules using the Private Link Endpoint Resource Name and Resource ID](../../../deploy-manage/security/azure-private-link-traffic-filters.md#ec-azure-create-traffic-filter-private-link-rule-set).
4. [Associate the private endpoint with your deployment](../../../deploy-manage/security/azure-private-link-traffic-filters.md#ec-azure-associate-traffic-filter-private-link-rule-set).
5. [Access the deployment over a Private Link](../../../deploy-manage/security/azure-private-link-traffic-filters.md#ec-azure-access-the-deployment-over-private-link).


### Find your private endpoint resource name [ec-find-your-resource-name]

1. Go to your Private Link Endpoint in the Azure Portal.
2. Select **JSON View**.
3. Copy the value of the top level **name** property.


### Find your private endpoint resource ID [ec-find-your-resource-id]

1. Go to your Private Link Endpoint in the Azure Portal.
2. Select **JSON View**.
3. Copy the value of the **properties.resourceGUID** property.

:::{image} ../../../images/cloud-ec-private-link-azure-json-view.png
:alt: Private endpoint JSON View
:class: screenshot
:::

:::{image} ../../../images/cloud-ec-private-link-azure-properties.png
:alt: Private endpoint Properties
:class: screenshot
:::


### Create rules using the Private Link Endpoint Resource Name and Resource ID [ec-azure-create-traffic-filter-private-link-rule-set]

When you have your private endpoint name and ID, you can create a Private Link traffic filter rule set.

::::{note}
The Private Link connection will be approved automatically after the traffic filter is created.
::::


1. From the **Account** menu, select **Traffic filters**.
2. Select **Create filter**.
3. Select **Private link endpoint**.
4. Create your rule set, providing a meaningful name and description.
5. Select the region for the rule set.
6. Enter your Private Endpoint Resource Name and Resource ID.
7. Select if this rule set should be automatically attached to new deployments.

    ::::{note}
    Each rule set is bound to a particular region and can be only assigned to deployments in the same region.
    ::::

8. (Optional) You can [claim your Private Endpoint Resource Name and Resource ID](../../../deploy-manage/security/claim-traffic-filter-link-id-ownership-through-api.md), so that no other organization is able to use it in a traffic filter ruleset.

Creating the filter approves the Private Link connection.

Let’s test the connection:

1. Find out the Elasticsearch cluster ID of your deployment. You can do that by selecting **Copy cluster id** in the Cloud UI. It looks something like `9c794b7c08fa494b9990fa3f6f74c2f8`.

    ::::{tip}
    The Elasticsearch cluster ID is **different** from the deployment ID, custom alias endpoint, and Cloud ID values that feature prominently in the user console.
    ::::

2. To access your Elasticsearch cluster over Private Link:

    * If you have a [custom endpoint alias](../../../deploy-manage/deploy/elastic-cloud/custom-endpoint-aliases.md) configured, you can use the custom endpoint URL to connect.

        `https://{{alias}}.{product}.{{private_hosted_zone_domain_name}}`

        For example:

        `https://my-deployment-d53192.es.privatelink.eastus2.azure.elastic-cloud.com`

    * Alternatively, use the following URL structure:

        `https://{{elasticsearch_cluster_ID}}.{private_hosted_zone_domain_name}:9243`

        For example:

        `https://6b111580caaa4a9e84b18ec7c600155e.privatelink.eastus2.azure.elastic-cloud.com:9243`

3. You can test the Azure portal part of the setup with the following command (substitute the region and Elasticsearch ID with your cluster).

    The output should look like this:

    ```sh
    $ curl -v https://6b111580caaa4a9e84b18ec7c600155e.privatelink.eastus2.azure.elastic-cloud.com:9243
    * Rebuilt URL to: https://6b111580caaa4a9e84b18ec7c600155e.privatelink.eastus2.azure.elastic-cloud.com:9243/
    *   Trying 192.168.46.5...         # <== note this IP address
    ..
    * SSL connection using TLS1.2 / ECDHE_RSA_AES_256_GCM_SHA384
    * 	 server certificate verification OK
    * 	 common name: *.privatelink.elastic-cloud.com (matched)
    ..
    < HTTP/1.1 403 Forbidden
    {"ok":false,"message":"Forbidden"}
    ```

    Check the IP address `192.168.46.5` it should be the same as the IP address of your private endpoint.

    The connection is established, and a valid certificate is presented to the client. The `403 Forbidden` is expected, you haven’t associate the rule set with any deployment yet.

4. In the event that the Private Link connection is not approved by Elastic Cloud, you’ll get an error message like the following. Double check that the filter you’ve created in the previous step uses the right resource name and GUID.

    ```sh
    $ curl -v https://6b111580caaa4a9e84b18ec7c600155e.privatelink.eastus2.azure.elastic-cloud.com:9243
    * Rebuilt URL to: https://6b111580caaa4a9e84b18ec7c600155e.privatelink.eastus2.azure.elastic-cloud.com:9243/
    *   Trying 192.168.46.5...
    * connect to 192.168.46.5 port 9243 failed: No route to host
    * Failed to connect to 6b111580caaa4a9e84b18ec7c600155e.privatelink.eastus2.azure.elastic-cloud.com port 9243: No route to host
    * Closing connection 0
    curl: (7) Failed to connect to 6b111580caaa4a9e84b18ec7c600155e.privatelink.eastus2.azure.elastic-cloud.com port 9243: No route to host
    ```


The next step is to [associate the rule set](../../../deploy-manage/security/aws-privatelink-traffic-filters.md#ec-associate-traffic-filter-private-link-rule-set) with your deployments.


### Associate a Private Link rule set with your deployment [ec-azure-associate-traffic-filter-private-link-rule-set]

To associate a Private Link rule set with your deployment:

1. Go to the deployment.
2. On the **Security** page, under **Traffic filters** select **Apply filter**.
3. Choose the filter you want to apply and select **Apply filter**.


### Access the deployment over a Private Link [ec-azure-access-the-deployment-over-private-link]

For traffic to connect with the deployment over Azure Private Link, the client making the request needs to be located within the VNet where you’ve created the private endpoint. You can also setup network traffic to flow through the originating VNet from somewhere else, such as another VNet or a VPN from your corporate network. This assumes that the private endpoint and the DNS record are also available within that context. Check your service provider documentation for setup instructions.

::::{important}
Use the alias you’ve set up as CNAME A record to access your deployment.
::::


For example, if your Elasticsearch ID is `6b111580caaa4a9e84b18ec7c600155e` and it is located in `eastus2` region you can access it under `https://6b111580caaa4a9e84b18ec7c600155e.privatelink.eastus2.azure.elastic-cloud.com:9243`.

```sh
$ curl -u 'username:password'  -v https://6b111580caaa4a9e84b18ec7c600155e.privatelink.eastus2.azure.elastic-cloud.com:9243
..
< HTTP/1.1 200 OK
..
```

::::{note}
If you are using Azure Private Link together with Fleet, and enrolling the Elastic Agent with a Private Link URL, you need to configure Fleet Server to use and propagate the Private Link URL by updating the **Fleet Server hosts** field in the **Fleet settings** section of Kibana. Otherwise, Elastic Agent will reset to use a default address instead of the Private Link URL. The URL needs to follow this pattern: `https://<Fleet component ID/deployment alias>.fleet.<Private hosted zone domain name>:443`.

Similarly, the Elasticsearch host needs to be updated to propagate the Private Link URL. The Elasticsearch URL needs to follow this pattern: `https://<Elasticsearch cluster ID/deployment alias>.es.<Private hosted zone domain name>:443`.

::::



## Edit a Private Link connection [ec-azure-edit-traffic-filter-private-link-rule-set]

You can edit a rule set name or to change the VPC endpoint ID.

1. From the **Account** menu, select **Traffic filters**.
2. Find the rule set you want to edit.
3. Select the **Edit** icon.


### Delete a Private Link rule set [ec-azure-delete-traffic-filter-private-link-rule-set]

If you need to remove a rule set, you must first remove any associations with deployments.

To delete a rule set with all its rules:

1. [Remove any deployment associations](../../../deploy-manage/security/azure-private-link-traffic-filters.md#ec-azure-remove-association-traffic-filter-private-link-rule-set).
2. From the **Account** menu, select **Traffic filters**.
3. Find the rule set you want to edit.
4. Select the **Remove** icon. The icon is inactive if there are deployments assigned to the rule set.


### Remove a Private Link rule set association from your deployment [ec-azure-remove-association-traffic-filter-private-link-rule-set]

To remove an association through the UI:

1. Go to the deployment.
2. On the **Security** page, under **Traffic filters** select **Remove**.


## Setting up an inter-region Private Link connection [ec-azure-inter-region-private-link]

Azure supports inter-region Private Link as described in the [Azure documentation](https://docs.microsoft.com/en-us/azure/private-link/private-endpoint-overview). "The Private Link resource can be deployed in a different region than the virtual network and private endpoint."

This means your deployment on Elastic Cloud can be in a different region than the Private Link endpoints or the clients that consume the deployment endpoints.

:::{image} ../../../images/cloud-ce-azure-inter-region-pl.png
:alt: Inter-region Private Link
:class: screenshot
:::

1. Set up Private Link Endpoint in region 1 for a deployment hosted in region 2.

    1. Create your Private Endpoint using the service alias for region 2 in the region 1 VNET (let’s call this VNET1).
    2. Create a Private Hosted Zone for region 2, and associate it with VNET1 similar to the step [Create a Private Link endpoint and DNS](../../../deploy-manage/security/azure-private-link-traffic-filters.md#ec-private-link-azure-dns). Note that you are creating these resources in region 1, VNET1.

2. [Create a traffic filter rule set](../../../deploy-manage/security/azure-private-link-traffic-filters.md#ec-azure-create-traffic-filter-private-link-rule-set) and [Associate the rule set](../../../deploy-manage/security/aws-privatelink-traffic-filters.md#ec-associate-traffic-filter-private-link-rule-set) through the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), just as you would for any deployment.
3. [Test the connection](../../../deploy-manage/security/azure-private-link-traffic-filters.md#ec-azure-access-the-deployment-over-private-link) from a VM or client in region 1 to your Private Link endpoint, and it should be able to connect to your Elasticsearch cluster hosted in region 2.
