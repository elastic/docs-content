---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/playground-troubleshooting.html
applies:
  stack:
  serverless:
---

# Troubleshooting [playground-troubleshooting]

::::{warning} 
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


Dense vectors are not searchable
:   Embeddings must be generated using the [inference processor](https://www.elastic.co/guide/en/elasticsearch/reference/current/inference-processor.html) with an ML node.

Context length error
:   You’ll need to adjust the size of the context you’re sending to the model. Refer to [Optimize model context](playground-context.md).

LLM credentials not working
:   Under **Model settings**, use the wrench button (🔧) to edit your GenAI connector settings.

Poor answer quality
:   Check the retrieved documents to see if they are valid. Adjust your {{es}} queries to improve the relevance of the documents retrieved. Refer to [View and modify queries](playground-query.md).

    You can update the initial instructions to be more detailed. This is called *prompt engineering*. Refer to this [OpenAI guide](https://platform.openai.com/docs/guides/prompt-engineering) for more information.

    You might need to click **⟳ Clear chat** to clear chat history and start a new conversation. If you mix topics, the model will find it harder to generate relevant responses.


