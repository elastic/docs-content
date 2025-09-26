By default, the {{ilm}} service is in the `RUNNING` state and manages all indices that have lifecycle policies.

You can stop {{ilm-init}} to suspend management operations for all indices. For example, you might stop {{ilm}} when performing scheduled maintenance or making changes to the cluster that could impact the execution of {{ilm-init}} actions.

::::{important}
When you stop {{ilm-init}}, [{{slm-init}}](/deploy-manage/tools/snapshot-and-restore/create-snapshots.md#automate-snapshots-slm) operations are also suspended. No snapshots will be taken as scheduled until you restart {{ilm-init}}. In-progress snapshots are not affected.
::::

To stop the {{ilm-init}} service and pause execution of all lifecycle policies, use the [{{ilm-init}} stop API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-stop):

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