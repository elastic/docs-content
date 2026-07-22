When you populate a control with an {{esql}} query, you can shape the values it offers in ways that selecting a field alone doesn't allow.

**Customize the values**

Use `CASE()` to replace raw field values with friendlier labels. This query returns the traffic source countries from the sample web logs, but shows `United States` in place of the raw `US` code:

```esql
FROM kibana_sample_data_logs
| EVAL geo_src_name = CASE(geo.src == "US", "United States", geo.src)
| STATS BY geo_src_name
```

:::{image} /explore-analyze/images/dashboard-control-query-customize-values.png
:alt: A control populated by an ES|QL query that relabels the US region as United States
:screenshot:
:::

**Filter the values**

Use `WHERE` to limit the values the control offers, instead of surfacing every value in the field. This query lists the hosts reporting metrics, excluding those in one region:

```esql
FROM metrics-hostmetricsreceiver.otel-default
| WHERE cloud.region != "eu - west - 2"
| STATS BY `host.name`
```

:::{image} /explore-analyze/images/dashboard-control-query-filter-values.png
:alt: A control populated by an ES|QL query that excludes hosts from one region
:screenshot:
:::
