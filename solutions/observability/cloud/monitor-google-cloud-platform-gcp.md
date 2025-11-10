---
navigation_title: GCP
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-gcp.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
---



# Monitor Google Cloud Platform (GCP) [monitor-gcp]


In this guide, you’ll learn how to monitor your Google Cloud Platform (GCP) deployments using Elastic {{observability}}: Logs and Infrastructure metrics.

::::{note}
If you don’t want to provision VM and install data shippers due to process and management overhead, you can skip this step and ingest logs directly from Pub/Sub in the Google Cloud Console to Elastic with [GCP Dataflow Templates](gcp-dataflow-templates.md).

::::



## What you’ll learn [_what_youll_learn_2]

You’ll learn how to:

* Set up a GCP Service Account.
* Ingest metrics using the [{{metricbeat}} Google Cloud Platform module](beats://reference/metricbeat/metricbeat-module-gcp.md) and view those metrics in {{kib}}.
* Export GCP audit logs through Pub/Sub topics.
* Ingest logs using the [{{filebeat}} Google Cloud module](beats://reference/filebeat/filebeat-module-gcp.md) and view those logs in {{kib}}.


## Before you begin [_before_you_begin_2]

Create an [{{ech}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body) deployment. The deployment includes an {{es}} cluster for storing and searching your data, and {{kib}} for visualizing and managing your data.


## Step 1: Setup a Service Account [_step_1_setup_a_service_account]

Google Cloud Platform implements [service accounts](https://cloud.google.com/compute/docs/access/service-accounts) as a way to access APIs securely. To monitor GCP with Elastic, you will need a service account. The easiest way is to use a predefined service account that GCP [creates automatically](https://cloud.google.com/compute/docs/access/service-accounts?hl=en#default_service_account). Alternatively, you can create a new service account. This tutorial creates a new one.

First, to access the service account menu, click **Menu** → **IAM & Admin** → **Service Accounts**.

:::{image} /solutions/images/observability-monitor-gcp-service-account-menu.png
:alt: Service account menu
:::

Next, click **Create Service Account**. Define the new service account name (for example, "gcp-monitor") and the description (for example, "Service account to monitor GCP services using the {{stack}}").

:::{image} /solutions/images/observability-monitor-gcp-service-account-name.png
:alt: Service account name
:::

::::{important}
Make sure to select the correct roles.

::::


To monitor GCP services, you need to add these roles to the service account:

**Compute Viewer**:

:::{image} /solutions/images/observability-monitor-gcp-service-account-roles-compute-viewer.png
:alt: Service account roles compute viewer
:::

**Monitoring Viewer**:

:::{image} /solutions/images/observability-monitor-gcp-service-account-roles-monitoring-viewer.png
:alt: Service account roles monitoring viewer
:::

**Pub/Sub Subscriber**:

:::{image} /solutions/images/observability-monitor-gcp-service-account-roles-pubsub-subscriber.png
:alt: Service account roles pub/sub subscriber
:::

The final result should be the following:

:::{image} /solutions/images/observability-monitor-gcp-service-account-roles-final.png
:alt: Service account roles result
:::

Click **Continue**, then skip granting users access to this service. Finally, click **Done**. The service account is now ready to be used.

Next, to use the service account, click **Manage keys**.

:::{image} /solutions/images/observability-monitor-gcp-service-account-manage-keys.png
:alt: Service account manage keys
:::

Then, add a new JSON key type by selecting **Create new key**.

:::{image} /solutions/images/observability-monitor-gcp-service-account-create-key.png
:alt: Service account create key
:::

After that, the credential file is downloaded. Keep this file in an accessible place to use later.


## Step 2: Install and configure {{metricbeat}} [_step_2_install_and_configure_metricbeat]

::::{note}
This tutorial assumes the Elastic cluster is already running. Make sure you have your **cloud ID** and your **credentials** on hand.

::::


To monitor GCP using the {{stack}}, you need two main components: an Elastic deployment to store and analyze the data and an agent to collect and ship the data.

Two agents can be used to monitor GCP: {{metricbeat}} is used to monitor metrics, and {{filebeat}} to monitor logs. You can run the agents on any machine. This tutorial uses a small GCP instance, e2-small (2 vCPUs, 2 GB memory), with an Ubuntu distribution.


### Install {{metricbeat}} [_install_metricbeat_3]

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

3. Rename the `metricbeat-[version]-windows-x86_64` directory to `Metricbeat`.

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

### Set up assets [_set_up_assets_4]

{{metricbeat}} comes with predefined assets for parsing, indexing, and visualizing your data. Run the following command to load these assets. It may take a few minutes.

```bash
./metricbeat setup -e -E 'cloud.id=YOUR_DEPLOYMENT_CLOUD_ID' -E 'cloud.auth=elastic:YOUR_SUPER_SECRET_PASS' <1>
```

1. Substitute your Cloud ID and an administrator’s `username:password` in this command. To find your Cloud ID, click on your [deployment](https://cloud.elastic.co/deployments).


::::{important}
Setting up {{metricbeat}} is an admin-level task that requires extra privileges. As a best practice, [use an administrator role to set up](beats://reference/metricbeat/privileges-to-setup-beats.md), and a more restrictive role for event publishing (which you will do next).

::::



### Configure {{metricbeat}} output [_configure_metricbeat_output_3]

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


Now that the output is working, you are going to set up the input (GCP).


## Step 3: Configure {{metricbeat}} Google Cloud Platform module [_step_3_configure_metricbeat_google_cloud_platform_module]

To collect metrics from Google Cloud Platform, use the [Google Cloud Platform](beats://reference/metricbeat/metricbeat-module-gcp.md) module. This module periodically fetches monitoring metrics from Google Cloud Platform using [Stackdriver Monitoring API](https://cloud.google.com/monitoring/api/metrics_gcp) for Google Cloud Platform services.

::::{warning}
Extra GCP charges on Stackdriver Monitoring API requests may be generated by this module. See [rough estimation of the number of API calls](beats://reference/metricbeat/metricbeat-module-gcp.md#gcp-api-requests) for more details.

::::


1. Enable the GCP module.

    ```bash
    ./metricbeat modules enable gcp
    ```

2. Edit the `modules.d/gcp.yml` file to configure which metrics to collect.

    ```yaml
    - module: gcp
      metricsets:
        - compute <1>
      zone: "" <2>
      project_id: "your-project-id" <3>
      period: 1m <4>
      credentials_file_path: "/home/ubuntu/credentials.json" <5>
    ```

    1. The `compute` metricset is a predefined metricset that collects some GCP compute metrics.
    2. Defines which zones to monitor, an empty value collects data from **all** zones
    3. Collects metrics within the `your-project-id` project-id.
    4. Collects metrics every minute
    5. The GCP credential file that you generated earlier. (Don’t forget to create the file if it does not exist and use the correct full path).

3. To check if {{metricbeat}} can collect data, test the input by running the following command:

    ```bash
    ./metricbeat test modules gcp
    ```

    {{metricbeat}} will print GCP metrics to the terminal, if the setup is correct.

4. When the input and output are ready, start {{metricbeat}} to collect the data.

    ```bash
    ./metricbeat -e
    ```

5. Finally, log into {{kib}} and open the **[{{metricbeat}} GCP] Compute Overview** dashboard.

    ![{{metricbeat}} compute overview dashboard](/solutions/images/observability-monitor-gcp-compute-overview-dashboard.png "")



## Step 4: Install and configure {{filebeat}} [_step_4_install_and_configure_filebeat]

Now that {{metricbeat}} is up and running, configure {{filebeat}} to collect Google Cloud logs.


#### Install {{filebeat}} [_install_filebeat_2]

Download and install {{filebeat}}.

:::::::{tab-set}

::::::{tab-item} DEB
```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-{{version.stack}}-amd64.deb
sudo dpkg -i filebeat-{{version.stack}}-amd64.deb
```
::::::

::::::{tab-item} RPM
```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-{{version.stack}}-x86_64.rpm
sudo rpm -vi filebeat-{{version.stack}}-x86_64.rpm
```
::::::

::::::{tab-item} MacOS
```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-{{version.stack}}-darwin-x86_64.tar.gz
tar xzvf filebeat-{{version.stack}}-darwin-x86_64.tar.gz
```
::::::

::::::{tab-item} Linux
```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-{{version.stack}}-linux-x86_64.tar.gz
tar xzvf filebeat-{{version.stack}}-linux-x86_64.tar.gz
```
::::::

::::::{tab-item} Windows
1. Download the [Filebeat Windows zip file](https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-{{version.stack}}-windows-x86_64.zip).

2. Extract the contents of the zip file into `C:\Program Files`.

3. Rename the `filebeat-[stack-version]-windows-x86_64` directory to `Filebeat`.

4. Open a PowerShell prompt as an Administrator (right-click the PowerShell icon and select *Run As Administrator*).

5. From the PowerShell prompt, run the following commands to install Filebeat as a Windows service:

  ```shell subs=true
  PS > cd 'C:\Program Files\Filebeat'
  PS C:\Program Files\Filebeat> .\install-service-filebeat.ps1
  ```

```{note}
If script execution is disabled on your system, you need to set the execution policy for the current session to allow the script to run. For example: `PowerShell.exe -ExecutionPolicy UnRestricted -File .\install-service-filebeat.ps1`.
```
::::::

:::::::

#### Set up assets [_set_up_assets_5]

{{filebeat}} comes with predefined assets for parsing, indexing, and visualizing your data. Run the following command to load these assets. It may take a few minutes.

```bash
./filebeat setup -e -E 'cloud.id=YOUR_DEPLOYMENT_CLOUD_ID' -E 'cloud.auth=elastic:YOUR_SUPER_SECRET_PASS' <1>
```

1. Substitute your Cloud ID and an administrator’s `username:password` in this command. To find your Cloud ID, click on your [deployment](https://cloud.elastic.co/deployments).


::::{important}
Setting up {{filebeat}} is an admin-level task that requires extra privileges. As a best practice, [use an administrator role to set up](beats://reference/filebeat/privileges-to-setup-beats.md) and a more restrictive role for event publishing (which you will do next).

::::



#### Configure {{filebeat}} output [_configure_filebeat_output_2]

Next, you are going to configure {{filebeat}} output to {{ecloud}}.

1. Use the {{filebeat}} keystore to store [secure settings](beats://reference/filebeat/keystore.md). Store the Cloud ID in the keystore.

    ```bash
    ./filebeat keystore create
    echo -n "<Your Deployment Cloud ID>" | ./filebeat keystore add CLOUD_ID --stdin
    ```

2. To store logs in {{es}} with minimal permissions, create an API key to send data from {{filebeat}} to {{ecloud}}. Log into {{kib}} (you can do so from the Cloud Console without typing in any permissions) and find `Dev Tools` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Send the following request:

    ```console
    POST /_security/api_key
    {
      "name": "filebeat-monitor-gcp",
      "role_descriptors": {
        "filebeat_writer": {
          "cluster": [
            "monitor",
            "read_ilm",
            "cluster:admin/ingest/pipeline/get", <1>
            "cluster:admin/ingest/pipeline/put" <1>
          ],
          "index": [
            {
              "names": ["filebeat-*"],
              "privileges": ["view_index_metadata", "create_doc"]
            }
          ]
        }
      }
    }
    ```

    1. {{filebeat}} needs extra cluster permissions to publish logs, which differs from the {{metricbeat}} configuration. You can find more details [here](beats://reference/filebeat/feature-roles.md).

3. The response contains an `api_key` and an `id` field, which can be stored in the {{filebeat}} keystore in the following format: `id:api_key`.

    ```bash
    echo -n "IhrJJHMB4JmIUAPLuM35:1GbfxhkMT8COBB4JWY3pvQ" | ./filebeat keystore add ES_API_KEY --stdin
    ```

    ::::{note}
    Make sure you specify the `-n` parameter; otherwise, you will have painful debugging sessions due to adding a newline at the end of your API key.

    ::::

4. To see if both settings have been stored, run the following command:

    ```bash
    ./filebeat keystore list
    ```

5. To configure {{filebeat}} to output to {{ecloud}}, edit the `filebeat.yml` configuration file. Add the following lines to the end of the file.

    ```yaml
    cloud.id: ${CLOUD_ID}
    output.elasticsearch:
      api_key: ${ES_API_KEY}
    ```

6. Finally, test if the configuration is working. If it is not working, verify that you used the right credentials and, if necessary, add them again.

    ```bash
    ./filebeat test output
    ```


Now that the output is working, you are going to set up the input (GCP).


## Step 5: Configure {{filebeat}} Google Cloud module [_step_5_configure_filebeat_google_cloud_module]

To collect logs from Google Cloud Platform, use the [Google Cloud Platform](beats://reference/filebeat/filebeat-module-gcp.md) module. This module periodically fetches logs that have been exported from Stackdriver to a Google Pub/Sub topic sink. There are three available filesets: `audit`, `vpcflow`, `firewall`. This tutorial covers the `audit` fileset.

1. Go to the **Logs Router** page to configure GCP to export logs to a Pub/Sub topic. Use the search bar to find the page:

    :::{image} /solutions/images/observability-monitor-gcp-navigate-logs-router.png
    :alt: Navigate to Logs Router page
    :::

    To set up the logs routing sink, click  **Create sink**. Set **sink name** as `monitor-gcp-audit-sink`. Select the **Cloud Pub/Sub topic** as the **sink service** and **Create new Cloud Pub/Sub topic** named `monitor-gcp-audit`:

    :::{image} /solutions/images/observability-monitor-gcp-create-pubsub-topic.png
    :alt: Create Pub/Sub topic
    :::

    Finally, under **Choose logs to include in sink**, add `logName:"cloudaudit.googleapis.com"` (it includes all audit logs). Click **create sink**.  It will look something like the following:

    :::{image} /solutions/images/observability-monitor-gcp-create-sink.png
    :alt: Create logs routing sink
    :::

2. Now go to the **Pub/Sub** page to add a subscription to the topic you just created. Use the search bar to find the page:

    :::{image} /solutions/images/observability-monitor-gcp-pub-sub.png
    :alt: GCP Pub/Sub
    :::

    To add a subscription to the `monitor-gcp-audit` topic click **Create subscription**:

    :::{image} /solutions/images/observability-monitor-gcp-pub-sub-create-subscription.png
    :alt: Create GCP Pub/Sub Subscription
    :::

    Set `monitor-gcp-audit-sub` as the **Subscription ID** and leave the **Delivery type** as pull:

    :::{image} /solutions/images/observability-monitor-gcp-pub-sub-subscription-id.png
    :alt: GCP Pub/Sub Subscription ID
    :::

    Finally, scroll down and click **Create**.

3. Now that GCP is configured to export audit logs, enable {{filebeat}} Google Cloud module.

    ```bash
    ./filebeat modules enable gcp
    ```

4. Edit the `modules.d/gcp.yml` file with the following configurations.

    ```yaml
    - module: gcp
      vpcflow:
        enabled: false <1>
      firewall:
        enabled: false <1>
      audit:
        enabled: true <2>
        var.project_id: "elastic-education" <3>
        var.topic: "monitor-gcp-audit" <4>
        var.subscription_name: "monitor-gcp-audit-sub" <5>
        var.credentials_file: "/home/ubuntu/credentials.json" <6>
    ```

    1. Disables both `vpcflow` and `firewall` filesets.
    2. Enables the `audit` fileset.
    3. Collects data within the `elastic-education` project-id.
    4. Collects logs from the `monitor-gcp-audit` topic.
    5. Google Cloud Pub/Sub topic subscription name.
    6. The GCP credential file that you generated earlier. (Don’t forget to create the file if it does not exist and to use the correct full path).

5. Start {{filebeat}} to collect the logs.

    ```bash
    ./filebeat -e
    ```

6. Finally, log into {{kib}} and open the **[{{filebeat}} GCP] Audit** dashboard.

    :::{image} /solutions/images/observability-monitor-gcp-audit-overview-dashboard.png
    :alt: {{filebeat}} audit overview dashboard
    :::
