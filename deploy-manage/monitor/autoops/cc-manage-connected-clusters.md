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

You can use the same installation command to connect multiple clusters, but remember that each cluster needs a separate, dedicated Elastic agent.

## Disconnect a cluster

Disconnect your self-managed cluster from your Cloud organization.

1. Log in to [{{ecloud}}](https://cloud.elastic.co/home).
2. In the **Connected clusters** section, locate the cluster you want to disconnect.
3. From that cluster’s actions menu, select **Disconnect cluster**.
4. Enter the cluster’s name in the field that appears and then select **Disconnect cluster**.

:::{warning}
Disconnecting a cluster cannot be reversed. The cluster’s connection to your {{ecloud}} account will end and all metrics and AutoOps data will be permanently deleted.
:::