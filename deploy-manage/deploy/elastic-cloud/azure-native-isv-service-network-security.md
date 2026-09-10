---
applies_to:
  deployment:
    ech: ga
products:
  - id: cloud-hosted
navigation_title: Network security
description: Restrict access to Azure Native Service hosted deployments with IP filters and private connection policies.
---

# Manage network security in the Azure Native Service

You can restrict access to {{ech}} deployments created through the [Azure Native Service](azure-native-isv-service.md) by applying [network security policies](/deploy-manage/security/network-security-policies.md). Policies include [IP filters](/deploy-manage/security/ip-filtering-cloud.md) and [private connections](/deploy-manage/security/private-connectivity.md).

This page covers how to create and associate those policies from the Azure portal Traffic Filter page.

:::{include} _snippets/azure-native-network-security-surfaces.md
:::

For {{ecloud}} Console steps that apply to both {{ech}} and {{serverless-short}}, refer to [](/deploy-manage/security/ip-filtering-cloud.md) and [](/deploy-manage/security/private-connectivity-azure.md).

Policies you create in the Azure portal appear in the {{ecloud}} Console under **Network security**, labeled **Created from Azure**. Policies created in the {{ecloud}} Console also appear in the Azure portal list. Linking or unlinking in either place updates the association.

Microsoft also documents this page in [Manage settings for your Elastic resource](https://learn.microsoft.com/en-us/azure/partner-solutions/elastic/manage#traffic-filters).


## Add a Private Link private connection policy

To create a private connection policy, you must first create the private endpoint and DNS records in Azure, and then create the policy in the Azure portal.

### Step 1: Create the private endpoint and DNS records in Azure

Follow the steps to [create your private endpoint and DNS entries in Azure](/deploy-manage/security/private-connectivity-azure.md#ec-private-link-azure-dns). This procedure creates the private endpoint and DNS records using regional [service aliases and private hosted zone names](/deploy-manage/security/private-connectivity-azure.md#ec-private-link-azure-service-aliases).

### Step 2: Create the private connection policy in the Azure portal

After you create the private endpoint and DNS records in Azure, you can create the private connection policy in the Azure portal.

1. In the Azure portal, open your Elastic resource, then select **Elastic Cloud Resource Configuration** > **Traffic Filter**.
2. Select **Add**.
3. Enter a filter name.
4. Set **Filter Type** to **Private Link**.
5. Choose how to identify the private endpoint:

   * **Select Existing**: Choose the Azure subscription that contains the private endpoint, then choose the private endpoint from the list.
   * **Add Manually**: Enter the private endpoint GUID and name. To find these values, refer to [](/deploy-manage/security/private-connectivity-azure.md#ec-find-your-resource-name) and [](/deploy-manage/security/private-connectivity-azure.md#ec-find-your-resource-id).

6. Create the filter.
7. Select the new filter in the list, then select **Link** so the status shows **Linked** for this deployment.

The policy must be in the same region as the deployment. Policies from other regions can appear in the list but remain **Not Linked** on this resource.

## Add an IP filter

Create and link an IP filter from the Azure portal to allowlist IPv4 addresses or CIDR blocks.

1. In the Azure portal, open your Elastic resource, then select **Elastic Cloud Resource Configuration** > **Traffic Filter**.
2. Select **Add**.
3. Enter a filter name.
4. Set **Filter Type** to **IP filtering rule set**.
5. Add the IPv4 addresses or CIDR blocks to allow.
6. Create the filter.
7. Select the filter, then select **Link**.

The policy must be in the same region as the deployment. Policies from other regions can appear in the list but remain **Not Linked** on this resource.

## Unlink or delete a policy

Remove a policy from this deployment, or delete it from your organization, in the Azure portal.

1. In the Azure portal, open your Elastic resource, then select **Elastic Cloud Resource Configuration** > **Traffic Filter**.
2. To stop a policy from applying to this deployment, select it and choose **Unlink**. The policy remains available in your organization.
3. To delete a policy, unlink it from all deployments first, then select **Delete**.
