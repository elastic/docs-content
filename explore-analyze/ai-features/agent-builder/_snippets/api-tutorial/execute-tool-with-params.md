```console
POST kbn://api/agent_builder/tools/_execute
{
  "tool_id": "example-books-esql-tool",
  "tool_params": {
    "maxYear": 1960, <1>
    "limit": 2 <2>
  }
}
```
1. Find books published before 1960
2. Return only the top 2 results
