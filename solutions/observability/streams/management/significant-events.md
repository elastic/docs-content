---
applies_to:
  serverless: ga
  stack: preview 9.1, ga 9.2
---

# Add significant events

Significant Events periodically runs a query on your stream to find important events. Significant events could be error messages, exceptions, or other log messages that are of interest to you.

To define significant events, either:

- **Generate significant events with AI:** (requires an [LLM connector](../../../security/ai/set-up-connectors-for-large-language-models-llm.md)) If you don't know what you're looking for, let AI suggest queries based on your data. This works by using the previously identified [features](./advanced.md#streams-advanced-features) in your Stream to create specific queries based on the data you have in your Stream. Then, select the suggestions that make sense to you.
- **Create significant events from a query:** If you know what you're looking for, write your own query to find important events.