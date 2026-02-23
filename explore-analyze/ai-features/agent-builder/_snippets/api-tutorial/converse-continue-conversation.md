```console
POST kbn://api/agent_builder/converse
{
  "input": "Can you find the longest book published before 1960?",
  "agent_id": "books-search-agent",
  "conversation_id": "<CONVERSATION_ID>" <1>
}
```

1. Use the conversation ID from the previous response to maintain context
