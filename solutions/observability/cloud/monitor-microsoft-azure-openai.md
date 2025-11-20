---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-azure-openai.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
---

# Monitor Microsoft Azure OpenAI [monitor-azure-openai]

::::{note}
**New to Elastic?** Refer to our [getting started guide](/solutions/observability/get-started/quickstart-monitor-hosts-with-elastic-agent.md) instead of the steps described here. Return to this tutorial after you’ve learned the basics.

::::


This tutorial shows you how to use the Elastic Azure OpenAI integration, the Azure portal, and {{agent}} to collect and monitor Azure OpenAI logs and metrics with Elastic {{observability}}.


## What you’ll learn [azure-openai-what-you-learn]

You’ll learn how to:

* Set up your Azure instance to allow the Azure OpenAI integration to collect logs and metrics.
* Configure the Azure OpenAI integration to collect logs and metrics.
* Install {{agent}} on your host.
* View your logs and metrics in {{kib}} using built-in dashboards and Discover.


## Step 1: Set up Azure to collect logs [azure-openai-set-up-logs]

The Elastic Azure OpenAI integration captures audit logs and request and response logs.

* Audit logs provide a range of information related to the use and management of Azure OpenAI services.
* Request and response logs provide information about each request made to the service and the corresponding response provided by the service.

