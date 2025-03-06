---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/deploy-elastic-endpoint.html
  - https://www.elastic.co/guide/en/serverless/current/security-install-endpoint-manually.html
---

# Enable access for macOS Monterey


To properly install and configure {{elastic-defend}} manually without a Mobile Device Management (MDM) profile, there are additional permissions that must be enabled on the host before {{elastic-endpoint}}—the installed component that performs {{elastic-defend}}'s threat monitoring and prevention—is fully functional:

* [Approve the system extension](/solutions/security/configure-elastic-defend/enable-access-for-macos-monterey.md#system-extension-endpoint)
* [Approve network content filtering](/solutions/security/configure-elastic-defend/enable-access-for-macos-monterey.md#allow-filter-content)
* [Enable Full Disk Access](/solutions/security/configure-elastic-defend/enable-access-for-macos-monterey.md#enable-fda-endpoint)

::::{note}
The following permissions that need to be enabled are required after you [configure and install the {{elastic-defend}} integration](/solutions/security/configure-elastic-defend/install-elastic-defend.md), which includes [enrolling the {{agent}}](/solutions/security/configure-elastic-defend/install-elastic-defend.md#enroll-security-agent).
::::


## Approve the system extension for {{elastic-endpoint}} [system-extension-endpoint]

For macOS Monterey (12.x), {{elastic-endpoint}} will attempt to load a system extension during installation. This system extension must be loaded in order to provide insight into system events such as process events, file system events, and network events.

The following message appears during installation:

:::{image} ../../../images/security-system-ext-blocked.png
:alt: system ext blocked
:::

1. Click **Open Security Preferences**.
2. In the lower-left corner of the **Security & Privacy** pane, click the **Lock button**, then enter your credentials to authenticate.

    :::{image} ../../../images/security-lock-button.png
    :alt: lock button
    :::

3. Click **Allow** to allow the {{elastic-endpoint}} system extension to load.

    :::{image} ../../../images/security-allow-system-ext.png
    :alt: allow system ext
    :::


## Approve network content filtering for {{elastic-endpoint}} [allow-filter-content]

After successfully loading the {{elastic-endpoint}} system extension,  an additional message appears, asking to allow {{elastic-endpoint}} to filter network content.

:::{image} ../../../images/security-filter-network-content.png
:alt: filter network content
:::


Click **Allow** to enable content filtering for the {{elastic-endpoint}} system extension. Without this approval, {{elastic-endpoint}} cannot receive network events and, therefore, cannot enable network-related features such as [host isolation](/solutions/security/endpoint-response-actions/isolate-host.md).


## Enable Full Disk Access for {{elastic-endpoint}} [enable-fda-endpoint]

{{elastic-endpoint}} requires Full Disk Access to subscribe to system events via the {{elastic-defend}} framework and to protect your network from malware and other cybersecurity threats. To enable Full Disk Access on endpoints running macOS Catalina (10.15) and later, you must manually approve {{elastic-endpoint}}.

::::{note}
The following instructions apply only to {{elastic-endpoint}} running version 8.0.0 and later. In {{serverless-short}}, versions 7.17.0 and earlier are not supported. To see Full Disk Access requirements for the Endgame sensor, refer to Endgame’s documentation.
::::


1. Open the **System Preferences** application.
2. Select **Security and Privacy**.

    :::{image} ../../../images/security-sec-privacy-pane.png
    :alt: sec privacy pane
    :class: screenshot
    :::

3. On the **Security and Privacy** pane, select the **Privacy** tab.
4. From the left pane, select **Full Disk Access**.

    :::{image} ../../../images/security-select-fda.png
    :alt: Select Full Disk Access
    :class: screenshot
    :::

5. In the lower-left corner of the pane, click the **Lock button**, then enter your credentials to authenticate.
6. In the **Privacy** tab,  confirm that `ElasticEndpoint` AND `co.elastic.systemextension` are selected to properly enable Full Disk Access.

    :::{image} ../../../images/security-select-endpoint-ext.png
    :alt: role+"screenshot"
    :::


In {{stack}}, if the endpoint is running {{elastic-endpoint}} version 7.17.0 or earlier:

1. In the lower-left corner of the pane, click the **Lock button**, then enter your credentials to authenticate.
2. Click the **+** button to view **Finder**.
3. Navigate to `/Library/Elastic/Endpoint`, then select the `elastic-endpoint` file.
4. Click **Open**.
5. In the **Privacy** tab, confirm that `elastic-endpoint` AND `co.elastic.systemextension` are selected to properly enable Full Disk Access.

:::{image} ../../../images/security-fda-7-16.png
:alt: fda 7 16
:::

