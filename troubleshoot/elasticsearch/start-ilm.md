---
navigation_title: Lifecycle management
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/start-ilm.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/start-slm.html
applies_to:
  stack:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---

# Troubleshoot index lifecycle management

If the automatic [{{ilm}}](/manage-data/lifecycle/index-lifecycle-management.md) ({{ilm-init}}) or [{{slm}}](/deploy-manage/tools/snapshot-and-restore/create-snapshots.md#automate-snapshots-slm) ({{slm-init}}) service is not working, you might need to check the lifecycle status, stop, or restart the service. You may also want to halt services during routine maintenance.

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

## Check status, stop, and restart {{ilm-init}}  [check-stop-start-ilm]

Follow these steps to check the current {{ilm-init}} status, and to start or restop the lifecycle management as needed.

### Get {{ilm-init}} status 

To see the current status of the {{ilm-init}} service, use the [Get Status API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-get-status):

```console
GET _ilm/status
```

Under normal operation, the response shows {{ilm-init}} is `RUNNING`:

```console-result
{
  "operation_mode": "RUNNING"
}
```

### Stop {{ilm-init}} 

You can stop {{ilm}} to suspend management operations for all indices. For example, you might stop {{ilm}} when performing scheduled maintenance or making changes to the cluster that could impact the execution of {{ilm-init}} actions.

To stop the {{ilm-init}} service and pause execution of all lifecycle policies, use the [Stop API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-stop):

```console
POST _ilm/stop
```

The response will look like this:

```console-result
{
  "acknowledged": true
}
```

The {{ilm-init}} service runs all policies to a point where it is safe to stop. 

While the {{ilm-init}} service is shutting down, run the status API to verify that {{ilm-init}} is stopping:

```console
GET _ilm/status
```

The response will look like this:

```console-result
{
  "operation_mode": "STOPPING"
}
```

Once all policies are at a safe stopping point, {{ilm-init}} moves into the `STOPPED` mode:

```console-result
{
  "operation_mode": "STOPPED"
}
```

::::{important}
When you stop {{ilm-init}}, [{{slm-init}}](/deploy-manage/tools/snapshot-and-restore/create-snapshots.md#automate-snapshots-slm) operations are also suspended. No snapshots will be taken as scheduled until you restart {{ilm-init}}. In-progress snapshots are not affected.
::::

### Start {{ilm-init}} [start-ilm]

If the automatic {{ilm}} or {{slm}} service is not working, you might need to start the service.

To restart {{ilm-init}} and resume executing policies, use the [Start API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-start). This puts the  {{ilm-init}} service in the `RUNNING` state and {{ilm-init}} begins executing policies from where it left off.

```console
POST _ilm/start
```

The response will look like this:

```console-result
{
  "acknowledged": true
}
```

Verify that {{ilm}} is now running:

```console
GET _ilm/status
```

The response will look like this:

```console-result
{
  "operation_mode": "RUNNING"
}
```

## Check status, stop, and restart {{slm-init}} [check-stop-start-slm]

Follow these steps to check the current {{slm-init}} status, and to start or restop the lifecycle management as needed.

### Get {{slm-init}} status 

To see the current status of the {{slm-init}} service, use the [Get Status API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-slm-get-status):

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

You can stop {{slm}} to suspend management operations for all snapshot. For example, you might stop {{slm}} o prevent it from taking scheduled snapshots during maintenance or when making cluster changes that could be impacted by snapshot operations.


To stop the {{slm-init}} service and pause execution of all lifecycle policies, use the [Stop API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-slm-stop):

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

### Start {{slm}} [start-slm]

In the event that automatic snapshot lifecycle management is disabled, new backup snapshots will not be created automatically.

Follow these steps to start the snapshot lifecycle management service:

[Start](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-slm-start) {{slm}}:

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
