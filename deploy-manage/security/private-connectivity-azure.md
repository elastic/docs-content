---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-traffic-filtering-vnet.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-traffic-filtering-vnet.html
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-hosted
  - id: cloud-serverless
navigation_title: Azure Private Link
sub:
  policy-type: "Private connection"
  service-name: "Azure Private Link"
  example-phz-dn: "privatelink.eastus2.azure.elastic-cloud.com"
  example-default-dn: "eastus2.azure.elastic-cloud.com"
  example-serverless-phz-dn: "private.eastus2.azure.elastic.cloud"
---

# Private connectivity with Azure Private Link

You can use Azure Private Link to establish a secure connection for your {{ech}} deployments and {{serverless-full}} projects to communicate with other Azure services. Azure routes the Private Link traffic within the Azure data center and never exposes it to the public internet.

Azure Private Link establishes a secure connection between two Azure VNets. The VNets can belong to separate accounts, for example a service provider and their service consumers. Azure routes the Private Link traffic within the Azure data centers and never exposes it to the public internet. In such a configuration, {{ecloud}} is the third-party service provider and the customers are service consumers.

Private Link is a connection between an Azure Private Endpoint and a Azure Private Link Service.

Azure Private Link requires that you also filter traffic to your deployments or projects by creating a private connection policy in {{ecloud}}. This limits traffic to your deployment or project to the private endpoint specified in the policy, along with any other filters defined in policies applied to the deployment or project.

To learn how private connection policies impact your deployment or project, refer to [](/deploy-manage/security/network-security-policies.md).

:::{tip}
* {{ech}} and {{serverless-full}} also support [IP filters](/deploy-manage/security/ip-filtering-cloud.md). You can apply both IP filters and private connections to a single {{ecloud}} resource.
* {applies_to}`ech: ga` If you created your deployment through the [Azure Native Service](/deploy-manage/deploy/elastic-cloud/azure-native-isv-service.md), you can also create and link Private Link private connection policies from the Azure portal Traffic Filter page. Refer to [](/deploy-manage/deploy/elastic-cloud/azure-native-isv-service-network-security.md).
:::

## Requirements
```{applies_to}
serverless:
```

The following requirements apply to the project where you want to apply a private connection policy:

:::{include} _snippets/network-sec-tier-reqs.md
:::

There are no specific requirements for other {{serverless-short}} project types or {{ech}} deployments.

## Considerations

Before you decide to set up private connectivity with Azure Private Link, review the following considerations:

### Private connections and regions

