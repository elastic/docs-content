---
applies_to:
  deployment:
    ess: ga
    ece: ga
navigation_title: "Remote cluster filters"
sub:
  policy-type: "Private connection"
---

# Remote cluster filtering

In {{ech}} (ECH) and {{ece}} (ECE), remote cluster filters let you control incoming traffic from other deployments that use the [remote clusters functionality](/deploy-manage/remote-clusters.md) with API key–based authentication. These filters are specific to ECH and ECE, because they rely on the certificates and proxy mechanisms provided by these environments.

::::{note} about terminology
In the case of remote clusters, the {{es}} cluster or deployment initiating the connection and requests is often referred to as the **local cluster**, while the {{es}} cluster or deployment receiving the requests is referred to as the **remote cluster**.
::::

::::{important}
Remote cluster filters aren’t supported when the local cluster runs in {{eck}} or is self-managed, or when connecting from an {{ece}} cluster to a remote {{ech}} deployment. For these cases, use an [IP filter](./ip-filtering-cloud.md) instead.

Refer to [Remote clusters and network security](/deploy-manage/remote-clusters.md#network-security) for more information about the remote clusters functionality, its relationship to network security, and the supported [use cases](/deploy-manage/remote-clusters.md#use-cases-network-security).
::::

## How remote cluster filters work

Remote cluster filters operate at the proxy level, filtering incoming connections based on the organization ID or {{es}} cluster ID of the local cluster that initiates the connection to the remote cluster service endpoint (default port `9443`).

Because of [how network security works](/deploy-manage/security/network-security.md#how-network-security-works), these filters are only relevant when network security is enabled on the remote cluster.
* If network security is disabled, all traffic is allowed by default and remote clusters work without any filtering policy.
* If network security is enabled, all traffic is blocked unless explicitly allowed. In this case, you must add a remote cluster filter in the remote cluster to permit remote cluster connections from the local clusters.

To apply a filter to a deployment, you must first create a security policy at the organization or platform level, and then apply it to your deployment.

This guide covers the following remote cluster filtering tasks:

* [Create a remote cluster filter](#create-remote-cluster-filter)
* [Associate a remote cluster filter with your deployment](#apply-remote-cluster-filter)
* [Remove a filter association from your deployment](#remove-association)
* [Edit a remote cluster filter](#edit-remote-cluster-filter)
* [Delete a remote cluster filter](#delete-remote-cluster-filter)

## Create a remote cluster filter [create-remote-cluster-filter]

:::::{tab-set}
:group: deployment
::::{tab-item} {{ech}}
:sync: ech
Remote cluster filters are presented in {{ecloud}} as a type of Private Connection filter. To create a remote cluster filter:

:::{include} _snippets/network-security-page.md
:::
4. Select **Create** > **Private connection**.
5. Select the cloud provider and region for the remote cluster filter. 
   
    :::{note}
    Network security policies are bound to a single region, and can be assigned only to deployments or projects in the same region. If you want to associate a policy with resources in multiple regions, then you have to create the same policy in all the regions you want to apply it to.
    :::

6. Under **Connectivity**, select **Remote cluster**.
7. Add a meaningful name and description for the filter.
8. In the **Organization ID** and **{{es}} ID** fields, enter the organization or cluster ID of the {{ecloud}} deployments from which you want to allow traffic. Provide one or both values; traffic is allowed if it matches either ID. To add multiple rules to the filter, use the plus (`+`) button.

    ::::{tip}
    * Find the organization ID on the organization page in the top-right menu, and the {{es}} ID of a deployment by selecting **Copy cluster ID** on the deployment management page.

    * {{ecloud}} supports filtering remote cluster traffic from deployments in the same and other ECH organizations, but not from ECE environments. Refer to the list of [supported use cases](/deploy-manage/remote-clusters.md#use-cases-network-security) for more information.
    ::::

9.  Optional: Under **Apply to resources**, associate the new filter with one or more deployments. After you associate the filter with a deployment, it will allow remote cluster traffic coming from the organization or {{es}} IDs defined in the rules.

    :::{note}
    You can apply multiple policies to a single deployment. For {{ech}} deployments, you can apply both IP filter policies and private connection policies. In case of multiple policies, traffic can match any associated policy to be forwarded to the resource. If none of the policies match, the request is rejected with `403 Forbidden`.

    [Learn more about how network security policies affect your deployment](network-security-policies.md).
    :::

8.  To automatically attach this filter to new deployments, select **Apply by default**.
9.   Click **Create**.
::::

::::{tab-item} {{ece}}
:sync: ece

To create a remote cluster filter:

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Security**.
3. Select **Create filter**.
4. Select **Remote cluster rule set** as the filter type.
5. Add a meaningful name and description for the rule set.
6. In the **Organization ID** and **{{es}} ID** fields, enter the organization or cluster ID of the deployments from which you want to allow traffic. Provide one or both values; traffic is allowed if it matches either ID. To add multiple rules to the filter, use the plus (`+`) button.

    :::{note}
    * ECE supports filtering remote cluster traffic from deployments in the same ECE system, in other ECE environments, or in {{ecloud}}.
    * For ECE systems, use the **Environment ID** from **Platform → Trust Management → Trust parameters** as the organization ID.
    * In {{ecloud}}, the organization ID is shown on the organization page in the top-right menu.
    * To get a deployment’s {{es}} ID, select **Copy cluster ID** on its management page in the Cloud UI or {{ecloud}} console.
    :::    

7. Select if this rule set should be automatically attached to new deployments.
8. Select **Create filter** to create the remote cluster filter.

:::{important}
Because this type of filter operates at the proxy level, if the local deployments or organizations in the filter belong to a different ECE environment or to ECH, you must add the transport TLS CA certificate of the local environment to the ECE proxy:

* Find the TLS CA certificate in the **Security -> Remote Connections -> CA certificates** section of any deployment of the environment that initiates the remote connection. In {{ecloud}}, each provider and region has its own CA certificate, while in ECE a single CA certificate is used for the entire installation.
    
* To add a CA certificate to the ECE proxy, go to **Platform -> Settings -> TLS certificates** in the UI and update the certificate chain used when configuring your ECE installation. Append the required CA certificates to the end of the chain. The final chain should look like this: `Proxy private key`, `Proxy SSL certificate`, `Proxy CA(s)`, followed by the remaining CAs. For more details, refer to [Add a proxy certificate](/deploy-manage/security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md#ece-tls-proxy).
:::


::::

:::::

## Associate a remote cluster filter with your deployment [apply-remote-cluster-filter]

After you've created the network security policy or rule set, you'll need to associate it with your deployment. To do that:

:::::::{tab-set}
:group: deployment

::::::{tab-item} {{ech}}
:sync: ech

#### From a deployment

:::{include} _snippets/associate-filter.md
:::

#### From the policy settings

:::{include} _snippets/network-security-page.md
:::
5. Find the policy you want to edit.
6. Under **Apply to resources**, associate the policy with one or more deployments.
7. Click **Update** to save your changes.
::::::

::::::{tab-item} {{ece}}
:sync: ece
:::{include} _snippets/associate-filter-ece.md
:::

::::::

:::::::

## Remove a filter association from your deployment [remove-association]

To remove a network security policy or rule set association from your deployment:

:::::::{tab-set}
:group: deployment

::::::{tab-item} {{ech}}
:sync: ech

You can remove associations from your deployments directly from the policy settings or from the deployment security page.

#### From your deployment security page
1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Hosted deployments** page, select your deployment.
3. Select the **Security** tab on the left-hand side menu bar.
4. Under **Network security**, find the security policy you want to disconnect.
5. Under **Actions**, click the **Delete** icon.

#### From the network security policy settings
:::{include} _snippets/network-security-page.md
:::
4. Find the remote cluster policy you want to edit, then select the **Edit** {icon}`pencil` button.
5. Under **Apply to resources**, click the `x` beside the resource that you want to disconnect.
6. Click **Update** to save your changes.


::::::

::::::{tab-item} {{ece}}
:sync: ece

:::{include} _snippets/detach-filter-ece.md
:::

::::::

:::::::

## Edit a remote cluster filter [edit-remote-cluster-filter]

You can edit a remote cluster filter policy name or change the list of allowed Organization IDs and {{es}} cluster IDs. To do that:

:::::::{tab-set}
:group: deployment

::::::{tab-item} {{ech}}
:sync: ech

:::{include} _snippets/network-security-page.md
:::
4. Find the remote cluster policy you want to edit, then select the **Edit** {icon}`pencil` button.
5. Select **Update** to save your changes.
::::::

::::::{tab-item} {{ece}}
:sync: ece

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Security**.
3. Find the rule set you want to edit.
4. Select the **Edit** {icon}`pencil` button.
5. Click **Update** to save your changes.
::::::

:::::::

## Delete a remote cluster filter [delete-remote-cluster-filter]

If you need to remove a remote cluster filter policy, you must first [remove any associations](#remove-association) with deployments.

To delete a filter:

:::::::{tab-set}
:group: deployment

::::::{tab-item} {{ech}}
:sync: ech

:::{include} _snippets/network-security-page.md
:::
4. Find the rule set you want to edit, then select the **Delete** {icon}`trash` button. The icon is inactive if there are deployments associated with the filter.
::::::

::::::{tab-item} {{ece}}
:sync: ece

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Security**.
3. Find the rule set you want to edit.
4. Click the **Delete** {icon}`trash` button. The button is inactive if there are deployments assigned to the rule set.
::::::

:::::::


