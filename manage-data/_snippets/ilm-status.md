To view the current status of the {{ilm-init}} service, use the [{{ilm-init}} status API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-get-status):

```console
GET _ilm/status
```

Under normal operation, the response shows {{ilm-init}} is `RUNNING`:

```console-result
{
  "operation_mode": "RUNNING"
}
```

You can also [](/manage-data/lifecycle/index-lifecycle-management/policy-view-status.md) for further information.