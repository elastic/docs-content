---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-azure.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
---

# Monitor Microsoft Azure with Beats [monitor-azure]

::::{note}
**Are you sure you want to use {{beats}}?**

{{agent}} is the recommended way to monitor Azure if you want to manage your agents centrally in {{fleet}}. To learn how to use {{agent}}, refer to [Monitor Microsoft Azure with {{agent}}](monitor-microsoft-azure-with-elastic-agent.md).

::::


In this tutorial, you’ll learn how to monitor your Microsoft Azure deployments using Elastic {{observability}}: Logs and Infrastructure metrics.


## What you’ll learn [azure-what-you-learn]

You’ll learn how to:

* Create an {{es}} resource in the Azure portal.
* Ingest Azure platform logs using the native integration and view those logs in {{kib}}.
* Ingest logs and metrics from your virtual machines and view those logs and infrastructure metrics in {{kib}}.
* Ingest other metrics (such as billing) using the [{{metricbeat}} Azure module](beats://reference/metricbeat/metricbeat-module-azure.md) and view those metrics in {{kib}}.


## Step 1: Create an {{es}} resource in the Azure portal [azure-step-one]

Microsoft Azure allows you to find, deploy, and manage {{es}} from within the Azure portal. The Microsoft Azure portal integration makes it faster and easier for you to experience the value of Elastic in your Azure environment. Behind the scenes, this process will provision a marketplace subscription with {{ecloud}}.


### Create an {{es}} resource [_create_an_es_resource]

1. Log in to the [Azure portal](https://portal.azure.com/).

    ::::{note}
    Ensure your Azure account is configured with **Owner** access on the subscription you want to deploy {{es}}. To learn more about Azure subscriptions, see the [Microsoft Azure documentation](https://docs.microsoft.com/en-us/azure/cost-management-billing/manage/add-change-subscription-administrator#assign-a-subscription-administrator).

    ::::

2. In the search bar, enter **{{es}}** and then select it.
3. Click **Create**.
4. Enter the **Subscription**, **Resource group**, and the **Resource name**.
5. Select a region and then click **Review + create**.

    ![Create Elastic resource](/solutions/images/observability-monitor-azure-create-elastic-resource.png "")

    ::::{note}
    We will cover **logs** and **infrastructure metrics** later in this tutorial.

    ::::

6. To create the {{es}} deployment, click **Create**.
7. After your deployment is complete, click **Go to resource**. Here you can see and configure your deployment details. To access the cluster, click **{{kib}}**.

    ![Elastic resource](/solutions/images/observability-monitor-azure-elastic-deployment.png "")


1. To single sign-on directly into Elastic, select your Azure account.
2. To see if there is any available data, click **Observability**. There should be no data yet, but next, you will ingest logs.

    ![{{kib}} {{observability}} page (no data)](/solutions/images/observability-monitor-azure-kibana-observability-page-empty.png "")



## Step 2: Ingest logs using the native integration [azure-step-two]

To ingest Azure subscription and resource logs into Elastic using the Microsoft Azure native integration is straightforward.

1. On to the {{es}} resource page in Azure, click **Ingest logs and metrics from Azure Services**.

    ![Click on Ingest logs and metrics from Azure Services](/solutions/images/observability-monitor-azure-elastic-click-ingest-logs.png "")

2. Check both checkboxes and click **Save**.

    ![Elastic configure logs and metrics](/solutions/images/observability-monitor-azure-elastic-config-logs-metrics.png "")

    ::::{note}
    This configuration can also be applied during the Elastic resource creation. To make the concepts clearer, this tutorial separates the two steps.

    ::::


    ::::{note}
    Native metrics collection is not fully supported yet and is discussed later.

    ::::

3. In {{kib}}, find the {{observability}} **Overview** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Refresh the page until you see some data. This may take a few minutes.
4. To analyze your subscription and resource logs, click **Show Logs**.


## Step 3: Ingest logs and metrics from your virtual machines. [azure-step-three]

1. Go to your Elastic resource and click **Virtual machines**.

    ![Elastic resource](/solutions/images/observability-monitor-azure-elastic-deployment.png "")

2. Select the VMs that you want to collect logs and metrics from, click **Install Extension**, and then click **OK**.

    ![Select VMs to collect logs and metrics from](/solutions/images/observability-monitor-azure-elastic-vms.png "")

3. Wait until it is installed and sending data (if the list does not update, click **Refresh** ). To see the logs from the VM, open **Discover** (find `Discover` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md)).

    To view VM metrics, go to **Infrastructure inventory** and then select a VM. (To open **Infrastructure inventory**, find **Infrastructure** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).)


::::{note}
Both logs and metrics are filtered by the VM name that you selected. To view the data for all the monitored VMs, delete the filter.

::::



## Step 4: Ingest other Azure metrics using the {{metricbeat}} Azure module [azure-step-four]

Some Azure metrics are not available via the native integration. If you want to collect those metrics, you need to use the [Azure Monitor REST API](https://docs.microsoft.com/en-us/rest/api/monitor/) and {{metricbeat}}.

The Azure Monitor REST API allows you to get insights into your Azure resources using different operations. To access the Azure Monitor REST API you need to use the Azure Resource Manager authentication model. Therefore, you must authenticate all requests with Azure Active Directory (Azure AD). You can create the service principal using the [Azure portal](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal) or [Azure PowerShell](https://docs.microsoft.com/en-us/powershell/azure/create-azure-service-principal-azureps?view=azps-2.7.0). Then, you need to grant access permission, which is detailed [here](https://docs.microsoft.com/en-us/azure/role-based-access-control/built-in-roles). This tutorial uses the Azure portal.


### Create an Azure service principal [_create_an_azure_service_principal_2]

1. Go to the [Azure Management Portal](https://portal.azure.com/). Search and click on **Azure Active Directory**.

    ![Search and click on Azure Active Directory](/solutions/images/observability-monitor-azure-search-active-directory.png "")

2. Click on **App registrations** in the navigation pane of the selected Active Directory and then click on **New registration**.

    ![Click on App registrations](/solutions/images/observability-monitor-azure-click-app-registration.png "")

3. Type the name of your application (this tutorial uses `monitor-azure`) and click on **Register** (leave all the other options with the default value).

    ![Register an application](/solutions/images/observability-monitor-azure-register-app.png "")

    Copy the **Application (client) ID**, and save it for future reference. This id is required to configure {{metricbeat}} to connect to your Azure account.

4. Click on **Certificates & secrets**. Then, click on **New client secret** to create a new security key.

    ![Click on new client secret](/solutions/images/observability-monitor-azure-click-client-secret.png "")

5. Type a key description and select a key duration in the expire list. Click on **Add** to create a client secret. The next page will display the key value under the **Value** field. Copy the secret and save it (along with your Client ID) for future reference.

    ::::{important}
    This is your only chance to copy this value. You can’t retrieve the key value after you leave the page.

    ::::



### Grant access permission for your service principal [_grant_access_permission_for_your_service_principal_2]

After creating the Azure service principal you need to grant it the correct permission. You need `Reader` permission to configure {{metricbeat}} to monitor your services.

1. On Azure Portal, search and click on **Subscriptions**.

    ![Search and click on Subscriptions](/solutions/images/observability-monitor-azure-search-subscriptions.png "")

2. In the Subscriptions page, click on your subscription.
3. Click on **Access control (IAM)** in the subscription navigation pane.
4. Click on **Add** and select **Add role assignment**.
5. Select the **Reader** role.
6. In the **Select** field, type the description name of the configured service principal (`monitor-azure`).

    ![Add role assignment](/solutions/images/observability-monitor-azure-add-role-assignment.png "")

7. Select the application and click on save to grant the service principal access to your subscription.


### Install and configure {{metricbeat}} [_install_and_configure_metricbeat_2]

To configure {{metricbeat}} you need the {{es}} cluster details.

1. On the {{es}} resource page, click **Manage changes in {{ecloud}}**.

    ![Elastic resource](/solutions/images/observability-monitor-azure-elastic-deployment.png "")

2. Copy the **Cloud ID** and keep it safe. You will use it later.

    ![{{ecloud}} deployment](/solutions/images/observability-monitor-azure-kibana-deployment.png "")

3. Click **Security** and then click **Reset password**. Confirm, and copy the password. Keep it safe as you will use it later.

    ![{{ecloud}} security](/solutions/images/observability-monitor-azure-kibana-security.png "")


You can run {{metricbeat}} on any machine. This tutorial uses a small Azure VM, **B2s** (2 vCPUs, 4 GB memory), with an Ubuntu distribution.


### Install {{metricbeat}} [_install_metricbeat_2]

Download and install {{metricbeat}}.

:::::::{tab-set}

::::::{tab-item} DEB
```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-{{version.stack}}-amd64.deb
sudo dpkg -i metricbeat-{{version.stack}}-amd64.deb
```
::::::

::::::{tab-item} RPM
```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-{{version.stack}}-x86_64.rpm
sudo rpm -vi metricbeat-{{version.stack}}-x86_64.rpm
```
::::::

::::::{tab-item} MacOS
```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-{{version.stack}}-darwin-x86_64.tar.gz
tar xzvf metricbeat-{{version.stack}}-darwin-x86_64.tar.gz
```
::::::

::::::{tab-item} Linux
```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-{{version.stack}}-linux-x86_64.tar.gz
tar xzvf metricbeat-{{version.stack}}-linux-x86_64.tar.gz
```
::::::

::::::{tab-item} Windows
1. Download the [Metricbeat Windows zip file](https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-{{version.stack}}-windows-x86_64.zip).

2. Extract the contents of the zip file into `C:\Program Files`.

3. Rename the _metricbeat-{{version.stack}}-windows-x86\_64_ directory to _Metricbeat_.

4. Open a PowerShell prompt as an Administrator (right-click the PowerShell icon and select *Run As Administrator*).

5. From the PowerShell prompt, run the following commands to install Metricbeat as a Windows service:

  ```shell subs=true
  PS > cd 'C:\Program Files\Metricbeat'
  PS C:\Program Files\Metricbeat> .\install-service-metricbeat.ps1
  ```

```{note}
If script execution is disabled on your system, you need to set the execution policy for the current session to allow the script to run. For example: `PowerShell.exe -ExecutionPolicy UnRestricted -File .\install-service-metricbeat.ps1`.
```
::::::

:::::::

### Set up assets [_set_up_assets_3]

{{metricbeat}} comes with predefined assets for parsing, indexing, and visualizing your data. Run the following command to load these assets. It may take a few minutes.

```bash
./metricbeat setup -e -E 'cloud.id=YOUR_DEPLOYMENT_CLOUD_ID' -E 'cloud.auth=elastic:YOUR_SUPER_SECRET_PASS' <1>
```

1. Substitute your Cloud ID and an administrator’s `username:password` in this command. To find your Cloud ID, click on your [deployment](https://cloud.elastic.co/deployments).


::::{important}
Setting up {{metricbeat}} is an admin-level task that requires extra privileges. As a best practice, [use an administrator role to set up](beats://reference/metricbeat/privileges-to-setup-beats.md), and a more restrictive role for event publishing (which you will do next).

::::



### Configure {{metricbeat}} output [_configure_metricbeat_output_2]

Next, you are going to configure {{metricbeat}} output to {{ecloud}}.

1. Use the {{metricbeat}} keystore to store [secure settings](beats://reference/metricbeat/keystore.md). Store the Cloud ID in the keystore.

    ```bash
    ./metricbeat keystore create
    echo -n "<Your Deployment Cloud ID>" | ./metricbeat keystore add CLOUD_ID --stdin
    ```

2. To store metrics in {{es}} with minimal permissions, create an API key to send data from {{metricbeat}} to {{ecloud}}. Log into {{kib}} (you can do so from the Cloud Console without typing in any permissions) and find `Dev Tools` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). From the **Console**, send the following request:

    ```console
    POST /_security/api_key
    {
      "name": "metricbeat-monitor",
      "role_descriptors": {
        "metricbeat_writer": {
          "cluster": ["monitor", "read_ilm"],
          "index": [
            {
              "names": ["metricbeat-*"],
              "privileges": ["view_index_metadata", "create_doc"]
            }
          ]
        }
      }
    }
    ```

3. The response contains an `api_key` and an `id` field, which can be stored in the {{metricbeat}} keystore in the following format: `id:api_key`.

    ```bash
    echo -n "IhrJJHMB4JmIUAPLuM35:1GbfxhkMT8COBB4JWY3pvQ" | ./metricbeat keystore add ES_API_KEY --stdin
    ```

    ::::{note}
    Make sure you specify the `-n` parameter; otherwise, you will have painful debugging sessions due to adding a newline at the end of your API key.

    ::::

4. To see if both settings have been stored, run the following command:

    ```bash
    ./metricbeat keystore list
    ```

5. To configure {{metricbeat}} to output to {{ecloud}}, edit the `metricbeat.yml` configuration file. Add the following lines to the end of the file.

    ```yaml
    cloud.id: ${CLOUD_ID}
    output.elasticsearch:
      api_key: ${ES_API_KEY}
    ```

6. Finally, test if the configuration is working. If it is not working, verify if you used the right credentials and add them again.

    ```bash
    ./metricbeat test output
    ```


Now that the output is working, you are going to set up the input (Azure).


### Configure {{metricbeat}} Azure module [_configure_metricbeat_azure_module]

To collect metrics from Microsoft Azure, use the [{{metricbeat}} Azure module](beats://reference/metricbeat/metricbeat-module-azure.md). This module periodically fetches monitoring metrics from Microsoft Azure using the [Azure Monitor REST API](https://docs.microsoft.com/en-us/rest/api/monitor/).

::::{warning}
Extra Azure charges on metric queries my be generated by this module. See [additional notes about metrics and costs](beats://reference/metricbeat/metricbeat-module-azure.md#azure-api-cost) for more details.

::::


1. The azure module configuration needs three ids and one secret. Use the commands below to store each one of them in the keystore.

    ```bash
    echo -n "<client_id>" | ./metricbeat keystore add AZURE_CLIENT_ID --stdin
    echo -n "<client_secret>" | ./metricbeat keystore add AZURE_CLIENT_SECRET --stdin
    echo -n "<tenant_id>" | ./metricbeat keystore add AZURE_TENANT_ID --stdin
    echo -n "<subscription_id>" | ./metricbeat keystore add AZURE_SUBSCRIPTION_ID --stdin
    ```

    ::::{note}
    You can find the `tenant_id` in the main Azure Active Directory page. You can find the `subscription_id` in the main Subscriptions page.

    ::::

2. Enable the Azure module.

    ```bash
    ./metricbeat modules enable azure
    ```

3. Edit the `modules.d/azure.yml` file to collect `billing` metrics.

    ```yaml
    - module: azure
      metricsets:
      - billing  <1>
      enabled: true
      period: 24h  <2>
      client_id: '${AZURE_CLIENT_ID:""}'
      client_secret: '${AZURE_CLIENT_SECRET:""}'
      tenant_id: '${AZURE_TENANT_ID:""}'
      subscription_id: '${AZURE_SUBSCRIPTION_ID:""}'
      refresh_list_interval: 600s
    ```

    1. The `billing` metricset is a predefined metricset that collects relevant usage data and forecast information of the subscription configured.
    2. Collects metrics every 24 hours. The period for `billing` metricset should be `24h` or multiples of `24h`.

4. To check if {{metricbeat}} can collect data, test the input by running the following command:

    ```bash
    ./metricbeat test modules azure
    ```

    {{metricbeat}} will print `billing` metrics to the terminal, if the setup is correct.

    ::::{note}
    If it returns a timeout error, try again. The `test modules` timeout is short.

    ::::

5. When the input and output are ready, start {{metricbeat}} to collect the data.

    ```bash
    ./metricbeat -e
    ```

6. Finally, log into {{kib}} and open the **[{{metricbeat}} Azure] Billing overview** dashboard. Keep in mind it collects data every 24 hours.

    ![{{metricbeat}} azure billing overview dashboard](/solutions/images/observability-monitor-azure-billing-overview-dashboard.png "")