For more on the fields ingested from audit and request and response logs, refer to the [Azure OpenAI integration](https://docs.elastic.co/en/integrations/azure_openai#settings) documentation.

Before {{agent}} can collect your logs and send them to {{kib}}, complete the following steps in the [Azure portal](https://portal.azure.com/):

1. Create an event hub to receive logs exported from the Azure service and make them available to the {{agent}}.
2. Configure diagnostic settings to send your logs to the event hub.
3. Create a storage account container where the {{agent}} can store consumer group information.


### Create an event hub [azure-openai-event-hub]

[Azure Event Hubs](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-about) is a data streaming platform and event ingestion service that you use to store in-flight Azure logs before sending them to {{es}}. For this tutorial, you create a single event hub because you are collecting logs from one service.

To create an Azure event hub:

1. Go to the [Azure portal](https://portal.azure.com/).
2. Search for and select **Event Hubs**.
3. Click **Create** and create a new Event Hubs namespace. You’ll need to create a new resource group, or choose an existing one.
4. Enter the required settings for the namespace and click **Review + create**.
5. Click **Create** to deploy the resource.
6. In the new namespace, click **+ Event Hub** and enter a name for the event hub.
7. Click **Review + create**, and then click **Create** to deploy the resource.
8. Make a note of the event hub name because you’ll use it to configure your integration settings in [Step 3: Configure the Azure OpenAI integration](#azure-openai-configure-integration).


### Configure diagnostic settings [azure-openai-diagnostic-settings]

Every Azure service that creates logs has diagnostic settings that allow you to export logs and metrics to an external destination. In this step, you’ll configure the Azure OpenAI service to export audit and request and response logs to the event hub you created in the previous step.

To configure diagnostic settings to export logs:

1. Go to the [Azure portal](https://portal.azure.com/) and open your OpenAI resource.
2. In the navigation pane, select **Diagnostic settings** → **Add diagnostic setting**.
3. Enter a name for the diagnostic setting.
4. In the list of log categories, select **Audit logs** and **Request and Response Logs**.
5. Under Destination details, select **Stream to an event hub** and select the namespace and event hub you created in [Create an event hub](#azure-openai-event-hub).
6. Save the diagnostic settings.


### Create a storage account container [azure-openai-storage-account-container]

The {{agent}} stores the consumer group information (state, position, or offset) in a storage account container. Making this information available to {{agent}}s allows them to share the logs processing and resume from the last processed logs after a restart. The {{agent}} can use one storage account container for all integrations. The agent uses the integration name and the event hub name to identify the blob to store the consumer group information uniquely.

To create the storage account:

1. Go to the [Azure portal](https://portal.azure.com/) and select **Storage accounts**.
2. Select **Create storage account**.
3. Under **Advanced**, make sure these settings are as follows:

    * **Hierarchical namespace**: disabled
    * **Minimum TLS version**: Version 1.2
    * **Access tier**: Hot

4. Under **Data protections**, make sure these settings are as follows:

    * **Enable soft delete for blobs**: disabled
    * **Enable soft delete for containers**: disabled

5. Click **Review + create**, and then click **Create**.
6. Make note of the storage account name and the storage account access keys because you’ll use them later to authenticate your Elastic application’s requests to this storage account in [Step 3: Configure the Azure OpenAI integration](#azure-openai-configure-integration).


## Step 2: Set up Azure to collect metrics [azure-openai-set-up-metrics]

The Azure OpenAI integration metric data stream collects the cognitive service metrics specific to the Azure OpenAI service. Before {{agent}} can collect your metrics and send them to {{kib}}, it needs an app registration to access Azure on your behalf and collect data using the Azure APIs.

Complete the following steps in your Azure instance to register a new Azure app:

1. Create the app registration.
2. Add credentials to the app.
3. Add role assignment to your app.


### Create an app registration [azure-openai-create-app]

To register your app:

1. Go to the [Azure portal](https://portal.azure.com/).
2. Search for and select **Microsoft Entra ID**.
3. Under **Manage**, select **App registrations** → **New registration**.
4. Enter a display name for your app (for example, `elastic-agent`).
5. Specify who can use the app.
6. The {{agent}} doesn’t use a redirect URI, so you can leave this field blank.
7. Click **Register**.
8. Make note of the **Application (client) ID** because you’ll use it to specify the **Client ID** in the integration settings in [Step 3: Configure the Azure OpenAI integration](#azure-openai-configure-integration).


### Create credentials and add them to your app [azure-openai-app-credentials]

Credentials allow your app to access Azure APIs and authenticate itself, so you won’t need to do anything at runtime. The Elastic Azure OpenAI integration uses client secrets to authenticate.

To create and add client secrets:

1. From the [Azure portal](https://portal.azure.com/), select the app you created in the previous section.
2. Select **Certificates & secrets** → **Client secrets** → **New client secret**.
3. Add a description (for example, "{{agent}} client secrets").
4. Select an expiration or specify a custom lifetime.
5. Select **Add**.
6. Make note of the **Value** in the **Client secrets** table because you’ll use it to specify the **Client Secret** in [Step 3: Configure the Azure OpenAI integration](#azure-openai-configure-integration).

    ::::{warning}
    The secret value is not viewable after you leave this page. Record the value in a safe place.
    ::::



### Add role assignment to your app [azure-openai-app-role-assignment]

To add a role assignment to your app:

1. From the [Azure portal](https://portal.azure.com/), search for and select **Subscriptions**.
2. Select the subscription to assign the app.
3. Select **Access control (IAM)**.
4. Select **Add** → **Add role assignment**.
5. In the **Role** tab, search for and select **Monitoring Reader**.
6. Click **Next** to open the **Members** tab.
7. Select **Assign access to** → **User, group, or service principal**, and select **Select members**.
8. Search for and select your app name (for example, "elastic-agent").
9. Click **Select**.
10. Click **Review + assign**.
11. Make note of the **Subscription ID** and **Tenant ID** from your Microsoft Entra because you’ll use these to specify settings in the integration.


## Step 3: Configure the Azure OpenAI integration [azure-openai-configure-integration]

1. Find **Integrations** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the query bar, search for **Azure OpenAI** and select the Azure OpenAI integration card.
3. Click **Add Azure OpenAI**.
4. Under Integration settings, configure the integration name and optionally add a description.

    ::::{tip}
    If you don’t have options for configuring the integration, you’re probably in a workflow designed for new deployments. Follow the steps, then return to this tutorial when you’re ready to configure the integration.
    ::::



### Configure logs collection [azure-openai-configure-integration-logs]

To collect Azure OpenAI logs, specify values for the following required fields:

**Event hub**
:   The name of the event hub you created earlier.

**Connection String**
:   The connection string primary key of the event hub namespace. To learn how to get the connection string, refer to [Get an Event Hubs connection string](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-get-connection-string) in the Azure documentation.

    ::::{tip}
    Instead of copying the connection string from the RootManageSharedAccessKey policy, you should create a new shared access policy (with permission to listen) and copy the connection string from the new policy.
    ::::


**Storage account**
:   The name of a blob storage account that you set up in [Create a storage account container](#azure-openai-storage-account-container). You can use the same storage account container for all integrations.

**Storage account key**
:   A valid access key defined for the storage account you created in [Create a storage account container](#azure-openai-storage-account-container).


### Configure metrics collection [azure-openai-configure-integration-metrics]

To collect Azure OpenAI metrics, specify values for the following required fields:

**Client ID**
:   The Application (client) ID that you copied earlier when you created the service principal.

**Client secret**
:   The secret value that you copied earlier.

**Tenant ID**
:   The tenant ID listed on the main Azure Active Directory Page.

**Subscription ID**
:   The subscription ID listed on the main Subscriptions page.

After you’ve finished configuring your integration, click **Save and continue**. You’ll get a notification that your integration was added. Select **Add {{agent}} to your hosts**.


## Step 4: Install {{agent}} [azure-openai-install-agent]

::::{important}
To get support for the latest API changes from Azure, we recommend that you use the latest in-service version of {{agent}} compatible with your {{stack}}. Otherwise, your integrations may not function as expected.
::::


You can install {{agent}} on any host that can access the Azure account and forward events to {{es}}.

1. In the popup, click **Add {{agent}} to your hosts** to open the **Add agent** flyout.

    ::::{tip}
    If you accidentally closed the popup, go to **{{fleet}}** → **Agents**, then click **Add agent** to access the installation instructions.
    ::::


    The **Add agent** flyout has two options: **Enroll in {{fleet}}** and **Run standalone**. The default is to enroll the agents in {{fleet}}, as this reduces the amount of work on the person managing the hosts by providing a centralized management tool in {{kib}}.

2. The enrollment token you need should already be selected.

    ::::{note}
    The enrollment token is specific to the {{agent}} policy that you just created. When you run the command to enroll the agent in {{fleet}}, you will pass in the enrollment token.
    ::::

3. To download, install, and enroll the {{agent}}, select your host operating system and copy the installation command shown in the instructions.
4. Run the command on the host where you want to install {{agent}}.

It takes a few minutes for {{agent}} to enroll in {{fleet}}, download the configuration specified in the policy, and start collecting data. You can wait to confirm incoming data, or close the window.


## Step 5: View logs and metrics in {{kib}} [azure-openai-view-data]

Now that your log and metric data is streaming to {{es}}, you can view them in {{kib}}. You have the following options for viewing your data:

* [View logs and metrics with the overview dashboard](#azure-openai-overview-dashboard): Use the built-in overview dashboard for insight into your Azure OpenAI service like total requests and token usage.
* [View logs and metrics with Discover](#azure-openai-discover): Use Discover to find and filter your log and metric data based on specific fields.


### View logs and metrics with the overview dashboard [azure-openai-overview-dashboard]

The Elastic Azure OpenAI integration comes with a built-in overview dashboard to visualize your log and metric data. To view the integration dashboards:

1. Find **Dashboards** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Search for **Azure OpenAI**.
3. Select the `[Azure OpenAI] Overview` dashboard.

From here, you’ll find visualizations of important metrics for your Azure OpenAI service, like the request rate, error rate, token usage, and chat completion latency. To zoom in on your data, click and drag across the bars in a visualization.

![screenshot of the Azure OpenAI integration dashboard](/solutions/images/observability-azure-openai-dashboard.png "")

For more on dashboards and visualization, refer to the [Dashboards and visualizations](/explore-analyze/dashboards.md) documentation.


### View logs and metrics with Discover [azure-openai-discover]

Find **Discover** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). From the data view drop-down, select either `logs-*` or `metrics-*` to view specific data. You can also create data views if, for example, you wanted to view both `logs-*` and `metrics-*` simultaneously.

![screenshot of the Discover data view dropdown](/solutions/images/observability-discover-data-view-menu.png "")

From here, filter your data and dive deeper into individual logs to find information and troubleshoot issues. For a list of Azure OpenAI fields you may want to filter by, refer to the [Azure OpenAI integration](https://docs.elastic.co/en/integrations/azure_openai#settings) docs.

:::{image} /solutions/images/observability-azure-openai-discover.png
:alt: screenshot of the discover main page
:screenshot:
:::

For more on using Discover and creating data views, refer to the [Discover](/explore-analyze/discover.md) documentation.

## Step 6: Monitor Microsoft Azure OpenAI APM with OpenTelemetry [azure-openai-apm]

The Azure OpenAI API provides useful data to help monitor and understand your code. Using OpenTelemetry, you can ingest this data into Elastic {{observability}}. From there, you can view and analyze your data to monitor the cost and performance of your applications.

For this tutorial, we’ll be using an [example Python application](https://github.com/mdbirnstiehl/AzureOpenAIAPMmonitoringOtel) and the Python OpenTelemetry libraries to instrument the application and send data to {{observability}}.


### Set your environment variables [azure-openai-apm-env-var]

To start collecting APM data for your Azure OpenAI applications, gather the OpenTelemetry OTLP exporter endpoint and authentication header from your {{ecloud}} instance:

1. Find **Integrations** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the **APM** integration.
3. Scroll down to **APM Agents** and select the **OpenTelemetry** tab.
4. Make note of the configuration values for the following configuration settings:

    * `OTEL_EXPORTER_OTLP_ENDPOINT`
    * `OTEL_EXPORTER_OTLP_HEADERS`


With the configuration values from the APM integration and your [Azure OpenAI API key and endpoint](https://learn.microsoft.com/en-us/azure/ai-services/openai/quickstart?tabs=command-line%2Cpython-new&pivots=programming-language-python#retrieve-key-and-endpoint), set the following environment variables using the export command on the command line:

```bash
export AZURE_OPENAI_API_KEY="your-Azure-OpenAI-API-key"
export AZURE_OPENAI_ENDPOINT="your-Azure-OpenAI-endpoint"
export OPENAI_API_VERSION="your_api_version"
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer%20<your-otel-exporter-auth-header>"
export OTEL_EXPORTER_OTLP_ENDPOINT="your-otel-exporter-endpoint"
export OTEL_RESOURCE_ATTRIBUTES=service.name=your-service-name
```


### Download Python libraries [azure-openai-apm-python-libraries]

Install the necessary Python libraries using this command:

```bash
pip3 install openai flask opentelemetry-distro[otlp] opentelemetry-instrumentation
```


### Instrument the application [azure-openai-apm-instrument]

The following code is from the [example application](https://github.com/mdbirnstiehl/AzureOpenAIAPMmonitoringOtel). In a real use case, you would add the import statements to your code.

The app we’re using in this tutorial is a simple example that calls Azure OpenAI APIs with the following message: “How do I send my APM data to Elastic Observability?”:

```python
import os

from flask import Flask
from openai import AzureOpenAI
from opentelemetry import trace

from monitor import count_completion_requests_and_tokens


# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

# Monkey-patch the openai.Completion.create function
client.chat.completions.create = count_completion_requests_and_tokens(
    client.chat.completions.create
)

tracer = trace.get_tracer("counter")


@app.route("/completion")
@tracer.start_as_current_span("completion")
def completion():
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": "How do I send my APM data to Elastic Observability?",
            }
        ],
        max_tokens=20,
        temperature=0,
    )
    return response.choices[0].message.content.strip()
```

The code uses monkey patching, a technique in Python that dynamically modifies the behavior of a class or module at runtime by modifying its attributes or methods, to modify the behavior of the `chat.completions` call so we can add the response metrics to the OpenTelemetry spans.

The [`monitor.py` file](https://github.com/mdbirnstiehl/AzureOpenAIAPMmonitoringOtel/blob/main/monitor.py) in the example application instruments the application and can be used to instrument your own applications.

```python
def count_completion_requests_and_tokens(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        counters["completion_count"] += 1
        response = func(*args, **kwargs)

        token_count = response.usage.total_tokens
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        cost = calculate_cost(response)
        strResponse = json.dumps(response, default=str)

        # Set OpenTelemetry attributes
        span = trace.get_current_span()
        if span:
            span.set_attribute("completion_count", counters["completion_count"])
            span.set_attribute("token_count", token_count)
            span.set_attribute("prompt_tokens", prompt_tokens)
            span.set_attribute("completion_tokens", completion_tokens)
            span.set_attribute("model", response.model)
            span.set_attribute("cost", cost)
            span.set_attribute("response", strResponse)
        return response

    return wrapper
```

Adding this data to our span lets us send it to our OTLP endpoint, so you can search for the data in {{observability}} and build dashboards and visualizations.

Implementing the following function allows you to calculate the cost of a single request to the OpenAI APIs.

```python
def calculate_cost(response):
    if response.model in ["gpt-4", "gpt-4-0314"]:
        cost = (
            response.usage.prompt_tokens * 0.03
            + response.usage.completion_tokens * 0.06
        ) / 1000
    elif response.model in ["gpt-4-32k", "gpt-4-32k-0314"]:
        cost = (
            response.usage.prompt_tokens * 0.06
            + response.usage.completion_tokens * 0.12
        ) / 1000
    elif "gpt-3.5-turbo" in response.model:
        cost = response.usage.total_tokens * 0.002 / 1000
    elif "davinci" in response.model:
        cost = response.usage.total_tokens * 0.02 / 1000
    elif "curie" in response.model:
        cost = response.usage.total_tokens * 0.002 / 1000
    elif "babbage" in response.model:
        cost = response.usage.total_tokens * 0.0005 / 1000
    elif "ada" in response.model:
        cost = response.usage.total_tokens * 0.0004 / 1000
    else:
        cost = 0
    return cost
```

To download the example application and try it for yourself, go to the [GitHub repo](https://github.com/mdbirnstiehl/AzureOpenAIAPMmonitoringOtel).


### View APM data from OpenTelemetry in {{kib}} [azure-openai-view-apm-data]

After ingesting your data, you can filter and explore it using Discover in {{kib}}. Go to **Discover** from the {{kib}} menu under **Analytics**. You can then filter by the fields sent to {{observability}} by OpenTelemetry, including:

* `numeric_labels.completion_count`
* `numeric_labels.completion_tokens`
* `numeric_labels.cost`
* `numeric_labels.prompt_tokens`
* `numeric_labels.token_count`

:::{image} /solutions/images/observability-azure-openai-apm-discover.png
:alt: screenshot of the discover main page
:screenshot:
:::

Then, use these fields to create visualizations and build dashboards. Refer to the [Dashboard and visualizations](/explore-analyze/dashboards.md) documentation for more information.

:::{image} /solutions/images/observability-azure-openai-apm-dashboard.png
:alt: screenshot of the Azure OpenAI APM dashboard
:screenshot:
:::


## What’s next? [azure-openai-alerts]

Now that you know how to find and visualize your Azure OpenAI logs and metrics, you’ll want to make sure you’re getting the most out of your data. Elastic has some useful tools to help you do that:

* **Alerts**: Create threshold rules to notify you when your metrics or logs reach or exceed a specified value: Refer to [Metric threshold](../incident-management/create-metric-threshold-rule.md) and [Log threshold](../incident-management/create-log-threshold-rule.md) for more on setting up alerts.
* **SLOs**: Set measurable targets for your Azure OpenAI service performance based on your metrics. Once defined, you can monitor your SLOs with dashboards and alerts and track their progress against your targets over time. Refer to [Service-level objectives (SLOs)](../incident-management/service-level-objectives-slos.md) for more on setting up and tracking SLOs.
* **Machine learning (ML) jobs**: Set up ML jobs to find anomalous events and patterns in your Azure OpenAI data. Refer to [Finding anomalies](/explore-analyze/machine-learning/anomaly-detection/ml-ad-finding-anomalies.md) for more on setting up ML jobs.