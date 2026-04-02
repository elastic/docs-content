```console
PUT kbn://api/agent_builder/tools/example-books-esql-tool
{
  "description": "An ES|QL query tool for finding the longest books published before a certain year",
  "configuration": {
    "query": "FROM kibana_sample_data_agents | WHERE DATE_EXTRACT(\"year\", release_date) < ?maxYear | SORT page_count DESC | LIMIT ?limit", <1>
    "params": {
      "maxYear": { <2>
        "type": "integer",
        "description": "Maximum year to filter books (exclusive)"
      },
      "limit": { <3>
        "type": "integer",
        "description": "Maximum number of results to return"
      }
    }
  }
}
```
1. Query with parameterized placeholders (`?maxYear`, `?limit`)
2. Integer parameter for filtering by publication year
3. Integer parameter for limiting results
