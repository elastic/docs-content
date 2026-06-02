## May 19, 2026 [elastic-2026-05-19-deprecations]

* Update `GET /api/status` endpoint details.
  For more information, check [#268942](https://github.com/elastic/kibana/pull/268942) [#202446](https://github.com/elastic/kibana/issues/202446).

  **Impact:** `GET /api/status` now requires the Elasticsearch `cluster:monitor` privilege to return the full payload, including host info, build details, core and plugin status, and metrics. Authenticated callers without `monitor`, and callers when the privilege check fails, receive the same minimal response shape that unauthenticated callers already receive: `{ status: { overall: { level } } }`. Kubernetes liveness and readiness probes are unaffected.

  **Action:** If you need to preserve the previous behavior while updating monitoring users or roles, set `status.statusPageBypassMonitorPrivilege: true` to allow authenticated users to access the full status API and `/status` page without `monitor`. The `/status` UI renders an explanatory prompt for users without `monitor` when the bypass is disabled.

