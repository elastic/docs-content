---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/configure-endpoint-integration-policy.html
  - https://www.elastic.co/guide/en/serverless/current/security-configure-endpoint-integration-policy.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Configure an integration policy for {{elastic-defend}}

After the {{agent}} is installed with the {{elastic-defend}} integration, several protections features — including preventions against malware, ransomware, memory threats, and malicious behavior — are automatically enabled on protected hosts. If needed, you can update the integration policy to configure protection settings, event collection, antivirus settings, trusted applications, trusted devices, event filters, host isolation exceptions, and blocked applications to meet your organization’s security needs.

You can also create multiple {{elastic-defend}} integration policies to maintain unique configuration profiles. To create an additional {{elastic-defend}} integration policy, find **Integrations** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then follow the steps for [adding the {{elastic-defend}} integration](/solutions/security/configure-elastic-defend/install-elastic-defend.md#add-security-integration).

::::{admonition} Requirements
To configure an integration policy:
* In {{stack}}, you must have the **{{elastic-defend}} Policy Management : All** [privilege](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md).
* In {{serverless-short}}, you must have the appropriate user role.
::::


::::{tip}
In addition to configuring an {{elastic-defend}} policy through the {{elastic-sec}} UI, you can create and customize an {{elastic-defend}} policy [through the API](/solutions/security/configure-elastic-defend/create-an-elastic-defend-policy-using-api.md).
::::


To configure an integration policy:

1. Find **Policies** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the integration policy you want to configure. The integration policy configuration page appears.
3. On the **Policy settings** tab, review and configure the following settings as appropriate:

    * [Malware protection](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#malware-protection)
    * [Ransomware protection](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#ransomware-protection)
    * [Memory threat protection](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#memory-protection)
    * [Malicious behavior protection](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#behavior-protection)
    * [Attack surface reduction](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#attack-surface-reduction)
    * [Device control](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#device-control)
    * [Event collection](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#event-collection)
    * [Register {{elastic-sec}} as antivirus (optional)](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#register-as-antivirus)
    * [Advanced policy settings (optional)](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#adv-policy-settings)
    * [Save the general policy settings](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#save-policy)

4. Click the **Trusted applications**, **Trusted devices**, **Event filters**, **Host isolation exceptions**, and **Blocklist** tabs to review the endpoint policy artifacts assigned to this integration policy (for more information, refer to [Trusted applications](/solutions/security/manage-elastic-defend/trusted-applications.md), [Trusted devices](/solutions/security/manage-elastic-defend/trusted-devices.md), [Event filters](/solutions/security/manage-elastic-defend/event-filters.md), [Host isolation exceptions](/solutions/security/manage-elastic-defend/host-isolation-exceptions.md), and [Blocklist](/solutions/security/manage-elastic-defend/blocklist.md)). On these tabs, you can:

    * Expand and view an artifact: Click the arrow next to its name.
    * View an artifact’s details: Click the actions menu (**…**), then select **View full details**.
    * Unassign an artifact: Click the actions menu (**…**), then select **Remove from policy**. This does not delete the artifact; this just unassigns it from the current policy.
    * Assign an existing artifact: Click **Assign *x* to policy**, then select an item from the flyout. This view lists any existing artifacts that aren’t already assigned to the current policy.

    ::::{note}
    You can’t create a new endpoint policy artifact while configuring an integration policy. To create a new artifact, go to its main page in the {{security-app}} (for example, to create a new trusted application, find **Trusted applications** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md)).
    ::::

5. Click the **Protection updates** tab to configure how {{elastic-defend}} receives updates from Elastic with the latest threat detections, malware models, and other protection artifacts. Refer to [Configure updates for protection artifacts](/solutions/security/configure-elastic-defend/configure-updates-for-protection-artifacts.md) for more information.


## Malware protection [malware-protection]

{{elastic-defend}} malware prevention detects and stops malicious attacks by using a machine learning model that looks for static attributes to determine if a file is malicious or benign.

By default, malware protection is enabled on Windows, macOS, and Linux hosts. To disable malware protection, turn off the **Malware protections** toggle.

::::{admonition} Requirements
:class: note
In {{serverless-short}}, malware protection requires the Endpoint Protection Essentials [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md).
::::

Malware protection levels are:

* **Detect**: Detects malware on the host and generates an alert. The agent will **not** block malware. You must pay attention to and analyze any malware alerts that are generated.
* **Prevent** (Default): Detects malware on the host, blocks it from executing, and generates an alert.

These additional options are available for malware protection:

* **Blocklist**: Enable or disable the [blocklist](/solutions/security/manage-elastic-defend/blocklist.md) for all hosts associated with this {{elastic-defend}} policy. The blocklist allows you to prevent specified applications from running on hosts, extending the list of processes that {{elastic-defend}} considers malicious.
* **Scan files upon modification**: By default, {{elastic-defend}} scans files every time they’re modified, which can be resource-intensive on hosts where files are frequently modified, such as servers and developer machines. Turn off this option to only scan files when they’re executed. {{elastic-defend}} will continue to identify malware as it attempts to run, providing a robust level of protection while improving endpoint performance.

Select **Notify user** to send a push notification in the host operating system when activity is detected or prevented. Notifications are enabled by default for the **Prevent** option.

::::{tip}
If you have the appropriate license or project feature tier, you can customize these notifications using the `Elastic Security {action} {filename}` syntax.
::::


:::{image} /solutions/images/security-malware-protection.png
:alt: Detail of malware protection section.
:screenshot:
:::


### Manage quarantined files [manage-quarantined-files]

When **Prevent** is enabled for malware protection, {{elastic-defend}} will quarantine any malicious file it finds (this includes files defined in the [blocklist](/solutions/security/manage-elastic-defend/blocklist.md)). Specifically, {{elastic-defend}} will remove the file from its current location, apply a rolling XOR with the key `ELASTIC`, move it to a different folder, and rename it as a GUID string, such as `318e70c2-af9b-4c3a-939d-11410b9a112c`.

The quarantine folder location varies by operating system:

* macOS: `/System/Volumes/Data/.equarantine`
* Linux: `.equarantine` at the root of the mount point of the file being quarantined
* Windows - {{elastic-defend}} versions 8.5 and later: `[DriveLetter:]\.equarantine`, unless the files are from the `C:` drive. These files are moved to `C:\Program Files\Elastic\Endpoint\state\.equarantine`.
* Windows - {{elastic-defend}} versions 8.4 and earlier: `[DriveLetter:]\.equarantine`, for any drive

To restore a quarantined file to its original state and location, [add an exception](/solutions/security/detect-and-alert/add-manage-exceptions.md) to the rule that identified the file as malicious. If the exception would’ve stopped the rule from identifying the file as malicious, {{elastic-defend}} restores the file.

You can access a quarantined file by using the `get-file` [response action command](/solutions/security/endpoint-response-actions.md#response-action-commands) in the response console. To do this, copy the path from the alert’s **Quarantined file path** field (`file.Ext.quarantine_path`), which appears under **Highlighted fields** in the alert details flyout. Then paste the value into the `--path` parameter. This action doesn’t restore the file to its original location, so you will need to do this manually.

::::{important}
When you retrieve a quarantined file using `get-file`, the XOR obfuscation is automatically reversed, and the original malicious file is retrieved.
::::

::::{note}
* In {{stack}}, response actions and the response console UI are [Enterprise subscription](https://www.elastic.co/pricing) features.
* In {{serverless-short}}, response actions and the response console UI are Endpoint Protection Complete [project features](/deploy-manage/deploy/elastic-cloud/project-settings.md).
::::


## Ransomware protection [ransomware-protection]

Behavioral ransomware prevention detects and stops ransomware attacks on Windows systems by analyzing data from low-level system processes. It is effective across an array of widespread ransomware families — including those targeting the system’s master boot record.

::::{admonition} Requirements
:class: note
* In {{stack}}, ransomware protection is enabled by default if you have a [Platinum or Enterprise license](https://www.elastic.co/pricing). If you upgrade to a Platinum or Enterprise license from Basic or Gold, ransomware protection will be disabled by default.
* In {{serverless-short}}, ransomware protection requires the Endpoint Protection Essentials [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md).
::::


Ransomware protection levels are:

* **Detect**: Detects ransomware on the host and generates an alert. {{elastic-defend}} will **not** block ransomware. You must pay attention to and analyze any ransomware alerts that are generated.
* **Prevent** (Default): Detects ransomware on the host, blocks it from executing, and generates an alert.

When ransomware protection is enabled, canary files placed in targeted locations on your hosts provide an early warning system for potential ransomware activity. When a canary file is modified, Elastic Defend immediately generates a ransomware alert. If **prevent** ransomware is active, {{elastic-defend}} terminates the process that modified the file.

Select **Notify user** to send a push notification in the host operating system when activity is detected or prevented. Notifications are enabled by default for the **Prevent** option.

::::{tip}
If you have the appropriate license or project feature tier, you can customize these notifications using the `Elastic Security {action} {filename}` syntax.
::::


:::{image} /solutions/images/security-ransomware-protection.png
:alt: Detail of ransomware protection section.
:screenshot:
:::


## Memory threat protection [memory-protection]

Memory threat protection detects and stops in-memory threats, such as shellcode injection, which are used to evade traditional file-based detection techniques.

::::{admonition} Requirements
:class: note
* In {{stack}}, memory threat protection is enabled by default if you have a [Platinum or Enterprise license](https://www.elastic.co/pricing). If you upgrade to a Platinum or Enterprise license from Basic or Gold, memory threat protection will be disabled by default.
* In {{serverless-short}}, memory threat protection requires the Endpoint Protection Essentials [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md).
::::


Memory threat protection levels are:

* **Detect**: Detects memory threat activity on the host and generates an alert. {{elastic-defend}} will **not** block the in-memory activity. You must pay attention to and analyze any alerts that are generated.
* **Prevent** (Default): Detects memory threat activity on the host, forces the process or thread to stop, and generates an alert.

Select **Notify user** to send a push notification in the host operating system when activity is detected or prevented. Notifications are enabled by default for the **Prevent** option.

::::{tip}
If you have the appropriate license or project feature tier, you can customize these notifications using the `Elastic Security {action} {rule}` syntax.
::::


:::{image} /solutions/images/security-memory-protection.png
:alt: Detail of memory protection section.
:screenshot:
:::


## Malicious behavior protection [behavior-protection]

Malicious behavior protection detects and stops threats by monitoring the behavior of system processes for suspicious activity. Behavioral signals are much more difficult for adversaries to evade than traditional file-based detection techniques.

::::{admonition} Requirements
:class: note
* In {{stack}}, malicious behavior protection is enabled by default if you have a [Platinum or Enterprise license](https://www.elastic.co/pricing). If you upgrade to a Platinum or Enterprise license from Basic or Gold, malicious behavior protection will be disabled by default.
* In {{serverless-short}}, malicious behavior protection requires the Endpoint Protection Essentials [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md).
::::


Malicious behavior protection levels are:

* **Detect**: Detects malicious behavior on the host and generates an alert. {{elastic-defend}} will **not** block the malicious behavior. You must pay attention to and analyze any alerts that are generated.
* **Prevent** (Default): Detects malicious behavior on the host, forces the process to stop, and generates an alert.

Select whether you want to use **Reputation service** for additional protection. Elastic’s reputation service leverages our extensive threat intelligence knowledge to make high confidence real-time prevention decisions. For example, reputation service can detect suspicious downloads of binaries with low or malicious reputation. Endpoints communicate with the reputation service directly at [https://cloud.security.elastic.co](https://cloud.security.elastic.co).

::::{note}
In {{stack}}, reputation service requires an active [Platinum or Enterprise subscription](https://www.elastic.co/pricing) and is available on cloud deployments only.
::::


Select **Notify user** to send a push notification in the host operating system when activity is detected or prevented. Notifications are enabled by default for the **Prevent** option.

::::{tip}
If you have the appropriate license or project feature tier, you can customize these notifications using the `Elastic Security {action} {rule}` syntax.
::::


:::{image} /solutions/images/security-behavior-protection.png
:alt: Detail of behavior protection section.
:screenshot:
:::


## Attack surface reduction [attack-surface-reduction]

This section helps you reduce vulnerabilities that attackers can target on Windows endpoints.

::::{admonition} Requirements
:class: note
In {{serverless-short}}, attack surface reduction requires the Endpoint Protection Essentials [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md).
::::

**Credential hardening**: Prevents attackers from stealing credentials stored in Windows system process memory. Turn on the toggle to remove any overly permissive access rights that aren’t required for standard interaction with the Local Security Authority Subsystem Service (LSASS). This feature enforces the principle of least privilege without interfering with benign system activity that is related to LSASS.

:::{image} /solutions/images/security-attack-surface-reduction.png
:alt: Detail of attack surface reduction section.
:screenshot:
:::

## Device control [device-control]

```yaml {applies_to}
stack: ga 9.2
serverless: ga
```


Device control helps protect your organization from data loss, malware, and unauthorized access by managing which devices can connect to your computers. Specifically, it restricts which external USB storage devices can connect to hosts that have {{elastic-defend}} installed. 

To configure device control for one or more hosts, edit the {{elastic-defend}} policy that affects those hosts. Your policy specifies which operations these devices are allowed to take on a host. You can create [trusted devices](/solutions/security/manage-elastic-defend/trusted-devices.md) to define exceptions to your policy for specific devices. 


:::{image} /solutions/images/security-defend-policy-device-control.png
:alt: Detail of device control section.
:screenshot:
:::

By default, each {{kib}} instance includes a Device Control dashboard. When at least one of your {{elastic-defend}} policies has device control enabled, the dashboard displays data about attempted device connections and their outcomes. To access it and review information about blocked connections, search for `device control` in the **Dashboards** page's **Custom Dashboards** section.

:::{important} 
To collect device control data, {{elastic-defend}} must be updated to at least version 9.2.0. Until you update it to this version, the device control dashboard will not appear and device control events will not be ingested. Device control blocking will still work. 
:::

## Event collection [event-collection]

In the **Settings** section, select which categories of events to collect on each operating system. Most categories are collected by default.

:::{image} /solutions/images/security-event-collection.png
:alt: Detail of event collection section.
:screenshot:
:::


## Register {{elastic-sec}} as antivirus (optional) [register-as-antivirus]

You can register {{elastic-sec}} as your hosts' antivirus software by enabling **Register as antivirus**.

::::{note}
Windows Server versions are not supported. Antivirus registration requires Windows Security Center, which is not included in Windows Server operating systems.
::::


By default, the **Sync with malware protection level** is selected to automatically set antivirus registration to match how you’ve configured {{elastic-defend}}'s [malware protection](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#malware-protection). If malware protection is turned on *and* set to **Prevent**, antivirus registration will also be enabled; in any other case, antivirus registration will be disabled.

If you don’t want to sync antivirus registration, you can set it manually with **Enabled** or **Disabled**.

:::{image} /solutions/images/security-register-as-antivirus.png
:alt: Detail of Register as antivirus option.
:screenshot:
:::


## Advanced policy settings (optional) [adv-policy-settings]

Users with unique configuration and security requirements can select **Show advanced settings** while configuring an {{elastic-defend}} integration policy to support advanced use cases. Hover over each setting to view a short description or refer to [](/reference/security/defend-advanced-settings.md) for more detailed explanations.

::::{note}
Advanced settings are not recommended for most users.
::::


This section includes:

* [Turn off diagnostic data for {{elastic-defend}}](/solutions/security/configure-elastic-defend/turn-off-diagnostic-data-for-elastic-defend.md)
* [Configure self-healing rollback for Windows endpoints](/solutions/security/configure-elastic-defend/configure-self-healing-rollback-for-windows-endpoints.md)
* [Configure Linux file system monitoring](/solutions/security/configure-elastic-defend/configure-linux-file-system-monitoring.md)
* [Configure data volume](/solutions/security/configure-elastic-defend/configure-data-volume-for-elastic-endpoint.md)


## Save the general policy settings [save-policy]

After you have configured the general settings on the **Policy settings** tab, click **Save**. A confirmation message appears.
