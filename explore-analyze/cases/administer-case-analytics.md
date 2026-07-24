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

The `reconcile/run_soon` and `reset` routes return a `404` error until you turn them on. To turn them on, add the following setting to [`kibana.yml`](/deploy-manage/stack-settings.md) and restart {{kib}}:

```yaml
xpack.cases.analyticsV2.enableAdminRoutes: true
```

You can also change how often the background update runs. The minimum is 5 minutes. Restart {{kib}} for the change to take effect:

```yaml
xpack.cases.analyticsV2.reconciliationIntervalMinutes: 30
```

## Check health, reconcile, or reset [case-analytics-admin-routes]

All admin routes are internal APIs. Include the `x-elastic-internal-origin: Kibana` header. For `POST` requests, also include `kbn-xsrf: true`.

```bash
# Check analytics health and reset progress
curl -s -u "${USER}:${PASS}" \
  -H "x-elastic-internal-origin: Kibana" \
  "${KIBANA_URL}/internal/cases/_analyticsV2/state"

# Force an immediate update (requires enableAdminRoutes: true)
curl -s -X POST -u "${USER}:${PASS}" \
  -H "kbn-xsrf: true" -H "x-elastic-internal-origin: Kibana" \
  "${KIBANA_URL}/internal/cases/_analyticsV2/reconcile/run_soon"

# Full rebuild - affects every space (requires enableAdminRoutes: true)
curl -s -X POST -u "${USER}:${PASS}" \
  -H "kbn-xsrf: true" -H "x-elastic-internal-origin: Kibana" \
  "${KIBANA_URL}/internal/cases/_analyticsV2/reset"
```

If you call `reconcile/run_soon` while an update is already running, the response includes `already_running: true` and no second update starts.

`reset` returns `202 Accepted` once it recreates the indices and starts rebuilding the data. The rebuild runs in the background and can take several minutes on large deployments. To track progress, call `GET .../state` and check the `active_reset.state` values (`phase`, `cases_processed`, `activity_processed`, and `attachments_processed`). When `active_reset` is `null`, the rebuild is complete. If you run another `reset` while one is in progress, it replaces the first.

::::{note}
The background update finds only cases that changed recently. To rebuild older cases that haven't changed in a long time, run a full `reset`.
::::
