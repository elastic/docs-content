---
applies_to:
  stack: ga 9.1
  serverless:
    security: all
products:
  - id: security
---


# Use AI Assistant's Knowledge Base to improve response quality

You can use AI Assistant's Knowledge Base to give it information on anything from threat hunting playbooks, to on-call rotations, security research, infrastructure information, your team's internal communications from platforms like Slack or Teams, and more — constrained only by your creativity. This page guides you through ingesting data from various sources into AI Assistant's Knowledge Base, and shows how this can improve the quality of its responses in a threat response scenario. 

## Prerequisites

Before following this guide, review the [Knowledge Base](/solutions/security/ai/ai-assistant-knowledge-base.md) topic for general information and prerequisites, and [enable Knowledge Base](/solutions/security/ai/ai-assistant-knowledge-base.md#enable-knowledge-base).

## Add relevant data from various sources to Knowledge Base

AI Assistant is more useful for incident response when it can access information about your organization's specific infrastructure, threat hunting playbooks, personnel, and processes. How you can add this data to Knowledge Base depends on its format and structure. This section provides several examples of useful data and how to add it. 

### Add your Slack messages to Knowledge Base

You can add messages from Slack channels to Knowledge Base using the Slack content connector. For instance, if you have a Slack channel that contains information about ongoing incidents, you could include that information in Knowledge Base to give AI Assistant more context about what your security team is dealing with. 

1. Use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to find "Content connectors". Click **+ New Connector** to open the **Create a connector** interface.
2. Follow the steps to [create a content connector](/solutions/security/get-started/content-connectors.md). During setup, select `Slack`, then follow the steps to [configure a Slack connector](elasticsearch://reference/search-connectors/es-connectors-slack.md). This ingests your selected data into {{es}}.
3. Follow the instructions to [add an index to Knowledge Base](/solutions/security/ai/ai-assistant-knowledge-base.md#). Select the index you created while setting up your new connector.

### Add your on-call rotation to Knowledge Base

If you add information about who is responsible for security incidents at different dates and times to Knowledge Base, AI Assistant can help you quickly follow the correct escalation protocol for potential threats. 

If information about your on-call rotation is contained in a file, you can follow the steps to [add an individual file](/solutions/security/ai/ai-assistant-knowledge-base.md#add-specific-file) to Knowledge Base. 

However, you can also copy and paste the information to directly [add it as a markdown document](/solutions/security/ai/ai-assistant-knowledge-base.md#knowledge-base-add-knowledge-document). Adding it as a markdown document is fast and easy to update when the on-call rotation changes. 

:::{image} /solutions/images/security-knowledge-base-add-on-call-rotation.png
:alt: Knowledge base's Edit document entry menu showing a snippet of an on call rotation document
:::

Whichever method you use to add the information to Knowledge Base, consider making it **Required knowledge**. This will ensure that all of AI Assistant's responses are informed by the on-call rotation, even if your prompt doesn't specify that the information is relevant. This makes it more likely that AI Assistant will suggest appropriate escalation steps when you ask it about a threat.

### Add your threat hunting playbooks to Knowledge Base
 
If you have threat hunting playbooks stored in a GitHub repository, you can add them to Knowledge Base using the GitHub content connector. This enables AI Assistant to tell your team about your organization's standard practices for responding to a wide range of potential threats. 

1. Use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to find "Content connectors". Click **+ New Connector** to open the **Create a connector** interface.
2. Follow the steps to [create a content connector](/solutions/security/get-started/content-connectors.md). During setup, select `GitHub`, then follow the steps to [configure a GitHub connector](elasticsearch://reference/search-connectors/es-connectors-github.md). This ingests your selected data into {{es}}.
3. Follow the instructions to [add an index to Knowledge Base](/solutions/security/ai/ai-assistant-knowledge-base.md#). Select the index you created while setting up your new connector.

::::{note}
The GitHub connector can only ingest issues, PRs and the following file types: `.markdown`, `.md`, `.rst`.
::::

## Use Knowledge Base in conversations

AI Assistant will use the information you've added to Knowledge Base to inform its responses to your prompts. With the information we've added in this guide, you can ask questions like:

- Is this alert related to any ongoing incidents?
- Who should I contact to escalate this potential threat?
- What should I do to respond to this threat?

Be creative, and experiment with adding different types of information to optimize AI Assistant for your team's purposes.

## Video demo: investigate an Attack Discovery using AI Assistant's Knowledge Base

The following video demo starts with a potential threat identified using Attack Discovery, and shows how the information you've added to Knowledge Base greatly increases AI Assistant's ability to help guide your team's incident response (click to play video):

[![Add knowledge index video](https://play.vidyard.com/SGrcygEFBCEJRURGjR8sMh.jpg)](https://videos.elastic.co/watch/SGrcygEFBCEJRURGjR8sMh?)

## Additional Resources

- Learn more about [Knowledge Base](https://www.elastic.co/guide/en/security/current/ai-assistant-knowledge-base.html)
- Learn to [Ingest data with Elastic connectors](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-connectors.html)
