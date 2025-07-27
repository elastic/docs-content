---
applies_to:
  deployment:
    self:
navigation_title: Manage connected clusters
---

# Manage connected clusters

Once your self-managed clusters are connected to {{ecloud}}, you can manage them from your {{ecloud}} home page.

:::{important}
You need the **Organization owner** role to perform these actions.
:::

## Connect additional clusters

To connect more self-managed clusters, we recommend repeating the steps to [connect your self-managed cluster to AutoOps](/deploy-manage/monitor/autoops/cc-connect-self-managed-to-autoops.md).

You can use the same installation command to connect multiple clusters, but remember that each cluster needs a separate, dedicated Elastic Agent.

## Disconnect a cluster

Complete the following steps to disconnect your self-managed cluster from your Cloud organization.

1. Log in to [{{ecloud}}](https://cloud.elastic.co/home).
2. In the **Connected clusters** section, locate the cluster you want to disconnect.
3. From that cluster’s actions menu, select **Disconnect cluster**.
4. Enter the cluster’s name in the field that appears and then select **Disconnect cluster**.

:::{include} /deploy-manage/monitor/_snippets/disconnect-cluster.md
:::