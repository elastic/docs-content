With an {{esql}} query, you can shape the values offered in the control more precisely. 

For example, use `WHERE` to limit the values the control offers, instead of surfacing every value in the field. The following query offers only the operating systems seen in requests for CSS files from the sample web logs, instead of every operating system in the data:

```esql
FROM kibana_sample_data_logs
| WHERE extension.keyword == "css"
| STATS BY machine.os.keyword
```
