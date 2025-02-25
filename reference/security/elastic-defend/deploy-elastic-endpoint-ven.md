---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/deploy-elastic-endpoint-ven.html
---

# Enable access for macOS Ventura and higher [deploy-elastic-endpoint-ven]

To properly install and configure {{elastic-defend}} manually without a Mobile Device Management (MDM) profile, there are additional permissions that must be enabled on the host before {{elastic-endpoint}}—the installed component that performs {{elastic-defend}}'s threat monitoring and prevention—is fully functional:

* [Approve the system extension](#system-extension-endpoint-ven)
* [Approve network content filtering](#allow-filter-content-ven)
* [Enable Full Disk Access](#enable-fda-endpoint-ven)

::::{note}
The following permissions that need to be enabled are required after you [configure and install the {{elastic-defend}} integration](/reference/security/elastic-defend/install-endpoint.md), which includes [enrolling the {{agent}}](/reference/security/elastic-defend/install-endpoint.md#enroll-security-agent).
::::



## Approve the system extension for {{elastic-endpoint}} [system-extension-endpoint-ven]

For macOS Ventura (13.0) and later, {{elastic-endpoint}} will attempt to load a system extension during installation. This system extension must be loaded in order to provide insight into system events such as process events, file system events, and network events.

The following message appears during installation:

:::{image} ../../../images/security-system_extension_blocked_warning_ven.png
:alt: system extension blocked warning ven
:class: screenshot
:::

1. Click **Open System Settings**.
2. In the left pane, click **Privacy & Security**.

    :::{image} ../../../images/security-privacy_security_ven.png
    :alt: privacy security ven
    :class: screenshot
    :::

3. On the right pane, scroll down to the Security section. Click **Allow** to allow the ElasticEndpoint system extension to load.

    :::{image} ../../../images/security-allow_system_extension_ven.png
    :alt: allow system extension ven
    :class: screenshot
    :::

4. Enter your username and password and click **Modify Settings** to save your changes.

    :::{image} ../../../images/security-enter_login_details_to_confirm_ven.png
    :alt: enter login details to confirm ven
    :class: screenshot
    :::



## Approve network content filtering for {{elastic-endpoint}} [allow-filter-content-ven]

After successfully loading the ElasticEndpoint system extension, an additional message appears, asking to allow {{elastic-endpoint}} to filter network content.

:::{image} ../../../images/security-allow_network_filter_ven.png
:alt: allow network filter ven
:class: screenshot
:::

Click **Allow** to enable content filtering for the ElasticEndpoint system extension. Without this approval, {{elastic-endpoint}} cannot receive network events and, therefore, cannot enable network-related features such as [host isolation](/solutions/security/endpoint-response-actions/isolate-host.md).


## Enable Full Disk Access for {{elastic-endpoint}} [enable-fda-endpoint-ven]

{{elastic-endpoint}} requires Full Disk Access to subscribe to system events via the {{elastic-defend}} framework and to protect your network from malware and other cybersecurity threats. Full Disk Access permissions is a privacy feature introduced in macOS Mojave (10.14) that prevents some applications from accessing your data.

If you have not granted Full Disk Access, the following notification prompt will appear.

:::{image} ../../../images/security-allow_full_disk_access_notification_ven.png
:alt: allow full disk access notification ven
:class: screenshot
:::

To enable Full Disk Access, you must manually approve {{elastic-endpoint}}.

::::{note}
The following instructions apply only to {{elastic-endpoint}} version 8.0.0 and later. To see Full Disk Access requirements for the Endgame sensor, refer to Endgame’s documentation.
::::


1. Open the **System Settings** application.
2. In the left pane, select **Privacy & Security**.

    :::{image} ../../../images/security-privacy_security_ven.png
    :alt: privacy security ven
    :class: screenshot
    :::

3. From the right pane, select **Full Disk Access**.

    :::{image} ../../../images/security-select_fda_ven.png
    :alt: Select Full Disk Access
    :class: screenshot
    :::

4. Enable `ElasticEndpoint` and `co.elastic` to properly enable Full Disk Access.

    :::{image} ../../../images/security-allow_fda_ven.png
    :alt: allow fda ven
    :class: screenshot
    :::


If the endpoint is running {{elastic-endpoint}} version 7.17.0 or earlier:

1. Click the **+** button to view **Finder**.
2. The system may prompt you to enter your username and password if you haven’t already.

    :::{image} ../../../images/security-enter_login_details_to_confirm_ven.png
    :alt: enter login details to confirm ven
    :class: screenshot
    :::

3. Navigate to `/Library/Elastic/Endpoint`, then select the `elastic-endpoint` file.
4. Click **Open**.
5. In the **Privacy** tab, confirm that `ElasticEndpoint` and `co.elastic.systemextension` are selected to properly enable Full Disk Access.

    :::{image} ../../../images/security-verify_fed_granted_ven.png
    :alt: Select Full Disk Access
    :class: screenshot
    :::
