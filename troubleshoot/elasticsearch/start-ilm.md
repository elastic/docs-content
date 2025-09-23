---
navigation_title: Lifecycle management
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/start-ilm.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/start-slm.html
applies_to:
  stack: all
products:
  - id: elasticsearch
---

# Troubleshoot snapshot and index lifecycle management

If the automatic [{{slm}}](/deploy-manage/tools/snapshot-and-restore/create-snapshots.md#automate-snapshots-slm) ({{slm-init}}) or [{{ilm}}](/manage-data/lifecycle/index-lifecycle-management.md) ({{ilm-init}}) service is not operating as expected, you might need to check its lifecycle status, stop, or restart the service. You may also want to halt services during routine maintenance.

All of the procedures on this page use the {{es}} APIs. To run these steps using {{kib}}:

1. Log in to the [{{ecloud}} console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Hosted deployments** panel, click the name of your deployment.

    ::::{note}
    If the name of your deployment is disabled your {{kib}} instances might be unhealthy, in which case contact [Elastic Support](https://support.elastic.co). If your deployment doesn’t include {{kib}}, all you need to do is [enable it first](../../deploy-manage/deploy/elastic-cloud/access-kibana.md).
    ::::

3. Open your deployment’s side navigation menu (placed under the Elastic logo in the upper left corner) and go to **Dev Tools > Console**.

    :::{image} /troubleshoot/images/elasticsearch-reference-kibana-console.png
    :alt: {{kib}} Console
    :screenshot:
    :::

4. Use the Dev Tools Console to run the API requests as described.



## Check status, stop, and restart {{slm-init}} [check-stop-start-slm]

Follow these steps to check the current {{slm-init}} status, and to stop or restart it as needed.

### Get {{slm-init}} status 

To see the current status of the {{slm-init}} service, use the [{{slm-init}} status API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-slm-get-status):

```console
GET _slm/status
```

Under normal operation, the response shows {{slm-init}} is `RUNNING`:

```console-result
{
  "operation_mode": "RUNNING"
}
```

### Stop {{slm-init}} 

You can stop {{slm}} to suspend management operations for all snapshots. For example, you might stop {{slm-init}} to prevent it from taking scheduled snapshots during maintenance or when making cluster changes that could be impacted by snapshot operations.

To stop the {{slm-init}} service and pause execution of all lifecycle policies, use the [{{slm-init}} stop API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-slm-stop):

```console
POST _slm/stop
```

Stopping {{slm-init}} does not stop any snapshots that are in progress. You can manually trigger snapshots with the run snapshot lifecycle policy API even if {{slm-init}} is stopped.

The response will look like this:

```console-result
{
  "acknowledged": true
}
```

Verify that {{slm}} has stopped:

```console
GET _slm/status
```

The response will look like this:

```console-result
{
  "operation_mode": "STOPPED"
}
```

### Start {{slm-init}} [start-slm]

In the event that automatic {{slm}} is disabled, new backup snapshots will not be created automatically.

To restart the {{slm-init}} service, use the [{{slm-init}} start API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-slm-start).

```console
POST _slm/start
```

The response will look like this:

```console-result
{
  "acknowledged": true
}
```

Verify the {{slm}} is now running:

```console
GET _slm/status
```

The response will look like this:

```console-result
{
  "operation_mode": "RUNNING"
}
```

## Check status, stop, and restart {{ilm-init}} [check-stop-start-ilm]

Follow these steps to check the current {{ilm-init}} status, and to stop or restart it as needed.

### Get {{ilm-init}} status 

:::{include} ../../manage-data/_snippets/ilm-status.md
:::

### Stop {{ilm-init}} 

:::{include} ../../manage-data/_snippets/ilm-stop.md
:::

### Start {{ilm-init}} 

:::{include} ../../manage-data/_snippets/ilm-start.md
:::