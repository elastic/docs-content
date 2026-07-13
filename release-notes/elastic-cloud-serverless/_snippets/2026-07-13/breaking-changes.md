## July 13, 2026 [elastic-2026-07-13-breaking-changes]

::::{dropdown} Dashboards and Visualizations APIs use short-hand duration units
  For more information, check [#274792]({{kib-pull}}274792).

  The `duration` format used in visualization configuration now uses short-hand unit values aligned with {{esql}} conventions for its `from` and `to` options. This affects the `api/visualizations` and `api/dashboards` APIs, for both by-value and by-reference panels. For example, `minutes` becomes `min`, `humanize` becomes `auto-approximate`, and `humanizePrecise` becomes `auto`.

  **Impact:** API requests that configure duration formats with the previous verbose unit names (for example, `minutes`, `humanize`, or `asMilliseconds`) are rejected.

  **Action:** Update the duration `from` and `to` values in your visualization and dashboard panel API payloads to the new short-hand units.
::::

::::{dropdown} Dashboard API search endpoint uses a new response schema and enforces a page size limit
  For more information, check [#268951]({{kib-pull}}268951).

  The response envelope for the Dashboard API search endpoint changed from `{ dashboards, page, total }` to `{ data, meta }`, where the pagination fields (`page`, `per_page`, and `total`) move under `meta`. The endpoint also enforces a maximum `per_page` of 1000.

  **Impact:** Requests that set `per_page` above 1000 are rejected. Clients that read `dashboards`, `page`, or `total` from the top level of the response no longer receive those fields.

  **Action:** Update Dashboard API search clients to read results from `data` and pagination from `meta`, and keep `per_page` at or below 1000.
::::
