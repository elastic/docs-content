# Troubleshoot logs [observability-troubleshoot-logs]

Use this page to find possible solutions for errors your encountering with your logs. This troubleshooting page is broken into the following sections:

* [Common onboarding issues](observability-troubleshoot-logs.md#logs-onboarding-troubleshooting)
* [Mapping and pipeline issues](observability-troubleshoot-logs.md#logs-common-mapping-troubleshooting)


## Common onboarding issues [logs-onboarding-troubleshooting]

This section provides possible solutions for errors you might encounter while onboarding your logs.


### User does not have permissions to create API key [observability-troubleshoot-logs-user-does-not-have-permissions-to-create-api-key]

When adding a new data using the guided instructions in your project (**Add data** → **Collect and analyze logs** → **Stream log files**), if you don’t have the required privileges to create an API key, you’ll see the following error message:

::::{note}
You need permission to manage API keys

::::



#### Solution [observability-troubleshoot-logs-solution]

You need to either:

* Ask an administrator to update your user role to at least **Developer** by going to the user icon on the header bar and opening **Organization** → **Members**. Read more about user roles in [Assign user roles and privileges](general-manage-organization.md#general-assign-user-roles). After your use role is updated, restart the onboarding flow.
* Get an API key from an administrator and manually add the API to the {{agent}} configuration. See [Configure the {{agent}}](observability-stream-log-files.md#observability-stream-log-files-step-3-configure-the-agent) for more on manually updating the configuration and adding the API key.


### Observability project not accessible from host [observability-troubleshoot-logs-observability-project-not-accessible-from-host]

If your Observability project is not accessible from the host, you’ll see the following error message after pasting the **Install the {{agent}}** instructions into the host:

```plaintext
Failed to connect to {host} port {port} after 0 ms: Connection refused
```


#### Solution [observability-troubleshoot-logs-solution-1]

The host needs access to your project. Port `443` must be open and the project’s {{es}} endpoint must be reachable. You can locate your project’s endpoint by clicking the help icon (![Help icon](../../../images/serverless-help.svg "")) and selecting **Endpoints**. Run the following command, replacing the URL with your endpoint, and you should get an authentication error with more details on resolving your issue:

```shell
curl https://your-endpoint.elastic.cloud
```


### Download {{agent}} failed [observability-troubleshoot-logs-download-agent-failed]

If the host was able to download the installation script but cannot connect to the public artifact repository, you’ll see the following error message:

```plaintext
Download Elastic Agent

Failed to download Elastic Agent, see script for error.
```


#### Solutions [observability-troubleshoot-logs-solutions]

* If the combination of the {{agent}} version and operating system architecture is not available, you’ll see the following error message:

    ```plaintext
    The requested URL returned error: 404
    ```

    To fix this, update the {{agent}} version in the installation instructions to a known version of the {{agent}}.

* If the {{agent}} was fully downloaded previously, you’ll see the following error message:

    ```plaintext
    Error: cannot perform installation as Elastic Agent is already running from this directory
    ```

    To fix this, delete previous downloads and restart the onboarding.

* You’re an Elastic Cloud Enterprise user without access to the Elastic downloads page.


### Install {{agent}} failed [observability-troubleshoot-logs-install-agent-failed]

If an {{agent}} already exists on your host, you’ll see the following error message:

```plaintext
Install Elastic Agent

Failed to install Elastic Agent, see script for error.
```


#### Solution [observability-troubleshoot-logs-solution-2]

You can uninstall the current {{agent}} using the `elastic-agent uninstall` command, and run the script again.

::::{warning}
Uninstalling the current {{agent}} removes the entire current setup, including the existing configuration.

::::



### Waiting for Logs to be shipped…​ step never completes [observability-troubleshoot-logs-waiting-for-logs-to-be-shipped-step-never-completes]

If the **Waiting for Logs to be shipped…​** step never completes, logs are not being shipped to your Observability project, and there is most likely an issue with your {{agent}} configuration.


#### Solution [observability-troubleshoot-logs-solution-3]

Inspect the {{agent}} logs for errors. See the [Debug standalone {{agent}}s](https://www.elastic.co/guide/en/fleet/current/debug-standalone-agents.html#inspect-standalone-agent-logs) documentation for more on finding errors in {{agent}} logs.


## Mapping and pipeline issues [logs-common-mapping-troubleshooting]

This section provides possible solutions for mapping and pipeline issues you might encounter with your logs.


### Keyword fields are too long [logs-mapping-troubleshooting-keyword-limit]

The `keyword` field limit is 32,766 bytes. When indexing a document, if your `keyword` field length exceeds this limit, you’ll see an error similar to the following:

```plaintext
max_bytes_length_exceeded_exception: bytes can be at most 32766 in length
```


#### Solution [logs-mapping-troubleshooting-keyword-limit-solution]

Avoid this error using one of the following options:

**Stop indexing the field:** If you don’t need the `keyword` field for aggregation or search, set `"index":false` in the index template to stop indexing the field.

**Convert the `keyword` field to a `text` field:** To continue indexing the field while avoiding length limits, you can convert the `keyword` field to a `text` field.

::::{note}
Aggregations on this field would no longer be supported, but the contents would be searchable.
::::


To convert the `keyword` field to a `text` field:

1. Create a new index with the `text` field data type.
2. Reindex from the `_source` field of the source index using the [`_reindex` API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex).


### Date format mismatch [logs-mapping-troubleshooting-date-mismatch]

If the format of the `date` field in your document doesn’t match the format set in your index template, you’ll see an error similar to the following:

```plaintext
failed to parse field [date] of type [date] in document with id 'KGcZb3cBqhj6kAxank_x'.
```


#### Solution [logs-mapping-troubleshooting-date-solution]

Add the format of the mismatched date to your index template. Multiple formats can be specified by separating them with `||` as a separator. Each format will be tried in turn until a matching format is found. For example:

$$$date-format-example$$$

```console
PUT my-index-000001
{
  "mappings": {
    "properties": {
      "date": {
        "type":   "date",
        "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
      }
    }
  }
}
```

Refer to the [`date` field type](https://www.elastic.co/guide/en/elasticsearch/reference/current/date.html) docs for more information.


### Grok or dissect pattern mismatch [logs-mapping-troubleshooting-grok-mismatch]

If the pattern in your grok or dissect processor doesn’t match the format of your document, you’ll see an error similar to the following:

```plaintext
Provided Grok patterns do not match field value...
```


#### Solution [logs-mapping-troubleshooting-grok-solution]

Make sure your [grok](https://www.elastic.co/guide/en/elasticsearch/reference/current/grok-processor.html) or [dissect](https://www.elastic.co/guide/en/elasticsearch/reference/current/dissect-processor.html) processor pattern matches your log document format.

You can build and debug grok patterns in {{kib}} using the [Grok Debugger](../../../explore-analyze/query-filter/tools/grok-debugger.md). Find the **Grok Debugger** by navigating to the **Developer tools** page using the navigation menu or the global search field.

From here, you can enter sample data representative of the log document you’re trying to ingest and the Grok pattern you want to apply to the data.

If you don’t see any **Structured Data** when you simulate the grok pattern, iterate on the pattern until you find the error.
