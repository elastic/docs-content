---
navigation_title: Troubleshooting
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/playground-troubleshooting.html
applies_to:
  stack: preview 9.0, beta 9.1
  serverless: beta
products:
  - id: kibana
---

# Troubleshooting RAG Playground [playground-troubleshooting]

Dense vectors are not searchable
:   Embeddings must be generated using the [inference processor](elasticsearch://reference/enrich-processor/inference-processor.md) with an ML node.

Context length error
:   You’ll need to adjust the size of the context you’re sending to the model. Refer to [Optimize model context](playground-context.md).

LLM credentials not working
:   Under **LLM settings**, use the {icon}`wrench` button to edit your GenAI connector settings.

Poor answer quality
:   Check the retrieved documents to verify if they are valid. Adjust your {{es}} queries to improve the relevance of the documents retrieved. Refer to [View and modify queries](playground-query.md).

    You can update the initial instructions to be more detailed. This is called *prompt engineering*. Refer to this [OpenAI guide](https://platform.openai.com/docs/guides/prompt-engineering) for more information.

    You might need to click **⟳ Clear chat** to clear chat history and start a new conversation. If you mix topics, the model will find it harder to generate relevant responses.


