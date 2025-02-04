---
navigation_title: "Elastic Defend"
---

# Troubleshoot {{elastic-defend}} [security-troubleshoot-endpoints]


This topic covers common troubleshooting issues when using {{elastic-defend}}'s [endpoint management tools](../../../solutions/security/manage-elastic-defend.md).


## Endpoints [ts-endpoints]

:::::{dropdown} Unhealthy {{agent}} status
In some cases, an `Unhealthy` {{agent}} status may be caused by a failure in the {{elastic-defend}} integration policy. In this situation, the integration and any failing features are flagged on the agent details page in {{fleet}}. Expand each section and subsection to display individual responses from the agent.

::::{tip}
Integration policy response information is also available from the **Endpoints** page in the {{security-app}} (**Assets*** → ***Endpoints**, then click the link in the **Policy status** column).

::::


:::{image} ../../../images/serverless--troubleshooting-unhealthy-agent-fleet.png
:alt: Agent details page in {{fleet}} with Unhealthy status and integration failures
:class: screenshot
:::

Common causes of failure in the {{elastic-defend}} integration policy include missing prerequisites or unexpected system configuration. Consult the following topics to resolve a specific error:

* [Approve the system extension for {{elastic-endpoint}}](../../../solutions/security/configure-elastic-defend/enable-access-for-macos-monterey.md#system-extension-endpoint) (macOS)
* [Enable Full Disk Access for {{elastic-endpoint}}](../../../solutions/security/configure-elastic-defend/enable-access-for-macos-monterey.md#enable-fda-endpoint) (macOS)
* [Resolve a potential system deadlock](../../../troubleshoot/security/elastic-defend.md) (Linux)

::::{tip}
If the {{elastic-defend}} integration policy is not the cause of the `Unhealthy` agent status, refer to [{{fleet}} troubleshooting](../../../troubleshoot/ingest/fleet/common-problems.md) for help with the {{agent}}.

::::


:::::


:::::{dropdown} Disabled to avoid potential system deadlock (Linux)
If you have an `Unhealthy` {{agent}} status with the message `Disabled due to potential system deadlock`, that means malware protection was disabled on the {{elastic-defend}} integration policy due to errors while monitoring a Linux host.

You can resolve the issue by configuring the policy’s [advanced settings](../../../solutions/security/configure-elastic-defend/configure-linux-file-system-monitoring.md) related to **fanotify**, a Linux feature that monitors file system events. By default, {{elastic-defend}} works with fanotify to monitor specific file system types that Elastic has tested for compatibility, and ignores other unknown file system types.

If your network includes nonstandard, proprietary, or otherwise unrecognized Linux file systems that cause errors while being monitored, you can configure {{elastic-defend}} to ignore those file systems. This allows {{elastic-defend}} to resume monitoring and protecting the hosts on the integration policy.

::::{warning}
Ignoring file systems can create gaps in your security coverage. Use additional security layers for any file systems ignored by {{elastic-defend}}.

::::


To resolve the potential system deadlock error:

1. Go to **Assets** → **Policies**, then click a policy’s name.
2. Scroll to the bottom of the policy and click **Show advanced settings**.
3. In the setting `linux.advanced.fanotify.ignored_filesystems`, enter a comma-separated list of file system names to ignore, as they appear in `/proc/filesystems` (for example: `ext4,tmpfs`). Refer to [Find file system names](../../../solutions/security/configure-elastic-defend/configure-linux-file-system-monitoring.md#find-file-system-names) for more on determining the file system names.
4. Click **Save**.

    Once you save the policy, malware protection is re-enabled.


:::::


:::::{dropdown} Required transform failed
If you encounter a `“Required transform failed”` notice on the Endpoints page, you can usually resolve the issue by restarting the transform. Refer to [Transforming data](../../../explore-analyze/transforms.md) for more information about transforms.

:::{image} ../../../images/serverless--troubleshooting-endpoints-transform-failed.png
:alt: Endpoints page with Required transform failed notice
:class: screenshot
:::

To restart a transform that’s not running:

1. Go to **Project settings** → **Management** → **Transforms**.
2. Enter `endpoint.metadata` in the search box to find the transforms for {{elastic-defend}}.
3. Click the **Actions** menu (![Actions menu icon](../../../images/serverless-boxesHorizontal.svg "")) and do one of the following for each transform, depending on the value in the **Status** column:

    * `stopped`: Select **Start** to restart the transform.
    * `failed`: Select **Stop** to first stop the transform, and then select **Start** to restart it.

        :::{image} ../../../images/serverless--troubleshooting-transforms-start.png
        :alt: Transforms page with Start option selected
        :class: screenshot
        :::

4. On the confirmation message that displays, click **Start** to restart the transform.
5. The transform’s status changes to `started`. If it doesn’t change, refresh the page.

:::::


::::{dropdown} {agent} and Endpoint connection issues
After {{agent}} installs Endpoint, Endpoint connects to {{agent}} over a local relay connection to report its health status and receive policy updates and response action requests. If that connection cannot be established, the {{elastic-defend}} integration will cause {{agent}} to be in an `Unhealthy` status, and Endpoint won’t operate properly.


### Identify if the issue is happening [security-troubleshoot-endpoints-identify-if-the-issue-is-happening]

You can identify if this issue is happening in the following ways:

* Run {{agent}}'s status command:

    * `sudo /opt/Elastic/Agent/elastic-agent status` (Linux)
    * `sudo /Library/Elastic/Agent/elastic-agent status` (macOS)
    * `c:\Program Files\Elastic\Agent\elastic-agent.exe status` (Windows)

        If the status result for `endpoint-security` says that Endpoint has missed check-ins or `localhost:6788` cannot be bound to, it might indicate this problem is occurring.

* If the problem starts happening right after installing Endpoint, check the value of `fleet.agent.id` in the following file:

    * `/opt/Elastic/Endpoint/elastic-endpoint.yaml` (Linux)
    * `/Library/Elastic/Endpoint/elastic-endpoint.yaml` (macOS)
    * `c:\Program Files\Elastic\Endpoint\elastic-endpoint.yaml` (Windows)

        If the value of `fleet.agent.id` is `00000000-0000-0000-0000-000000000000`, this indicates this problem is occurring.

        ::::{note}
        If this problem starts happening after Endpoint has already been installed and working properly, then this value will have changed even though the problem is happening.

        ::::



### Examine Endpoint logs [security-troubleshoot-endpoints-examine-endpoint-logs]

If you’ve confirmed that the issue is happening, you can look at Endpoint log messages to identify the cause:

* `Failed to find connection to validate. Is Agent listening on 127.0.0.1:6788?` or `Failed to validate connection. Is Agent running as root/admin?` means that Endpoint is not able to create an initial connection to {{agent}} over port `6788`.
* `Unable to make GRPC connection in deadline(60s). Fetching connection info again` means that Endpoint’s original connection to {{agent}} over port `6788` worked, but the connection over port `6789` is failing.


### Resolve the issue [security-troubleshoot-endpoints-resolve-the-issue]

To debug and resolve the issue, follow these steps:

1. Examine the Endpoint diagnostics file named `analysis.txt`, which contains information about what may cause this issue. {{agent}} diagnostics automatically include Endpoint diagnostics.
2. Make sure nothing else on your device is listening on ports `6788` or `6789` by running:

    * `sudo netstat -anp --tcp` (Linux)
    * `sudo netstat -an -f inet` (macOS)
    * `netstat -an` (Windows)

3. Make sure `localhost` can be resolved to `127.0.0.1` by running:

    * `ping -4 -c 1 localhost` (Linux)
    * `ping -c 1 localhost` (macOS)
    * `ping -4 localhost` (Windows)


::::


::::{dropdown} {elastic-defend} deployment issues
After deploying {{elastic-defend}}, you might encounter warnings or errors in the endpoint’s **Policy status** in {{fleet}} if your mobile device management (MDM) is misconfigured or certain permissions for {{elastic-endpoint}} aren’t granted. The following sections explain issues that can cause warnings or failures in the endpoint’s policy status.


### Connect Kernel has failed [security-troubleshoot-endpoints-connect-kernel-has-failed]

This means that the system extension or kernel extension was not approved. Consult the following topics for approving the system extension, either with MDM or without MDM:

* [Approve the system extension with MDM](../../../solutions/security/configure-elastic-defend/deploy-on-macos-with-mdm.md#security-deploy-with-mdm-approve-the-system-extension)
* [Approve the system extension without MDM](../../../solutions/security/configure-elastic-defend/enable-access-for-macos-ventura-higher.md#system-extension-endpoint-ven)

You can validate the system extension is loaded by running

```txt
sudo systemextensionsctl list | grep co.elastic.systemextension
```

In the command output, the system extension should be marked as "active enabled".


### Connect Kernel has failed and the system extension is loaded [security-troubleshoot-endpoints-connect-kernel-has-failed-and-the-system-extension-is-loaded]

If the system extension is loaded and kernel connection still fails, this means that Full Disk Access was not granted. {{elastic-endpoint}} requires Full Disk Access to subscribe to system events via the {{elastic-defend}} framework, which is one of the primary sources of eventing information used by {{elastic-endpoint}}. Consult the following topics for granting Full Disk Access, either with MDM or without MDM:

* [Enable Full Disk Access with MDM](../../../solutions/security/configure-elastic-defend/deploy-on-macos-with-mdm.md#security-deploy-with-mdm-enable-full-disk-access)
* [Enable Full Disk Access without MDM](../../../solutions/security/configure-elastic-defend/enable-access-for-macos-ventura-higher.md#enable-fda-endpoint-ven)

You can validate that Full Disk Access is approved by running

```txt
sudo /Library/Elastic/Endpoint/elastic-endpoint test install
```

If the command output doesn’t contain a message about enabling Full Disk Access, the approval was successful.


### Detect Network Events has failed [security-troubleshoot-endpoints-detect-network-events-has-failed]

This means that the network extension content filtering was not approved. Consult the following topics for approving network content filtering, either with MDM or without MDM:

* [Approve network content filtering with MDM](../../../solutions/security/configure-elastic-defend/deploy-on-macos-with-mdm.md#security-deploy-with-mdm-approve-network-content-filtering)
* [Approve network content filtering without MDM](../../../solutions/security/configure-elastic-defend/enable-access-for-macos-ventura-higher.md#allow-filter-content-ven)

You can validate that network content filtering is approved by running

```txt
sudo /Library/Elastic/Endpoint/elastic-endpoint test install
```

If the command output doesn’t contain a message about approving network content filtering, the approval was successful.


### Full Disk Access has a warning [security-troubleshoot-endpoints-full-disk-access-has-a-warning]

This means that Full Disk Access was not granted for one or all {{elastic-endpoint}} components. Consult the following topics for granting Full Disk Access, either with MDM or without MDM:

* [Enable Full Disk Access with MDM](../../../solutions/security/configure-elastic-defend/deploy-on-macos-with-mdm.md#security-deploy-with-mdm-enable-full-disk-access)
* [Enable Full Disk Access without MDM](../../../solutions/security/configure-elastic-defend/enable-access-for-macos-ventura-higher.md#enable-fda-endpoint-ven)

You can validate that Full Disk Access is approved by running

```txt
sudo /Library/Elastic/Endpoint/elastic-endpoint test install
```

If the command output doesn’t contain a message about enabling Full Disk Access, the approval was successful.

::::


::::{dropdown} Disable {{elastic-defend}}'s self-healing feature on Windows
:name: disable-self-healing


### Volume Snapshot Service issues [self-healing-vss-issues]

{{elastic-defend}}'s self-healing feature rolls back recent filesystem changes when a prevention alert is triggered. This feature uses the Windows Volume Snapshot Service. Although it’s uncommon for this to cause issues, you can turn off this {{elastic-defend}} feature if needed.

If issues occur and the self-healing feature is enabled, you can turn it off by setting `windows.advanced.alerts.rollback.self_healing.enabled` to `false` in the integration policy advanced settings. Refer to [Self-healing rollback (Windows)](../../../solutions/security/configure-elastic-defend/configure-self-healing-rollback-for-windows-endpoints.md) for more information.

{{elastic-defend}} may also use the Volume Snapshot Service to ensure the feature works properly even when it’s turned off. To opt out of this, set `windows.advanced.diagnostic.rollback_telemetry_enabled` to `false` in the same settings.


### Known compatibility issues [self-healing-compatibility-issues]

There are some known compatibility issues between {{elastic-defend}}'s self-healing feature and filesystem replication features, including [DFS Replication](https://learn.microsoft.com/en-us/windows-server/storage/dfs-replication/dfsr-overview) and Veeam Replication. This may manifest as `DFSR Event ID 1102`:

`The DFS Replication service has temporarily stopped replication because another application is performing a backup or restore operation. Replication will resume after the backup or restore operation has finished.`

There are no known workarounds for this issue other than to turn off the self-healing feature.

::::
