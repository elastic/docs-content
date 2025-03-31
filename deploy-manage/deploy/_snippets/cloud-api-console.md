With the {{es}} API console, you can interact with a specific {{es}} deployment directly from the {{ecloud}} Console or Cloud UI without having to authenticate again. This RESTful API access is limited to the specific cluster and works only for {{es}} API calls.

You can find this console in the {{ecloud}} Console or Cloud UI when selecting a specific deployment to manage. From the {{es}} menu, select **API Console**.

:::{note}
This API Console is different from the [Dev Tools Console](/explore-analyze/query-filter/tools/console.md) available in {{kib}}, from which you can call {{es}} and {{kib}} APIs. On the {{es}} API Console, you cannot run {{kib}} APIs.

This API console is intended for admin purposes. Avoid running normal workload like indexing or search requests.
:::