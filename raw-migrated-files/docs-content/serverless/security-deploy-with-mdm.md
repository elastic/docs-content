---
navigation_title: "Deploy on macOS with MDM"
---

# Deploy {{elastic-defend}} on macOS with mobile device management [security-deploy-with-mdm]


To silently install and deploy {{elastic-defend}} without the need for user interaction, you need to configure a mobile device management (MDM) profile for {{elastic-endpoint}}—the installed component that performs {{elastic-defend}}'s threat monitoring and prevention. This allows you to pre-approve the {{elastic-endpoint}} system extension and grant Full Disk Access to all the necessary components.

This page explains how to deploy {{elastic-defend}} silently using Jamf.


## Configure a Jamf MDM profile [security-deploy-with-mdm-configure-a-jamf-mdm-profile]

In Jamf, create a configuration profile for {{elastic-endpoint}}. Follow these steps to configure the profile:

1. [Approve the system extension](../../../solutions/security/configure-elastic-defend/deploy-on-macos-with-mdm.md#security-deploy-with-mdm-approve-the-system-extension).
2. [Approve network content filtering](../../../solutions/security/configure-elastic-defend/deploy-on-macos-with-mdm.md#security-deploy-with-mdm-approve-network-content-filtering).
3. [Enable notifications](../../../solutions/security/configure-elastic-defend/deploy-on-macos-with-mdm.md#security-deploy-with-mdm-enable-notifications).
4. [Enable Full Disk Access](../../../solutions/security/configure-elastic-defend/deploy-on-macos-with-mdm.md#security-deploy-with-mdm-enable-full-disk-access).


### Approve the system extension [security-deploy-with-mdm-approve-the-system-extension]

1. Select the **System Extensions** option to configure the system extension policy for the {{elastic-endpoint}} configuration profile.
2. Make sure that **Allow users to approve system extensions** is selected.
3. In the **Allowed Team IDs and System Extensions** section, add the {{elastic-endpoint}} system extension:

    1. (Optional) Enter a **Display Name** for the {{elastic-endpoint}} system extension.
    2. From the **System Extension Types** dropdown, select **Allowed System Extensions**.
    3. Under **Team Identifier**, enter `2BT3HPN62Z`.
    4. Under **Allowed System Extensions**, enter `co.elastic.systemextension`.

4. Save the configuration.

:::{image} ../../../images/serverless-system-extension-jamf.png
:alt: system extension jamf
:class: screenshot
:::


### Approve network content filtering [security-deploy-with-mdm-approve-network-content-filtering]

1. Select the **Content Filter** option to configure the Network Extension policy for the {{elastic-endpoint}} configuration profile.
2. Under **Filter Name**, enter `ElasticEndpoint`.
3. Under **Identifier**, enter `co.elastic.endpoint`.
4. In the **Socket Filter** section, fill in these fields:

    1. **Socket Filter Bundle Identifier**: Enter `co.elastic.systemextension`
    2. **Socket Filter Designated Requirement**: Enter the following:

        ```txt
        identifier "co.elastic.systemextension" and anchor apple generic and certificate 1[field.1.2.840.113635.100.6.2.6] /* exists */ and certificate leaf[field.1.2.840.113635.100.6.1.13] /* exists */ and certificate leaf[subject.OU] = "2BT3HPN62Z"
        ```

5. In the **Network Filter** section, fill in these fields:

    1. **Network Filter Bundle Identifier**: Enter `co.elastic.systemextension`
    2. **Network Filter Designated Requirement**: Enter the following:

        ```txt
        identifier "co.elastic.systemextension" and anchor apple generic and certificate 1[field.1.2.840.113635.100.6.2.6] /* exists */ and certificate leaf[field.1.2.840.113635.100.6.1.13] /* exists */ and certificate leaf[subject.OU] = "2BT3HPN62Z"
        ```

6. Save the configuration.

:::{image} ../../../images/serverless-content-filtering-jamf.png
:alt: content filtering jamf
:class: screenshot
:::


### Enable notifications [security-deploy-with-mdm-enable-notifications]

1. Select the **Notifications** option to configure the Notification Center policy for the {{elastic-endpoint}} configuration profile.
2. Under **App Name**, enter `Elastic Security.app`.
3. Under **Bundle ID**, enter `co.elastic.alert`.
4. In the **Settings** section, include these options with the following settings:

    1. **Critical Alerts**: Enable
    2. **Notifications**: Enable
    3. **Banner alert type**: Persistent
    4. **Notifications on Lock Screen**: Display
    5. **Notifications in Notification Center**: Display
    6. **Badge app icon**: Display
    7. **Play sound for notifications**: Enable

5. Save the configuration.

:::{image} ../../../images/serverless-notifications-jamf.png
:alt: notifications jamf
:class: screenshot
:::


### Enable Full Disk Access [security-deploy-with-mdm-enable-full-disk-access]

1. Select the **Privacy Preferences Policy Control** option to configure the Full Disk Access policy for the {{elastic-endpoint}} configuration profile.
2. Add a new entry with the following details:

    1. Under **Identifier**, enter `co.elastic.systemextension`.
    2. From the **Identifier Type** dropdown, select **Bundle ID**.
    3. Under **Code Requirement**, enter the following:

        ```txt
        identifier "co.elastic.systemextension" and anchor apple generic and certificate 1[field.1.2.840.113635.100.6.2.6] /* exists */ and certificate leaf[field.1.2.840.113635.100.6.1.13] /* exists */ and certificate leaf[subject.OU] = "2BT3HPN62Z"
        ```

    4. Make sure that **Validate the Static Code Requirement** is selected.

3. Add a second entry with the following details:

    1. Under **Identifier**, enter `co.elastic.endpoint`.
    2. From the **Identifier Type** dropdown, select **Bundle ID**.
    3. Under **Code Requirement**, enter the following:

        ```txt
        identifier "co.elastic.endpoint" and anchor apple generic and certificate 1[field.1.2.840.113635.100.6.2.6] /* exists */ and certificate leaf[field.1.2.840.113635.100.6.1.13] /* exists */ and certificate leaf[subject.OU] = "2BT3HPN62Z"
        ```

    4. Make sure that **Validate the Static Code Requirement** is selected.

4. Add a third entry with the following details:

    1. Under **Identifier**,  enter `co.elastic.elastic-agent`.
    2. From the **Identifier Type** dropdown, select **Bundle ID**.
    3. Under **Code Requirement**, enter the following:

        ```txt
        identifier "co.elastic.elastic-agent" and anchor apple generic and certificate 1[field.1.2.840.113635.100.6.2.6] /* exists */ and certificate leaf[field.1.2.840.113635.100.6.1.13] /* exists */ and certificate leaf[subject.OU] = "2BT3HPN62Z"
        ```

    4. Make sure that **Validate the Static Code Requirement** is selected.

5. Save the configuration.

:::{image} ../../../images/serverless-fda-jamf.png
:alt: fda jamf
:class: screenshot
:::

After you complete these steps, generate the mobile configuration profile and install it onto the macOS machines. Once the profile is installed, {{elastic-defend}} can be deployed without the need for user interaction.
