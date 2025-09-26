---
applies_to:
  stack: ga 9.2
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Device control

Device control helps protect your organization from data loss, malware, and unauthorized access by managing which devices can connect to your computers. Specifically, it restricts which external storage devices—such as USB drives and hard drives—can connect to endpoints that have {{elastic-defend}} installed. You can select which


## Configure Device Control for your hosts using {{elastic-defend}} 

To configure Device Control for one or more hosts, edit the {{elastic-defend}} policy that affects those hosts. 

:::{note}
By default, new {{elastic-defend}} policies have Device Control enabled, with all device types set to **Block**. {{elastic-defend}} policies that existed before Device Control was supported have Device Control disabled by default. 
:::


## Add Trusted Devices to specify which devices are exempt from Device Control

Trusted Devices are specific external devices that can connect to your protected hosts regardless of Device Control settings. Use Trusted Devices to avoid interfering with expected workflows that involve known hardware. Trusted Devices can apply to a specific policy, or globally to all policies. 

Add a Trusted Device to a single policy:

1. Navigate to the {{elastic-defend}} policy for which you want to create a Trusted Device.
2. Go to the **Trusted Devices** tab, and click **Assign trusted devices to policy**.
3. 

Add a Trusted Device globally:

1. Go to the **Trusted Devices** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **+ Add trusted device**. The Add trusted application flyout opens.
