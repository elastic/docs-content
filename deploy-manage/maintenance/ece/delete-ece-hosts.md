---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-delete-runner.html
applies_to:
  deployment:
     ece:
---

# Delete ECE hosts [ece-delete-runner]

You might need to delete hosts for several reasons:

* To remove some resources from your Elastic Cloud Enterprise installation if they are no longer required.
* To remove a faulty host from the Cloud UI so that it is no longer part of your Elastic Cloud Enterprise installation.

Deleting a host only removes the host from your installation, it does not [remove the Elastic Cloud Enterprise software from the host](../../uninstall/uninstall-elastic-cloud-enterprise.md). After the host has been deleted, you can repurpose or troubleshoot the physical host on which the Elastic Cloud Enterprise host was located.

To delete hosts:

1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Hosts**.
   Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. For hosts that hold the allocator role:
   1. [Enable maintenance mode](enable-maintenance-mode.md) on the allocator.
   2. [Move all nodes off the allocator](move-nodes-instances-from-allocators.md) and to other allocators in your installation.

4. Go to **Hosts** and select a host.
5. Select **Manage roles** from the **Manage host** menu and remove all assigned roles.
6. Select **Demote host** from the **Manage host** menu if present. If the **Delete host** option is already enabled, skip this step.
7. Remove *all running* containers from the host, starting from the container with name `frc-runners-runner`. Then remove the storage directory (the default `/mnt/data/elastic/`). You can use the recommended [cleanup command](../../uninstall/uninstall-elastic-cloud-enterprise.md).  Upon doing so, the UI should reflect the host is **Disconnected**, allowing the host to be deleted.
8. Select **Delete host** and confirm.

::::{tip}
Refresh the page if the button isn’t active.
::::
