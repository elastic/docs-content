---
applies:
  stack:
  serverless:
navigation_title: "CSV"
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/reporting-troubleshooting-csv.html
---



# CSV [reporting-troubleshooting-csv]


::::{note}
We recommend using CSV reports to export moderate amounts of data only. The feature enables analysis of data in external tools, but it is not intended for bulk export or to backup Elasticsearch data. Report timeout and incomplete data issues are likely if you are exporting data where:

* More than 250 MB of data is being exported
* Data is stored on slow storage tiers
* Any shard needed for the search is unavailable
* Network latency between nodes is high
* Cross-cluster search is used
* ES|QL is used and result row count exceeds the limits of ES|QL queries

To work around the limitations, use filters to create multiple smaller reports, or extract the data you need directly with the Elasticsearch APIs.

For more information on using Elasticsearch APIs directly, see [Scroll API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-scroll), [Point in time API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-open-point-in-time), [ES|QL](../query-filter/languages/esql-rest.md) or [SQL](../query-filter/languages/sql-rest-format.md#_csv) with CSV response data format. We recommend that you use an official Elastic language client: details for each programming language library that Elastic provides are in the [{{es}} Client documentation](https://www.elastic.co/guide/en/elasticsearch/client/index.html).

[Reporting parameters](https://www.elastic.co/guide/en/kibana/current/reporting-settings-kb.html) can be adjusted to overcome some of these limiting scenarios. Results are dependent on data size, availability, and latency factors and are not guaranteed.

::::


The CSV export feature in Kibana makes queries to Elasticsearch and formats the results into CSV. This feature offers a solution that attempts to provide the most benefit to the most use cases. However, things could go wrong during export. Elasticsearch can stop responding, repeated querying can take so long that authentication tokens can time out, and the format of exported data can be too complex for spreadsheet applications to handle. Such situations are outside of the control of Kibana. If the use case becomes complex enough, it’s recommended that you create scripts that query Elasticsearch directly, using a scripting language like Python and the public {{es}} APIs.

For advice about common problems, refer to [Troubleshooting](reporting-troubleshooting.md).


## Configuring CSV export to use the scroll API [reporting-troubleshooting-csv-configure-scan-api]

The Kibana CSV export feature collects all of the data from Elasticsearch by using multiple requests to page over all of the documents. Internally, the feature uses the [Point in time API and `search_after` parameters in the queries](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-open-point-in-time) to do so. There are some limitations related to the point in time API:

1. Permissions to read data aliases alone will not work: the permissions are needed on the underlying indices or data streams.
2. In cases where data shards are unavailable or time out, the export will be empty rather than returning partial data.

Some users may benefit from using the [scroll API](https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html#scroll-search-results), an alternative to paging through the data. The behavior of this API does not have the limitations of point in time API, however it has its own limitations:

1. Search is limited to 500 shards at the very most.
2. In cases where the data shards are unavailable or time out, the export may return partial data.

If you prefer the internal implementation of CSV export to use the scroll API, you can configure this in `kibana.yml`:

```yaml
xpack.reporting.csv.scroll.strategy: scroll
```

For more details about CSV export settings, go to [CSV settings](https://www.elastic.co/guide/en/kibana/current/reporting-settings-kb.html#reporting-csv-settings).


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

:::{image} https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt4758e67aaec715d9/67897d0be92e090a6dc626a8/inspect-query-from-csv-export.gif
:alt: Inspect the query used for CSV export
:class: screenshot
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
