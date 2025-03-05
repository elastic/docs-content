# GCP Private Service Connect traffic filters [ec-traffic-filtering-psc]

Traffic filtering, to allow only Private Service Connect connections, is one of the security layers available in {{ecloud}}. It allows you to limit how your deployments can be accessed.

Read more about [Traffic Filtering](../../../deploy-manage/security/traffic-filtering.md) for the general concepts behind traffic filtering in {{ecloud}}.

::::{note}
Private Service Connect filtering is supported only for Google Cloud regions.
::::


Private Service Connect establishes a secure connection between two Google Cloud VPCs. The VPCs can belong to separate accounts, for example a service provider and their service consumers. Google Cloud routes the Private Service Connect traffic within the Google Cloud data centers and never exposes it to the public internet. In such a configuration, Elastic Cloud is the third-party service provider and the customers are service consumers.

Private Link is a connection between a Private Service Connect Endpoint and a Service Attachment. [Learn more about using Private Service Connect on Google Cloud](https://cloud.google.com/vpc/docs/private-service-connect#benefits-services).

::::{tip}
Private Service Connect connections are regional, your Private Service Connect Endpoint needs to live in the same region as your deployment. The Endpoint can be accessed from any region once you enable its [*Global Access*](https://cloud.google.com/vpc/docs/about-accessing-vpc-hosted-services-endpoints#global-access) feature.
::::



## Private Service Connect URIs [ec-private-service-connect-uris]

Service Attachments are set up by Elastic in all supported GCP regions under the following URIs:

::::{dropdown} **GCP Public Regions**
| **Region** | **Service Attachment URI** | **Private zone DNS name** |
| --- | --- | --- |
| `asia-east1` | `projects/cloud-production-168820/regions/asia-east1/serviceAttachments/proxy-psc-production-asia-east1-v1-attachment` | `psc.asia-east1.gcp.elastic-cloud.com` |
| `asia-northeast1` | `projects/cloud-production-168820/regions/asia-northeast1/serviceAttachments/proxy-psc-production-asia-northeast1-v1-attachment` | `psc.asia-northeast1.gcp.cloud.es.io` |
| `asia-northeast3` | `projects/cloud-production-168820/regions/asia-northeast3/serviceAttachments/proxy-psc-production-asia-northeast3-v1-attachment` | `psc.asia-northeast3.gcp.elastic-cloud.com` |
| `asia-south1` | `projects/cloud-production-168820/regions/asia-south1/serviceAttachments/proxy-psc-production-asia-south1-v1-attachment` | `psc.asia-south1.gcp.elastic-cloud.com` |
| `asia-southeast1` | `projects/cloud-production-168820/regions/asia-southeast1/serviceAttachments/proxy-psc-production-asia-southeast1-v1-attachment` | `psc.asia-southeast1.gcp.elastic-cloud.com` |
| `asia-southeast2` | `projects/cloud-production-168820/regions/asia-southeast2/serviceAttachments/proxy-psc-production-asia-southeast2-v1-attachment` | `psc.asia-southeast2.gcp.elastic-cloud.com` |
| `australia-southeast1` | `projects/cloud-production-168820/regions/australia-southeast1/serviceAttachments/proxy-psc-production-australia-southeast1-v1-attachment` | `psc.australia-southeast1.gcp.elastic-cloud.com` |
| `europe-north1` | `projects/cloud-production-168820/regions/europe-north1/serviceAttachments/proxy-psc-production-europe-north1-v1-attachment` | `psc.europe-north1.gcp.elastic-cloud.com` |
| `europe-west1` | `projects/cloud-production-168820/regions/europe-west1/serviceAttachments/proxy-psc-production-europe-west1-v1-attachment` | `psc.europe-west1.gcp.cloud.es.io` |
| `europe-west2` | `projects/cloud-production-168820/regions/europe-west2/serviceAttachments/proxy-psc-production-europe-west2-v1-attachment` | `psc.europe-west2.gcp.elastic-cloud.com` |
| `europe-west3` | `projects/cloud-production-168820/regions/europe-west3/serviceAttachments/proxy-psc-production-europe-west3-v1-attachment` | `psc.europe-west3.gcp.cloud.es.io` |
| `europe-west4` | `projects/cloud-production-168820/regions/europe-west4/serviceAttachments/proxy-psc-production-europe-west4-v1-attachment` | `psc.europe-west4.gcp.elastic-cloud.com` |
| `europe-west9` | `projects/cloud-production-168820/regions/europe-west9/serviceAttachments/proxy-psc-production-europe-west9-v1-attachment` | `psc.europe-west9.gcp.elastic-cloud.com` |
| `me-west1` | `projects/cloud-production-168820/regions/me-west1/serviceAttachments/proxy-psc-production-me-west1-v1-attachment` | `psc.me-west1.gcp.elastic-cloud.com` |
| `northamerica-northeast1` | `projects/cloud-production-168820/regions/northamerica-northeast1/serviceAttachments/proxy-psc-production-northamerica-northeast1-v1-attachment` | `psc.northamerica-northeast1.gcp.elastic-cloud.com` |
| `southamerica-east1` | `projects/cloud-production-168820/regions/southamerica-east1/serviceAttachments/proxy-psc-production-southamerica-east1-v1-attachment` | `psc.southamerica-east1.gcp.elastic-cloud.com` |
| `us-central1` | `projects/cloud-production-168820/regions/us-central1/serviceAttachments/proxy-psc-production-us-central1-v1-attachment` | `psc.us-central1.gcp.cloud.es.io` |
| `us-east1` | `projects/cloud-production-168820/regions/us-east1/serviceAttachments/proxy-psc-production-us-east1-v1-attachment` | `psc.us-east1.gcp.elastic-cloud.com` |
| `us-east4` | `projects/cloud-production-168820/regions/us-east4/serviceAttachments/proxy-psc-production-us-east4-v1-attachment` | `psc.us-east4.gcp.elastic-cloud.com` |
| `us-west1` | `projects/cloud-production-168820/regions/us-west1/serviceAttachments/proxy-psc-production-us-west1-v1-attachment` | `psc.us-west1.gcp.cloud.es.io` |

::::


The process of setting up the Private link connection to your clusters is split between Google Cloud (e.g. by using Google Cloud console), and Elastic Cloud UI. These are the high-level steps:

| Google Cloud console | Elastic Cloud UI |
| --- | --- |
| 1. Create a Private Service Connect endpoint using Elastic Cloud Service Attachment URI. |  |
| 2. Create a DNS record pointing to the Private Service Connect endpoint. |  |
|  | 3. Create a Private Service Connect rule set with the **PSC Connection ID**. |
|  | 4. Associate the Private Service Connect rule set with your deployments. |
|  | 5. Interact with your deployments over Private Service Connect. |


## Create your Private Service Connect endpoint and DNS entries in Google Cloud [ec-private-service-connect-enpoint-dns]

1. Create a Private Service Connect endpoint in your VPC using the Service Attachment URI for your region.

    Follow the [Google Cloud instructions](https://cloud.google.com/vpc/docs/configure-private-service-connect-services#create-endpoint) for details on creating a Private Service Connect endpoint to access Private Service Connect services.

    Use [the Service Attachment URI for your region](../../../deploy-manage/security/gcp-private-service-connect-traffic-filters.md#ec-private-service-connect-uris). Select the **Published service** option and enter the selected *Service Attachment URI* as the **Target service**. For example for the region `asia-southeast1` the Service Attachment URI is `projects/cloud-production-168820/regions/asia-southeast1/serviceAttachments/proxy-psc-production-asia-southeast1-v1-attachment`

    ::::{note}
    you need to [reserve a static internal IP address](https://cloud.google.com/compute/docs/ip-addresses/reserve-static-internal-ip-address) in your VPC. The address is used by Private Service Connect endpoint.
    ::::


    Note down the **PSC Connection ID**, e.g. `18446744072646845332`.

2. Create a DNS record.

    1. Create a *DNS Zone* of type **Private**. Set the **DNS name** to *Private zone DNS name* for your region. For example, in *asia-southeast1* use `psc.asia-southeast1.gcp.elastic-cloud.com` as the zone domain name. Make sure the zone is associated with your VPC.
    2. Then create a DNS record set with an A record pointing to the Private Service Connect endpoint IP. Use `*` as the **DNS name**, `A` as the **Resource Record Type**, and put the Private Service Connect endpoint IP address as the record value.

        Follow the [Google Cloud instructions](https://cloud.google.com/dns/docs/records#adding_a_record) for details on creating an A record which points to your Private Service Connect endpoint IP address.

3. Test the connection.

    Find out the Elasticsearch cluster ID of your deployment. You can do that by selecting **Copy cluster id** in the Cloud UI. It looks something like `9c794b7c08fa494b9990fa3f6f74c2f8`.

    ::::{tip}
    The Elasticsearch cluster ID is **different** from the deployment ID, custom alias endpoint, and Cloud ID values that feature prominently in the user console.
    ::::


    To access your Elasticsearch cluster over Private Link:,

    * If you have a [custom endpoint alias](../../../deploy-manage/deploy/elastic-cloud/custom-endpoint-aliases.md) configured, you can use the custom endpoint URL to connect.

        `https://{{alias}}.{product}.{{private_hosted_zone_domain_name}}`

        For example:

        `https://my-deployment-d53192.es.psc.asia-southeast1.gcp.elastic-cloud.com`

    * Alternatively, use the following URL structure:

        `https://{{elasticsearch_cluster_ID}}.{private_hosted_zone_domain_name}:9243`

        For example:

        `https://6b111580caaa4a9e84b18ec7c600155e.psc.asia-southeast1.gcp.elastic-cloud.com:9243`


    You can test the Google Cloud console part of the setup with the following command (substitute the region and Elasticsearch ID with your cluster):

    ```sh
    $ curl -v https://6b111580caaa4a9e84b18ec7c600155e.psc.asia-southeast1.gcp.elastic-cloud.com:9243
    ..
    *   Trying 192.168.100.2...
    ..
    < HTTP/2 403
    ..
    {"ok":false,"message":"Forbidden"}
    ```

    Check the IP address `192.168.100.2`. it should be the same as the IP address assigned to your Private Service Connect endpoint.

    The connection is established, and a valid certificate is presented to the client. The `403 Forbidden` is expected, you haven’t associated any deployment with the Private Service Connect endpoint yet.



## Add the Private Service Connect rules to your deployments [ec-private-service-connect-allow-from-psc-connection-id]

Follow these high-level steps to add private link rules to your deployments.

1. [Find your Private Service Connect connection ID](../../../deploy-manage/security/gcp-private-service-connect-traffic-filters.md#ec-find-your-psc-connection-id).
2. [Create rules using the Private Service Connect endpoint connection ID](../../../deploy-manage/security/gcp-private-service-connect-traffic-filters.md#ec-psc-create-traffic-filter-psc-rule-set).
3. [Associate the Private Service Connect endpoint with your deployment](../../../deploy-manage/security/gcp-private-service-connect-traffic-filters.md#ec-psc-associate-traffic-filter-psc-rule-set).
4. [Access the deployment over the Private Service Connect](../../../deploy-manage/security/gcp-private-service-connect-traffic-filters.md#ec-psc-access-the-deployment-over-psc).


### Find your Private Service Connect connection ID [ec-find-your-psc-connection-id]

1. Go to your Private Service Connect endpoint in the Google Cloud console.
2. Copy the value of **PSC Connection ID**.


### Create rules using the Private Service Connect endpoint connection ID [ec-psc-create-traffic-filter-psc-rule-set]

When you have your Private Service Connect endpoint connection ID, you can create a traffic filter rule set.

1. From the **Account** menu, select **Traffic filters**.
2. Select **Create filter**.
3. Select **Private Service Connect endpoint**.
4. Create your rule set, providing a meaningful name and description.
5. Select the region for the rule set.
6. Enter your **PSC Connection ID**.
7. Select if this rule set should be automatically attached to new deployments.

    ::::{note}
    Each rule set is bound to a particular region and can be only assigned to deployments in the same region.
    ::::

8. (Optional) You can [claim your PSC Connection ID](../../../deploy-manage/security/claim-traffic-filter-link-id-ownership-through-api.md), so that no other organization is able to use it in a traffic filter ruleset.

The next step is to [associate the rule set](../../../deploy-manage/security/aws-privatelink-traffic-filters.md#ec-associate-traffic-filter-private-link-rule-set) with your deployments.


### Associate the Private Service Connect endpoint with your deployment [ec-psc-associate-traffic-filter-psc-rule-set]

To associate a private link rule set with your deployment:

1. Go to the deployment.
2. On the **Security** page, under **Traffic filters** select **Apply filter**.
3. Choose the filter you want to apply and select **Apply filter**.


### Access the deployment over the Private Service Connect [ec-psc-access-the-deployment-over-psc]

For traffic to connect with the deployment over Private Service Connect, the client making the request needs to be located within the VPC where you’ve created the Private Service Connect endpoint. You can also setup network traffic to flow through the originating VPC from somewhere else, such as another VPC or a VPN from your corporate network. This assumes that the Private Service Connect endpoint and the DNS record are also available within that context. Check your cloud service provider documentation for setup instructions.

::::{important}
Use the alias you’ve set up as CNAME A record to access your deployment.
::::


For example, if your Elasticsearch ID is `6b111580caaa4a9e84b18ec7c600155e` and it is located in `asia-southeast1` region you can access it under `https://6b111580caaa4a9e84b18ec7c600155e.psc.asia-southeast1.gcp.elastic-cloud.com:9243`.

```sh
$ curl -u 'username:password' -v https://6b111580caaa4a9e84b18ec7c600155e.psc.asia-southeast1.gcp.elastic-cloud.com:9243
..
< HTTP/1.1 200 OK
..
```

::::{note}
If you are using Private Service Connect together with Fleet, and enrolling the Elastic Agent with a Private Service Connect URL, you need to configure Fleet Server to use and propagate the Private Service Connect URL by updating the **Fleet Server hosts** field in the **Fleet settings** section of Kibana. Otherwise, Elastic Agent will reset to use a default address instead of the Private Service Connect URL. The URL needs to follow this pattern: `https://<Fleet component ID/deployment alias>.fleet.<private zone DNS name>:443`.

Similarly, the Elasticsearch host needs to be updated to propagate the Private Service Connect URL. The Elasticsearch URL needs to follow this pattern: `https://<Elasticsearch cluster ID/deployment alias>.es.<private zone DNS name>:443`.

The settings `xpack.fleet.agents.fleet_server.hosts` and `xpack.fleet.outputs` that are needed to enable this configuration in {{kib}} are currently available on-prem only, and not in the [Kibana settings in {{ecloud}}](../../../deploy-manage/deploy/elastic-cloud/edit-stack-settings.md).

::::



## Edit a Private Service Connect rule set [ec-psc-edit-traffic-filter-psc-rule-set]

You can edit a rule set name or to change the PSC connection ID.

1. From the **Account** menu, select **Traffic filters**.
2. Find the rule set you want to edit.
3. Select the **Edit** icon.


### Delete a Private Service Connect rule set [ec-psc-delete-psc-rule-set]

If you need to remove a rule set, you must first remove any associations with deployments.

To delete a rule set with all its rules:

1. [Remove any deployment associations](../../../deploy-manage/security/gcp-private-service-connect-traffic-filters.md#ec-psc-remove-association-psc-rule-set).
2. From the **Account** menu, select **Traffic filters**.
3. Find the rule set you want to edit.
4. Select the **Remove** icon. The icon is inactive if there are deployments assigned to the rule set.


### Remove a Private Service Connect rule set association from your deployment [ec-psc-remove-association-psc-rule-set]

To remove an association through the UI:

1. Go to the deployment.
2. On the **Security** page, under **Traffic filters** select **Remove**.
