---
applies_to:
  deployment:
    ess: ga
    ece: ga
navigation_title: "Remote cluster filters"
---

# Remote cluster filtering

In {{ech}} (ECH) and {{ece}} (ECE), remote cluster filters let you control incoming traffic from other deployments that use the [Remote clusters functionality](/deploy-manage/remote-clusters.md) with [API key–based authentication](/deploy-manage/remote-clusters/remote-clusters-api-key.md).

::::{note} about terminology
In the case of remote clusters, the {{es}} cluster or deployment initiating the connection and requests is often referred to as the **local cluster**, while the {{es}} cluster or deployment receiving the requests is referred to as the **remote cluster**.
::::

Remote cluster filters operate at the proxy level, filtering incoming connections based on the organization ID or {{es}} cluster ID of the local cluster that initiates the connection to the remote cluster service endpoint (default port `9443`).

Because of [how network security works](/deploy-manage/security/network-security.md#how-network-security-works), these filters are only relevant when network security is enabled on the remote cluster.
* If network security is disabled, all traffic is allowed by default and remote clusters work without any filtering policy.
* If network security is enabled, all traffic is blocked unless explicitly allowed. In this case, you must add a remote cluster filter in the remote cluster to permit remote cluster connections from the local clusters.

Refer to [Remote clusters and network security](/deploy-manage/remote-clusters.md#network-security) for more information about the remote clusters functionality, its relationship to network security, and the supported use cases.

## Create remote cluster filter [create-remote-cluster-filter]

:::::{tab-set}

::::{tab-item} {{ech}}

Remote cluster filters are presented in {{ecloud}} as a type of Private Connection filters. To create a remote cluster filter:

:::{include} _snippets/network-security-page.md
:::
4. Select **Create** > **Private connection**.
5. Select the cloud provider and region for the remote cluster filter. 
   
    :::{tip}
    Network security policies are bound to a single region, and can be assigned only to deployments or projects in the same region. If you want to associate an IP filter with resources in multiple regions, then you have to create the same filter in all the regions you want to apply it to.
    :::

6. In the **Connectivity** section, select **Remote cluster**.
7. Add a meaningful name and description for the filter.
8. In the **Organization ID** and **{{es}} ID** fields, enter the organization or cluster ID of the {{ecloud}} deployments from which you want to allow traffic. Provide one or both values; traffic is allowed if it matches either ID. To add multiple rules to the filter, use the plus (`+`) button.

    ::::{tip}
    Find the organization ID on the organization page in the top-right menu, and the {{es}} ID of a deployment by selecting **Copy cluster ID** on the deployment management page.
    ::::

    % Not sure if we want any of this
    ::::{important}
    Network security filtering for remote cluster traffic from ECE to ECH is not supported. These filters apply only to {{ecloud}} resources, so the values must be {{ecloud}} IDs.

    If you require network security policies in the remote deployment for remote cluster connections coming from ECE, consider configuring the remote clusters with the deprecated [TLS certificate–based authentication model](/deploy-manage/remote-clusters/ece-remote-cluster-ece-ess.md). Traffic with this model is authenticated through mTLS and is not subject to network security filters.

    Refer to [Remote clusters and network security](/deploy-manage/remote-clusters.md#network-security) for more information.
    ::::    

9.  Optional: Under **Apply to resources**, associate the new filter with one or more deployments. After you associate the filter with a deployment, it will allow remote cluster traffic coming from the organization or {{es}} IDs defined in the rules.

    :::{tip}
    You can apply multiple policies to a single deployment. For {{ech}} deployments, you can apply both IP filter policies and private connection policies. In case of multiple policies, traffic can match any associated policy to be forwarded to the resource. If none of the policies match, the request is rejected with `403 Forbidden`.

    [Learn more about how network security policies affect your deployment](network-security-policies.md).
    :::

8.  To automatically attach this filter to new deployments, select **Apply by default**.
9.   Click **Create**.


::::

::::{tab-item} {{ece}}

To create a remote cluster filter:

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Security**.
3. Select **Create filter**.
4. Select **Remote cluster rule set** as the filter type.
5. Add a meaningful name and description for the rule set.
6. In the **Organization ID** and **{{es}} ID** fields, enter the organization or cluster ID of the deployments from which you want to allow traffic. Provide one or both values; traffic is allowed if it matches either ID. To add multiple rules to the filter, use the plus (`+`) button.

    :::note
    * ECE supports filtering remote cluster traffic from deployments in the same ECE system, in other ECE environments, or in {{ecloud}}.
    * For ECE systems, use the **Environment ID** from **Platform → Trust Management → Trust parameters** as the organization ID.
    * In {{ecloud}}, the organization ID is shown on the organization page in the top-right menu.
    * To get a deployment’s {{es}} ID, select **Copy cluster ID** on its management page in the Cloud UI.
    :::    

7. Select if this rule set should be automatically attached to new deployments.
8. Select **Create filter** to create the remote cluster filter.

:::{important}
Because this type of filter operates at the proxy level, if the local deployments or organizations in the filter belong to a different ECE environment or to ECH, you must add the transport TLS CA certificate of the local environment to the ECE proxy:

* Find the TLS CA certificate in the **Security -> Remote Connections -> CA certificates** section of any deployment of the environment that initiates the remote connection. In {{ecloud}}, each provider and region has its own CA certificate, while in ECE a single CA certificate is used per installation.
    
* To add a CA certificate to the ECE proxy, go to **Platform -> Settings -> TLS certificates** in the UI and update the certificate chain used when configuring your ECE installation. Append the required CA certificates to the end of the chain. The final chain should look like this: `Proxy private key`, `Proxy SSL certificate`, `Proxy CA(s)`, followed by the remaining CAs. For more details, refer to [Add a proxy certificate](/deploy-manage/security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md#ece-tls-proxy).
:::


::::

:::::

## Associate a remote filter to a deployment

(Work in progress)

On ECE: 

After you’ve created the policy or rule set, you’ll need to associate it with your deployment:

1. Go to the deployment.
2. On the **Security** page, under **Traffic filters**, select **Apply filter**.
3. Choose the filter you want to apply and select **Apply filter**.


On Cloud:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Hosted deployments** page, select your deployment.
3. Select the **Security** tab on the left-hand side menu bar.
4. Under **Network security**, select **Apply policies** > **IP filter**.
5. Choose the IP filter you want to apply and select **Apply**.
