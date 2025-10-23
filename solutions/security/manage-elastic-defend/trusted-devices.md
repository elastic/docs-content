---
applies_to:
  stack: ga 9.2
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Trusted devices

By default, {{elastic-defend}} policies have [device control](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#device-control) enabled, with access level set to block all operations. This prevents external storage devices from connecting to protected hosts.

Trusted devices are specific external devices that are allowed to connect to your protected hosts regardless of device control settings. Create trusted devices to avoid interfering with expected workflows that involve known hardware. 

By default, a trusted device is recognized globally across all hosts running {{elastic-defend}}. You can also assign a trusted device to a specific {{elastic-defend}} integration policy, enabling the device to be trusted by only the hosts assigned to that policy.

## Add a trusted device

Add a trusted device to exempt it from device control:

1. Go to the **Trusted Devices** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **+ Add trusted device**. The Add trusted device flyout opens.
3. Name your trusted device and give it a description. 
4. In the **Conditions** section, specify the operating system(s) and the `Device ID`. 
5. Select an option in the **Assignment** section:
    * **Global**: Assign the trusted device to all {{elastic-defend}} integration policies.
    * **Per Policy**: Assign the trusted device to one or more specific {{elastic-defend}} integration policies.
6. Click **Add trusted device**.

## View and manage trusted devices

The **Trusted devices** page displays all the trusted devices that have been added to the {{security-app}}. To refine the list, use the search bar to search by name, description, or field value.

:::{image} /solutions/images/security-trusted-devices-list.png
:alt: trusted apps list
:screenshot:
:::


### Edit a trusted device

You can individually modify each trusted device. You can also change the policies that a trusted device is assigned to.

To edit a trusted device:

1. Click the actions menu (**…**) on the trusted device you want to edit, then select **Edit trusted device**.
2. Modify details as needed.
3. Click **Save**.


### Delete a trusted device

You can delete a trusted device, which removes it entirely from all {{elastic-defend}} integration policies.

To delete a trusted device:

1. Click the actions menu (**…**) on the trusted device you want to delete, then select **Delete trusted device**.
2. On the dialog that opens, verify that you are removing the correct device, then click **Delete**. A confirmation message appears.
