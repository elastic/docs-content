---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-maintenance-mode.html
applies_to:
  deployment:
     ece:
---

# Enable maintenance mode [ece-maintenance-mode]

Maintenance mode lets you perform actions on an allocator safely that might otherwise carry some risk. For example, if you want to remove the allocator role from a host, enabling maintenance mode prevents new Elasticsearch clusters and Kibana instances from being provisioned on the allocator whilst you are moving the existing nodes to another allocator or whilst you are removing the role.

To put an allocator into maintenance mode:

1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Allocators**.
3. Choose the allocator you want to work with and select **Enable Maintenance Mode**. Confirm the action.
   Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

After the allocator enters maintenance mode, no new Elasticsearch nodes or Kibana instances will be started on the allocator. Existing nodes will continue to work as expected. You can now safely perform actions like [moving nodes off the allocator](move-nodes-instances-from-allocators.md).

If you want to make the allocator fully active again, select **Disable Maintenance Mode**. Confirm the action.

::::{tip}
If you need the existing instances to stop routing requests, refer to the [stop routing request documentation](start-stop-routing-requests.md) to learn more.

::::
