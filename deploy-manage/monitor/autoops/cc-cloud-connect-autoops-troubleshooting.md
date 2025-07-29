---
applies_to:
  deployment:
    self:
    ece:
    eck:
navigation_title: Troubleshooting
---

# AutoOps for self-managed clusters troubleshooting

Learn about issues that might come up when using AutoOps with your self-managed cluster.

## Troubleshoot issues

Use this guide to troubleshoot any issues you may encounter.

:::{dropdown} I’m trying to create a Cloud organization, but I’m already part of a different one.

:::{include} /deploy-manage/monitor/_snippets/single-cloud-org.md
:::

:::

:::{dropdown} I need to uninstall {{agent}}.

Refer to [](/solutions/security/configure-elastic-defend/uninstall-elastic-agent.md) for instructions.
:::

:::{dropdown} My self-managed cluster was disconnected from {{ecloud}} and I want to reconnect it.

If the cluster was disconnected by one of the users in your Cloud organization, you can repeat the [installation process](/deploy-manage/monitor/autoops/cc-connect-self-managed-to-autoops.md) to reconnect. If not, explore [additional resources](/troubleshoot/index.md#troubleshoot-additional-resources) or [contact us](/troubleshoot/index.md#contact-us).

:::{include} /deploy-manage/monitor/_snippets/disconnect-cluster.md
:::

:::

:::{dropdown} After running the installation command, I can't move on to the next steps.

If an error appears on the screen, follow the suggestion in the error message and try to run the command again. If the issue is not resolved, explore [additional resources](/troubleshoot/index.md#troubleshoot-additional-resources) or [contact us](/troubleshoot/index.md#contact-us).
:::

## Potential errors

The following table shows the errors you might encounter if something goes wrong while you set up and use AutoOps for self-managed clusters.

| Error code | Error message | Description |
| :--- | :--- | :--- |
| `HTTP_401` | Authentication failed | Connection denied because of an authentication error. Verify that your API key and password are correct and all [necessary privileges](/deploy-manage/monitor/autoops/cc-connect-self-managed-to-autoops.md#configure-agent) have been granted. |
| `HTTP_502` | Server error | Received an invalid response from the server. Verify the server status and network configuration. |
| `HTTP_503` | Server unavailable | Invalid or corrupt response received from the server. The server acting as a proxy may be busy or undergoing scheduled maintenance. If the issue persists, check the cluster's health and resource usage. |
| `HTTP_504` | Request timed out | Did not receive a response from the cluster within the expected time frame. Check the cluster's performance or consider changing your connection timeout settings. |
| `CLUSTER_ALREADY_CONNECTED` | Cluster connected to another account | This cluster is already connected to another {{ecloud}} organization. Disconnect it and then try again. |
| `CLUSTER_NOT_READY` | {{es}} cluster is still connecting | Your {{es}} cluster is not yet ready to connect. Wait a few moments for it to finish starting up and then try again. |
| `HTTP_0` | Connection error | {{agent}} couldn't connect to the cluster. There may be various reasons for this issue. Review the [documentation](/deploy-manage/monitor/autoops/cc-autoops-as-cloud-connected.md) or contact [Elastic support](https://cloud.elastic.co/login?source=support&fromURI=https%3A%2F%2Fauth.elastic.co%2Fapp%2Felastic-customer_dreammachinecustomer_1%2Fexkgw653gkKlRTQXQ1t7%2Fsso%2Fsaml) if the issue persists. |
| `LICENSE_EXPIRED` | Elastic license is expired | Contact [sales](https://www.elastic.co/contact#sales) to renew your license. |
| `LICENSE_USED_BY_ANOTHER_ACCOUNT` | License key connected to another account | A license key can only be connected to one {{ecloud}} organization. Contact [Elastic support](https://cloud.elastic.co/login?source=support&fromURI=https%3A%2F%2Fauth.elastic.co%2Fapp%2Felastic-customer_dreammachinecustomer_1%2Fexkgw653gkKlRTQXQ1t7%2Fsso%2Fsaml) for help. |
| `VERSION_MISMATCH` | {{es}} version is unsupported | Upgrade your cluster to a [supported version](https://www.elastic.co/support/eol). |
| `UNKNOWN_ERROR` | Installation failed | {{agent}} couldn't be installed due to an unknown issue. Consult the troubleshooting guide or contact [Elastic support](https://cloud.elastic.co/login?source=support&fromURI=https%3A%2F%2Fauth.elastic.co%2Fapp%2Felastic-customer_dreammachinecustomer_1%2Fexkgw653gkKlRTQXQ1t7%2Fsso%2Fsaml) for more help. |