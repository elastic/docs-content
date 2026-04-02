---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-azure-native.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
---

# Monitor Microsoft Azure with the Azure Native ISV Service [monitor-azure-native]

::::{note}
The {{ecloud}} Azure Native ISV Service allows you to deploy managed instances of the {{stack}} directly in Azure, through the Azure integrated marketplace. The service includes native capabilities for consolidating Azure logs and metrics in Elastic. For more information, refer to [Azure Native ISV Service](/deploy-manage/deploy/elastic-cloud/azure-native-isv-service.md).

**Using {{agent}} to monitor Azure?** Refer to [Monitor Microsoft Azure with {{agent}}](monitor-microsoft-azure-with-elastic-agent.md).

::::


In this tutorial, you’ll learn how to:

* Create an {{es}} resource in the Azure portal.
* Ingest Azure platform logs using the Azure Native ISV Service.
* Ingest logs and metrics from your virtual machines.
* Visualize the logs and metrics in {{kib}}.

::::{tip}
The full product name in the Azure integrated marketplace is `Elastic Cloud (Elasticsearch) - An Azure Native ISV Service`.
::::



## Step 1: Create an {{es}} resource in the Azure portal [azure-create-resource]

::::{important}
These steps will not work if you have an active GCP or AWS deployment in {{ecloud}} that is already associated with the email address used for your Azure account. To avoid this problem, delete your GCP and AWS deployments in {{ecloud}}, or use a different Azure account. If this does not resolve your issue, reach out to us at `support@elastic.co`.
::::


Microsoft Azure allows you to find, deploy, and manage {{es}} from within the Azure portal. The Azure Native ISV Service makes it faster and easier for you to experience the value of Elastic in your Azure environment. Behind the scenes, this process provisions a marketplace subscription with {{ecloud}}.


### Create an {{es}} resource [_create_an_es_resource_2]

1. Log in to the [Azure portal](https://portal.azure.com/).

    ::::{note}
    Ensure your Azure account is configured with **Owner** access on the subscription you want to use to deploy {{es}}. To learn more about Azure subscriptions, refer to the [Microsoft Azure documentation](https://docs.microsoft.com/en-us/azure/cost-management-billing/manage/add-change-subscription-administrator#assign-a-subscription-administrator).

    ::::

2. In the search bar, enter **Elastic Cloud (Elasticsearch)** and then select **Elastic Cloud (Elasticsearch) – An Azure Native ISV Service**.
3. Click **Create**.
4. Enter the **Subscription**, **Resource group**, and the **Resource name**.
5. Select an {{es}} version.
6. Select a region and then click **Review + create**.

    ::::{note}
    Don’t change any settings under Logs & metrics yet. We will cover logs and infrastructure metrics later in this tutorial.

    ::::


    :::{image} /solutions/images/observability-monitor-azure-native-create-elastic-resource.png
    :alt: Screenshot of Elastic resource creation in Azure
    :screenshot:
    :::

7. To create the {{es}} deployment, click **Create**.
8. After deployment is complete, click **Go to resource**. Here you can view and configure your deployment details. To access the cluster, click **{{kib}}**.

    :::{image} /solutions/images/observability-monitor-azure-native-elastic-deployment.png
    :alt: Screenshot of deployment details for Elastic resource in Azure
    :screenshot:
    :::

9. Click **Accept** (if necessary) to grant permissions to use your Azure account, then log in to {{ecloud}} using your Azure credentials as a single sign-on.
10. To look for available data, click **Observability**. There should be no data yet. Next, you’ll ingest logs.


## Step 2: Ingest logs by using the Azure Native ISV Service [azure-ingest-logs-native-integration]

To ingest Azure subscription and resource logs into Elastic, you use the Azure Native ISV Service.

1. In the Azure portal, go to your {{es}} resource page and click **Ingest logs and metrics from Azure Services**.
2. Under **Logs**, select both checkboxes to collect subscription activity logs and Azure resource logs. Click **Save**.

    :::{image} /solutions/images/observability-monitor-azure-native-elastic-config-logs-metrics.png
    :alt: Screenshot of logs and metrics configuration for Elastic resource in Azure
    :screenshot:
    :::

    ::::{note}
    This configuration can also be applied during the Elastic resource creation. To make the concepts clearer, this tutorial separates the two steps.
    ::::


    ::::{note}
    Native metrics collection for Azure services is not fully supported yet. To learn how to collect metrics from Azure services, refer to [Monitor Microsoft Azure with {{agent}}](monitor-microsoft-azure-with-elastic-agent.md).
    ::::

3. In {{kib}}, under **{{observability}}**, find **Overview** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Refresh the page until you see some data. This may take a few minutes.
4. To analyze your subscription and resource logs, click **Show Logs**.


## Step 3: Ingest logs and metrics from your virtual machines (VMs) [azure-ingest-VM-logs-metrics]

1. In the Azure portal, go to your {{es}} resource and click **Virtual machines**.
2. Select the VMs that you want to collect logs and metrics from, click **Install Extension**, and then click **OK**.

    :::{image} /solutions/images/observability-monitor-azure-native-elastic-vms.png
    :alt: Screenshot that shows VMs selected for logs and metrics collection
    :screenshot:
    :::

3. Wait until the extension is installed and sending data (if the list does not update, click **Refresh** ).
4. Back in {{kib}}, view the **Discover** again. Notice that you can filter the view to show logs for a specific instance, for example `cloud.instance.name : "ingest-tutorial-linux"`.
5. To view VM metrics, go to **Infrastructure inventory** and then select a VM. (To open **Infrastructure inventory**, find **Infrastructure** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).)

    To explore the data further, click **Open as page**.


Congratulations! You have completed the tutorial.
