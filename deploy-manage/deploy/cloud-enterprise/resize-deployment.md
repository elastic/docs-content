---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-resize-deployment.html
---

# Resize deployment [ece-resize-deployment]

Elasticsearch scales to whatever capacity you need and with as many nodes as the available resources can support. If you don’t have enough available resources, [add some capacity first](../../maintenance/ece/scale-out-installation.md).

::::{tip} 
You can also enable autoscaling on a deployment to have the available resources for components, such as data tiers and machine learning nodes, adjust automatically as the demands on the deployment change over time. Check [Deployment autoscaling](../../autoscaling.md) to learn more.
::::


To resize a deployment:

1. [Log into the Cloud UI](log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From your deployment menu, go to the **Edit** page.
4. Change the deployment configuration:

    Fault tolerance
    :   If the initial deployment you created uses only one availability zone, it is not fault tolerant. On a production system, enable [high availability](ece-ha.md) by changing your deployment to use at least two availability zones, three for mission-critical deployments. The number of instances comes from the number of zones and the type of template. Having more nodes or instances lets you scale out horizontally by adding more processing capacity to your deployment.

        ::::{warning} 
        Deployments that use only one availability zone are not highly available and are at risk of data loss, if you do not [configure an external snapshot repository](../../tools/snapshot-and-restore/cloud-enterprise.md) to enable regular backups. To safeguard against data loss, you must use at least two data centers and configure an external repository for backups.
        ::::


    RAM per instance
    :   Node and instance capacity should be sufficient to sustain your search workload, even if you lose an availability zone. Currently, half of the memory is assigned to the JVM heap. For example, on an Elasticsearch cluster node with 32 GB RAM, 16 GB would be allotted to heap. Up to 64 GB RAM and 1 TB storage per node are supported.

        A summary of your sections for each instance and the entire deployment are available for you to review before finalizing your changes.

5. Select **Save changes**.


## Example: From very small to very large [ece_example_from_very_small_to_very_large] 

This example shows you how to change an existing, very basic deployment to use high availability and to add capacity.

To scale your deployment from very small to very large:

1. [Log into the Cloud UI](log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From your deployment menu, go to the **Edit** page.
4. Under **Fault tolerance**, select **3 zones** for mission critical environments*.
5. Under **RAM per instance**, select **64 GB memory / 2 TB storage**.
6. Select **Save changes**.

There is no downtime when adding high availability. Deployments with high availability will continue to handle user requests, even if the configuration changes are applied.

