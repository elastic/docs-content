---
navigation_title: Administer
applies_to:
  stack: ga 9.5
products:
  - id: kibana
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
description: Check case analytics health, force updates, and rebuild the analytics indices with internal Kibana API routes.
---

# Administer case analytics [administer-case-analytics]

As an administrator, you can check the health of case analytics, force an immediate update, or rebuild the indices from scratch. These operations use internal API routes under `/internal/cases/_analyticsV2/` and require a superuser.

| Route | Availability | Purpose |
| --- | --- | --- |
| `GET /internal/cases/_analyticsV2/state` | Always available when case analytics is on | Reports health, the last update time, and any rebuild in progress |
| `POST /internal/cases/_analyticsV2/reconcile/run_soon` | Requires `enableAdminRoutes: true` | Forces an immediate update |
| `POST /internal/cases/_analyticsV2/reset` | Requires `enableAdminRoutes: true` | Rebuilds all three indices and their data sources from your current cases |

::::{warning}
One set of case analytics indices serves the entire deployment across all spaces. These operations affect **all spaces**, not only the space you run them from. For example, running `reset` from any space rebuilds the analytics data and the **Case Analytics** {{data-source}} for every space. Plan a reset as a deployment-wide operation.
::::

## Turn on admin routes [turn-on-case-analytics-admin-routes]

The `reconcile/run_soon` and `reset` routes return a `404` error until you turn them on. To turn them on, add the following setting to your [`kibana.yml`](/deploy-manage/stack-settings.md) and restart {{kib}}:

```yaml
xpack.cases.analyticsV2.enableAdminRoutes: true
```

You can also change how often the background update runs. The minimum is 5 minutes. Restart {{kib}} for the change to take effect:

```yaml
xpack.cases.analyticsV2.reconciliationIntervalMinutes: 30
```

## Run admin operations [case-analytics-admin-routes]

All admin routes are internal APIs. Include the `x-elastic-internal-origin: Kibana` header, and for `POST` requests, also include `kbn-xsrf: true`.

### Check health and rebuild progress [case-analytics-check-health]

The `state` route is always available when case analytics is on. Use it to check health, the last update time, and the progress of any rebuild:

```bash
curl -s -u "${USER}:${PASS}" \
  -H "x-elastic-internal-origin: Kibana" \
  "${KIBANA_URL}/internal/cases/_analyticsV2/state"
```

While a rebuild is running, check the `active_reset.state` values: `phase`, `cases_processed`, `activity_processed`, and `attachments_processed`. When `active_reset` is `null`, the rebuild is complete.

### Force an immediate update [case-analytics-force-update]

Force an update instead of waiting for the next scheduled background update. This route requires [admin routes to be turned on](#turn-on-case-analytics-admin-routes):

```bash
curl -s -X POST -u "${USER}:${PASS}" \
  -H "kbn-xsrf: true" -H "x-elastic-internal-origin: Kibana" \
  "${KIBANA_URL}/internal/cases/_analyticsV2/reconcile/run_soon"
```

If an update is already running, the response includes `already_running: true` and no second update starts.

::::{note}
The background update finds only cases that changed recently. To rebuild older cases that haven't changed in a long time, run a full `reset`.
::::

### Rebuild the indices from your cases [case-analytics-rebuild-indices]

Recreate all three indices and their data sources from your current cases. This route requires [admin routes to be turned on](#turn-on-case-analytics-admin-routes):

```bash
curl -s -X POST -u "${USER}:${PASS}" \
  -H "kbn-xsrf: true" -H "x-elastic-internal-origin: Kibana" \
  "${KIBANA_URL}/internal/cases/_analyticsV2/reset"
```

* `reset` returns `202 Accepted`, then recreates the indices and rebuilds the data in the background. On large deployments, the rebuild can take several minutes.
* The rebuild runs in batches in the background and doesn't disrupt active case work.
* To track progress, use the `state` route, described in [Check health and rebuild progress](#case-analytics-check-health).
* Running another `reset` while one is in progress replaces the first.
