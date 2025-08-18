---
applies_to:
  stack: ga 9.1
  serverless:
    security: all
products:
  - id: security
---


# Use the AI Assistant's Knowledge Base to Supercharge Security Operations

AI Assistant Knowledge Base feature lets you provide custom, organization-specific context to the AI Assistant, making its responses more accurate, relevant, and actionable. By adding documents, indices, and external data sources, you can tailor the assistant to your environment, SOC strategy, threat intelligence, and operational workflows.

## Overview

- **What is the Knowledge Base?**
  - A feature that allows the AI Assistant to recall and use custom documents and indices as context for its responses.
  - Supports everything from infrastructure details, on-call rotations, SOC playbooks, threat intelligence, and more.
  - Entries can be private (user-specific) or global (shared across the space).

- **Why use it?**
  - Increases the utility of the Security AI Assistant by grounding answers in your organization’s real data and processes.
  - Enables richer, more actionable responses for incident response, alert investigation, and SOC operations.

## Prerequisites

- Required privileges: `Elastic AI Assistant: All` (with sub-privileges for Knowledge Base and Field Selection/Anonymization).
- Machine Learning enabled (minimum 4 GB ML node).
- [Enable autoscaling](https://www.elastic.co/guide/en/cloud/current/autoscaling.html) is recommended.
- Knowledge Base must be enabled for each Kibana space individually.

## Step 1: Enable the Knowledge Base

- **From an AI Assistant conversation:**
  - Open a chat, select a model, and click **Setup Knowledge Base** (button only appears if not already enabled).
- **From Security AI settings:**
  - Use the global search field to find "AI Assistant for Security".
  - On the **Knowledge Base** tab, click **Setup Knowledge Base**.

> _Comment: Confirm if enabling from the conversation is available in all environments or only certain versions._

## Step 2: Configure Alert Context

- AI Assistant can use up to N (configurable, up to 500) open or acknowledged alerts from the last 24 hours as context.
- Use the slider in the Knowledge Base tab to select how many alerts to include.
- Alerts are ordered by risk score and recency; building block alerts are excluded.

> _Comment: Confirm maximum number of alerts supported for context (docs mention up to 500, but token limits may apply)._

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

- [AI Assistant Knowledge Base documentation](https://www.elastic.co/guide/en/security/current/ai-assistant-knowledge-base.html)
- [Elastic Security Labs](https://www.elastic.co/security-labs)
- [Ingest data with Elastic connectors](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-connectors.html)
