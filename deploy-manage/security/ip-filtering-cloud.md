---
navigation_title: In ECH or Serverless
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-traffic-filtering-ip.html
  - https://www.elastic.co/guide/en/cloud/current/ec-traffic-filtering-ip.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-traffic-filtering-ip.html
applies_to:
  deployment:
    ess: ga
    ece: ga
    serverless: ga
products:
  - id: cloud-hosted
  - id: cloud-serverless
sub:
  policy-type: "IP filter"
---

# Manage IP filters in ECH or Serverless

Traffic filtering, by IP address or CIDR block, is one of the security layers available in {{ece}} and {{ech}}. It allows you to limit how your deployments can be accessed.

There are types of filters are available for filtering by IP address or CIDR block:

* **Ingress or inbound IP filters**: These restrict access to your deployments from a set of IP addresses or CIDR blocks. These filters are available through the UI.
* **Egress or outbound IP filters**: These restrict the set of IP addresses or CIDR blocks accessible from your deployment. These might be used to restrict access to a certain region or service. This feature is in beta and is currently only available through the [Traffic Filtering API](/deploy-manage/security/ec-traffic-filtering-through-the-api.md).

Follow the step described here to set up ingress or inbound IP filters through the {{ecloud}} Console.

To learn how IP filter policies work together, and alongside [private connection policies](private-link-traffic-filters.md), refer to [](/deploy-manage/security/network-security-policies.md).

To learn how to manage IP traffic filters using the Traffic Filtering API, refer to [](/deploy-manage/security/ec-traffic-filtering-through-the-api.md).

:::{note}
To learn how to create IP filters for {{ece}} deployments, refer to [](ip-filtering-ece.md).

To learn how to create IP filters for self-managed clusters or {{eck}} deployments, refer to [](ip-filtering-basic.md).
:::

## Apply an IP filter to a deployment or project

To apply an IP filter to a deployment or project, you must first create a rule set at the organization or platform level, and then apply the rule set to your deployment.

### Step 1: Create an IP filter policy

You can combine multiple IP address and CIDR block traffic sources into a single IP filter policy, so we recommend that you group sources according to what they allow, and make sure to label them accordingly. Because multiple sets can be applied to a deployment, you can be as granular in your policies as you feel is necessary.

To create an IP filter policy:

:::{include} _snippets/network-security-page.md
::: 
4. Select **Create** > **IP filter**.
3. Select the resource type that the IP filter will be applied to: either hosted deployments or serverless projects.
4. Select the cloud provider and region for the filter. 
   
    :::{tip}
    Network security policies are bound to a single region, and can be assigned only to deployments or projects in the same region. If you want to associate a policy with resources in multiple regions, then you have to create the same policy in all the regions you want to apply it to.
    :::
5. Add a meaningful name and description for the filter.
6. Under **Access control**, select whether the filter should be applied to ingress or egress traffic. Currently, only ingress traffic filters are supported.
7. Add one or more allowed sources using IPv4, or a range of addresses with CIDR.

    ::::{note}
    DNS names are not supported in network security policies.
    ::::
8.  Optional: Under **Apply to resources**, associate the new filter with one or more deployments or projects. After you associate the filter with a deployment or project, it starts filtering traffic.
9.  To automatically attach this IP filter policy to new deployments or projects, select **Apply by default**.
10.  Click **Create**.

### Step 2: Associate a policy with a deployment or project

You can associate a network security policy with your deployment or project from the policy's settings, or from your deployment or project's settings. After you associate the policy with a deployment or project, it starts filtering traffic.

#### From a deployment or project

:::{include} _snippets/associate-filter.md
:::

#### From the policy settings

:::{include} _snippets/network-security-page.md
:::
5. Find the policy you want to edit.
6. Under **Apply to resources**, associate the policy with one or more deployments or projects.
7. Click **Update** to save your changes.

## Remove an IP filter policy from your deployment or project [remove-filter-deployment]

If you want to a specific IP filter policy from a deployment or project, or delete the policy, you’ll need to disconnect it from any associated deployments or projects first. You can do this from the policy's settings, or from your deployment or project's settings. To remove an association through the UI:

#### From your deployment or project

::::{tab-set}
:group: hosted-serverless
:::{tab-item} Serverless project
:sync: serverless
1. Find your project on the home page or on the **Serverless projects** page, then select **Manage** to access its settings menus.

    On the **Hosted deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.
2. On the **Network security** page, find the IP filter policy that you want to disconnect. 
3. Under **Actions**, click the **Delete** icon.
:::
:::{tab-item} Hosted deployment
:sync: hosted
1. Find your deployment on the home page or on the **Hosted deployments** page, then select **Manage** to access its settings menus.

    On the **Hosted deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.
2. On the **Security** page, under **Network security**, find the IP filter policy that you want to disconnect. 
3. Under **Actions**, click the **Delete** icon.
:::
::::

#### From the IP filter policy settings

:::{include} _snippets/network-security-page.md
:::
5. Find the policy you want to edit, then click the **Edit** icon.
6. Under **Apply to resources**, click the `x` beside the resource that you want to disconnect.
7. Click **Update** to save your changes.

## Edit an IP filter policy

You can edit an IP filter policy's name or description, change the allowed traffic sources, and change the associated resources, and more.

:::{include} _snippets/network-security-page.md
:::
4. Find the policy you want to edit, then click the **Edit** icon.
5. Click **Update** to save your changes.

:::{tip}
You can also edit network security policies from your deployment's **Security** page or your project's **Network security** page.
:::

## Delete an IP filter policy

If you need to remove a policy, you must first remove any associations with deployments.

To delete a policy:

:::{include} _snippets/network-security-page.md
:::
4. Find the policy you want to edit, then click the **Delete** icon. The icon is inactive if there are deployments or projects associated with the policy.