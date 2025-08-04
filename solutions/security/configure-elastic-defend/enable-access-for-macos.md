---
navigation_title: Enable access on macOS
applies_to:
  stack: ga
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Enable {{elastic-defend}} access on macOS [deploy-elastic-endpoint]

To properly install and configure {{elastic-defend}} manually without a Mobile Device Management (MDM) profile, there are additional permissions that must be enabled on the host before {{elastic-endpoint}}—the installed component that performs {{elastic-defend}}'s threat monitoring and prevention—is fully functional:

* [Approve the system extension](#system-extension-endpoint)
* [Approve network content filtering](#allow-filter-content)
* [Enable Full Disk Access](#enable-fda-endpoint)

::::{note}
The following permissions that need to be enabled are required after you [configure and install the {{elastic-defend}} integration](install-elastic-defend.md), which includes [enrolling the {{agent}}](install-elastic-defend.md#enroll-security-agent).
::::


## Approve the system extension for {{elastic-endpoint}} [system-extension-endpoint]

{{elastic-endpoint}} will attempt to load a system extension during installation. This system extension must be loaded in order to provide insight into system events such as process events, file system events, and network events. A message prompting you to approve the system extension appears during installation.

Select your macOS version to view specific steps for your system.

::::{tab-set}
:group: os
:::{tab-item} Sequoia (15.x) and later
:sync: sequoia
1. Click **Open System Settings**.
2. In the **General** pane, click **Login Items & Extensions**.
3. In the **Login Items & Extensions** pane, scroll down to the **Extensions** section. Click the info icon next to **Endpoint Security Extensions** and toggle `ElasticEndpoint`.
4. Enter your username and password and click **OK** to save your changes.
:::

:::{tab-item} Ventura (13.x) and Sonoma (14.x)
:sync: ventura
1. Click **Open System Settings**.
2. In the left pane, click **Privacy & Security**.
3. In the right pane, scroll down to the **Security** section. Click **Allow** to allow the `ElasticEndpoint` system extension to load.
4. Enter your username and password and click **Modify Settings** to save your changes.
:::

:::{tab-item} Monterey (12.x)
:sync: monterey
1. Click **Open Security Preferences**.
2. In the lower-left corner of the **Security & Privacy** pane, click the lock icon, then enter your credentials to authenticate.
3. Click **Allow** to allow the `ElasticEndpoint` system extension to load.
:::

::::


## Approve network content filtering for {{elastic-endpoint}} [allow-filter-content]

After successfully loading the `ElasticEndpoint` system extension, an additional message appears, asking to allow {{elastic-endpoint}} to filter network content.

Click **Allow** to enable content filtering for the `ElasticEndpoint` system extension. Without this approval, {{elastic-endpoint}} cannot receive network events and, therefore, cannot enable network-related features such as [host isolation](../endpoint-response-actions/isolate-host.md).


## Enable Full Disk Access for {{elastic-endpoint}} [enable-fda-endpoint]

{{elastic-endpoint}} requires Full Disk Access to subscribe to system events via the {{elastic-defend}} framework and to protect your network from malware and other cybersecurity threats. Full Disk Access permissions is a privacy feature introduced in macOS Mojave (10.14) that prevents some applications from accessing your data.

To enable Full Disk Access, you must manually approve {{elastic-endpoint}}.

::::{note}
To see Full Disk Access requirements for the Endgame sensor, refer to Endgame’s documentation.
::::

Select your macOS version to view specific steps for your system.

::::{tab-set}
:group: os
:::{tab-item} Ventura (13.x) and later
:sync: ventura
If you have not granted Full Disk Access, a notification prompt will appear.

### {{elastic-endpoint}} v.8.0.0 and later
The following instructions apply to {{elastic-endpoint}} version 8.0.0 and later. 

1. Open the **System Settings** application.
2. In the left pane, select **Privacy & Security**.
3. From the right pane, select **Full Disk Access**.
4. Enable `ElasticEndpoint` and `co.elastic` to properly enable Full Disk Access.


### {{elastic-endpoint}} v.7.17.0 and earlier
```{applies_to}
serverless: unavailable
```
In {{stack}}, if the host is running {{elastic-endpoint}} version 7.17.0 or earlier:

1. Open the **System Settings** application.
2. In the left pane, select **Privacy & Security**.
3. From the right pane, select **Full Disk Access**.
4. Click the **+** button to view **Finder**. The system may prompt you to enter your username and password if you haven’t already.
5. Navigate to `/Library/Elastic/Endpoint`, then select the `elastic-endpoint` file, and click **Open**.
6. In the **Privacy** tab, confirm that `ElasticEndpoint` and `co.elastic.systemextension` are selected to properly enable Full Disk Access.
:::

:::{tab-item} Monterey (12.x)
:sync: monterey
### {{elastic-endpoint}} v.8.0.0 and later
The following instructions apply to {{elastic-endpoint}} version 8.0.0 and later.

1. Open the **System Preferences** application.
2. Select **Security and Privacy**.
3. On the **Security and Privacy** pane, select the **Privacy** tab.
4. From the left pane, select **Full Disk Access**.
5. In the lower-left corner of the pane, click the lock icon, then enter your credentials to authenticate.
6. In the **Privacy** tab,  confirm that `ElasticEndpoint` AND `co.elastic.systemextension` are selected to properly enable Full Disk Access.

### {{elastic-endpoint}} v.7.17.0 and earlier
```{applies_to}
serverless: unavailable
```
In {{stack}}, if the host is running {{elastic-endpoint}} version 7.17.0 or earlier:

1. Open the **System Preferences** application.
2. Select **Security and Privacy**.
3. On the **Security and Privacy** pane, select the **Privacy** tab.
4. From the left pane, select **Full Disk Access**.
5. In the lower-left corner of the pane, click the lock icon, then enter your credentials to authenticate.
6. Click the **+** button to view **Finder**.
7. Navigate to `/Library/Elastic/Endpoint`, then select the `elastic-endpoint` file, and click **Open**.
85. In the **Privacy** tab, confirm that `elastic-endpoint` AND `co.elastic.systemextension` are selected to properly enable Full Disk Access.
:::

::::