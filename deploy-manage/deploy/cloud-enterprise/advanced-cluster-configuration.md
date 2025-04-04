---
applies_to:
  deployment:
    ece: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-advanced-configuration.html
---

# Advanced cluster configuration [ece-advanced-configuration]

Most configuration changes can be made safely from other parts of the Cloud UI. You should use the **Advanced cluster configuration** page to make changes only if the functionality is not available elsewhere and if you know what you are doing or are being directed by someone from Elastic.

To edit the cluster configuration directly:

1. [Log into the Cloud UI](log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From your deployment menu, go to the **Edit** page then go to the bottom of the page and select **advanced {{es}} configuration**.
4. Edit the configuration:

    * The contents of the **Deployment configuration** section describe your current configuration, such as the current capacity, the node count, the installed {{es}} version, and so forth. You can manually edit the configuration.
    * The **{{es}} cluster data** section describes additional parts of your cluster, such as its name, whether snapshots are enabled, security information, and whether {{kib}} is enabled.

5. Select **Save** for the sections that you modified to apply the new configuration. You should receive a message that your new configuration is successful.

::::{warning}
You can break things when editing the cluster deployment configuration. Use this functionality only if you know what you are doing or if you are being directed by someone from Elastic.
::::
