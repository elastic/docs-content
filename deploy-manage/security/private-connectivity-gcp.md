---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-traffic-filtering-psc.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-traffic-filtering-psc.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
navigation_title: GCP Private Service Connect
sub:
  policy-type: "Private connection"
  service-name: "Private Service Connect"
  example-phz-dn: "psc.asia-southeast1.gcp.elastic-cloud.com"
  example-default-dn: "us-central1.gcp.cloud.es.io"
---

# Private connectivity with GCP Private Service Connect

You can use GCP Private Service Connect to establish a secure connection for your {{ecloud}} deployments to communicate with other GCP services. GCP routes the Private Link traffic within the GCP data center and never exposes it to the public internet.

GCP Private Service Connect connects your Virtual Private Cloud (VPC) to the GCP-hosted services that you use, treating them as if they were in your VPC. You can create and use VPC endpoints to securely access GCP-hosted services.

You can also optionally filter traffic to your deployments by creating virtual private connection (VPC) filters as part of your private connection policy in {{ecloud}}. This limits traffic to your deployment to the VPC specified in the policy, as well as any other policies applied to the deployment.

Private Link is a connection between a Private Service Connect Endpoint and a Service Attachment. [Learn more about using Private Service Connect on Google Cloud](https://cloud.google.com/vpc/docs/private-service-connect#benefits-services).

To learn how private connection policies impact your deployment, refer to [](/deploy-manage/security/network-security-policies.md).

:::{tip}
{{ech}} also supports [IP filters](/deploy-manage/security/ip-filtering-cloud.md). You can apply both IP filters and private connections to a single {{ecloud}} resource.
:::

## Considerations

* Private connectivity with Private Service Connect is supported only in Google Cloud regions.

* Private Service Connect connections are regional. As a result, your Private Service Connect endpoint needs to be created in the same region as your deployment. The endpoint can be accessed from any region after you enable its [Global Access](https://cloud.google.com/vpc/docs/about-accessing-vpc-hosted-services-endpoints#global-access) feature.

## Private Service Connect URIs [ec-private-service-connect-uris]

Service Attachments are set up by Elastic in all supported GCP regions under the following URIs:

::::{dropdown} GCP public regions
| Region | Service attachment URI | Private zone DNS name |
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

## Set up a private connection 

The process of setting up the Private link connection to your deployments is split between Google Cloud and the {{ecloud}} UI. These are the high-level steps:

| Google Cloud console | {{ecloud}} |
| --- | --- |
| [1. Create a Private Service Connect endpoint using {{ecloud}} Service Attachment URI.](#ec-private-service-connect-enpoint-dns) |  |
| [2. Create a DNS record pointing to the Private Service Connect endpoint.](#ec-private-service-connect-enpoint-dns) |  |
|  | [3. Optional: Create a private connection policy with the PSC Connection ID.](#create-private-connection-policy) |
|  | [4. Optional: Associate the private connection policy with your deployments.](#associate-private-connection-policy) |
|  | [5. Interact with your deployments over Private Service Connect.](#ec-psc-access-the-deployment-over-psc) |

After you create your private connection policy, you can [edit](#edit-private-connection-policy), [disassociate](#remove-private-connection-policy), or [delete](#delete-private-connection-policy) it.

:::{admonition} Private connection policies are optional
Private connection policies are optional for GCP Private Service Connect. After the Private Service Connect endpoint and DNS record are created, private connectivity is established.

Creating a private connection policy and associating it with your deployments allows you to do the following: 

* Record that you've established private connectivity between GCP and Elastic in the applicable region.
* [View a list of the resources](network-security-policies.md#protected-resources-overview) that have private connections applied.
* Optionally filter traffic to your deployment using VPC filters.
:::

### Create your Private Service Connect endpoint and DNS entries in Google Cloud [ec-private-service-connect-enpoint-dns]

1. Create a Private Service Connect endpoint in your VPC using the Service Attachment URI for your region.

    Follow the [Google Cloud instructions](https://cloud.google.com/vpc/docs/configure-private-service-connect-services#create-endpoint) for details on creating a Private Service Connect endpoint to access Private Service Connect services.

    Use [the Service Attachment URI for your region](#ec-private-service-connect-uris). Select the **Published service** option and enter the selected Service Attachment URI as the **Target service**. For example, for the region `asia-southeast1` the Service Attachment URI is `projects/cloud-production-168820/regions/asia-southeast1/serviceAttachments/proxy-psc-production-asia-southeast1-v1-attachment`

    ::::{note}
    you need to [reserve a static internal IP address](https://cloud.google.com/compute/docs/ip-addresses/reserve-static-internal-ip-address) in your VPC. The address is used by Private Service Connect endpoint.
    ::::


    Note down the **PSC Connection ID**, e.g. `18446744072646845332`.

2. Create a DNS record.

    1. Create a DNS Zone of type **Private**. 
   
       Refer to the **Private zone DNS name** column in the [Private Service Connect URIs](#ec-private-service-connect-uris) table for the name of the zone. For example, in `asia-southeast1`, use `psc.asia-southeast1.gcp.elastic-cloud.com` as the zone domain name. Make sure the zone is associated with your VPC.
    2. Create a DNS record set with an A record pointing to the Private Service Connect endpoint IP. Use `*` as the **DNS name**, `A` as the **Resource record type**, and put the Private Service Connect endpoint IP address as the record value.

        Follow the [Google Cloud instructions](https://cloud.google.com/dns/docs/records#adding_a_record) for details on creating an A record which points to your Private Service Connect endpoint IP address.

### Test the connection

After you create your Private Service Connect endpoint and DNS entries, verify that you are able to reach your cluster over Private Link.

    :::{include} _snippets/find-endpoint.md
    :::

To test the connection:

1. If needed, find the endpoint of an application in your deployment:
    
    :::{include} _snippets/find-endpoint.md
    :::

 1. Access your cluster over Private Link:

    * If you have a [custom endpoint alias](/deploy-manage/deploy/elastic-cloud/custom-endpoint-aliases.md) configured, you can use the custom endpoint URL to connect.
    * Test the setup using the following cURL command. Pass the username and password for a user that has access to the cluster. Make sure to replace the URL with your deployment's endpoint information and the private hosted zone domain name that you registered.

    **Request**
    ```sh
    $ curl -v https://my-deployment-d53192.es.psc.asia-southeast1.gcp.elastic-cloud.com:9243 -u {username}:{password}
    ```

    **Response**
    ```sh
    ..
    *   Trying 192.168.100.2...
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

Check the IP address. it should be the same as the IP address assigned to your Private Service Connect endpoint.

The connection is established, and a valid certificate is presented to the client. Elastic responds, in the case of the {{es}} endpoint, with basic information about the cluster.

## Optional: Create a private connection policy [ec-private-service-connect-allow-from-psc-connection-id]

After you test your Private Link connection, you can create a private connection policy in {{ecloud}}. 

Private connection policies are optional for GCP Private Service Connect. After the Private Service Connect endpoint and DNS record are created, private connectivity is established.

Creating a private connection policy and associating it with your deployments allows you to do the following: 

* Record that you've established private connectivity between GCP and Elastic in the applicable region.
* Filter traffic to your deployment using VPC filters.

Follow these high-level steps to add a private connection policy that can be associated with your deployments.

1. Optional: [Find your Private Service Connect connection ID](#ec-find-your-psc-connection-id).
2. [Create policies using the Private Service Connect endpoint connection ID](#create-private-connection-policy).
3. [Associate the Private Service Connect endpoint with your deployment](#associate-private-connection-policy).

### Optional: Find your Private Service Connect connection ID [ec-find-your-psc-connection-id]

The PSC connection ID is only required if you want to filter traffic to your deployment using VPC filters.

1. Go to your Private Service Connect endpoint in the Google Cloud console.
2. Copy the value of **PSC Connection ID**.

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
12. Optional: Under **VPC filter**, enter your Private Service Connect endpoint connection ID. You should only specify a Private Service Connect endpoint connection ID if you want to filter traffic to your deployment. 
    
    If you don't specify a VPC filter, then the private connection policy acts only as a record that you've established private connectivity between AWS and Elastic in the applicable region.
    
    :::{tip}
    You can apply multiple policies to a single deployment. The policies can be of different types. In case of multiple policies, traffic can match any associated policy to be forwarded to the resource. If none of the policies match, the request is rejected with `403 Forbidden`.

    [Learn more about how network security policies affect your deployment](network-security-policies.md).
    :::

13. Optional: Under **Apply to resources**, associate the new private connection policy with one or more deployments. If you specified a VPC filter, then after you associate the filter with a deployment, it starts filtering traffic.
14. To automatically attach this private connection policy to new deployments, select **Apply by default**.
15.  Click **Create**.
16. (Optional) You can [claim your Private Service Connect endpoint connection ID](/deploy-manage/security/claim-private-connection-api.md), so that no other organization is able to use it in a private connection policy.

The next step is to [associate the policy](#associate-private-connection-policy) with your deployment.

### Optional: Associate a policy with a deployment [associate-private-connection-policy]

You can associate a private connection policy with your deployment from the policy's settings, or from your deployment's settings. 

If the policy contains a VPC filter, then after you associate the policy with a deployment, it starts filtering traffic. 

If the policy doesn't contain a VPC filter, then the association can serve as a reminder that a Private Service Connect endpoint exists for the deployment's region.

#### From a deployment

:::{include} _snippets/associate-filter.md
:::

#### From the policy settings

:::{include} _snippets/network-security-page.md
:::
5. Find the policy you want to edit.
6. Under **Apply to resources**, associate the policy with one or more deployments.
7. Click **Update** to save your changes.

## Access the deployment over the Private Service Connect [ec-psc-access-the-deployment-over-psc]

For traffic to connect with the deployment over Private Service Connect, the client making the request needs to be located within the VPC where you’ve created the Private Service Connect endpoint. You can also set up network traffic to flow through the originating VPC from somewhere else, such as another VPC or a VPN from your corporate network. This assumes that the Private Service Connect endpoint and the DNS record are also available within that context. Check your cloud service provider documentation for setup instructions.

::::{important}
Use the alias you’ve set up as CNAME A record to access your deployment.
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
    $ curl -v https://my-deployment-d53192.es.psc.asia-southeast1.gcp.elastic-cloud.com:9243 -u {username}:{password}
    ```

    **Response**
    ```sh
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

### GCP Private Service Connect and Fleet

:::{include} _snippets/private-connection-fleet.md
:::

## Manage private connection policies

After you create your private connection policy, you can edit it, remove it from your deployment, or delete it.

### Edit a private connection policy [edit-private-connection-policy]

You can edit a policy's name, description, VPC endpoint ID, and more.

:::{include} _snippets/network-security-page.md
:::
1. Find the policy you want to edit, then click the **Edit** {icon}`pencil` button.
2. Click **Update** to save your changes.

:::{tip}
You can also edit network security policies from your deployment's **Security** page or your project's **Network security** page.
:::


### Remove a private connection policy from your deployment [remove-private-connection-policy]

If you want to a specific policy from a deployment, or delete the policy, then you need to disconnect it from any associated deployments first. You can do this from the policy's settings, or from your deployment's settings. To remove an association through the UI:

#### From your deployment

1. Find your deployment on the home page or on the **Hosted deployments** page, then select **Manage** to access its settings menus.

    On the **Hosted deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.
2. On the **Security** page, under **Network security**, find the policy that you want to disconnect. 
3. Under **Actions**, click the **Delete** icon.

#### From the policy settings

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
