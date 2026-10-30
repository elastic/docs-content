---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/policies-page-ov.html
  - https://www.elastic.co/guide/en/serverless/current/security-policies-page.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Policies


The **Policies** page lists all of the integration policies configured for {{elastic-defend}}.

::::{admonition} Requirements
You must have the **{{elastic-defend}} Policy Management** [privilege](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md) or the appropriate user role to access this feature.
::::

Click on an integration policy’s name to configure its settings. For more information on configuring an integration policy, refer to [](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md).

:::{image} /solutions/images/security-policy-list.png
:alt: policy list
:screenshot:
:::

:::{tip}
:applies_to: {stack: ga 9.6+, serverless: ga}
To get help understanding policy settings, comparing policies, or assessing a change before you make it, use the [`elastic-defend-policy-management`](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md#agent-builder-elastic-defend-policy-management-skill) {{agent-builder}} skill. For example prompts, refer to [{{elastic-defend}} policy management](/solutions/security/ai/agent-builder/skills-use-cases.md#defend-policy-management).
:::
