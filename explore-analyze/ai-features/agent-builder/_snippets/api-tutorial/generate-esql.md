```console
POST kbn://api/agent_builder/tools/_execute
{
  "tool_id": "platform.core.generate_esql", <1>
  "tool_params": {
    "query": "Build an ES|QL query to get the book with the most pages", <2>
    "index": "kibana_sample_data_agents" <3>
  }
}
```
1. ID of the built-in {{esql}} generator tool
2. Natural language description of the desired query
3. Index to query
