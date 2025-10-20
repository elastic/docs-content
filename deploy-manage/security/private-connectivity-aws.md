---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-traffic-filtering-vpc.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-traffic-filtering-vpc.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
navigation_title: AWS PrivateLink
sub:
  policy-type: "Private connection"
  service-name: "AWS PrivateLink"
  example-phz-dn: "vpce.us-east-1.aws.elastic-cloud.com"
  example-default-dn: "us-east-1.aws.elastic-cloud.com"
---

# Private connectivity with AWS PrivateLink

You can use AWS PrivateLink to establish a secure connection for your {{ecloud}} deployments to communicate with other AWS services. AWS routes the PrivateLink traffic within the AWS data center and never exposes it to the public internet.

AWS PrivateLink connects your Virtual Private Cloud (VPC) to the AWS-hosted services that you use, treating them as if they were in your VPC. You can create and use VPC endpoints to securely access AWS-hosted services.

You can also optionally filter traffic to your deployments by creating virtual private connection (VPC) filters as part of your private connection policy in {{ecloud}}. This limits traffic to your deployment to the VPC specified in the policy, as well as any other policies applied to the deployment.

To learn how private connection policies impact your deployment, refer to [](/deploy-manage/security/network-security-policies.md).

:::{tip}
{{ech}} also supports [IP filters](/deploy-manage/security/ip-filtering-cloud.md). You can apply both IP filters and private connections to a single {{ecloud}} resource.
:::

## Considerations

Before you begin, review  the following considerations:

### Private connections and regions

Private connectivity with AWS PrivateLink is supported only in AWS regions.

AWS interface virtual private connection (VPC) endpoints are configured for one or more availability zones (AZ). In some regions, our VPC endpoint service is not present in all the possible AZs that a region offers. You can only choose AZs that are common on both sides. As the names of AZs (for example `us-east-1a`) differ between AWS accounts, the following list of AWS regions shows the ID (e.g. `use1-az4`) of each available AZ for the service.

