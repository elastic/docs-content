---
applies_to:
  stack: ga 9.1
  serverless:
    security: all
products:
  - id: security
---


# Use AI Assistant's Knowledge Base to Supercharge Security Operations

This guide walks you through an example of how you can give custom information to the AI Assistant to customize it for your needs and improve the quality of its responses. It can remember everything from threat hunting playbooks, to on-call rotations, security research, infrastructure information, your team's internal communications from platforms like Slack or Teams, and more — constrained only by your creativity.

## Prerequisites

Before following this guide, review the [Knowlege Base](/solutions/security/ai/ai-assistant-knowledge-base.md) topic for general information and prerequisites, and [enable knowledge base](/solutions/security/ai/ai-assistant-knowledge-base.md#enable-knowledge-base).

## Step 3: Add Knowledge Sources

### Add Individual Documents

- Click **New → Document** in the Knowledge Base tab.
- Name the document, choose sharing (Global/Private), and enter content in Markdown.
- Optionally mark as "Required knowledge" to always include as context.

### Add Indices

- Click **New → Index**.
- Specify index name, sharing, semantic text field(s), data description, query instructions, and output fields.
- Indices must have at least one [semantic text](https://www.elastic.co/guide/en/elasticsearch/reference/current/semantic-text.html) field.

### Add Data via Connectors or Web Crawlers

- Use Elastic connectors (GitHub, Jira, Google Drive, S3, etc.) or web crawlers to ingest external data into indices.
- Add those indices to the Knowledge Base as above.

> _Comment: Confirm if there are any limitations on connector types or index sizes for Knowledge Base ingestion._

## Step 4: Use Knowledge Base in Conversations

- When enabled, the AI Assistant automatically leverages Knowledge Base entries to inform its responses.
- You can instruct the assistant to "remember" information during chat (creates a private document).
- Required knowledge entries are always included as context.

## Step 5: Manage and Share Knowledge

- Entries can be edited, deleted, or marked as required.
- Global entries affect all users in the space; private entries are user-specific.
- Elastic Security Labs research is pre-populated as global knowledge.

## Best Practices

- Include operational details (on-call rotations, escalation contacts, infrastructure maps).
- Add threat intelligence feeds and SOC playbooks.
- Use connectors to keep knowledge sources up-to-date automatically.
- Monitor token limits—too much context may exceed LLM limits.

## Troubleshooting & Known Limitations

- Token/context window limits depend on the selected LLM model.
- Large indices or too many alerts may cause errors—reduce context size if needed.
- ML node sizing and autoscaling are critical for performance.

## Additional Resources

- [Knowledge Base](https://www.elastic.co/guide/en/security/current/ai-assistant-knowledge-base.html)
- []
- [Ingest data with Elastic connectors](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-connectors.html)