Private connectivity with Azure Private Link is supported only in Azure regions. You can set up private connections in [Azure regions where {{ecloud}} is available](#ec-private-link-azure-service-aliases). You can also set up [inter-region Private Link connections](#ec-azure-inter-region-private-link) to reach your deployment or project from additional Azure regions.

For {{serverless-full}}, Private Link is not available in the Azure `northeurope` region because of Azure capacity limitations. For the full list of supported regions, refer to [Azure Private Link Service aliases](#ec-private-link-azure-service-aliases).

## Limitations

When using Azure Private Link, the following limitations apply:

```{include} _snippets/private-connectivity-limitations-ech.md
```

* **North Europe region:** {applies_to}`serverless:` Private Link is not available for {{serverless-full}} projects in the Azure `northeurope` region because of Azure capacity limitations. {{ech}} deployments in `northeurope` are not affected.

## Azure Private Link Service aliases [ec-private-link-azure-service-aliases]

Private Link Services are set up by Elastic in all supported Azure regions under the following aliases. Some metadata might differ between {{ech}} and {{serverless-full}}, even if the region is the same.

:::::{applies-switch}
::::{applies-item} ess: ga
:::{dropdown} Azure public regions
| Region | Azure Private Link Service alias | Private hosted zone domain name |
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

:::
::::
::::{applies-item} serverless: ga
:::{note}
Private Link is not available for {{serverless-full}} in the Azure `northeurope` region because of Azure capacity limitations.
:::

:::{dropdown} Azure public regions
| Region | Azure Private Link Service alias | Private hosted zone domain name |
| --- | --- | --- |
| australiaeast | australiaeast-prod-privatelink-serverless.274cbc58-219f-481d-bc66-9a7b46d63be8.australiaeast.azure.privatelinkservice | private.australiaeast.azure.elastic.cloud |
| eastus | eastus-prod-privatelink-serverless.00ee2891-1e3c-491b-b7cd-a5be7a2a42fc.eastus.azure.privatelinkservice | private.eastus.azure.elastic.cloud |
| eastus2 | eastus2-prod-privatelink-serverless.46552e7f-8404-48e2-8c79-66801ef74a76.eastus2.azure.privatelinkservice | private.eastus2.azure.elastic.cloud |
| germanywestcentral | germanywestcentral-prod-privatelink-serverless.bece7bbd-ce63-4728-aeda-ad42238d9d66.germanywestcentral.azure.privatelinkservice | private.germanywestcentral.azure.elastic.cloud |
| southeastasia | southeastasia-prod-privatelink-serverless.ca3fc3e6-1b18-41a9-adcd-2c4ea7ca342e.southeastasia.azure.privatelinkservice | private.southeastasia.azure.elastic.cloud |
| spaincentral | spaincentral-prod-privatelink-serverless.66548bb8-1b56-40b6-b679-062db94282a6.spaincentral.azure.privatelinkservice | private.spaincentral.azure.elastic.cloud |
| uaenorth | uaenorth-prod-privatelink-serverless.235f486d-71e1-490d-9bab-49edc5d6a875.uaenorth.azure.privatelinkservice | private.uaenorth.azure.elastic.cloud |
| westus2 | westus2-prod-privatelink-serverless.f03c3599-2fbc-4cb5-8a79-7cff7a0e2f2c.westus2.azure.privatelinkservice | private.westus2.azure.elastic.cloud |

:::

You can also view the service metadata for your selected region by starting to [create a new private connection policy](#ec-azure-allow-traffic-from-link-id) for the region and expanding the **Service metadata** dropdown.

::::
:::::

## Set up a private connection

The process of setting up a private connection with Azure Private Link is split between Azure (for example, by using Azure portal), and the {{ecloud}} UI. These are the high-level steps:

| Azure portal | {{ecloud}} |
| --- | --- |
| 1. [Create a private endpoint using {{ecloud}} service alias](#ec-private-link-azure-dns). |  |
| 2. [Create a DNS record pointing to the private endpoint](#ec-private-link-azure-dns). |  |
|  | 3. [Create a private connection policy](#ec-azure-allow-traffic-from-link-id). |
|  | 4. [Associate the Azure private connection policy with your deployments or projects](#associate-private-connection-policy). |
|  | 5. **Optional**: [Add an IP filter to allow SSO to {{kib}} from the {{ecloud}} console.](#sso-kib-ip-filter) |
|  | 6. [Interact with your deployments or projects over Private Link](#ec-azure-access-the-deployment-over-private-link). |

After you create your private connection policy, you can [edit](#edit-private-connection-policy), [disassociate](#remove-private-connection-policy), or [delete](#delete-private-connection-policy) it.

### Create your private endpoint and DNS entries in Azure [ec-private-link-azure-dns]

1. Create a private endpoint in your VNet using the alias for your region.

    Follow the [Azure instructions](https://docs.microsoft.com/en-us/azure/private-link/create-private-endpoint-portal#create-a-private-endpoint) for details on creating a private endpoint to an endpoint service.

    Use [the service aliases for your region](#ec-private-link-azure-service-aliases). Select the **Connect to an Azure resource by resource ID or alias** option. For example, for resources in `eastus2`:
    
    * For {{ech}} deployments: The service alias is `eastus2-prod-002-privatelink-service.64359fdd-7893-4215-9929-ece3287e1371.eastus2.azure.privatelinkservice`.
    * For {{serverless-short}} projects: The service alias is `eastus2-prod-privatelink-serverless.46552e7f-8404-48e2-8c79-66801ef74a76.eastus2.azure.privatelinkservice`.

    ::::{note}
    The Private Link endpoint is created in the `Awaiting Approval` state. We validate and approve the endpoints when you create the private connection policy using the Private Link `resource ID`, as described in [Create a private connection policy](#ec-azure-allow-traffic-from-link-id).
    ::::

2. Create a DNS record.

    1. Create a private DNS zone.

        Refer to the **Private hosted zone domain name** column in the [Azure Private Link Service aliases](#ec-private-link-azure-service-aliases) table for the name of the zone. 
        
        For example, in `eastus2`:
        
        * For {{ech}} deployments: Use `privatelink.eastus2.azure.elastic-cloud.com`.
        * For {{serverless-short}} projects: Use `private.eastus2.azure.elastic.cloud`.
        
        Using this zone domain name is required to ensure certificate names match.

        :::{tip}
        Private hosted zone domain names differ between {{ech}} and {{serverless-full}}, even if the region is the same.
        :::

    2. After creating the private DNS zone, associate the zone with your VNet by creating a [virtual network link](https://learn.microsoft.com/en-us/azure/dns/private-dns-getstarted-portal).
    3. Create a DNS A record pointing to the private endpoint. Use `*` as the record name, `A` as the type, and put the private endpoint IP address as the record value.

        Follow the [Azure instructions](https://docs.microsoft.com/en-us/azure/dns/private-dns-getstarted-portal#create-an-additional-dns-record) for details on creating an A record which points to your private endpoint IP address.

        ::::{tip}
        The private endpoint IP address is available through the network interface for the private endpoint.
        ::::



## Create a private connection policy [ec-azure-allow-traffic-from-link-id]

After you create your private endpoint and DNS entries, you can create a private connection policy in {{ecloud}}.

Follow these high-level steps to add a private connection policy that can be associated with your deployments or projects.

1. [Find your private endpoint resource name](#ec-find-your-resource-name).
2. [Find your private endpoint resource ID](#ec-find-your-resource-id).
3. [Create policies using the Private Link Endpoint resource ID](#create-private-connection-policy).
4. [Test the connection](#test-the-connection).
5. [Associate the private endpoint with your deployment or project](#associate-private-connection-policy).

### Find your private endpoint resource name [ec-find-your-resource-name]

1. Go to your Private Link Endpoint in the Azure Portal.
2. Select **JSON View**.
3. Copy the value of the top level **name** property.

### Find your private endpoint resource ID [ec-find-your-resource-id]

1. Go to your Private Link Endpoint in the Azure Portal.
2. Select **JSON View**.
3. Copy the value of the **properties.resourceGUID** property.

:::{image} /deploy-manage/images/cloud-ec-private-link-azure-json-view.png
:alt: Private endpoint JSON view
:screenshot:
:::

:::{image} /deploy-manage/images/cloud-ec-private-link-azure-properties.png
:alt: Private endpoint properties
:screenshot:
:::


### Create a policy using the Private Link Endpoint resource [create-private-connection-policy]

When you have your private endpoint name and ID, you can create a private connection policy.

::::{note}
The Private Link connection will be approved automatically after the private connection policy is created.
::::


:::{include} _snippets/network-security-page.md
:::
3. Select **Private connection**.
4. Select the resource type that the private connection will be applied to.
5.  Select the cloud provider and region for the private connection.

    :::{tip}
    Private connection policies are bound to a single resource type and region, and can be assigned only to resources with the same resource type and in the same region. If you want to associate a policy with multiple resource types or resources in multiple regions, then you have to recreate the policy for all applicable resource types and regions.
    :::
6.  Under **Connectivity**, select **PrivateLink**.
7.  Enter your private endpoint **Resource name** and **Resource ID**. When applied to a deployment or project, this information will be used to filter traffic.

    :::{tip}
    You can apply multiple policies to a single deployment or project. The policies can be of different types. In case of multiple policies, traffic can match any associated policy to be forwarded to the resource. If none of the policies match, the request is rejected with `403 Forbidden`.

    [Learn more about how network security policies affect your deployment or project](network-security-policies.md).
    :::

8.  Optional: Under **Apply to resources**, associate the new private connection policy with one or more deployments or projects. After you associate the filter with a resource, it starts filtering traffic.

    :::{tip}
    Associating the private connection policy with deployments or projects is optional. After the private connection policy is created, private connectivity is established.

    Associating the policy with your deployments or projects allows you to do the following:

    * [View a list of the resources](network-security-policies.md#protected-resources-overview) that have private connections applied.
    * Filter traffic to your deployment or project.
    :::

9. To automatically attach this private connection policy to new resources of this type, select **Apply by default**.
10.  Click **Create**.
11. (Optional) If you created a private connection policy for {{ech}} deployments, you can [claim your Private Endpoint resource name and ID](/deploy-manage/security/claim-private-connection-api.md), so that no other organization is able to use it in a private connection policy.

Creating the policy approves the Private Link connection.

After the private link connection is approved, you can optionally [test the connection](#test-the-connection), and then [associate the policy](#associate-private-connection-policy) with your deployment or project.

### Test the connection

After you create your private connection, you can check that you're able to reach your deployment or project over Private Link.

:::::{applies-switch}
::::{applies-item} ess: ga
:::{include} _snippets/private-url-struct.md
:::
::::
::::{applies-item} serverless: ga
:::{include} _snippets/private-url-struct-serverless.md
:::
::::
:::::

:::{tip}
Private hosted zone domain names differ between {{ech}} and {{serverless-full}}, even if the region is the same.
:::

To test the connection:

1. If needed, find the endpoint of an application in your deployment or project:

    :::::{applies-switch}
    :::: {applies-item} ess: ga
    :::{include} _snippets/find-endpoint.md
    :::
    ::::
    :::: {applies-item} serverless: ga
    :::{include} _snippets/find-endpoint-serverless.md
    :::
    ::::
    :::::

2. Test the setup using the following cURL command. Pass the username and password for a user that has access to the cluster.

    ::::{applies-switch}
    :::{applies-item} ess: ga
    Make sure to replace the URL with your deployment's endpoint information and the private hosted zone domain name that you registered.

    **Request**

    ```sh
    $ curl -v https://my-deployment-d53192.es.privatelink.eastus2.azure.elastic-cloud.com:9243 -u {username}:{password}
    ```

    **Response**

    ```sh
    * Rebuilt URL to: https://my-deployment-d53192.es.privatelink.eastus2.azure.elastic-cloud.com:9243/
    *   Trying 192.168.46.5... # note this IP address
    ..
    * SSL connection using TLS1.2 / ECDHE_RSA_AES_256_GCM_SHA384
    * 	 server certificate verification OK
    * 	 common name: *.privatelink.elastic-cloud.com (matched)
    ..
        < HTTP/1.1 200 OK
    ..
    {
        "name" : "instance-0000000009",
        "cluster_name" : "fb7e805e5cfb4931bdccc4f3cb591f5f",
        "cluster_uuid" : "2cTHeCQYS2a0iH7YnQHrIQ",
        "version" : { ... },
        "tagline" : "You Know, for Search"
    }
    ```

    Check the IP address `192.168.46.5`. It should be the same as the IP address of your private endpoint.

    The connection is established, and a valid certificate is presented to the client. Elastic responds, in the case of the {{es}} endpoint, with basic information about the cluster.
    :::
    :::{applies-item} serverless: ga
    Make sure to replace the URL with the **Private endpoint** URL from your project.

    **Request**

    ```sh
    $ curl -v https://my-project-d53192.es.private.eastus2.azure.elastic.cloud -u {username}:{password}
    ```

    **Response**

    ```sh
    * Server certificate:
    *  subject: CN=*.es.private.eastus2.azure.elastic.cloud
    *  SSL certificate verify ok.
    ..
        < HTTP/1.1 200 OK
    ..
    {
        "name" : "instance-0000000009",
        "cluster_name" : "fb7e805e5cfb4931bdccc4f3cb591f5f",
        "cluster_uuid" : "2cTHeCQYS2a0iH7YnQHrIQ",
        "version" : { ... },
        "tagline" : "You Know, for Search"
    }
    ```

    The connection is established, and a valid certificate is presented to the client. In the case of the {{es}} endpoint, Elastic responds with basic information about the cluster.
    :::
    ::::

### Troubleshoot connection failures

If your test connection fails, the following are some common errors and what they can indicate.

#### No route to host

If the test connection fails with a `No route to host` error, the Private Link connection is not approved by {{ecloud}}. Double check that the filter you've created in the previous step uses the right resource ID.


```sh
* connect to 192.168.46.5 port 9243 failed: No route to host
* Failed to connect to my-deployment-d53192.es.privatelink.eastus2.azure.elastic-cloud.com port 9243: No route to host
* Closing connection 0
curl: (7) Failed to connect to my-deployment-d53192.es.privatelink.eastus2.azure.elastic-cloud.com port 9243: No route to host
```

#### 403 Forbidden

If the TLS connection succeeds but the request returns a `403 Forbidden` response with `Forbidden due to traffic filtering`, the network path is valid but your private connection policy is missing or misconfigured. Verify that the resource name and resource ID in the policy exactly match the `name` and `properties.resourceGUID` values of the Azure private endpoint, and that the policy is associated with the target deployment or project.

```sh
HTTP/1.1 403 Forbidden
...
Forbidden due to traffic filtering
```

### Associate a private connection policy with a deployment or project [associate-private-connection-policy]

You can associate a private connection policy with your deployment or project from the policy's settings, or from your deployment's or project's settings.

After you associate the policy with a deployment or project, it starts filtering traffic.

:::{tip}
Associating the private connection policy with deployments or projects is optional. After the private connection policy is created, private connectivity is established.

Associating the policy with your deployments or projects allows you to do the following:

* [View a list of the resources](network-security-policies.md#protected-resources-overview) that have private connections applied.
* Filter traffic to your deployment or project.
:::

#### From a deployment or project

:::::{applies-switch}
::::{applies-item} ess: ga
:::{include} _snippets/associate-filter.md
:::
::::
::::{applies-item} serverless: ga
1. Find your project on the home page or on the **Serverless projects** page, then select **Manage** to access its settings menus.

   On the **Serverless projects** page, you can narrow your projects by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.
2. On the **Security** page, under **Network security**, select **Apply policies** > **{{policy-type}}**.
3. Choose the policy you want to apply and select **Apply**.
::::
:::::

#### From the policy settings

:::{include} _snippets/network-security-page.md
:::
3. Find the policy you want to edit.
4. Under **Apply to resources**, associate the policy with one or more deployments or projects.
5. Click **Update** to save your changes.

## Optional: Add an IP filter to allow SSO to {{kib}} from the {{ecloud}} console [sso-kib-ip-filter]

:::{include} _snippets/ip-filter-for-pc.md
:::

## Access the resource over a Private Link [ec-azure-access-the-deployment-over-private-link]

For traffic to connect with the deployment or project over Azure Private Link, the client making the request needs to be located within the VNet where you’ve created the private endpoint. You can also set up network traffic to flow through the originating VNet from somewhere else, such as another VNet or a VPN from your corporate network. This assumes that the private endpoint and the DNS record are also available within that context. Check your service provider documentation for setup instructions.

::::{important}
Use the alias you've set up as an A record to access your resource.
::::

:::::{applies-switch}
::::{applies-item} ess: ga
:::{include} _snippets/private-url-struct.md
:::
::::
::::{applies-item} serverless: ga
:::{include} _snippets/private-url-struct-serverless.md
:::
::::
:::::

:::{tip}
Private hosted zone domain names differ between {{ech}} and {{serverless-full}}, even if the region is the same.
:::

To access the deployment or project:

1. If needed, find the endpoint of an application in your deployment or project:

    :::::{applies-switch}
    :::: {applies-item} ess: ga
    :::{include} _snippets/find-endpoint.md
    :::
    ::::
    :::: {applies-item} serverless: ga
    :::{include} _snippets/find-endpoint-serverless.md
    :::
    ::::
    :::::

2. Send a request:

    ::::{applies-switch}
    :::{applies-item} ess: ga
    **Request**
    ```sh
    $ curl -v https://my-deployment-d53192.es.privatelink.eastus2.azure.elastic-cloud.com:9243 -u {username}:{password}
    ```

    **Response**
    ```sh
    * Rebuilt URL to: https://my-deployment-d53192.es.privatelink.eastus2.azure.elastic-cloud.com:9243/
    *   Trying 192.168.46.5...
    ..
    * SSL connection using TLS1.2 / ECDHE_RSA_AES_256_GCM_SHA384
    * 	 server certificate verification OK
    * 	 common name: *.privatelink.elastic-cloud.com (matched)
    ..
        < HTTP/1.1 200 OK
    ..
    {
        "name" : "instance-0000000009",
        "cluster_name" : "fb7e805e5cfb4931bdccc4f3cb591f5f",
        "cluster_uuid" : "2cTHeCQYS2a0iH7YnQHrIQ",
        "version" : { ... },
        "tagline" : "You Know, for Search"
    }
    ```
    :::
    :::{applies-item} serverless: ga
    **Request**
    ```sh
    $ curl -v https://my-project-d53192.es.private.eastus2.azure.elastic.cloud -u {username}:{password}
    ```

    **Response**
    ```sh
    * Server certificate:
    *  subject: CN=*.es.private.eastus2.azure.elastic.cloud
    *  SSL certificate verify ok.
    ..
        < HTTP/1.1 200 OK
    ..
    {
        "name" : "instance-0000000009",
        "cluster_name" : "fb7e805e5cfb4931bdccc4f3cb591f5f",
        "cluster_uuid" : "2cTHeCQYS2a0iH7YnQHrIQ",
        "version" : { ... },
        "tagline" : "You Know, for Search"
    }
    ```
    :::
    ::::

### Azure Private Link and Fleet

:::{include} _snippets/private-connection-fleet.md
:::

## Setting up an inter-region Private Link connection [ec-azure-inter-region-private-link]

Azure supports inter-region Private Link as described in the [Azure documentation](https://docs.microsoft.com/en-us/azure/private-link/private-endpoint-overview).

This means your deployment or project on {{ecloud}} can be in a different region than the Private Link endpoints or the clients that consume the deployment or project endpoints.

:::{image} /deploy-manage/images/cloud-ce-azure-inter-region-pl.png
:alt: Inter-region Private Link
:screenshot:
:::

1. Set up Private Link Endpoint in region 1 for a deployment or project hosted in region 2.

    1. Create your Private Link Endpoint using the service alias for region 2 in the region 1 VNet (let’s call this VNet1).
    2. Create a Private Hosted Zone for region 2, and associate it with VNet1 similar to the [Create a Private Link endpoint and DNS](#ec-private-link-azure-dns) step. Note that you are creating these resources in region 1, VNet1.

2. [Create a private connection policy](#create-private-connection-policy) in the region where your deployment or project is hosted, and [associate it](#associate-private-connection-policy) with your deployment or project.

3. [Test the connection](#ec-azure-access-the-deployment-over-private-link) from a VM or client in region 1 to your Private Link endpoint, and it should be able to connect to your {{es}} deployment or project hosted in region 2.

## Manage private connection policies

After you create your private connection policy, you can edit it, remove it from your deployment or project, or delete it.

### Edit a private connection policy [edit-private-connection-policy]

You can edit a policy's name, description, resource name, Private Endpoint filter, and more.

:::{include} _snippets/network-security-page.md
:::
3. Find the policy you want to edit, then click the **Edit** {icon}`pencil` button.
4. Click **Update** to save your changes.

:::{tip}
You can also edit private connection policies from your deployment or project's **Security** page or your project's **Network security** page.
:::

### Remove a private connection policy from your deployment or project [remove-private-connection-policy]

If you want to remove a specific policy from a deployment or project, or delete the policy, then you need to disconnect it from any associated deployments or projects first. You can do this from the policy's settings, or from your deployment or project's settings. To remove an association through the UI:

#### From your deployment or project

::::{applies-switch}
:::{applies-item} ess: ga
1. Find your deployment on the home page or on the **Hosted deployments** page, then select **Manage** to access its settings menus.

    On the **Hosted deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.
2. On the **Security** page, under **Network security**, find the policy that you want to disconnect.
3. Under **Actions**, click the **Delete** icon.
:::
:::{applies-item} serverless: ga
1. Find your project on the home page or on the **Serverless projects** page, then select **Manage** to access its settings menus.

   On the **Serverless projects** page, you can narrow your projects by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.
2. On the **Security** page, under **Network security**, find the policy that you want to disconnect.
3. Under **Actions**, click the **Delete** icon.
:::
::::

#### From the private connection policy settings

:::{include} _snippets/network-security-page.md
:::
3. Find the policy you want to edit, then click the **Edit** {icon}`pencil` button.
4. Under **Apply to resources**, click the `x` beside the resource that you want to disconnect.
5. Click **Update** to save your changes.

### Delete a private connection policy [delete-private-connection-policy]

If you need to delete a policy, you must first remove any associations with deployments or projects.

To delete a policy:

:::{include} _snippets/network-security-page.md
:::
3. Find the policy you want to edit, then click the **Delete** icon. The icon is inactive if there are deployments or projects associated with the policy.
