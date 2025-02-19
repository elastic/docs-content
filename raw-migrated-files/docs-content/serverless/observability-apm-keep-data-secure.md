# Use APM securely [observability-apm-keep-data-secure]

::::{admonition} Required role
:class: note

The **Editor** role or higher is required to create and manage API keys. To learn more, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::


When setting up Elastic APM, it’s essential to ensure that the data collected by APM agents is sent to Elastic securely and that sensitive data is protected.


## Secure communication with APM agents [observability-apm-keep-data-secure-secure-communication-with-apm-agents]

Communication between APM agents and the managed intake service is both encrypted and authenticated. Requests without a valid API key will be denied.


### Create a new API key [observability-apm-keep-data-secure-create-a-new-api-key]

To create a new API key:

1. In your {{obs-serverless}} project, go to any **Applications** page.
2. Click **Settings**.
3. Select the **APM agent keys** tab.
4. Click **Create APM agent key**.
5. Name the key and assign privileges to it.
6. Click **Create APM agent key**.
7. Copy the key now. You will not be able to see it again. API keys do not expire.


### Delete an API key [observability-apm-keep-data-secure-delete-an-api-key]

To delete an API key:

1. From any of the **Application** pages, click **Settings**.
2. Select the **APM agent keys** tab.
3. Search for the API key you want to delete.
4. Click the trash can icon to delete the selected API key.


### View existing API keys [observability-apm-keep-data-secure-view-existing-api-keys]

To view all API keys for your project:

1. Expand **Project settings**.
2. Select **Management**.
3. Select **API keys**.


## Data security [observability-apm-keep-data-secure-data-security]

When setting up Elastic APM, it’s essential to review all captured data carefully to ensure it doesn’t contain sensitive information like passwords, credit card numbers, or health data.

Some APM agents offer a way to manipulate or drop APM events *before* they leave your services. Refer to the relevant agent’s documentation for more information and examples:


### Java [observability-apm-keep-data-secure-java]

**`include_process_args`**: Remove process arguments from transactions. This option is disabled by default. Read more in the [Java agent configuration docs](https://www.elastic.co/guide/en/apm/agent/java/current/config-reporter.html#config-include-process-args).


### .NET [observability-apm-keep-data-secure-net]

**Filter API**: Drop APM events *before* they are sent to Elastic. Read more in the [.NET agent Filter API docs](https://www.elastic.co/guide/en/apm/agent/dotnet/current/public-api.html#filter-api).


### Node.js [observability-apm-keep-data-secure-nodejs]

* **`addFilter()`**: Drop APM events *before* they are sent to Elastic. Read more in the [Node.js agent API docs](https://www.elastic.co/guide/en/apm/agent/nodejs/current/agent-api.html#apm-add-filter).
* **`captureExceptions`**: Remove errors raised by the server-side process by disabling the `captureExceptions` configuration option. Read more in [the Node.js agent configuration docs](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#capture-exceptions).


### Python [observability-apm-keep-data-secure-python]

**Custom processors**: Drop APM events *before* they are sent to Elastic. Read more in the [Python agent Custom processors docs](https://www.elastic.co/guide/en/apm/agent/python/current/sanitizing-data.html).


### Ruby [observability-apm-keep-data-secure-ruby]

**`add_filter()`**: Drop APM events *before* they are sent to Elastic. Read more in the [Ruby agent API docs](https://www.elastic.co/guide/en/apm/agent/ruby/current/api.html#api-agent-add-filter).
