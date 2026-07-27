---
navigation_title: Analyze with AI
applies_to:
  stack: ga 9.5
  serverless: ga
products:
  - id: kibana
  - id: security
  - id: observability
  - id: cloud-serverless
description: Send a case to an AI chat conversation to summarize it or use it as context.
---

# Analyze a case with AI [analyze-cases-with-ai]

Send a case to an {{agent-builder}} chat conversation to summarize it or use it as context for follow-up questions.

## Before you begin [analyze-cases-with-ai-prereqs]

Make sure the following requirements are met:

- [{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md) must be available, with the Agent chat experience selected.
- At least an Enterprise subscription ({{stack}}) or the appropriate [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md) ({{serverless-short}}).
- The `xpack.cases.chat.enabled` setting must be `true`. It's `false` by default.

## Send a case to a chat conversation [analyze-cases-with-ai-send]

To analyze a case, open it from the **Cases** page and use one of the following actions in the case details header:

- **Add to chat**: Opens a new {{agent-builder}} conversation with the current case attached as context. You send the first message when you're ready.
- **Summarize case**: Opens a conversation with the case attached and a pre-filled prompt that asks the agent to summarize the case and suggest next steps.

### What the agent receives [analyze-cases-with-ai-context]

The attached context includes the following case details:

- Case ID
- Title
- Description
- Status
- Severity
- Tags
- Assignees
- Category
- Created and updated timestamps
- Alert, comment, attachment, and observable counts
- Connector name
- A link back to the case

### What you can do with a case in a chat [analyze-cases-with-ai-actions]

After a case is attached, you can ask the agent to act on it directly from the conversation. For example, you can:

- Add case comments. For example, after the agent summarizes a case, you can ask it to add that summary as a comment.
- Update case metadata, such as the status, severity, tags, category, title, and description.
- Change the assignees.
- Add attachments, such as alerts, events, or observables.

### Keep the case and chat in sync [analyze-cases-with-ai-sync]

If you keep the chat open, the case page updates in real time to show any changes the agent makes.
