---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-add-capacity.html
applies_to:
  deployment:
     ece:
---

# Scale out your installation [ece-add-capacity]

Elastic Cloud Enterprise scales to whatever capacity you need. If you need more processing capacity because your allocators are close to being maxed out or because you want to enable high availability and need an additional availability zone, simply add more capacity and change your deployment configuration to make use of it.

Check the available capacity:

1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Allocators** to view the available capacity.
   Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.
   In this case 3 GB and 6 GB on two different allocators:
   :::{image} ../../../images/cloud-enterprise-ece-available-capacity.png
   :alt: The available capacity in an installation
   :::

If this is not sufficient, add more capacity to your installation:

1. [Install Elastic Cloud Enterprise on additional hosts](../../deploy/cloud-enterprise/install-ece-on-additional-hosts.md) to create additional capacity.
2. [Add capacity](https://www.elastic.co/docs/api/doc/cloud-enterprise/operation/operation-set-allocator-settings) to existing allocators by updating the allocator settings when adding memory to the host.
3. [Assign roles](../../deploy/cloud-enterprise/assign-roles-to-hosts.md) to the additional hosts. If you need to handle a larger search or logging workload, assign the new hosts the allocator role.
4. (Optional) [Tag allocators](../../deploy/cloud-enterprise/ece-configuring-ece-tag-allocators.md) to the new host to indicate what kind of hardware you have available.
5. [Resize your deployment](../../deploy/cloud-enterprise/resize-deployment.md) to handle a larger workload.
