# AWS PrivateLink traffic filters [ec-traffic-filtering-vpc]

Traffic filtering, to only AWS PrivateLink connections, is one of the security layers available in {{ecloud}}. It allows you to limit how your deployments can be accessed.

Read more about [Traffic Filtering](../../../deploy-manage/security/traffic-filtering.md) for the general concepts behind traffic filtering in {{ecloud}}.

::::{note}
PrivateLink filtering is supported only for AWS regions. AWS does not support cross-region PrivateLink connections. Your PrivateLink endpoint needs to be in the same region as your target deployments. Additional details can be found in the [AWS VPCE Documentation](https://docs.aws.amazon.com/vpc/latest/userguide/vpce-interface.md#vpce-interface-limitations). AWS interface VPC endpoints get created in availability zones (AZ). In some regions, our VPC endpoint *service* is not present in all the possible AZs that a region offers. You can only choose AZs that are common on both sides. As the *names* of AZs (for example `us-east-1a`) differ between AWS accounts, the following list of AWS regions shows the *ID* (e.g. `use1-az4`) of each available AZ for the service. Check [interface endpoint availability zone considerations](https://docs.aws.amazon.com/vpc/latest/userguide/vpce-interface.md#vpce-interface-availability-zones) for more details.
::::


::::{note}
Transport client is not supported over PrivateLink connections.
::::


AWS PrivateLink establishes a secure connection between two AWS Virtual Private Clouds (VPCs). The VPCs can belong to separate accounts, i.e. a service provider and its service consumers. AWS routes the PrivateLink traffic within the AWS data center and never exposes it to the public internet. In such a configuration, Elastic Cloud is the third-party service provider and the customers are service consumers.

PrivateLink is a connection between a VPC Endpoint and a PrivateLink Service.


## PrivateLink service names and aliases [ec-private-link-service-names-aliases]

PrivateLink Service is set up by Elastic in all supported AWS regions under the following service names:

::::{dropdown} **AWS Public Regions**
| **Region** | **VPC Service Name** | **Private hosted zone domain name** | **AZ Names (AZ IDs)** |
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


::::{dropdown} **GovCloud Regions**
| **Region** | **VPC Service Name** | **Private hosted zone domain name** |
| --- | --- | --- |
| us-gov-east-1 (GovCloud) | `com.amazonaws.vpce.us-gov-east-1.vpce-svc-0bba5ffa04f0cb26d` | `vpce.us-gov-east-1.aws.elastic-cloud.com` |

::::


The process of setting up the PrivateLink connection to your clusters is split between AWS (e.g. by using AWS console) and Elastic Cloud UI. These are the high-level steps:

| AWS console | Elastic Cloud |
| --- | --- |
| 1. Create a VPC endpoint using Elastic Cloud service name. |  |
| 2. Create a DNS record pointing to the VPC endpoint. |  |
|  | 3. Create a PrivateLink rule set with your VPC endpoint ID. |
|  | 4. Associate the PrivateLink rule set with your deployments. |
|  | 5. Interact with your deployments over PrivateLink. |


## Ensure your VPC endpoint is in all availability zones supported by {{ecloud}} on the region for the VPC service [ec-aws-vpc-overlapping-azs]

::::{note}
Ensuring that your VPC is in all supported Elastic Cloud availability zones for a particular region avoids potential for a traffic imbalance. That imbalance may saturate some coordinating nodes and underutilize others in the deployment, eventually impacting performance. Enabling all supported Elastic Cloud zones ensures that traffic is balanced optimally.
::::


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

The mapping will be different for your region. Our production VPC Service for `us-east-1` is located in `use1-az2`, `use1-az4`, `use1-az6`. We need to create the VPC Endpoint for the preceding mapping in at least one of `us-east-1a`, `us-east-1d`, `us-east-1b`.


## Create your VPC endpoint and DNS entries in AWS [ec-aws-vpc-dns]

1. Create a VPC endpoint in your VPC using the service name for your region.

    Follow the [AWS instructions](https://docs.aws.amazon.com/vpc/latest/userguide/vpce-interface.md#create-interface-endpoint) for details on creating a VPC interface endpoint to an endpoint service.

    Use [the service name for your region](../../../deploy-manage/security/aws-privatelink-traffic-filters.md#ec-private-link-service-names-aliases).

    :::{image} ../../../images/cloud-ec-private-link-service.png
    :alt: PrivateLink
    :class: screenshot
    :::

    The security group for the endpoint should at minimum allow for inbound connectivity from your instances CIDR range on ports 443 and 9243. Security groups for the instances should allow for outbound connnectibity to the endpoint on ports 443 and 9243.

2. Create a DNS record.

    1. Create a *Private hosted zone*. Consult  *Private hosted zone domain name* in *PrivateLink service names and aliases* for the name of the zone. For example, in *us-east-1* use `vpce.us-east-1.aws.elastic-cloud.com` as the zone domain name. Don’t forget to associate the zone with your VPC.

        :::{image} ../../../images/cloud-ec-private-link-private-hosted-zone-example.png
        :alt: Private hosted zone example
        :class: screenshot
        :::

    2. Then create a DNS CNAME alias pointing to the PrivateLink Endpoint. Add the record to a private DNS zone in your VPC. Use `*` as the record name, and the VPC endpoint DNS name as a value.

        Follow the [AWS instructions](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-creating.md) for details on creating a CNAME record which points to your VPC endpoint DNS name.

        :::{image} ../../../images/cloud-ec-private-link-cname.png
        :alt: PrivateLink CNAME
        :class: screenshot
        :::

3. Test the connection.

    Find out the endpoint of your deployment. You can do that by selecting **Copy endpoint** in the Cloud UI. It looks something like `my-deployment-d53192.es.us-east-1.aws.found.io`. `my-deployment-d53192` is an alias, and `es` is the product you want to access within your deployment.

    To access your Elasticsearch cluster over PrivateLink:

    * If you have a [custom endpoint alias](../../../deploy-manage/deploy/elastic-cloud/custom-endpoint-aliases.md) configured, you can use the custom endpoint URL to connect.
    * Alternatively, use the following URL structure:

        `https://{{alias}}.{product}.{{private_hosted_zone_domain_name}}`

        For example:

        `https://my-deployment-d53192.es.vpce.us-east-1.aws.elastic-cloud.com`


    ::::{tip}
    You can use either 443, or 9243 as a port.
    ::::


    You can test the AWS console part of the setup with a following curl (substitute the region and Elasticsearch ID with your cluster):

    ```sh
    $ curl -v https://my-deployment-d53192.es.vpce.us-east-1.aws.elastic-cloud.com
    ..
    * Server certificate:
    *  subject: CN=*.us-east-1.aws.elastic-cloud.com
    *  SSL certificate verify ok.
    ..
    {"ok":false,"message":"Forbidden"}
    * Connection #0 to host my-deployment-d53192.es.vpce.us-east-1.aws.elastic-cloud.com left intact
    ```

    The connection is established, and a valid certificate is presented to the client. The `403 Forbidden` is expected, because you haven’t allowed the traffic over this PrivateLink connection yet.



## Add the private link rules to your deployments [ec-add-vpc-elastic]

Follow these high-level steps to add private link rules to your deployments.

1. [Find your VPC endpoint ID](../../../deploy-manage/security/aws-privatelink-traffic-filters.md#ec-find-your-endpoint).
2. [Create rules using the VPC endpoint](../../../deploy-manage/security/aws-privatelink-traffic-filters.md#ec-create-traffic-filter-private-link-rule-set).
3. [Associate the VPC endpoint with your deployment](../../../deploy-manage/security/aws-privatelink-traffic-filters.md#ec-associate-traffic-filter-private-link-rule-set).
4. [Access the deployment over a private link](../../../deploy-manage/security/aws-privatelink-traffic-filters.md#ec-access-the-deployment-over-private-link).


### Finding your VPC endpoint ID [ec-find-your-endpoint]

Having trouble finding your VPC endpoint ID? You can find it in the AWS console.

:::{image} ../../../images/cloud-ec-private-link-endpoint-id.png
:alt: VPC Endpoint ID
:class: screenshot
:::


### Create rules with the VPC endpoint [ec-create-traffic-filter-private-link-rule-set]

Once you know your VPC endpoint ID you can create a private link traffic filter rule set.

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.
3. Under the **Features** tab, open the **Traffic filters** page.
4. Select **Create filter**.
5. Select **Private link endpoint**.
6. Create your rule set, providing a meaningful name and description.
7. Select the region for the rule set.
8. Enter your VPC endpoint ID.
9. Select if this rule set should be automatically attached to new deployments.

    ::::{note}
    Each rule set is bound to a particular region and can be only assigned to deployments in the same region.
    ::::

10. (Optional) You can [claim your VPC endpoint ID](../../../deploy-manage/security/claim-traffic-filter-link-id-ownership-through-api.md), so that no other organization is able to use it in a traffic filter ruleset.

The next step is to [associate the rule set](../../../deploy-manage/security/aws-privatelink-traffic-filters.md#ec-associate-traffic-filter-private-link-rule-set) with your deployments.


### Associate a PrivateLink rule set with your deployment [ec-associate-traffic-filter-private-link-rule-set]

To associate a private link rule set with your deployment:

1. Go to the deployment.
2. On the **Security** page, under **Traffic filters** select **Apply filter**.
3. Choose the filter you want to apply and select **Apply filter**.


### Access the deployment over a PrivateLink [ec-access-the-deployment-over-private-link]

For traffic to connect with the deployment over a PrivateLink, the client making the request needs to be located within the VPC where you’ve created the VPC endpoint. You can also setup network traffic to flow through the originating VPC from somewhere else, such as another VPC or VPN from your corporate network. This assumes that the VPC endpoint and the DNS record are also available within that context. Check your service provider documentation for setup instructions.

::::{important}
Use the alias you’ve set up as CNAME DNS record to access your deployment.
::::


If your deployment alias is `my-deployment-12ab9b` and it is located in `us-east-1` region you can access it under `https://my-deployment-12ab9b.es.vpce.us-east-1.aws.elastic-cloud.com`.

```sh
$ curl -u 'username:password' -v https://my-deployment-d53192.es.vpce.us-east-1.aws.elastic-cloud.com
..
< HTTP/1.1 200 OK
..
```

::::{note}
If you are using AWS PrivateLink together with Fleet, and enrolling the Elastic Agent with a PrivateLink URL, you need to configure Fleet Server to use and propagate the PrivateLink URL by updating the **Fleet Server hosts** field in the **Fleet settings** section of Kibana. Otherwise, Elastic Agent will reset to use a default address instead of the PrivateLink URL. The URL needs to follow this pattern: `https://<Fleet component ID/deployment alias>.fleet.<Private hosted zone domain name>:443`.

Similarly, the Elasticsearch host needs to be updated to propagate the Privatelink URL. The Elasticsearch URL needs to follow this pattern: `https://<Elasticsearch cluster ID/deployment alias>.es.<Private hosted zone domain name>:443`.

The settings `xpack.fleet.agents.fleet_server.hosts` and `xpack.fleet.outputs` that are needed to enable this configuration in {{kib}} are currently available on-prem only, and not in the [Kibana settings in {{ecloud}}](../../../deploy-manage/deploy/elastic-cloud/edit-stack-settings.md).

::::



## Edit a PrivateLink connection [ec-edit-traffic-filter-private-link-rule-set]

You can edit a rule set name or to change the VPC endpoint ID.

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.
3. Under the **Features** tab, open the **Traffic filters** page.
4. Find the rule set you want to edit.
5. Select the **Edit** icon.


### Delete a PrivateLink rule set [ec-delete-traffic-filter-private-link-rule-set]

If you need to remove a rule set, you must first remove any associations with deployments.

To delete a rule set with all its rules:

1. [Remove any deployment associations](../../../deploy-manage/security/aws-privatelink-traffic-filters.md#ec-remove-association-traffic-filter-private-link-rule-set).
2. Under the **Features** tab, open the **Traffic filters** page.
3. Find the rule set you want to edit.
4. Select the **Remove** icon. The icon is inactive if there are deployments assigned to the rule set.


### Remove a PrivateLink rule set association from your deployment [ec-remove-association-traffic-filter-private-link-rule-set]

To remove an association through the UI:

1. Go to the deployment.
2. On the **Security** page, under **Traffic filters** select **Remove**.
