```console
POST kbn://api/agent_builder/agents
{
  "id": "books-search-agent", <1>
  "name": "Books Search Helper", <2>
  "description": "Hi! I can help you search and analyze the books in our sample data collection.", <3>
  "labels": ["books", "sample-data", "search"], <4>
  "avatar_color": "#BFDBFF", <5>
  "avatar_symbol": "📚", <6>
  "configuration": {
    "instructions": "You are a helpful agent that assists users in searching and analyzing book data from the kibana_sample_data_agents index. Help users find books by author, title, or analyze reading patterns.", <7>
    "tools": [ <8>
      {
        "tool_ids": [
          "example-books-esql-tool",
          "platform.core.search",
          "platform.core.list_indices",
          "platform.core.get_index_mapping",
          "platform.core.get_document_by_id"
        ]
      }
    ]
  }
}
```
1. Unique identifier for the agent
2. Display name shown in the UI
3. Greeting message users see when starting a conversation
4. Labels for organizing and filtering agents
5. Avatar background color (hex code)
6. Avatar symbol or emoji
7. System instructions that guide the agent's behavior
8. Tools the agent can use - includes your custom tool and built-in tools
