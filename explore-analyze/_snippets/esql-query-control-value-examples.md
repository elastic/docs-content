When you populate a control with an {{esql}} query, you can shape the values it offers in ways that selecting a field alone doesn't allow. For example, use `WHERE` to limit the values the control offers, instead of surfacing every value in the field. This query lists the hosts reporting metrics, excluding those in one region:

```esql
FROM metrics-hostmetricsreceiver.otel-default
| WHERE cloud.region != "eu - west - 2"
| STATS BY `host.name`
```

:::{image} /explore-analyze/images/dashboard-control-query-filter-values.png
:alt: A control populated by an ES|QL query that excludes hosts from one region
:screenshot:
:::
