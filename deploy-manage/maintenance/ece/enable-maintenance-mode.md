---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-maintenance-mode.html
applies_to:
  deployment:
    ece:
products:
  - id: cloud-enterprise
---

# Enable maintenance mode [ece-maintenance-mode]

Maintenance mode lets you perform actions on hosts safely that might otherwise carry some risk. 

## Allocator maintenance mode

If you want to remove the allocator role from a host, enabling maintenance mode prevents new {{es}} clusters and {{kib}} instances from being provisioned on the allocator whilst you are moving the existing nodes to another allocator or whilst you are removing the role.

To put an allocator into maintenance mode:

1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Allocators**.
3. Choose the allocator you want to work with, click **Manage allocator** then select **Enable allocator maintenance**. Confirm the action.
   Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

After the allocator enters maintenance mode, no new {{es}} nodes or {{kib}} instances will be started on the allocator. Existing nodes will continue to work as expected. You can now safely perform actions like [moving nodes off the allocator](move-nodes-instances-from-allocators.md).

If you want to make the allocator fully active again, select **Disable allocator maintenance**. Confirm the action.

::::{tip}
If you need the existing instances to stop routing requests, refer to the [stop routing request documentation](../start-stop-routing-requests.md) to learn more.
::::

## Controller maintenance mode

Placing a controller (also known as a "coordinator") in maintenance mode stops it from accepting new deployment configuration changes. Any deployment changes that are in progress continue processing. New deployment change requests get routed to other controllers, if available.

To put a controller into maintenance mode:

1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Control Planes**.
3. Locate the controller you want to manage and select **Enable controller maintenance**. Confirm the action.

If you want to make the controller fully active again, select **Disable controller maintenance**. Confirm the action.
