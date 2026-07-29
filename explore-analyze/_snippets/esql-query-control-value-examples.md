When you populate a control with an {{esql}} query, you can shape the values it offers in ways that selecting a field alone doesn't allow. For example, use `WHERE` to limit the values the control offers, instead of surfacing every value in the field. This query offers only the operating systems seen in requests for CSS files from the sample web logs, instead of every operating system in the data:

```esql
FROM kibana_sample_data_logs
| WHERE extension.keyword == "css"
| STATS BY machine.os.keyword
```

:::{image} /explore-analyze/images/dashboard-control-query-filter-values.png
:alt: A control populated by an ES|QL query that filters the offered values to operating systems seen in CSS file requests
:screenshot:
:::
