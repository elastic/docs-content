# Enable access for macOS Ventura and higher [security-deploy-elastic-endpoint-ven]

To properly install and configure {{elastic-defend}} manually without a Mobile Device Management (MDM) profile, there are additional permissions that must be enabled on the host before {{elastic-endpoint}}—the installed component that performs {{elastic-defend}}'s threat monitoring and prevention—is fully functional:

* [Approve the system extension](../../../solutions/security/configure-elastic-defend/enable-access-for-macos-ventura-higher.md#system-extension-endpoint-ven)
* [Approve network content filtering](../../../solutions/security/configure-elastic-defend/enable-access-for-macos-ventura-higher.md#allow-filter-content-ven)
* [Enable Full Disk Access](../../../solutions/security/configure-elastic-defend/enable-access-for-macos-ventura-higher.md#enable-fda-endpoint-ven)

::::{note}
The following permissions that need to be enabled are required after you [configure and install the {{elastic-defend}} integration](../../../solutions/security/configure-elastic-defend/install-elastic-defend.md), which includes [enrolling the {{agent}}](../../../solutions/security/configure-elastic-defend/install-elastic-defend.md#enroll-security-agent).

::::



## Approve the system extension for {{elastic-endpoint}} [system-extension-endpoint-ven]

For macOS Ventura (13.0) and later, {{elastic-endpoint}} will attempt to load a system extension during installation. This system extension must be loaded in order to provide insight into system events such as process events, file system events, and network events.

The following message appears during installation:

:::{image} ../../../images/serverless--getting-started-install-endpoint-ven-system_extension_blocked_warning_ven.png
:alt:  getting started install endpoint ven system extension blocked warning ven
:class: screenshot
:::

1. Click **Open System Settings**.
2. In the left pane, click **Privacy & Security**.

    :::{image} ../../../images/serverless--getting-started-install-endpoint-ven-privacy_security_ven.png
    :alt:  getting started install endpoint ven privacy security ven
    :class: screenshot
    :::

3. On the right pane, scroll down to the Security section. Click **Allow** to allow the ElasticEndpoint system extension to load.

    :::{image} ../../../images/serverless--getting-started-install-endpoint-ven-allow_system_extension_ven.png
    :alt:  getting started install endpoint ven allow system extension ven
    :class: screenshot
    :::

4. Enter your username and password and click **Modify Settings** to save your changes.

    :::{image} ../../../images/serverless--getting-started-install-endpoint-ven-enter_login_details_to_confirm_ven.png
    :alt:  getting started install endpoint ven enter login details to confirm ven
    :class: screenshot
    :::



## Approve network content filtering for {{elastic-endpoint}} [allow-filter-content-ven]

After successfully loading the ElasticEndpoint system extension, an additional message appears, asking to allow {{elastic-endpoint}} to filter network content.

:::{image} ../../../images/serverless--getting-started-install-endpoint-ven-allow_network_filter_ven.png
:alt:  getting started install endpoint ven allow network filter ven
:class: screenshot
:::

Click **Allow** to enable content filtering for the ElasticEndpoint system extension. Without this approval, {{elastic-endpoint}} cannot receive network events and, therefore, cannot enable network-related features such as [host isolation](../../../solutions/security/endpoint-response-actions/isolate-host.md).


## Enable Full Disk Access for {{elastic-endpoint}} [enable-fda-endpoint-ven]

{{elastic-endpoint}} requires Full Disk Access to subscribe to system events using the {{elastic-defend}} framework and to protect your network from malware and other cybersecurity threats. Full Disk Access permissions is a privacy feature introduced in macOS Mojave (10.14) that prevents some applications from accessing your data.

If you have not granted Full Disk Access, the following notification prompt will appear.

:::{image} ../../../images/serverless--getting-started-install-endpoint-ven-allow_full_disk_access_notification_ven.png
:alt:  getting started install endpoint ven allow full disk access notification ven
:class: screenshot
:::

To enable Full Disk Access, you must manually approve {{elastic-endpoint}}.

::::{note}
The following instructions apply only to {{elastic-endpoint}} version 8.0.0 and later. Versions 7.17.0 and earlier are not supported. To see Full Disk Access requirements for the Endgame sensor, refer to Endgame’s documentation.

::::


1. Open the **System Settings** application.
2. In the left pane, select **Privacy & Security**.

    :::{image} ../../../images/serverless--getting-started-install-endpoint-ven-privacy_security_ven.png
    :alt:  getting started install endpoint ven privacy security ven
    :class: screenshot
    :::

3. From the right pane, select **Full Disk Access**.

    :::{image} ../../../images/serverless--getting-started-install-endpoint-ven-select_fda_ven.png
    :alt: Select Full Disk Access
    :class: screenshot
    :::

4. Enable `ElasticEndpoint` and `co.elastic` to properly enable Full Disk Access.

    :::{image} ../../../images/serverless--getting-started-install-endpoint-ven-allow_fda_ven.png
    :alt:  getting started install endpoint ven allow fda ven
    :class: screenshot
    :::