Refer to [interface endpoint availability zone considerations](https://docs.aws.amazon.com/vpc/latest/userguide/vpce-interface.html#vpce-interface-availability-zones) for more details.

### Availability zones

Elastic [charges](/deploy-manage/cloud-organization/billing/cloud-hosted-deployment-billing-dimensions.md) for inter-node traffic regardless of whether nodes are in the same or different availability zones (AZ). As a result, placing the deployment nodes within a single AZ, instead of two or three, does not reduce inter-node costs.

On the customer VPC side, the inter-availability zone data transfer, within the same AWS region, towards AWS PrivateLink endpoints, [is free of charge](https://aws.amazon.com/about-aws/whats-new/2022/04/aws-data-transfer-price-reduction-privatelink-transit-gateway-client-vpn-services/). As a result, you do not incur charges for cross-AZ data transfer within your VPC when the target is the AWS Privatelink {{ecloud}} service endpoint. We recommend you set up the VPC endpoints in all supported {{ecloud}} AZs for a particular region for maximum traffic throughput and resiliency.

If Elastic and your VPC overlap in two AZs or less, you can create subnets and VPC PrivateLink endpoints in your VPC within the same availability zones where the Elastic PrivateLink service is present.

### Transport client

Transport client is not supported over PrivateLink connections.

## PrivateLink service names and aliases [ec-private-link-service-names-aliases]

PrivateLink Service is set up by Elastic in all supported AWS regions under the following service names:

::::{dropdown} AWS public regions
| Region | VPC service name | Private hosted zone domain name | AZ names (AZ IDs) |
| --- | --- | --- | --- |
| af-south-1 | `com.amazonaws.vpce.af-south-1.vpce-svc-0d3d7b74f60a6c32c` | `vpce.af-south-1.aws.elastic-cloud.com` | `af-south-1a` (`afs1-az1`), `af-south-1b` (`afs1-az2`), `af-south-1c` (`afs1-az3`) |
| ap-east-1 | `com.amazonaws.vpce.ap-east-1.vpce-svc-0f96fbfaf55558d5c` | `vpce.ap-east-1.aws.elastic-cloud.com` | `ap-east-1a` (`ape1-az1`), `ap-east-1b` (`ape1-az2`), `ap-east-1c` (`ape1-az3`) |
| ap-northeast-1 | `com.amazonaws.vpce.ap-northeast-1.vpce-svc-0e1046d7b48d5cf5f` | `vpce.ap-northeast-1.aws.elastic-cloud.com` | `ap-northeast-1b` (`apne1-az4`), `ap-northeast-1c` (`apne1-az1`), `ap-northeast-1d` (`apne1-az2`) |
| ap-northeast-2 | `com.amazonaws.vpce.ap-northeast-2.vpce-svc-0d90cf62dae682b84` | `vpce.ap-northeast-2.aws.elastic-cloud.com` | `ap-northeast-2a` (`apne2-az1`), `ap-northeast-2b` (`apne2-az2`), `ap-northeast-2c` (`apne2-az3`) |
| ap-south-1 | `com.amazonaws.vpce.ap-south-1.vpce-svc-0e9c1ae5caa269d1b` | `vpce.ap-south-1.aws.elastic-cloud.com` | `ap-south-1a` (`aps1-az1`), `ap-south-1b` (`aps1-az3`), `ap-south-1c` (`aps1-az2`) |
| ap-southeast-1 | `com.amazonaws.vpce.ap-southeast-1.vpce-svc-0cbc6cb9bdb683a95` | `vpce.ap-southeast-1.aws.elastic-cloud.com` | `ap-southeast-1a` (`apse1-az1`), `ap-southeast-1b` (`apse1-az2`), `ap-southeast-1c` (`apse1-az3`) |
| ap-southeast-2 | `com.amazonaws.vpce.ap-southeast-2.vpce-svc-0cde7432c1436ef13` | `vpce.ap-southeast-2.aws.elastic-cloud.com` | `ap-southeast-2a` (`apse2-az1`), `ap-southeast-2b` (`apse2-az3`), `ap-southeast-2c` (`apse2-az2`) |
| ca-central-1 | `com.amazonaws.vpce.ca-central-1.vpce-svc-0d3e69dd6dd336c28` | `vpce.ca-central-1.aws.elastic-cloud.com` | `ca-central-1a` (`cac1-az1`), `ca-central-1b` (`cac1-az2`), `ca-central-1d` (`cac1-az4`) |
| eu-central-1 | `com.amazonaws.vpce.eu-central-1.vpce-svc-081b2960e915a0861` | `vpce.eu-central-1.aws.elastic-cloud.com` | `eu-central-1a` (`euc1-az2`), `eu-central-1b` (`euc1-az3`), `eu-central-1c` (`euc1-az1`) |
| eu-central-2 | `com.amazonaws.vpce.eu-central-2.vpce-svc-07deba12e07d77434` | `vpce.eu-central-2.aws.elastic-cloud.com` | `eu-central-2a` (`euc2-az1`), `eu-central-2b` (`euc2-az2`), `eu-central-2c` (`euc2-az3`) |
| eu-south-1 | `com.amazonaws.vpce.eu-south-1.vpce-svc-03d8fc8a66a755237` | `vpce.eu-south-1.aws.elastic-cloud.com` | `eu-south-1a` (`eus1-az1`), `eu-south-1b` (`eus1-az2`), `eu-south-1c` (`eus1-az3`) |
| eu-north-1 | `com.amazonaws.vpce.eu-north-1.vpce-svc-05915fc851f802294` | `vpce.eu-north-1.aws.elastic-cloud.com` | `eu-north-1a` (`eun1-az1`), `eu-north-1b` (`eun1-az2`), `eu-north-1c` (`eun1-az3`) |
| eu-west-1 | `com.amazonaws.vpce.eu-west-1.vpce-svc-01f2afe87944eb12b` | `vpce.eu-west-1.aws.elastic-cloud.com` | `eu-west-1a` (`euw1-az2`), `eu-west-1b` (`euw1-az1`), `eu-west-1c` (`euw1-az3`) |
| eu-west-2 | `com.amazonaws.vpce.eu-west-2.vpce-svc-0e42a2c194c97a1d0` | `vpce.eu-west-2.aws.elastic-cloud.com` | `eu-west-2a` (`euw2-az2`), `eu-west-2b` (`euw2-az3`), `eu-west-2c` (`euw2-az1`) |
| eu-west-3 | `com.amazonaws.vpce.eu-west-3.vpce-svc-0d6912d10db9693d1` | `vpce.eu-west-3.aws.elastic-cloud.com` | `eu-west-3a` (`euw3-az1`), `eu-west-3b` (`euw3-az2`), `eu-west-3c` (`euw3-az3`) |
| me-south-1 | `com.amazonaws.vpce.me-south-1.vpce-svc-0381de3eb670dcb48` | `vpce.me-south-1.aws.elastic-cloud.com` | `me-south-3a` (`mes1-az1`), `me-south-3b` (`mes1-az2`), `me-south-3c` (`mes1-az3`) |
| sa-east-1 | `com.amazonaws.vpce.sa-east-1.vpce-svc-0b2dbce7e04dae763` | `vpce.sa-east-1.aws.elastic-cloud.com` | `sa-east-1a` (`sae1-az1`), `sa-east-1b` (`sae1-az2`), `sa-east-1c` (`sae1-az3`) |
| us-east-1 | `com.amazonaws.vpce.us-east-1.vpce-svc-0e42e1e06ed010238` | `vpce.us-east-1.aws.elastic-cloud.com` | `us-east-1a` (`use1-az4`), `us-east-1b` (`use1-az6`), `us-east-1e` (`use1-az2`) |
| us-east-2 | `com.amazonaws.vpce.us-east-2.vpce-svc-02d187d2849ffb478` | `vpce.us-east-2.aws.elastic-cloud.com` | `us-east-2a` (`use2-az1`), `us-east-2b` (`use2-az2`), `us-east-2a` (`use2-az3`) |
| us-west-1 | `com.amazonaws.vpce.us-west-1.vpce-svc-00def4a16a26cb1b4` | `vpce.us-west-1.aws.elastic-cloud.com` | `us-west-1a` (`usw1-az1`), `us-west-1b` (`usw1-az2`), `us-west-1c` (`usw1-az3`) |
| us-west-2 | `com.amazonaws.vpce.us-west-2.vpce-svc-0e69febae1fb91870` | `vpce.us-west-2.aws.elastic-cloud.com` | `us-west-2a` (`usw2-az2`), `us-west-2b` (`usw2-az1`), `us-west-2c` (`usw2-az3`) |
::::


::::{dropdown} GovCloud regions
| Region | VPC service name | Private hosted zone domain name |
| --- | --- | --- |
| us-gov-east-1 (GovCloud) | `com.amazonaws.vpce.us-gov-east-1.vpce-svc-0bba5ffa04f0cb26d` | `vpce.us-gov-east-1.aws.elastic-cloud.com` |
::::

## Set up a private connection

The process of setting up a private connection with AWS PrivateLink is split between the AWS console and the {{ecloud}} UI. These are the high-level steps:

| AWS console | {{ecloud}} |
| --- | --- |
| 1. [Create a VPC endpoint using {{ecloud}} service name.](#ec-aws-vpc-dns) |  |
| 2. [Create a DNS record pointing to the VPC endpoint.](#ec-aws-vpc-dns) |  |
|  | 3. **Optional**: [Create a private connection policy.](#ec-add-vpc-elastic)<br><br>A private connection policy is required to filter traffic using the VPC endpoint ID. |
|  | 4. **Optional**: [Associate the private connection policy with deployments](#associate-private-connection-policy). |
|  | 5. [Interact with your deployments over PrivateLink](#ec-access-the-deployment-over-private-link). |

After you create your private connection policy, you can [edit](#edit-private-connection-policy), [disassociate](#remove-private-connection-policy), or [delete](#delete-private-connection-policy) it.

:::{admonition} Private connection policies are optional
Private connection policies are optional for AWS PrivateLink. After the VPC endpoint and DNS record are created, private connectivity is established.

Creating a private connection policy and associating it with your deployments allows you to do the following: 

* Record that you've established private connectivity between AWS and Elastic in the applicable region.
* [View a list of the resources](network-security-policies.md#protected-resources-overview) that have private connections applied.
* Optionally filter traffic to your deployment using VPC filters.
:::


### Before you begin [ec-aws-vpc-overlapping-azs]

Before you begin, you should ensure your VPC endpoint is in all availability zones supported by {{ecloud}} on the region for the VPC service.

Ensuring that your VPC is in all supported {{ecloud}} availability zones for a particular region avoids potential for a traffic imbalance. That imbalance may saturate some coordinating nodes and underutilize others in the deployment, eventually impacting performance. Enabling all supported {{ecloud}} zones ensures that traffic is balanced optimally.

You can find the zone name to zone ID mapping with AWS CLI:

```sh
$ aws ec2 describe-availability-zones --region us-east-1 | jq -c '.AvailabilityZones[] | { id: .ZoneId, name: .ZoneName } ' | sort
{"id":"use1-az1","name":"us-east-1c"}
{"id":"use1-az2","name":"us-east-1e"}
{"id":"use1-az3","name":"us-east-1d"}
{"id":"use1-az4","name":"us-east-1a"}
{"id":"use1-az5","name":"us-east-1f"}
{"id":"use1-az6","name":"us-east-1b"}
```

The mapping will be different for your region. Our production VPC Service for `us-east-1` is located in `use1-az2`, `use1-az4`, `use1-az6`. We need to create the VPC Endpoint for the preceding mapping in at least one of `us-east-1e`, `us-east-1a`, `us-east-1b`.

:::{note}
This limitation does not apply to [cross-region PrivateLink connections](#ec-aws-inter-region-private-link). If you're creating a cross-region connection, then you don't need to check that your VPC is present in all availability zones.
:::

### Create your VPC endpoint and DNS entries in AWS [ec-aws-vpc-dns]

1. Create a VPC endpoint in your VPC using the service name for your region.

    Refer to the [AWS documentation](https://docs.aws.amazon.com/vpc/latest/userguide/vpce-interface.html#create-interface-endpoint) for additional details on creating a VPC interface endpoint to an endpoint service.

    Select **PrivateLink Ready partner services** as the endpoint type. Use [the service name for your region](#ec-private-link-service-names-aliases) as the **Service name**.

    :::{image} /deploy-manage/images/cloud-ec-private-link-service.png
    :alt: PrivateLink
    :screenshot:
    :::

    The security group for the endpoint should, at minimum, allow for inbound connectivity from your instances' CIDR range on ports 443 and 9243. Security groups for the instances should allow for outbound connectivity to the endpoint on ports 443 and 9243.

    :::{tip}
    You can also create a cross-region endpoint. Refer to [Setting up an cross-region Private Link connection](#ec-aws-inter-region-private-link).
    :::

2. Create a DNS record.

    1. Create a Private hosted zone. 

        Refer to the **Private hosted zone domain name** column in the [PrivateLink service names and aliases](#ec-private-link-service-names-aliases) table for the name of the zone. For example, in `us-east-1`, use `vpce.us-east-1.aws.elastic-cloud.com` as the zone domain name. 
        
        Don’t forget to associate the zone with your VPC.

        :::{image} /deploy-manage/images/cloud-ec-private-link-private-hosted-zone-example.png
        :alt: Private hosted zone example
        :screenshot:
        :::

    2. Create a DNS CNAME alias pointing to the PrivateLink endpoint. Add the record to a private DNS zone in your VPC. Use `*` as the record name, and the VPC endpoint DNS name as a value.

        Refer to the [AWS documentation](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-creating.html) for details on creating a CNAME record which points to your VPC endpoint DNS name.

        :::{image} /deploy-manage/images/cloud-ec-private-link-cname.png
        :alt: PrivateLink CNAME
        :screenshot:
        :::

### Test the connection

After you create your VPC endpoint and DNS entries, check that you are able to reach your cluster over PrivateLink.

:::{include} _snippets/private-url-struct.md
:::

To test the connection:

1. If needed, find the endpoint of an application in your deployment:
   
    :::{include} _snippets/find-endpoint.md
    :::

2. Test the setup using the following cURL command. Pass the username and password for a user that has access to the cluster. Make sure to replace the URL with your deployment's endpoint information and the private hosted zone domain name that you registered.

    **Request**
    ```sh
    $ curl -v https://my-deployment-d53192.es.vpce.us-east-1.aws.elastic-cloud.com -u {username}:{password}
    ```
    **Response**
    ```sh
    * Server certificate:
    *  subject: CN=*.us-east-1.aws.elastic-cloud.com
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

The connection is established, and a valid certificate is presented to the client. Elastic responds, in the case of the {{es}} endpoint, with basic information about the cluster.

## Optional: Create a private connection policy [ec-add-vpc-elastic]

After you test your PrivateLink connection, you can create a private connection policy in {{ecloud}}. 

Private connection policies are optional for AWS PrivateLink. After the VPC endpoint and DNS record are created, private connectivity is established.

Creating a private connection policy and associating it with your deployments allows you to do the following: 

* Record that you've established private connectivity between AWS and Elastic in the applicable region.
* Filter traffic to your deployment using VPC filters.

Follow these high-level steps to add a private connection policy that can be associated with your deployments.

1. Optional: [Find your VPC endpoint ID](#ec-find-your-endpoint).
2. [Create a private connection policy using the VPC endpoint](#create-private-connection-policy).
3. [Associate the VPC endpoint with your deployment](#associate-private-connection-policy).

### Optional: Find your VPC endpoint ID [ec-find-your-endpoint]

The VPC endpoint ID is only required if you want to filter traffic to your deployment using VPC filters.

You can find your VPC endpoint ID in the AWS console:

:::{image} /deploy-manage/images/cloud-ec-private-link-endpoint-id.png
:alt: VPC Endpoint ID
:screenshot:
:::

### Create a new private connection policy [create-private-connection-policy]

Create a new private connection policy.

:::{include} _snippets/network-security-page.md
:::
4. Select **Private connection**.
3. Select the resource type that the private connection will be applied to. Currently, only hosted deployments are supported.
10. Select the cloud provider and region for the private connection. 
   
    :::{tip}
    Private connection policies are bound to a single region, and can be assigned only to deployments in the same region. If you want to associate a policy with resources in multiple regions, then you have to create the same policy in all the regions you want to apply it to.
    :::
11. Under **Connectivity**, select **Privatelink**.
12. Optional: Under **VPC filter**, enter your VPC endpoint ID. You should only specify a VPC filter if you want to filter traffic to your deployment. 
    
    If you don't specify a VPC filter, then the private connection policy acts only as a record that you've established private connectivity between AWS and Elastic in the applicable region.
    
    :::{tip}
    You can apply multiple policies to a single deployment. The policies can be of different types. In case of multiple policies, traffic can match any associated policy to be forwarded to the resource. If none of the policies match, the request is rejected with `403 Forbidden`.

    [Learn more about how network security policies affect your deployment](network-security-policies.md).
    :::

13. Optional: Under **Apply to resources**, associate the new private connection policy with one or more deployments. If you specified a VPC filter, then after you associate the filter with a deployment, it starts filtering traffic.
14. To automatically attach this private connection policy to new deployments, select **Apply by default**.
15.  Click **Create**.
16. (Optional) You can [claim your VPC endpoint ID](/deploy-manage/security/claim-private-connection-api.md), so that no other organization is able to use it in a private connection policy.

The next step is to [associate the policy](#associate-private-connection-policy) with your deployment.

### Optional: Associate a private connection policy with a deployment [associate-private-connection-policy]

You can associate a private connection policy with your deployment from the policy's settings, or from your deployment's settings. 

If the policy contains a VPC filter, then after you associate the policy with a deployment, it starts filtering traffic. 

If the policy doesn't contain a VPC filter, then the association can serve as a reminder that a VPC endpoint exists for the deployment's region.

#### From a deployment

:::{include} _snippets/associate-filter.md
:::

#### From the policy settings

:::{include} _snippets/network-security-page.md
:::
5. Find the policy you want to edit.
6. Under **Apply to resources**, associate the policy with one or more deployments.
7. Click **Update** to save your changes.

## Access the deployment over a PrivateLink [ec-access-the-deployment-over-private-link]

For traffic to connect with the deployment over AWS PrivateLink, the client making the request needs to be located within the VPC where you’ve created the VPC endpoint. You can also set up network traffic to flow through the originating VPC from somewhere else, such as another VPC or VPN from your corporate network. This assumes that the VPC endpoint and the DNS record are also available within that context. Check your service provider documentation for setup instructions.

::::{important}
Use the alias you’ve set up as CNAME DNS record to access your deployment.
::::

:::{include} _snippets/private-url-struct.md
:::

To access the deployment:

1. If needed, find the endpoint of an application in your deployment:
   
    :::{include} _snippets/find-endpoint.md
    :::

2. Send a request:

    **Request**
    ```sh
    $ curl -v https://my-deployment-d53192.es.vpce.us-east-1.aws.elastic-cloud.com -u {username}:{password}
    ```
    **Response**
    ```sh
    * Server certificate:
    *  subject: CN=*.us-east-1.aws.elastic-cloud.com
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

### AWS PrivateLink and Fleet

:::{include} _snippets/private-connection-fleet.md
:::

## Setting up a cross-region PrivateLink connection [ec-aws-inter-region-private-link]

AWS supports cross-region PrivateLink as described on the [AWS blog](https://aws.amazon.com/blogs/networking-and-content-delivery/introducing-cross-region-connectivity-for-aws-privatelink/).

This means your deployment on {{ecloud}} can be in a different region than the PrivateLink endpoints or the clients that consume the deployment endpoints.

In this example, `region 1` contains your VPC endpoint and `region 2` is the region where your deployment is hosted.

1. Begin to create your VPC endpoint in `region 1`, as described in [Create your VPC endpoint and DNS entries in AWS](#ec-aws-vpc-dns). In the service settings, do the following:

    * In the **Service name** field, enter the [VPC service name](#ec-private-link-service-names-aliases) for `region 2`.
    * Select **Enable Cross Region endpoint** and select `region 2` from the **Select a region** drop-down list.

1. [Create a private connection policy](#create-private-connection-policy) in the region where your deployment is hosted (`region 2`), and [associate it](#associate-private-connection-policy) with your deployment.
   
2. [Test the connection](#ec-access-the-deployment-over-private-link) from a VM or client in `region 1` to your Private Link endpoint, and it should be able to connect to your {{es}} cluster hosted in `region 2`.

## Manage private connection policies

After you create your private connection policy, you can edit it, remove it from your deployment, or delete it.

### Edit a private connection policy [edit-private-connection-policy]

You can edit a policy's name, description, VPC endpoint ID, and more.

:::{include} _snippets/network-security-page.md
:::
1. Find the policy you want to edit, then click the **Edit** {icon}`pencil` button.
2. Click **Update** to save your changes.

:::{tip}
You can also edit private connection policies from your deployment's **Security** page or your project's **Network security** page.
:::

### Remove a private connection policy from your deployment [remove-private-connection-policy]

If you want to a specific policy from a deployment, or delete the policy, then you need to disconnect it from any associated deployments first. You can do this from the policy's settings, or from your deployment's settings. To remove an association through the UI:

#### From your deployment

1. Find your deployment on the home page or on the **Hosted deployments** page, then select **Manage** to access its settings menus.

    On the **Hosted deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.
2. On the **Security** page, under **Network security**, find the policy that you want to disconnect. 
3. Under **Actions**, click the **Delete** icon.

#### From the private connection policy settings

:::{include} _snippets/network-security-page.md
:::
5. Find the policy you want to edit, then click the **Edit** {icon}`pencil` button.
6. Under **Apply to resources**, click the `x` beside the resource that you want to disconnect.
7. Click **Update** to save your changes.


### Delete a private connection policy [delete-private-connection-policy]

If you need to remove a policy, you must first remove any associations with deployments.

To delete a policy:

:::{include} _snippets/network-security-page.md
:::
4. Find the policy you want to edit, then click the **Delete** icon. The icon is inactive if there are deployments associated with the policy.
