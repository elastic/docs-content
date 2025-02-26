---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/example-standalone-monitor-nginx-serverless.html
---

# Example: Use standalone Elastic Agent with Elastic Cloud Serverless to monitor nginx [example-standalone-monitor-nginx-serverless]

This guide walks you through a simple monitoring scenario so you can learn the basics of setting up standalone {{agent}}, using it to work with {{serverless-full}} and an Elastic integration.

Following these steps, you’ll deploy the {{stack}}, install a standalone {{agent}} on a host to monitor an nginx web server instance, and access visualizations based on the collected logs.

1. [Install nginx](#nginx-guide-install-nginx-serverless).
2. [Create an {{serverless-full}} project](#nginx-guide-sign-up-serverless).
3. [Create an API key](#nginx-guide-create-api-key-serverless).
4. [Create an {{agent}} policy](#nginx-guide-create-policy-serverless).
5. [Add the Nginx Integration](#nginx-guide-add-integration-serverless).
6. [Configure standalone {{agent}}](#nginx-guide-configure-standalone-agent-serverless).
7. [Confirm that your {{agent}} data is flowing](#nginx-guide-confirm-agent-data-serverless).
8. [View your system data](#nginx-guide-view-system-data-serverless).
9. [View your nginx logging data](#nginx-guide-view-nginx-data-serverless).


## Prerequisites [nginx-guide-prereqs-serverless]

To get started, you need:

1. An internet connection and an email address for your {{ecloud}} trial.
2. A Linux host machine on which you’ll install an nginx web server. The commands in this guide use an Ubuntu image but any Linux distribution should be fine.


## Step 1: Install nginx [nginx-guide-install-nginx-serverless]

To start, we’ll set up a basic [nginx web server](https://docs.nginx.com/nginx/admin-guide/web-server/).

1. Run the following command on an Ubuntu Linux host, or refer to the [nginx install documentation](https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/) for the command appropriate to your operating system.

    ```sh
    sudo apt install nginx
    ```

2. Open a web browser and visit your host machine’s external URL, for example `http://192.168.64.17/`. You should see the nginx welcome message.

    :::{image} images/guide-nginx-welcome.png
    :alt: Browser window showing Welcome to nginx!
    :class: screenshot
    :::



## Step 2: Create an {{serverless-full}} project [nginx-guide-sign-up-serverless]

::::{note}
If you’ve already signed up for a trial deployment you can skip this step.
::::


Now that your web server is running, let’s get set up to monitor it in {{ecloud}}. An {{ecloud}} {{serverless-short}} project offers you all of the features of the {{stack}} as a hosted service. To test drive your first deployment, sign up for a free {{ecloud}} trial:

1. Go to our [{{ecloud}} Trial](https://cloud.elastic.co/registration?elektra=guide-welcome-cta) page.
2. Enter your email address and a password.

    :::{image} images/guide-sign-up-trial.png
    :alt: Start your free Elastic Cloud trial
    :class: screenshot
    :::

3. After you’ve [logged in](https://cloud.elastic.co/login), select **Create project**.
4. On the **Observability** tab, select **Next**. The **Observability** and **Security** projects both include {{fleet}}, which you can use to create a policy for the {{agent}} that will monitor your nginx installation.
5. Give your project a name. You can leave the default options or select a different cloud provider and region.
6. Select **Create project**, and then wait a few minutes for the new project to set up.
7. Once the project is ready, select **Continue**. At this point, you access {{kib}} and a selection of setup guides.


## Step 3: Create an {{es}} API key [nginx-guide-create-api-key-serverless]

1. When your {{serverless-short}} project is ready, open the {{kib}} menu and go to **Project settings** → **Management → API keys**.
2. Select **Create API key**.
3. Give the key a name, for example `nginx example API key`.
4. Leave the other default options and select **Create API key**.
5. In the **Create API key** confirmation dialog, change the dropdown menu setting from `Encoded` to `Beats`. This sets the API key to the format used for communication between {{agent}} and {{es}}.
6. Copy the generated API key and store it in a safe place. You’ll use it in a later step.


## Step 4: Create an {{agent}} policy [nginx-guide-create-policy-serverless]

{{agent}} is a single, unified way to add monitoring for logs, metrics, and other types of data to a host. It can also protect hosts from security threats, query data from operating systems, and more. A single agent makes it easy and fast to deploy monitoring across your infrastructure. Each agent has a single policy (a collection of input settings) that you can update to add integrations for new data sources, security protections, and more.

1. Open the {{kib}} menu and go to **Project settings** → **{{fleet}} → Agent policies**.

    :::{image} images/guide-agent-policies.png
    :alt: Agent policies tab in Fleet
    :::

2. Click **Create agent policy**.
3. Give your policy a name. For this example we’ll call it `nginx-policy`.
4. Leave **Collect system logs and metrics** selected.
5. Click **Create agent policy**.

    :::{image} images/guide-create-agent-policy.png
    :alt: Create agent policy UI
    :::



## Step 5: Add the Nginx Integration [nginx-guide-add-integration-serverless]

Elastic integrations are a streamlined way to connect your data from popular services and platforms to the {{stack}}, including nginx.

1. From the **{{fleet}} → Agent policies** tab, click the link for your new `nginx-policy`.

    :::{image} images/guide-nginx-policy.png
    :alt: The nginx-policy UI with integrations tab selected
    :::

2. Note that the System integration (`system-1`) is included because you opted earlier to collect system logs and metrics.
3. Click **Add integration**.
4. On the Integrations page search for "nginx".

    :::{image} images/guide-integrations-page.png
    :alt: Integrations page with nginx in the search bar
    :::

5. Select the **Nginx** card.
6. Click **Add Nginx**.
7. Click the link to **Add integration only (skip agent installation)**. You’ll install standalone {{agent}} in a later step.
8. Here, you can select options such as the paths to where your nginx logs are stored, whether or not to collect metrics data, and various other settings.

    For now, leave all of the default settings and click **Save and continue** to add the Nginx integration to your `nginx-policy` policy.

    :::{image} images/guide-add-nginx-integration.png
    :alt: Add Nginx Integration UI
    :::

9. In the confirmation dialog, select to **Add {{agent}} later**.

    :::{image} images/guide-nginx-integration-added.png
    :alt: Nginx Integration added confirmation UI with Add {{agent}} later selected.
    :::



## Step 6: Configure standalone {{agent}} [nginx-guide-configure-standalone-agent-serverless]

Rather than opt for {{fleet}} to centrally manage {{agent}}, you’ll configure an agent to run in standalone mode, so it will be managed by hand.

1. Open the {{kib}} menu and go to **{{fleet}} → Agents** and click **Add agent**.
2. For the **What type of host are you adding?** step, select `nginx-policy` from the drop-down menu if it’s not already selected.
3. For the **Enroll in {{fleet}}?** step, select **Run standalone**.

    :::{image} images/guide-add-agent-standalone01.png
    :alt: Add agent UI with nginx-policy and Run-standalone selected.
    :::

4. For the **Configure the agent** step, choose **Download Policy**. Save the `elastic-agent.yml` file to a directory on the host where you’ll install nginx for monitoring.

    Have a look inside the policy file and notice that it contains all of the input, output, and other settings for the Nginx and System integrations. If you already have a standalone agent installed on a host with an existing {{agent}} policy, you can use the method described here to add a new integration. Just add the settings from the **Configure the agent** step to your existing `elastic-agent.yml` file.

5. For the **Install {{agent}} on your host** step, select the tab for your host operating system and run the commands on your host.

    :::{image} images/guide-install-agent-on-host.png
    :alt: Install {{agent}} on your host step, showing tabs with the commands for different operating systems.
    :::

    ::::{note}
    {{agent}} commands should be run as `root`. You can prefix each agent command with `sudo` or you can start a new shell as `root` by running `sudo su`. If you need to run {{agent}} commands without `root` access, refer to [Run {{agent}} without administrative privileges](/reference/ingestion-tools/fleet/elastic-agent-unprivileged.md).

    ::::


    If you’re prompted with `Elastic Agent will be installed at {installation location} and will run as a service. Do you want to continue?` answer `Yes`.

    If you’re prompted with `Do you want to enroll this Agent into Fleet?` answer `no`.

6. You can run the `status` command to confirm that {{agent}} is running.

    ```cmd
    elastic-agent status

    ┌─ fleet
    │  └─ status: (STOPPED) Not enrolled into Fleet
    └─ elastic-agent
       └─ status: (HEALTHY) Running
    ```

    Since you’re running the agent in standalone mode the `Not enrolled into Fleet` message is expected.

7. Open the `elastic-agent.yml` policy file that you saved.
8. Near the top of the file, replace:

    ```yaml
        username: '${ES_USERNAME}'
        password: '${ES_PASSWORD}'
    ```

    with:

    ```yaml
        api_key: '<your-api-key>'
    ```

    where `your-api-key` is the API key that you generated in [Step 3: Create an {{es}} API key](#nginx-guide-create-api-key-serverless).

9. Find the location of the default `elastic-agent.yml` policy file that is included in your {{agent}} install. Install directories for each platform are described in [Installation layout](/reference/ingestion-tools/fleet/installation-layout.md). In our example Ubuntu image the default policy file can be found in `/etc/elastic-agent/elastic-agent.yml`.
10. Replace the default policy file with the version that you downloaded and updated. For example:

    ```sh
    cp /home/ubuntu/homedir/downloads/elastic-agent.yml /etc/elastic-agent/elastic-agent.yml
    ```

    ::::{note}
    You may need to prefix the `cp` command with `sudo` for the permission required to replace the default file.
    ::::


    By default, {{agent}} monitors the configuration file and reloads the configuration automatically when `elastic-agent.yml` is updated.

11. Run the `status` command again, this time with the `--output yaml` option which provides structured and much more detailed output. See the [`elastic-agent status`](/reference/ingestion-tools/fleet/agent-command-reference.md#elastic-agent-status-command) command documentation for more details.

    ```shell
    elastic-agent status --output yaml
    ```

    The results show you the agent status together with details about the running components, which correspond to the inputs and outputs defined for the integrations that have been added to the {{agent}} policy, in this case the System and Nginx Integrations.

12. At the top of the command output, the `info` section contains details about the agent instance. Make a note of the agent ID. In this example the ID is `4779b439-1130-4841-a878-e3d7d1a457d0`. You’ll use that ID in the next section.

    ```yaml
    elastic-agent status --output yaml

    info:
      id: 4779b439-1130-4841-a878-e3d7d1a457d0
      version: 8.9.1
      commit: 5640f50143410fe33b292c9f8b584117c7c8f188
      build_time: 2023-08-10 17:04:04 +0000 UTC
      snapshot: false
    state: 2
    message: Running
    ```



## Step 7: Confirm that your {{agent}} data is flowing [nginx-guide-confirm-agent-data-serverless]

Now that {{agent}} is running, it’s time to confirm that the agent data is flowing into {{es}}.

1. Check that {{agent}} logs are flowing.

    1. Open the {{kib}} menu and go to **Observability → Discover**.
    2. In the KQL query bar, enter the query `agent.id : "{{agent-id}}"` where `{{agent-id}}` is the ID you retrieved from the `elastic-agent status --output yaml` command. For example: `agent.id : "4779b439-1130-4841-a878-e3d7d1a457d0"`.

        If {{agent}} has connected successfully with your {{ecloud}} deployment, the agent logs should be flowing into {{es}} and visible in {{kib}} Discover.

        :::{image} images/guide-agent-logs-flowing.png
        :alt: Kibana Discover shows agent logs are flowing into Elasticsearch.
        :::

2. Check that {{agent}} metrics are flowing.

    1. Open the {{kib}} menu and go to **Observability → Dashboards**.
    2. In the search field, search for `Elastic Agent` and select `[Elastic Agent] Agent metrics` in the results.

        like the agent logs, the agent metrics should be flowing into {{es}} and visible in {{kib}} Dashboard. You can view metrics on CPU usage, memory usage, open handles, events rate, and more.

        :::{image} images/guide-agent-metrics-flowing.png
        :alt: Kibana Dashboard shows agent metrics are flowing into Elasticsearch.
        :::



## Step 8: View your system data [nginx-guide-view-system-data-serverless]

In the step to [create an {{agent}} policy](#nginx-guide-create-policy-serverless) you chose to collect system logs and metrics, so you can access those now.

1. View your system logs.

    1. Open the {{kib}} menu and go to **Project settings → Integrations → Installed integrations**.
    2. Select the **System** card and open the **Assets** tab. This is a quick way to access all of the dashboards, saved searches, and visualizations that come with each integration.
    3. Select `[Logs System] Syslog dashboard`.
    4. Select the calandar icon and change the time setting to `Today`. The {{kib}} Dashboard shows visualizations of Syslog events, hostnames and processes, and more.

2. View your system metrics.

    1. Return to **Project settings → Integrations → Installed integrations**.
    2. Select the **System** card and open the **Assets** tab.
    3. This time, select `[Metrics System] Host overview`.
    4. Select the calandar icon and change the time setting to `Today`. The {{kib}} Dashboard shows visualizations of host metrics including CPU usage, memory usage, running processes, and others.

        :::{image} images/guide-system-metrics-dashboard.png
        :alt: The System metrics host overview showing CPU usage, memory usage, and other visualizations
        :::



## Step 9: View your nginx logging data [nginx-guide-view-nginx-data-serverless]

Now let’s view your nginx logging data.

1. Open the {{kib}} menu and go to **Project settings → Integrations → Installed integrations**.
2. Select the **Nginx** card and open the **Assets** tab.
3. Select `[Logs Nginx] Overview`. The {{kib}} Dashboard opens with geographical log details, response codes and errors over time, top pages, and more.
4. Refresh your nginx web page several times to update the logging data. You can also try accessing the nginx page from different web browsers. After a minute or so, the `Browsers breakdown` visualization shows the respective volume of requests from the different browser types.

    :::{image} images/guide-nginx-browser-breakdown.png
    :alt: Kibana Dashboard shows agent metrics are flowing into Elasticsearch.
    :::


Congratulations! You have successfully set up monitoring for nginx using standalone {{agent}} and an {{serverless-full}} project.


## What’s next? [_whats_next]

* Learn more about [{{fleet}} and {{agent}}](/reference/ingestion-tools/fleet/index.md).
* Learn more about [{{integrations}}](integration-docs://docs/reference/index.md).
