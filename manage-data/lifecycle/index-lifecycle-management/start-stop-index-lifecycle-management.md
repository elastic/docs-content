---
navigation_title: Start and stop {{ilm-init}}
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/start-stop-ilm.html
applies_to:
  stack: ga
  serverless: ga
---

# Start and stop index lifecycle management [start-stop-ilm]

By default, the {{ilm-init}} service is in the `RUNNING` state and manages all indices that have lifecycle policies.

You can stop {{ilm}} to suspend management operations for all indices. For example, you might stop {{ilm}} when performing scheduled maintenance or making changes to the cluster that could impact the execution of {{ilm-init}} actions.

::::{important}
When you stop {{ilm-init}}, [{{slm-init}}](../../../deploy-manage/tools/snapshot-and-restore/create-snapshots.md#automate-snapshots-slm) operations are also suspended. No snapshots will be taken as scheduled until you restart {{ilm-init}}. In-progress snapshots are not affected.
::::



## Get {{ilm-init}} status [get-ilm-status]

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


## Stop {{ilm-init}} [stop-ilm]

To stop the {{ilm-init}} service and pause execution of all lifecycle policies, use the [Stop API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-stop):

```console
POST _ilm/stop
```
%  TEST[continued]

{{ilm-init}} service runs all policies to a point where it is safe to stop. While the {{ilm-init}} service is shutting down, the status API shows {{ilm-init}} is in the `STOPPING` mode:

```console-result
{
  "operation_mode": "STOPPING"
}
```
%  TESTRESPONSE[s/"STOPPING"/$body.operation_mode/]

Once all policies are at a safe stopping point, {{ilm-init}} moves into the `STOPPED` mode:

```console-result
{
  "operation_mode": "STOPPED"
}
```
%  TESTRESPONSE[s/"STOPPED"/$body.operation_mode/]


## Start {{ilm-init}} [_start_ilm_init]

To restart {{ilm-init}} and resume executing policies, use the [Start API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-start). This puts the  {{ilm-init}} service in the `RUNNING` state and {{ilm-init}} begins executing policies from where it left off.

```console
POST _ilm/start
```
%  TEST[continued]

