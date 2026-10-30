In {{obs-serverless}} and {{sec-serverless}} projects, search is optimized for fast, responsive performance on data from the most recent day, while historical data remains available for broader analysis.

:::{dropdown} Search performance
:open:
{{es-serverless}} projects are geared toward [search use cases](/solutions/search.md), so they provide the [Search Power and Search Boost Window settings](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-ai-lake-settings) to let you control search performance and cost. These settings aren't available in {{obs-serverless}} and {{sec-serverless}} projects. Instead, search capacity is sized automatically based on the volume of search-ready data in your project: time series data from the most recent day, plus non-time series data. Search capacity does not scale automatically based on query load. Ingest runs on a separate tier and does not compete with search.

Queries on data older than the most recent day are read from general storage rather than the search-ready cache, which is slower and uses more capacity per query. {{search-load-sources}} add to the load.

Signs that capacity is saturated include {{search-saturation-signals}}, `Request timed out` errors in {{kib}}, circuit breaker exceptions, and rising query latency in Discover. To reduce load, {{search-reduce-load}}.

If your workload would benefit from extending this window or requires additional search capacity, contact Elastic Support.
:::
