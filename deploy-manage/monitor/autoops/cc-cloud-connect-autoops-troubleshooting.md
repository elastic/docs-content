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

# AutoOps for ECE, ECK, or self-managed clusters troubleshooting

Learn about issues that might come up when connecting your clusters and using AutoOps.

## Troubleshoot issues

Use this guide to troubleshoot any issues you may encounter.

* [I’m trying to create a Cloud organization, but I’m already part of a different one.](#single-cloud-org)
* [I need to uninstall {{agent}}.](#unistall-agent)
* [My cluster was disconnected from {{ecloud}} and I want to reconnect it.](#disconnected-cluster)
* [After running the installation command, I can't move on to the next steps.](#next-steps)
* [My organization's firewall might be preventing {{agent}} from collecting and sending metrics.](#firewall)
* [{{agent}} is failing to connect because it doesn't recognize my SSL certificate.](#custom-cert)
* [I went through the wizard with {{ECK}} (ECK) as my installation method, but I can't view any connected clusters in my account.](#eck-no-clusters) {applies_to}`eck: ga 3.3`
* [My `AutoOpsAgentPolicy` resource entered the `Invalid` phase after a license change.](#invalid-phase-license-change) {applies_to}`eck: ga 3.3`

$$$single-cloud-org$$$**I’m trying to create a Cloud organization, but I’m already part of a different one.**
:   :::{include} /deploy-manage/monitor/_snippets/single-cloud-org.md
:::

$$$unistall-agent$$$**I need to uninstall {{agent}}.**
:   Refer to [](/solutions/security/configure-elastic-defend/uninstall-elastic-agent.md) for instructions.

$$$disconnected-cluster$$$**My cluster was disconnected from {{ecloud}} and I want to reconnect it.**
:   If the cluster was disconnected by one of the users in your Cloud organization, you can repeat the [installation process](/deploy-manage/monitor/autoops/cc-connect-self-managed-to-autoops.md) to reconnect. If not, explore [additional resources](/troubleshoot/index.md#troubleshoot-additional-resources) or [contact us](/troubleshoot/index.md#contact-us).

$$$next-steps$$$**After running the installation command, I can't move on to the next steps.**
:   If an error appears on the screen, follow the suggestion in the error message and try to run the command again. If the issue is not resolved, explore [additional resources](/troubleshoot/index.md#troubleshoot-additional-resources) or [contact us](/troubleshoot/index.md#contact-us).

:::{tip}
If you're having issues connecting your cluster to AutoOps and sending metrics to {{ecloud}}, run the [AutoOps Connectivity Check](../autoops/autoops-connectivity-check.md) to test your configuration.
:::

$$$firewall$$$**My organization's firewall might be preventing {{agent}} from collecting and sending metrics.**
:   If you're having issues with connecting your cluster to AutoOps and you suspect that a firewall may be the reason, refer to [](/deploy-manage/monitor/autoops/autoops-sm-troubleshoot-firewalls.md).

$$$custom-cert$$$**{{agent}} is failing to connect because it doesn't recognize my SSL certificate.**
:   If {{agent}} is failing to connect your cluster to AutoOps because it doesn't recognize your SSL certificate, refer to [](/deploy-manage/monitor/autoops/autoops-sm-custom-certification.md). 

$$$eck-no-clusters$$$**I went through the wizard with {{ECK}} (ECK) as my installation method, but I can't view any connected clusters in my account.** {applies_to}`eck: ga 3.3`
:   Refer to [](/deploy-manage/monitor/autoops/autoops-sm-troubleshoot-eck-no-clusters.md) to diagnose and resolve common issues.

$$$invalid-phase-license-change$$$**My `AutoOpsAgentPolicy` resource entered the `Invalid` phase after a license change.** {applies_to}`eck: ga 3.3`
:   The [minimum required {{agent}} version](/deploy-manage/monitor/autoops/cc-connect-self-managed-to-autoops.md#prerequisites) for the ECK installation method depends on your license type. Enterprise licenses require agent versions 9.2.1 and later, and Basic licenses require versions 9.2.4 or later. If your license is downgraded from Enterprise to Basic and your agent version is between 9.2.1 and 9.2.3, the policy will fail validation and enter the `Invalid` phase.

    To resolve this issue, upgrade {{agent}}.

## Run the AutoOps Connectivity Check

Run the [AutoOps Connectivity Check](../autoops/autoops-connectivity-check.md) to test your system and diagnose any issues that might prevent you from connecting your cluster to AutoOps.

## Potential errors

The following table shows the errors you might encounter if something goes wrong while you set up and use AutoOps in your clusters.

| Error code | Error message | Description |
| :--- | :--- | :--- |
| `HTTP_401` | Authentication failed | Connection denied because of an authentication error. Run the AutoOps Connectivity Check script to diagnose the issue. [Learn more](../autoops/autoops-connectivity-check.md). |
| `HTTP_502` | Server error | Received an invalid response from the server. There may be an issue with the server status or network configuration. Run the AutoOps Connectivity Check script to diagnose the issue. [Learn more](../autoops/autoops-connectivity-check.md). |
| `HTTP_503` | Server unavailable | Invalid or corrupt response received from the server. The server acting as a proxy may be busy or undergoing scheduled maintenance. If the issue persists, check the cluster's health and resource usage. |
| `HTTP_504` | Request timed out | Did not receive a response from the cluster within the expected time frame. Check the cluster's performance or consider changing your connection timeout settings. |
| `CLUSTER_ALREADY_CONNECTED` | Cluster connected to another account | This cluster is already connected to another {{ecloud}} organization. Disconnect it and then try again. |
| `CLUSTER_NOT_READY` | {{es}} cluster is still connecting | Your {{es}} cluster is not yet ready to connect. Wait a few moments for it to finish starting up and then try again. |
| `HTTP_0` | Connection error | {{agent}} couldn't connect to the cluster. Run the AutoOps Connectivity Check script to diagnose the issue. [Learn more](../autoops/autoops-connectivity-check.md). If the issue persists, contact [Elastic support](https://support.elastic.co/) (for clusters on an Enterprise or Platinum license) or visit the [community forums](https://discuss.elastic.co/c/elastic-stack/monitoring/103). |
| `VERSION_MISMATCH` | {{es}} version is unsupported | Upgrade your cluster to a [supported version](https://www.elastic.co/support/eol). |
| `UNKNOWN_ERROR` | Installation failed | Could not install {{agent}}. Consult the [troubleshooting guide](../autoops/cc-cloud-connect-autoops-troubleshooting.md) or run the AutoOps Connectivity Check script to test your network settings. If the issue persists, contact [Elastic support](https://support.elastic.co/) (for clusters on an Enterprise or Platinum license) or visit the [community forums](https://discuss.elastic.co/c/elastic-stack/monitoring/103). |
| `x509` | Certificate signed by unknown authority | {{agent}} couldn't connect. SSL certificate signed by unknown authority. |
