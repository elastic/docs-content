Optionally add a data stream lifecycle to manage retention, performance, and storage.
For example, use the [update data stream lifecycles]({{es-apis}}operation/operation-indices-put-data-lifecycle) API:

```console
PUT _data_stream/my-new-tsds/_lifecycle
{
  "enabled": true,
  "data_retention": "365d" <1>
}
```

1. The retention period of this data stream is set to 365 days. This means that {{es}} is allowed to delete data that is older than a year at its own discretion.

For more details, refer to [Set a data stream's lifecycle](/manage-data/lifecycle/data-stream/tutorial-update-existing-data-stream.md#set-lifecycle).

Alternatively, you can use {{ilm}}. Refer to [](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md) and [](/manage-data/lifecycle/index-lifecycle-management/policy-apply.md).
