---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-nginx.html
applies_to:
  stack: ga
products:
  - id: observability
---

# Tutorial: Observe your nginx instances [monitor-nginx]

::::{note}
**New to Elastic?** Follow the steps in our [getting started guide](/solutions/observability/get-started/quickstart-monitor-hosts-with-elastic-agent.md) instead of the steps described here. Return to this tutorial after you’ve learned the basics.

::::


Use the [nginx Elastic integration](https://docs.elastic.co/en/integrations/nginx) and the {{agent}} to collect valuable metrics and logs from your nginx instances. Then, use built-in dashboards and tools like Discover to visualize and monitor your nginx data from one place. This data provides valuable insight into your nginx instances—for example:

* A spike in error logs for a certain resource may mean you have a deleted resource that is still needed.
* Access logs can show when a service’s peak times are, and, from this, when it might be best to perform things like maintenance.
* A sudden spike in client requests may point to something malicious, like a DDoS attack.


## What you’ll learn [monitor-nginx-what-youll-learn]

This guide walks you through using Elastic {{observability}} to monitor your nginx instances, including:

* Collecting logs and metrics from nginx instances using an {{agent}} and the nginx integration.
* Centralizing the data in the {{stack}}.
* Exploring the data in real time using tailored dashboards and {{observability}} UIs.


## Data types [monitor-nginx-data-types]

The nginx integration collects both logs and metrics.

**Logs**
:   Collect logs to keep a record of events that happen in your nginx instances like when client requests and errors occur.

    **Access logs** provide information about each request processed by the nginx server. Use these logs for troubleshooting, monitoring performance, and analyzing user behavior.

    **Error logs** provide diagnostic information about errors that occur when the nginx server is handling requests. Use these logs to understand why errors occur, assess error impact, and debug issues.


**Metrics**
:   Collect metrics for insight into the state of your nginx instances. This includes information like the total number of active client connections by status, the total number of client requests, and more. Use these metrics to monitor server load, detect bottlenecks, understand client behavior, and plan for capacity.


## Before you begin [monitor-nginx-prereqs]

Before you can monitor nginx, you need the following:

* {{es}} for storing and searching your observability data
* {{kib}} for visualizing and managing it.
* If you want to collect metrics, make sure your nginx instance is [configured for metric collection](https://docs.nginx.com/nginx-amplify/nginx-amplify-agent/configuring-metric-collection/).


## Step 1: Add the nginx integration [monitor-nginx-add-integration]

Follow these steps to add the nginx integration to your deployment:

1. Find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Enter "nginx" in the search bar, and select the **Nginx** integration.
3. Select **Add Nginx** at the top of the integration page.
4. Select **Add integration only (skip agent installation)** at the bottom of the page.


## Step 2: Configure the nginx integration [monitor-nginx-configure-integration]

The nginx integration can fetch different logs and metrics from your nginx instances. From the **Add Nginx integration** page, configure which logs and metrics you want the integration to collect. Refer to the following sections for more information on configuring the integration.


### Collect logs [monitor-nginx-collect-logs]

The nginx integration can collect access logs and error logs.

* **Access logs:** Turn this option on to collect logs about client requests.
* **Error logs:** Turn this option on to collect logs about issues nginx encounters with varying severity levels.

Configure the following for both access logs and error logs:

**Paths**
:   The location of your logs.

**Preserve original event**
:   Turn on to add a raw copy of the original event to the `event.original` field.


### Collect metrics [monitor-nginx-collect-metrics]

The nginx integration collects `stub_status` metrics from your instances. Make sure your nginx instance is [configured for metric collection](https://docs.nginx.com/nginx-amplify/nginx-amplify-agent/configuring-metric-collection/). Configure the following to collect metrics:

**Hosts**
:   The address of the server that Elastic will connect to for collecting metrics.

**Period**
:   How frequently to poll for metrics. The default is every 10 seconds.


## Step 3: Add {{agent}} [monitor-nginx-add-agent]

After you’ve configured your integration, you need to add an {{agent}} to your host to collect data and send it to the {{stack}}. You have two options for adding the {{agent}}, **enroll in {{fleet}}** or **run standalone**.

[**Fleet**](#monitor-nginx-enroll-in-fleet)
:   Enrolling in {{fleet}} lets you automatically deploy updates and centrally manage the agent.

[**Standalone**](#monitor-nginx-run-standalone)
:   Standalone agents need to be manually updated on the host where the agent is installed.

For more on


### Enroll in {{fleet}} [monitor-nginx-enroll-in-fleet]

Follow the instructions from the **Add agent** screen to install the {{agent}} on your host:

1. Under **Enroll in Fleet?**, make sure **Enroll in Fleet** is selected.
2. Under **Install {{agent}} on your host**, copy the command for your system and run it on your host. You can reuse the command on multiple hosts.
3. After the agent starts on your host, you’ll see confirmation that the agent was enrolled in {{fleet}}.


### Run standalone {{agent}} [monitor-nginx-run-standalone]

Before installing and running the standalone {{agent}}, you need to create an API key. To create an {{ecloud}} API key:

1. To open the **API keys** management page, find it in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Create API key**.
3. Give the key a name. For example, `nginx API key`.
4. Leave the other default options and select **Create API key**.
5. In the **Create API key** confirmation dialog, change the dropdown menu setting from `Encoded` to `Beats`. This sets the API key format for communication between {{agent}} (which is based on {{beats}}) and {{es}}.
6. Copy the generated API key and store it in a safe place.

After creating your API key, follow the instructions from the **Add agent** screen to install the {{agent}} on your host:

1. Under **Enroll in Fleet?**, select **Run standalone**.
2. Under **Configure the agent**, select **Download Policy**. Save the `elastic-agent.yml` file to a directory on the host where you’ll install nginx for monitoring.
3. Open the policy file and notice that it contains all of the input, output, and other settings for the nginx and System integrations.

    Replace:

    ```yaml
        username: '${ES_USERNAME}'
        password: '${ES_PASSWORD}'
    ```

    with:

    ```yaml
        api_key: '<your-api-key>'
    ```

    Where `your-api-key` is the key you created previously in this section.

    If you already have a standalone agent installed on a host with an existing {{agent}} policy, add the settings from the **Configure the agent** step to your existing `elastic-agent.yml` file.

4. Under **Install {{agent}} on your host**, select the tab for your host operating system and run the commands on your host.
5. If you’re prompted with `Elastic Agent will be installed at {installation location} and will run as a service. Do you want to continue?` answer `Yes`.

    If you’re prompted with `Do you want to enroll this Agent into Fleet?` answer `no`.

6. Run the `status` command to confirm that {{agent}} is running.

    ```yaml
    elastic-agent status

    ┌─ fleet
    │  └─ status: (STOPPED) Not enrolled into Fleet
    └─ elastic-agent
       └─ status: (HEALTHY) Running
    ```



## Step 4: Explore your logs and metrics [monitor-nginx-explore-logs-and-metrics]

Use {{kib}} to view the metric and log data collected by {{agent}}. Refer to the following sections for more information on viewing your data:

* [View metrics in {{kib}}](#monitor-nginx-explore-metrics)
* [View logs](#monitor-nginx-explore-logs)


### View metrics in {{kib}} [monitor-nginx-explore-metrics]

The nginx integration has a built-in dashboard that shows the full picture of your nginx metrics in one place. To open the nginx dashboard:

1. Find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Installed integrations**.
3. Select the **Nginx** card and open the **Assets** tab.
4. Select either the `[Metrics Nginx] Overview` dashboard.

The **Metrics Nginx overview** shows visual representations of total requests, processed requests, heartbeat/up, active connections, reading/writing/waiting rates, request rate, accepts and handled rates, and drops rate.

:::{image} /solutions/images/observability-nginx-metrics-dashboard.png
:alt: nginx metrics dashboard
:screenshot:
:::


### View logs [monitor-nginx-explore-logs]

After your nginx logs are ingested, view and explore your logs using [Discover](#monitor-nginx-discover) or the [nginx logs dashboards](#monitor-nginx-logs-dashboard).


#### Discover [monitor-nginx-discover]

With Discover, you can quickly search and filter your log data, get information about the structure of log fields, and display your findings in a visualization.

Find `Discover` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

Filter your results to see logs from the nginx integration from the data selector:

1. From the **Data view** menu, select all logs.

2. Filter the log results using the KQL search bar. Enter `data_stream.dataset : "nginx.error"` to show nginx error logs or `data_stream.dataset : "nginx.access"` to show nginx access logs.

#### nginx logs dashboards [monitor-nginx-logs-dashboard]

The nginx integration has built-in dashboards that show the full picture of your nginx logs in one place. To open the nginx dashboards:

1. Find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Installed integrations**.
3. Select the **Nginx** card and open the **Assets** tab.
4. Select either the `[Logs Nginx] Overview` dashboard or the `[Logs Nginx] Access and error logs` dashboard.

The **Nginx logs overview** dashboard shows visual representations of geographical log details, response codes over time, errors over time, the top pages sending logs, data volume, a breakdown of which operating systems are sending logs, and a breakdown of which browsers are sending logs.

:::{image} /solutions/images/observability-nginx-logs-overview-dashboard.png
:alt: nginx logs overview dashboard
:screenshot:
:::

The **Nginx access and error logs** dashboard shows your access logs over time, and lists your access and error logs.

:::{image} /solutions/images/observability-nginx-logs-access-error-dashboard.png
:alt: nginx access and error logs dashboard
:screenshot:
:::


## Step 5: Find anomalies in your nginx access logs [monitor-nginx-ml]

Use the [nginx Elastic integration](https://docs.elastic.co/en/integrations/nginx) machine learning (ML) module to help find unusual activity in your nginx access logs. Monitoring anomalies in your access logs helps you detect:

* security threats
* network issues
* system performance issues
* operational efficiency issues


### nginx anomaly detection jobs [monitor-nginx-ml-jobs]

The nginx ML module provides the following anomaly detection jobs:

$$$horizontal$$$

Low request rates (`low_request_rate_nginx`)
:   Uses the [`low_count`](/reference/data-analysis/machine-learning/ml-count-functions.md#ml-count) function to detect abnormally low request rates. Abnormally low request rates might indicate that network issues or other issues are preventing requests from reaching the server.

Unusual source IPs - high request rates (`source_ip_request_rate_nginx`)
:   Uses the [`hight_count`](/reference/data-analysis/machine-learning/ml-count-functions.md#ml-count) function to detect abnormally high request rates from individual IP addresses. Many requests from a single IP or small group of IPs might indicate something malicious like a distributed denial of service (DDoS) attack where a large number of requests are sent to overwhelm the server and make it unavailable to users.

Unusual source IPs - high distinct count of URLs (`source_ip_url_count_nginx`)
:   Uses the [`high_distinct_count`](/reference/data-analysis/machine-learning/ml-count-functions.md#ml-distinct-count) function to detect individual IP addresses accessing abnormally high numbers of unique URLs. A single IP accessing many unique URLs might indicate something malicious like web scraping or an attempt to find sensitive data or vulnerabilities.

Unusual status code rates (`status_code_rate_nginx`)
:   Uses the [`count`](/reference/data-analysis/machine-learning/ml-count-functions.md#ml-count) function to detect abnormal error status code rates. A high rate of status codes could indicate problems with broken links, bad URLs, or unauthorized access attempts. A high rate of status codes could also point to server issues like limited resources or bugs in your code.

Unusual visitor rates (`visitor_rate_nginx`)
:   Uses the [`non_zero_count`](/reference/data-analysis/machine-learning/ml-count-functions.md#ml-nonzero-count) function to detect abnormal visitor rates. High visitor rates could indicate something malicious like a DDoS attack. Low visitor rates could indicate issues with access to the server.

::::{note}
These anomaly detection jobs are available when you have data that matches the query specified in the ML module manifest. Users not following this tutorial can refer to [nginx integration ML modules](https://docs.elastic.co/en/integrations/nginx#ml-modules) for more about the ML module manifest.
::::



### Before you begin [monitor-nginx-ml-prereqs]

Verify that your environment is set up properly to use the {{ml-features}}. If {{es}} {{security-features}} are enabled, you need a user with permissions to manage {{anomaly-jobs}}. Refer to [Set up ML features](/explore-analyze/machine-learning/setting-up-machine-learning.md).


### Add nginx ML jobs [monitor-nginx-ml-add-jobs]

Add the nginx ML jobs from the nginx integration to start using anomaly detection:

* To open **Jobs**, find **Machine Learning** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

    1. Select **Create job**.
    2. In the search bar, enter **nginx** and select **Nginx access logs [Logs Nginx]**.
    3. Under **Use preconfigured jobs**, select the **Nginx access logs** card.
    4. Select **Create jobs**.


Back on the **Anomaly Detection Jobs** page, you should see the nginx anomaly detection jobs—`low_request_rate_nginx`, `source_ip_request_rate_nginx`, `source_ip_url_count_nginx`, `status_code_rate_nginx`, and `visitor_rate_nginx`.


### Explore your anomaly detection job results [monitor-nginx-ml-explore]

View your anomaly detection job results using the Anomaly Explorer or Single Metric Viewer found under **Anomaly Detection** in the Machine Learning menu. The Anomaly Explorer shows the results from all or any combination of your nginx ML jobs. The Single Metric Viewer focuses on a specific job. These tools offer a comprehensive view of anomalies and help find patterns and irregularities across data points and time intervals.

Refer to [View anomaly detection job results](/explore-analyze/machine-learning/anomaly-detection/ml-ad-view-results.md) for more on viewing and understanding your anomaly detection job results.


### Set up alerts [monitor-nginx-ml-alert]

With the nginx ML jobs detecting anomalies, you can set rules to generate alerts when your jobs meet specific conditions. For example, you could set up a rule on the `low_request_rate_nginx` job to alert when low request rates hit a specific severity threshold. When you get alerted, you can make sure your server isn’t experiencing issues.

Refer to [Generating alerts for anomaly detection jobs](/explore-analyze/machine-learning/anomaly-detection/ml-configuring-alerts.md) for more on setting these rules and generating alerts.
