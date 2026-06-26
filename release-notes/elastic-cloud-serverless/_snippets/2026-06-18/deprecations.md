## June 18, 2026 [elastic-2026-06-18-deprecations]

* Deprecate experimental public Significant Events APIs.
  For more information, check [#273310](https://github.com/elastic/kibana/pull/273310).

  **Impact:** Calls to the experimental public Significant Events API endpoints (`/api/streams/{name}/queries*` and `/api/streams/{name}/significant_events`) return deprecation warnings and will be removed in a future release.

  **Action:** There are no replacement APIs at this time.

