---
navigation_title: "Limitations & known issues"
applies_to:
  stack: preview 9.2
  deployment: 
    self: unavailable
  serverless:
    elasticsearch: preview
---

# Limitations and known issues in {{agent-builder}}

## Model Selection

Today we only use the `rainbow-sprinkles` model running on the Elastic Inference Service which is Claude 3.7, on Cloud / Serverless. Locally this picks the first AI connector available. Currently we do not have UI controls to select which connector (and therefore which model) to use. 


{{agent-builder}} has some limitations to be aware of:

Known Bugs
Unable to follow up with a question in a conversation (resolved in latest 9.2-snapshot, affects serverless)
Unable to use MCP server (resolved in latest 9.2-snapshot, affects serverless) 



We're continuously working to improve these areas and welcome your feedback to help shape the future development of {{agent-builder}}.