---
navigation_title: In ECH or Serverless
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-traffic-filtering-ip.html
  - https://www.elastic.co/guide/en/cloud/current/ec-traffic-filtering-ip.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-traffic-filtering-ip.html
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-hosted
  - id: cloud-serverless
sub:
  policy-type: "IP filter"
---

# Manage IP filters in ECH or Serverless

Filtering network traffic, by IP address or CIDR block, is one of the security layers available in {{ece}} and {{ech}}. It allows you to limit how your deployments can be accessed. IP filters are a type of [network security policy](/deploy-manage/security/network-security-policies.md).

There are types of filters are available for filtering by IP address or CIDR block:

* **Ingress or inbound IP filters**: These restrict access to your deployments from a set of IP addresses or CIDR blocks. These filters are available through the UI.
* **Egress or outbound IP filters**: These restrict the set of IP addresses or CIDR blocks accessible from your deployment. These might be used to restrict access to a certain region or service. This feature is currently only available through the [Traffic Filtering API](/deploy-manage/security/network-security-api.md). {applies_to}`ess: beta` {applies_to}`serverless: unavailable` 

Follow the step described here to set up ingress or inbound IP filters through the {{ecloud}} Console.

To learn how IP filters work together, and alongside [private connection policies](private-connectivity.md), refer to [](/deploy-manage/security/network-security-policies.md).

To learn how to manage IP filters using the Traffic Filtering API, refer to [](/deploy-manage/security/network-security-api.md).

:::{note}
To learn how to create IP filters for {{ece}} deployments, refer to [](ip-filtering-ece.md).

To learn how to create IP filters for self-managed clusters or {{eck}} deployments, refer to [](ip-filtering-basic.md).
:::

## Apply an IP filter to a deployment or project

To apply an IP filter to a deployment or project, you must first create an IP filter policy (referred to as "IP filter") at the organization or platform level, and then apply it to your deployment.

### Step 1: Create an IP filter

You can combine multiple IP address and CIDR block traffic sources into a single IP filter, so we recommend that you group sources according to what they allow, and make sure to label them accordingly. Because multiple IP filters can be applied to a deployment, you can be as granular in your IP filter policies as you require.

To create an IP filter:

:::{include} _snippets/network-security-page.md
::: 
1. Select **Create** > **IP filter**.
2. Select the resource type that the IP filter will be applied to: either hosted deployments or serverless projects.
3. Select the cloud provider and region for the IP filter. 
   
    :::{tip}
    IP filters are bound to a single region, and can be assigned only to deployments or projects in the same region. If you want to associate an IP filter with resources in multiple regions, then you have to create the same filter in all the regions you want to apply it to.
    :::
4. Add a meaningful name and description for the IP filter.
5. Under **Access control**, select whether the IP filter should be applied to ingress or egress traffic. Currently, only ingress traffic filters are supported.
6. Add one or more allowed sources using IPv4, or a range of addresses with CIDR.

    ::::{note}
    DNS names are not supported in IP filters.
    ::::
7.  Optional: Under **Apply to resources**, associate the new filter with one or more deployments or projects. After you associate the  IP filter with a deployment or project, it starts filtering traffic.

    :::{tip}
    You can apply multiple policies to a single deployment. For {{ech}} deployments, you can apply both IP filter policies and private connection policies. In case of multiple policies, traffic can match any associated policy to be forwarded to the resource. If none of the policies match, the request is rejected with `403 Forbidden`.

    [Learn more about how network security policies affect your deployment](network-security-policies.md).
    :::

8.  To automatically attach this IP filter to new deployments or projects, select **Apply by default**.
9.   Click **Create**.

### Step 2: Associate an IP filter with a deployment or project

You can associate an IP filter with your deployment or project from the IP filter's settings, or from your deployment or project's settings. After you associate the IP filter with a deployment or project, it starts filtering traffic.

:::{tip}
You can apply multiple policies to a single deployment. For {{ech}} deployments, you can apply both IP filter policies and private connection policies. In case of multiple policies, traffic can match any associated policy to be forwarded to the resource. If none of the policies match, the request is rejected with `403 Forbidden`.

[Learn more about how network security policies affect your deployment](network-security-policies.md).
:::

#### From a deployment or project

::::{tab-set}
:::{tab-item} Serverless
1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Serverless projects** page, select your project.
3. Select the **Network security** tab on the left-hand side menu bar.
4. Select **Apply policies** > **IP filter**.
6. Choose the IP filter you want to apply and select **Apply**.
:::
:::{tab-item} Hosted
1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Hosted deployments** page, select your deployment.
3. Select the **Security** tab on the left-hand side menu bar.
4. Under **Network security**, select **Apply policies** > **IP filter**.
5. Choose the IP filter you want to apply and select **Apply**.
:::
::::

#### From the IP filter settings

:::{include} _snippets/network-security-page.md
:::
5. Find the IP filter you want to edit.
6. Under **Apply to resources**, associate the IP filter with one or more deployments or projects.
7. Click **Update** to save your changes.

## Remove an IP filter from your deployment or project [remove-filter-deployment]

If you want to a specific IP filter from a deployment or project, or delete the IP filter, you’ll need to disconnect it from any associated deployments or projects first. You can do this from the IP filter's settings, or from your deployment or project's settings. To remove an association through the UI:

#### From your deployment or project

::::{tab-set}
:group: hosted-serverless
:::{tab-item} Serverless project
:sync: serverless
1. Find your project on the home page or on the **Serverless projects** page, then select **Manage** to access its settings menus.

    On the **Hosted deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.
2. On the **Network security** page, find the IP filter that you want to disconnect. 
3. Under **Actions**, click the **Delete** icon.
:::
:::{tab-item} Hosted deployment
:sync: hosted
1. Find your deployment on the home page or on the **Hosted deployments** page, then select **Manage** to access its settings menus.

    On the **Hosted deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.
2. On the **Security** page, under **Network security**, find the IP filter that you want to disconnect. 
3. Under **Actions**, click the **Delete** icon.
:::
::::

#### From the IP filter settings

:::{include} _snippets/network-security-page.md
:::
5. Find the IP filter you want to edit, then click the **Edit** {icon}`pencil` button.
6. Under **Apply to resources**, click the `x` beside the resource that you want to disconnect.
7. Click **Update** to save your changes.

## Edit an IP filter

You can edit an IP filter's name or description, change the allowed traffic sources, and change the associated resources, and more.

:::{include} _snippets/network-security-page.md
:::
1. Find the IP filter you want to edit, then click the **Edit** {icon}`pencil` button.
2. Click **Update** to save your changes.

:::{tip}
You can also edit IP filters from your deployment's **Security** page or your project's **Network security** page.
:::

## Delete an IP filter

If you need to remove an IP filter, you must first remove any associations with deployments.

To delete an IP filter:

:::{include} _snippets/network-security-page.md
:::
1. Find the IP filter you want to edit, then click the **Delete** {icon}`trash` button. The icon is inactive if there are deployments or projects associated with the IP filter.
