---
applies_to:
  stack: ga 9.1
  serverless:
    security: all
products:
  - id: security
---


# Use AI Assistant's Knowledge Base to improve response quality

You can use AI Assistant's Knowledge Base to give it information on anything from threat hunting playbooks, to on-call rotations, security research, infrastructure information, your team's internal communications from platforms like Slack or Teams, and more — constrained only by your creativity. This page guides you through an example of how to ingest data from various sources into AI Assistant's Knowledge Base, and shows how this can improve the quality of its responses in a threat response scenario. 

## Prerequisites

Before attempting to follow this guide, review the [Knowlege Base](/solutions/security/ai/ai-assistant-knowledge-base.md) topic for general information and prerequisites, and [enable Knowledge Base](/solutions/security/ai/ai-assistant-knowledge-base.md#enable-knowledge-base).

## Add relevant data from various sources to Knowledge Base

AI Assistant is more useful for incident response when it can access information about your organization's specific infrastructure, threat hunting playbooks, personnel, and processes. How you can add this data to Knowledge Base depends on its format and structure. This section provides several examples of useful data and how to add it.

### Add your Slack messages to Knowledge Base

You can add messages from Slack channels to Knowledge Base using the Slack content connector. For instance, if you have a Slack channel that contains information about ongoing incidents, you could include that information in Knowledge Base to give AI Assistant more context about what your security team is dealing with. 

1. Use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to find "Content connectors". Click **+ New Connector** to open the **Create a connector** interface.
2. Follow the steps to [create a content connector](/solutions/security/get-started/content-connectors.md). This ingests your selected data into {{es}}. During setup, select `Slack`, and configure the connector to ingest your desired data.
3. Follow the instructions to [add an index to Knowledge Base](/solutions/security/ai/ai-assistant-knowledge-base.md#). Select the index you created while setting up your new connector.

### Add your on-call rotation to Knowledge Base

If you add information about who is responsible for security incidents at different dates and times to Knowledge Base, AI Assistant can help you quickly follow the correct escalation protocol for potential threats. 

If information about your on-call rotation is contained in a file, you can follow the steps to [add an individual file](/solutions/security/ai/ai-assistant-knowledge-base.md#add-specific-file) to Knowledge Base. 

However, you can also copy and paste the information to directly [add it as a markdown document](/solutions/security/ai/ai-assistant-knowledge-base.md#knowledge-base-add-knowledge-document). Adding it as a markdown document is fast, and easy to update when the on-call rotation changes. 

### Add your threat hunting playbooks to Knowledge Base
 
If you have threat hunting playbooks stored in a GitHub repository, you can add them to Knowledge Base using the GitHub content connector. This enables AI Assistant to tell your team about your organization's standard practices for responding to a wide range of potential threats. 

1. Use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to find "Content connectors". Click **+ New Connector** to open the **Create a connector** interface.
2. Follow the steps to [create a content connector](/solutions/security/get-started/content-connectors.md). This ingests your selected data into {{es}}. During setup, select `GitHub`, and configure the connector to ingest your desired data.
3. Follow the instructions to [add an index to Knowledge Base](/solutions/security/ai/ai-assistant-knowledge-base.md#). Select the index you created while setting up your new connector.


:::{image} /solutions/images/security-knowledge-base-add-on-call-rotation.png
:alt: Knowledge base's Edit document entry menu showing a snippet of an on call rotation document
:::

Whichever method you use to add the information to Knowledge Base, consier making it **Required knowledge**. This will ensure that all of AI Assistant's responses are informed by the on-call rotation, even if your prompt doesn't specify that the information is relevant. This makes it more likely that AI Assistant will suggest appropriate escalation steps when you ask it about a threat.


## Use Knowledge Base in conversations

AI Assistant will automatically use information you've added to Knowledge Base to inform its responses to your questions. With the information we've added in this example
- You can instruct the assistant to "remember" information during chat (creates a private document).
- Required knowledge entries are always included as context.

## Step 5: Manage and Share Knowledge

- Entries can be edited, deleted, or marked as required.
- Global entries affect all users in the space; private entries are user-specific.
- Elastic Security Labs research is pre-populated as global knowledge.

## Additional Resources

- [Knowledge Base](https://www.elastic.co/guide/en/security/current/ai-assistant-knowledge-base.html)
- []
- [Ingest data with Elastic connectors](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-connectors.html)
