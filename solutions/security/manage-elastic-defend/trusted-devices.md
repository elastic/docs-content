---
applies_to:
  stack: ga 9.2
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Trusted devices

By default, new {{elastic-defend}} policies have Device Control enabled, with all operations set to **Block**. This prevents external storage devices from connecting to protected hosts.

Trusted Devices are specific external devices that are allowed to connect to your protected hosts regardless of Device Control settings. Create Trusted Devices to avoid interfering with expected workflows that involve known hardware. Trusted Devices can apply to a specific policy, or globally to all policies. 

## Add Trusted Devices to exempt them from Device Control

1. Go to the **Trusted Devices** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **+ Add trusted device**. The Add trusted device flyout opens.
3. Name your trusted device and give it a description. 
4. In the **Conditions** section, specify the operating system and the `Device ID`. 
5. Select either **Global** or **Per policy**.
6. Click **Add trusted device**.

## Add a Trusted Device to a policy

1. Navigate to the {{elastic-defend}} policy to which you want to add a Trusted Device.
2. Go to the **Trusted Devices** tab, and click **Assign trusted devices to policy**.
3. Next, select one or more existing trusted devices, then click **+ Assign trusted devices to policy**.


## View the Device Control dashboard

By default, each new {{kib}} instance includes a Device Control dashboard. When at least one of your {{elastic-defend}} policies has Device Control enabled, the dashboard displays data about attempted device connections and their outcomes.