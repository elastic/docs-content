---
description: Troubleshoot common CSV export issues including timeouts, socket errors, token expiration, and scroll API configuration.
navigation_title: CSV
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/reporting-troubleshooting-csv.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---



# CSV [reporting-troubleshooting-csv]

CSV export in {{kib}} queries {{es}} and formats the results as downloadable CSV files. While this works well for moderate data exports, issues can occur with large datasets, slow storage, network latency, or authentication timeouts. This page helps you diagnose and resolve common CSV export problems.

Common issues include:

* Report timeouts when exporting more than 250 MB of data
* Incomplete data when shards are unavailable or using {{ccs}}
* Socket hangup errors during long-running exports
* Token expiration for SAML-authenticated deployments

For general troubleshooting guidance, refer to [Troubleshooting](reporting-troubleshooting.md).

::::{note}
CSV export is designed for moderate data amounts only. It enables data analysis in external tools but is not intended for bulk export or {{es}} backups. Report timeout and incomplete data issues are likely when exporting data where:

* More than 250 MB of data is being exported
* Data is stored on slow storage tiers
* Any shard needed for the search is unavailable
* Network latency between nodes is high
* {{ccs}} is used
* {{esql}} is used and result row count exceeds the limits of {{esql}} queries

To work around these limitations, use filters to create multiple smaller reports, or extract data directly with {{es}} APIs. For information on using {{es}} APIs directly, refer to [Scroll API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-scroll), [Point in time API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-open-point-in-time), [{{esql}}](elasticsearch://reference/query-languages/esql/esql-rest.md), or [SQL](elasticsearch://reference/query-languages/sql/sql-rest-format.md#_csv) with CSV response data format. Consider using an official {{es}} client: refer to [{{es}} Client documentation](/reference/elasticsearch-clients/index.md).

You can adjust [Reporting parameters](kibana://reference/configuration-reference/reporting-settings.md) to overcome some limiting scenarios. Results depend on data size, availability, and latency factors and are not guaranteed.

::::


## Configuring CSV export to use the scroll API [reporting-troubleshooting-csv-configure-scan-api]

The Kibana CSV export feature collects all of the data from Elasticsearch by using multiple requests to page over all of the documents. Internally, the feature uses the [Point in time API and `search_after` parameters in the queries](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-open-point-in-time) to do so. There are some limitations related to the point in time API:

1. Permissions to read data aliases alone will not work: the permissions are needed on the underlying indices or data streams.
2. In cases where data shards are unavailable or time out, the export will be empty rather than returning partial data.

Some users may benefit from using the [scroll API](elasticsearch://reference/elasticsearch/rest-apis/paginate-search-results.md#scroll-search-results), an alternative to paging through the data. The behavior of this API does not have the limitations of point in time API, however it has its own limitations:

1. Search is limited to 500 shards at the very most.
2. In cases where the data shards are unavailable or time out, the export may return partial data.

If you prefer the internal implementation of CSV export to use the scroll API, you can configure this in [`kibana.yml`](/deploy-manage/stack-settings.md):

```yaml
xpack.reporting.csv.scroll.strategy: scroll
```

For more details about CSV export settings, go to [CSV settings](kibana://reference/configuration-reference/reporting-settings.md#reporting-csv-settings).


## Socket hangups [reporting-troubleshooting-csv-socket-hangup]

A "socket hangup" is a generic type of error meaning that a remote service (in this case Elasticsearch or a proxy in Cloud) closed the connection. Kibana can’t foresee when this might happen and can’t force the remote service to keep the connection open. To work around this situation, consider lowering the size of results that come back in each request or increase the amount of time the remote services will allow to keep the request open. For example:

```yaml
xpack.reporting.csv.scroll.size: 50
xpack.reporting.csv.scroll.duration: 2m
```

Such changes aren’t guaranteed to solve the issue, but give the functionality a better chance of working in this use case. Unfortunately, lowering the scroll size will require more requests to Elasticsearch during export, which adds more time overhead, which could unintentionally create more instances of auth token expiration errors.


## Inspecting the query used for CSV export [reporting-troubleshooting-inspect-query-used-for-export]

The listing of reports in **Stack Management > Reporting** allows you to inspect the query used for CSV export. It can be helpful to see the raw responses from Elasticsearch, or determine if there are performance improvements to be gained by changing the way you query the data.

1. Go to **Stack Management > Reporting** and click the info icon next to a report.
2. In the footer of the report flyout, click **Actions**.
3. Click **Inspect query in Console** in the **Actions** menu.
4. This will open the **Console** application, pre-filled with the queries used to generate the CSV export.

:::{image} /explore-analyze/images/inspect-query-from-csv-export.gif
:alt: Inspect the query used for CSV export
:screenshot:
:::


## Token expiration [reporting-troubleshooting-csv-token-expired]

A relatively common type of error seen for CSV exports is: `security_exception Root causes: security_exception: token expired`.

This error occurs in deployments that use token-based authentication (SAML tokens) when it takes too long to create the CSV report with the authentication cached in report job details.

This means that the deployment is stable, but the size of the requested report is too large to complete within the time allowed by the authentication token available to the Reporting task.


### Avoiding token expiration [avoid-token-expiration]

You can use the following workarounds for this error:

* Create smaller reports. Instead of creating one report that covers a large time range, create multiple reports that cover segmented time ranges.
* Increase `xpack.security.authc.token.timeout`, which is set to `20m` by default.
* To avoid token expirations completely, use a type of authentication that doesn’t expire (such as Basic auth), or run the export using scripts that query {{es}} directly.
