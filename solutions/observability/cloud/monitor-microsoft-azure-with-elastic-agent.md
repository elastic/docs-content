---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-azure-elastic-agent.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
---

# Monitor Microsoft Azure with Elastic Agent [monitor-azure-elastic-agent]

::::{note}
**New to Elastic?** Refer to our [getting started guide](/solutions/observability/get-started/quickstart-monitor-hosts-with-elastic-agent.md) instead of the steps described here. Return to this tutorial after you’ve learned the basics.

**Using the native Azure integration from the marketplace?** Refer to [Monitor Microsoft Azure with the Azure Native ISV Service](monitor-microsoft-azure-with-azure-native-isv-service.md).

::::


In this tutorial, you’ll learn how to deploy {{agent}} and monitor your Azure infrastructure with Elastic {{observability}}.


## What you’ll learn [azure-elastic-agent-what-you-learn]

You’ll learn how to:

* Create an Azure service principal with permissions to read monitoring data.
* Collect Azure billing metrics.
* Collect Azure activity logs.
* Visualize the logs and infrastructure metrics in {{kib}}.


## Step 1: Create an Azure service principal [azure-collect-metrics]

In this step, you create an Azure service principal and then grant them access to use the Azure REST API.

The [Azure REST API](https://learn.microsoft.com/en-us/rest/api/azure/) allows you to get insights into your Azure resources using different operations. To access the Azure REST API, you need to use the Azure Resource Manager authentication model. Therefore, you must authenticate all requests with Azure Active Directory (Azure AD). You can create the service principal using the [Azure portal](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal) or [Azure PowerShell](https://docs.microsoft.com/en-us/powershell/azure/create-azure-service-principal-azureps?view=azps-2.7.0). Then, you need to grant access permission, which is detailed [here](https://docs.microsoft.com/en-us/azure/role-based-access-control/built-in-roles). This tutorial shows how to use the Azure portal.


### Create an Azure service principal [_create_an_azure_service_principal]

1. Go to the [Microsoft Azure Portal](https://portal.azure.com/). Search for and select **Azure Active Directory**.
2. In the navigation pane, select **App registrations** and then click **New registration**.
3. Type the name of your application (this tutorial uses `ingest-tutorial-monitor-azure`) and click **Register** (accept the default values for other settings).

    :::{image} /solutions/images/observability-agent-tut-azure-register-app.png
    :alt: Screenshot of the application registration
    :screenshot:
    :::

    Copy the **Application (client) ID** and save it for later. This ID is required to configure {{agent}} to connect to your Azure account.

4. In the navigation pane, select **Certificates & secrets**, and then click **New client secret** to create a new security key.

    :::{image} /solutions/images/observability-agent-tut-azure-click-client-secret.png
    :alt: Screenshot of adding a new client secret
    :screenshot:
    :::

5. Type a description of the secret and select an expiration. Click **Add** to create the client secret. Under **Value**, copy the secret value and save it (along with your client ID) for later.

    ::::{important}
    This is your only chance to copy the secret value. You can’t retrieve this value after you leave this page!

    ::::



### Grant access permission for your service principal [_grant_access_permission_for_your_service_principal]

After creating the Azure service principal, you need to grant it the correct permissions. You need the `Billing Reader` role to configure {{agent}} to collect billing metrics.

1. In the Azure Portal, search for and select **Subscriptions**.
2. In the Subscriptions page, click the name of your subscription.
3. In the navigation pane, select **Access control (IAM)**.
4. Click **Add** and select **Add role assignment**.
5. On the **Roles** tab, select the **Billing Reader** role, then click **Next**.
6. On the **Members** tab, select the option to assign access to **User, group, or service principal**.
7. Click **Select members**, then search for and select the principal you created earlier.
8. For the description, enter the name of your service principal.
9. Click **Next** to review the role assignment:

    :::{image} /solutions/images/observability-agent-tut-azure-add-role-assignment.png
    :alt: Screen capture of adding a role assignment
    :screenshot:
    :::

10. Click **Review + assign** to grant the service principal access to your subscription.


## Step 2: Install the Azure Billing Metrics integration [elastic-agent-add-azure-integration]

In this step, you install the Azure Billing Metrics integration in {{kib}}. This integration contains an input for collecting metrics, such as Azure usage details and forecast information, about your subscription.

To add the integration:

1. Find **Integrations** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the query bar, search for **Azure Billing** and select the Azure Billing Metrics integration to see more details about it.
3. Click **Add Azure Billing Metrics**.
4. Under Integration settings, configure the integration name and optionally add a description.

    ::::{tip}
    If you don’t see options for configuring the integration, you’re probably in a workflow designed for new deployments. Follow the steps, then return to this tutorial when you’re ready to configure the integration.
    ::::

5. Specify values for all the required fields. For more information about these settings, refer to the [Azure Billing Metrics](https://docs.elastic.co/en/integrations/azure_billing) documentation.

    **Client ID**
    :   The Application (client) ID that you copied earlier when you created the service principal.

    **Client secret**
    :   The secret value that you copied earlier.

    **Tenant ID**
    :   The tenant ID listed on the main Azure Active Directory Page.

    **Subscription ID**
    :   The subscription ID listed on the main Subscriptions page.

        :::{image} /solutions/images/observability-agent-tut-azure-integration-settings.png
        :alt: Screenshot of integration settings for Azure
        :screenshot:
        :::

6. Make sure the **Collect Azure Billing metrics** selector is turned on.
7. Accept the defaults to create a new agent policy.
8. Click **Save and continue**. This step takes a minute or two to complete. When it’s done, you’ll have an agent policy that contains the Azure configuration you just specified.

A popup should appear that prompts you to **Add {{agent}} to your hosts**.


## Step 3: Install and run an {{agent}} on your machine [azure-elastic-agent-install]

::::{important}
To get support for the latest API changes from Azure, we recommend that you use the latest in-service version of {{agent}} compatible with your {{stack}}. Otherwise your integrations may not function as expected.
::::


You can install {{agent}} on any host that can access the Azure account and forward events to {{es}}.

1. In the popup, click **Add {{agent}} to your hosts** to open the **Add agent** flyout.

    ::::{tip}
    If you accidentally closed the popup, go to **{{fleet}} → Agents**, then click **Add agent** to access the installation instructions.
    ::::


    The **Add agent** flyout has two options: **Enroll in {{fleet}}** and **Run standalone**. The default is to enroll the agents in {{fleet}}, as this reduces the amount of work on the person managing the hosts by providing a centralized management tool in {{kib}}.

2. The enrollment token you need should already be selected.

    ::::{note}
    The enrollment token is specific to the {{agent}} policy that you just created. When you run the command to enroll the agent in {{fleet}}, you will pass in the enrollment token.
    ::::

3. To download, install, and enroll the {{agent}}, select your host operating system and copy the installation command shown in the instructions.
4. Run the command on the host where you want to install {{agent}}.

It takes a few minutes for {{agent}} to enroll in {{fleet}}, download the configuration specified in the policy, and start collecting data. You can wait to confirm incoming data, or close the window.


## Step 4: Visualize Azure billing metrics [azure-elastic-agent-visualize-metrics]

Now that the metrics are streaming to {{es}}, you can visualize them in {{kib}}. Find **Dashboards** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Search for Azure Billing and select the dashboard called **[Azure Billing] Billing Overview**.

:::{image} /solutions/images/observability-agent-tut-azure-billing-dashboard.png
:alt: Screenshot of Azure billing overview dashboard
:screenshot:
:::

Keep in mind {{agent}} collects data every 24 hours.


## Step 5: Collect Azure activity logs [azure-elastic-agent-collect-azure-activity-logs]

Azure activity logs provide insight into the operations performed on resources in your subscription, such as when and who modified resources, and when virtual machines were started (or failed to start).

In this step, you configure Azure to export activity logs to an Azure event hub, then you configure the Azure Logs integration to read logs from the event hub and send them to {{es}}.


### Create an event hub for your logs [azure-elastic-agent-create-event-hub]

[Azure Event Hubs](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-about) is a data streaming platform and event ingestion service that you use to store in-flight Azure logs before sending them to {{es}}. For this tutorial, you create a single event hub because you are collecting logs from one service: the Azure Monitor service.

To create an Azure event hub:

1. Go to the Azure portal.
2. Search for and select **Event Hubs**.
3. Click **Create** and create a new Event Hubs namespace. You’ll need to create a new resource group, or choose an existing one.
4. Enter the required settings for the namespace and click **Review + create**.

    :::{image} /solutions/images/observability-agent-tut-azure-create-eventhub.png
    :alt: Screenshot of window for creating an event hub namespace
    :screenshot:
    :::

5. Click **Create** to deploy the resource.
6. In the new namespace, click **+ Event Hub** and enter a name for the event hub.
7. Click **Review + create**, and then click **Create** to deploy the resource.
8. Make a note of the namespace and event hub name because you will need them later.

:::::{note}
**When do I need more than one event hub?**

Typically you create an event hub for each service you want to monitor. For example, imagine that you want to collect activity logs from the Azure Monitor service plus signin and audit logs from the Active Directory service. Rather than sending all logs to a single event hub, you create an event hub for each service:

:::{image} /solutions/images/observability-agent-tut-azure-event-hub-diagram.png
:alt: Diagram that shows an event hub for Active Directory logs and an event hub for activity logs
:::

This setup is more efficient than using a single event hub for all logs because it:

* Ensures that you publish only the logs expected by the downstream integration.
* Saves bandwidth and compute resources because inputs only need to process relevant logs, rather than processing all the logs for all your monitored services, then discarding unneeded logs.
* Avoids duplicates that might result from multiple inputs inadvertently reading and processing the same logs.

For high-volume deployments, you might even want to have a dedicated event hub for each data stream.

:::::



### Configure diagnostic settings to send logs to the event hub [azure-elastic-agent-configure-azure-diagnostics]

Every Azure service that creates logs has diagnostic settings that allow you to export logs and metrics to an external destination. In this step, you configure the Azure Monitor service to export activity logs to the event hub you created earlier.

To configure diagnostic settings for the Azure Monitor service:

1. Go to the Azure portal and go to **Home → Monitor**.
2. In the navigation page, select **Activity log**, and then click **Export Activity Logs**.
3. Select your subscription and click **Add diagnostic setting**.
4. Enter a name for the diagnostic setting.
5. In the list of log categories, select the logs you want to export.
6. Under Destination details, select **Stream to an event hub** and select the namespace and event hub you created earlier. For example:

    :::{image} /solutions/images/observability-agent-tut-azure-log-categories.png
    :alt: Screenshot of Azure diagnostic settings showing Administrative
    :screenshot:
    :::

7. Save the diagnostic settings.


### Configure the Azure Logs integration to collect activity logs [azure-elastic-agent-configure-logs-integration]

Now that activity logs are streaming into the event hub, you can configure the Azure activity log integration to ingest the logs.

To add the integration:

1. Find **Integrations** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the query bar, search for **Azure activity logs** and select the Azure activity logs integration to see more details about it.
3. Click **Add Azure activity logs**.
4. Under Integration settings, configure the integration name and optionally add a description.
5. Specify values for all the required fields. For more information about these settings, refer to the [Azure activity logs](https://docs.elastic.co/en/integrations/azure/activitylogs) documentation.

    **Eventhub**
    :   The name of the event hub you created earlier.

    **Connection String**
    :   The connection string primary key of the event hub namespace. To learn how to get the connection string, refer to [Get an Event Hubs connection string](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-get-connection-string) in the Azure documentation.

        ::::{tip}
        Instead of copying the connection string from the RootManageSharedAccessKey policy, you should create a new shared access policy (with permission to listen) and copy the connection string from the new policy.
        ::::


    **Storage account**
    :   The name of a blob storage account that {{agent}} can use to store information about logs consumed by the agent. You can use the same storage account container for all integrations.

    **Storage account key**
    :   A valid access key defined for the storage account.

        :::{image} /solutions/images/observability-agent-tut-azure-activity-log-settings.png
        :alt: Screenshot of integration settings for Azure activity logs
        :screenshot:
        :::

6. Make sure the **Collect Azure activity logs from Event Hub** selector is turned on.
7. Under **Existing hosts**, select the agent policy that created earlier.
8. Save and deploy the integration.

    This step takes a minute or two to complete. When it’s done, you’ll have an agent policy that contains the Azure activity logs configuration plus the billing metrics configuration. The deployed {{agent}} will pick up the policy change and start sending Azure activity logs to {{es}}.



## Step 5: Visualize Azure activity logs [azure-elastic-agent-visualize-azure-logs]

Now that logs are streaming into {{es}}, you can visualize them in {{kib}}. To see the raw logs, find **Discover** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Notice that you can filter on a specific data stream. For example, you can use `data_stream.dataset : "azure.activitylogs"` to show Azure activity logs.

The Azure activity logs integration also comes with pre-built dashboards that you can use to visualize the data. In {{kib}}, open the main menu and click **Dashboard**. Search for Azure activity and select the dashboard called **[Logs Azure] User Activity**:

:::{image} /solutions/images/observability-agent-tut-azure-activity-logs-dashboard.png
:alt: Screenshot of Azure activity logs dashboard
:screenshot:
:::

Congratulations! You have completed the tutorial.
