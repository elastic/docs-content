```console
POST kbn://api/agent_builder/tools
{
  "id": "example-books-esql-tool", <1>
  "type": "esql", <2>
  "description": "An ES|QL query tool for getting the book with the most pages", <3>
  "configuration": {
    "query": "FROM kibana_sample_data_agents | SORT page_count DESC | LIMIT 1", <4>
    "params": {} <5>
  }
}
```
1. Unique identifier for the tool
2. Tool type - `esql` for {{esql}} query tools
3. Description that helps agents understand when to use this tool
4. The {{esql}} query to run
5. Query parameters (empty for this basic example)
