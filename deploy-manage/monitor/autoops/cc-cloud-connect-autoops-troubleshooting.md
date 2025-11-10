---
applies_to:
  deployment:
    self:
    ece:
    eck:
navigation_title: Troubleshooting
products:
  - id: cloud-kubernetes
  - id: cloud-enterprise
---

# AutoOps for self-managed clusters troubleshooting

Learn about issues that might come up when connecting your clusters and using AutoOps.

## Troubleshoot issues

Use this guide to troubleshoot any issues you may encounter.

* [I’m trying to create a Cloud organization, but I’m already part of a different one.](#single-cloud-org)
* [I need to uninstall {{agent}}.](#unistall-agent)
* [My cluster was disconnected from {{ecloud}} and I want to reconnect it.](#disconnected-cluster)
* [After running the installation command, I can't move on to the next steps.](#next-steps)
* [My organization's firewall may be preventing {{agent}} from collecting and sending metrics.](#firewall)

$$$single-cloud-org$$$**I’m trying to create a Cloud organization, but I’m already part of a different one.**
:   :::{include} /deploy-manage/monitor/_snippets/single-cloud-org.md
:::

$$$unistall-agent$$$**I need to uninstall {{agent}}.**
:   Refer to [](/solutions/security/configure-elastic-defend/uninstall-elastic-agent.md) for instructions.

$$$disconnected-cluster$$$**My cluster was disconnected from {{ecloud}} and I want to reconnect it.**
:   If the cluster was disconnected by one of the users in your Cloud organization, you can repeat the [installation process](/deploy-manage/monitor/autoops/cc-connect-self-managed-to-autoops.md) to reconnect. If not, explore [additional resources](/troubleshoot/index.md#troubleshoot-additional-resources) or [contact us](/troubleshoot/index.md#contact-us).

$$$next-steps$$$**After running the installation command, I can't move on to the next steps.**
:   If an error appears on the screen, follow the suggestion in the error message and try to run the command again. If the issue is not resolved, explore [additional resources](/troubleshoot/index.md#troubleshoot-additional-resources) or [contact us](/troubleshoot/index.md#contact-us).

$$$firewall$$$**My organization's firewall may be preventing {{agent}} from collecting and sending metrics.**
:   If you're having issues with connecting your cluster to AutoOps and you suspect that a firewall may be the reason, refer to [](/deploy-manage/monitor/autoops/autoops-sm-troubleshoot-firewalls.md).

## Potential errors

The following table shows the errors you might encounter if something goes wrong while you set up and use AutoOps on your clusters.

| Error code | Error message | Description |
| :--- | :--- | :--- |
| `HTTP_401` | Authentication failed | Connection denied because of an authentication error. Verify that your API key and password are correct and all [necessary privileges](/deploy-manage/monitor/autoops/cc-connect-self-managed-to-autoops.md#configure-agent) have been granted. |
| `HTTP_502` | Server error | Received an invalid response from the server. Verify the server status and network configuration. |
| `HTTP_503` | Server unavailable | Invalid or corrupt response received from the server. The server acting as a proxy may be busy or undergoing scheduled maintenance. If the issue persists, check the cluster's health and resource usage. |
| `HTTP_504` | Request timed out | Did not receive a response from the cluster within the expected time frame. Check the cluster's performance or consider changing your connection timeout settings. |
| `CLUSTER_ALREADY_CONNECTED` | Cluster connected to another account | This cluster is already connected to another {{ecloud}} organization. Disconnect it and then try again. |
| `CLUSTER_NOT_READY` | {{es}} cluster is still connecting | Your {{es}} cluster is not yet ready to connect. Wait a few moments for it to finish starting up and then try again. |
| `HTTP_0` | Connection error | {{agent}} couldn't connect to the cluster. There may be various reasons for this issue. Review the [documentation](/deploy-manage/monitor/autoops/cc-autoops-as-cloud-connected.md) or contact [Elastic support](https://support.elastic.co/) if the issue persists. |
| `LICENSE_EXPIRED` | Elastic license is expired | Contact [sales](https://www.elastic.co/contact#sales) to renew your license. |
| `LICENSE_USED_BY_ANOTHER_ACCOUNT` | License key connected to another account | A license key can only be connected to one {{ecloud}} organization. Contact [Elastic support](https://support.elastic.co/) for help. |
| `VERSION_MISMATCH` | {{es}} version is unsupported | Upgrade your cluster to a [supported version](https://www.elastic.co/support/eol). |
| `UNKNOWN_ERROR` | Installation failed | {{agent}} couldn't be installed due to an unknown issue. Consult the troubleshooting guide or contact [Elastic support](https://support.elastic.co/) for more help. |
| | Failed to register Cloud Connected Mode: cluster license type is not supported | The cluster you are trying to connect doesn't have the required license to connect to AutoOps. For more information, refer to the [prerequisites](/deploy-manage/monitor/autoops/cc-connect-self-managed-to-autoops.md#prerequisites). |
