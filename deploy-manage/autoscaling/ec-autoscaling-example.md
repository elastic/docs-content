---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoscaling-example.html
---

# Autoscaling example [ec-autoscaling-example]

To help you better understand the available autoscaling settings, this example describes a typical autoscaling workflow on sample {{ech}} deployment.

1. Enable autoscaling:

    * On an **existing deployment**, open the deployment **Edit** page to find the option to turn on autoscaling.
    * When you create a new deployment, you can find the autoscaling option under **Advanced settings**.

        Once you confirm your changes or create a new deployment, autoscaling is activated with system default settings that you can adjust as needed (though for most use cases the default settings will likely suffice).

2. View and adjust autoscaling settings on data tiers:

    1. Open the **Edit** page for your deployment to get the current and maximum size per zone of each Elasticsearch data tier. In this example, the hot data and content tier has the following settings:

        |     |     |     |
        | --- | --- | --- |
        | **Current size per zone** | **Maximum size per zone** |  |
        | 45GB storage | 1.41TB storage |  |
        | 1GB RAM | 32GB RAM |  |
        | Up to 2.5 vCPU | 5 vCPU |  |

        The fault tolerance for the data tier is set to 2 availability zones.

        :::{image} ../../images/cloud-ec-ce-autoscaling-data-summary2.png
        :alt: A screenshot showing sizing information for the autoscaled data tier
        :::

    2. Use the dropdown boxes to adjust the current and/or the maximum size of the data tier. Capacity will be added to the hot content and data tier when required, based on its past and present storage usage, until it reaches the maximum size per zone. Any scaling events are applied simultaneously across availability zones. In this example, the tier has plenty of room to scale relative to its current size, and it will not scale above the maximum size setting. There is no minimum size setting since downward scaling is currently not supported on data tiers.

3. View and adjust autoscaling settings on a machine learning instance:

    1. From the deployment **Edit** page you can check the minimum and maximum size of your deployment’s machine learning instances. In this example, the machine learning instance has the following settings:

        |     |     |     |
        | --- | --- | --- |
        | **Minimum size per zone** | **Maximum size per zone** |  |
        | 1GB RAM | 64GB RAM |  |
        | 0.5 vCPU up to 8 vCPU | 32 vCPU |  |

        The fault tolerance for the machine learning instance is set to 1 availability zone.

        :::{image} ../../images/cloud-ec-ce-autoscaling-ml-summary2.png
        :alt: A screenshot showing sizing information for the autoscaled machine learning node
        :::

    2. Use the dropdown boxes to adjust the minimum and/or the maximum size of the data tier. Capacity will be added to or removed from the machine learning instances as needed. The need for a scaling event is determined by the expected memory and vCPU requirements for the currently configured machine learning job. Any scaling events are applied simultaneously across availability zones. Note that unlike data tiers, machine learning nodes do not have a **Current size per zone** setting. That setting is not needed since machine learning nodes support both upward and downward scaling.

4. Over time, the volume of data and the size of any machine learning jobs in your deployment are likely to grow. Let’s assume that to meet storage requirements your hot data tier has scaled up to its maximum allowed size of 64GB RAM and 32 vCPU. At this point, a notification appears on the deployment overview page letting you know that the tier has scaled to capacity. You’ll also receive an alert by email.
5. If you expect a continued increase in either storage, memory, or vCPU requirements, you can use the **Maximum size per zone** dropdown box to adjust the maximum capacity settings for your data tiers and machine learning instances, as appropriate. And, you can always re-adjust these levels downward if the requirements change.

As you can see, autoscaling greatly reduces the manual work involved to manage a deployment. The deployment capacity adjusts automatically as demands change, within the boundaries that you define. Check our main [Deployment autoscaling](../autoscaling.md) page for more information.

