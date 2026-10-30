---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/attack-discovery-ai-assistant-incident-reporting.html
  - https://www.elastic.co/guide/en/serverless/current/security-ai-usecase-incident-reporting.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Identify, investigate, and document threats

Together, [Attack Discovery](/solutions/security/ai/attack-discovery/index.md) and [{{agent-builder}}](/solutions/security/ai/agent-builder/agent-builder.md) can help you identify and mitigate threats, investigate incidents, and generate incident reports in various languages so you can monitor and protect your environment.

In this guide, you'll learn how to:

* [Use Attack Discovery to identify threats](#use-case-incident-reporting-use-attack-discovery-to-identify-threats)
* [Use {{agent-builder}} to analyze a threat](#use-case-incident-reporting-agent-builder-analyze)
* [Document the incident in a case](#use-case-incident-reporting-agent-builder-case)
* [Translate incident information to a different human language](#use-case-incident-reporting-agent-builder-translate)

If you use AI Assistant, refer to [Use AI Assistant (deprecated)](#use-case-incident-reporting-ai-assistant).

## Use Attack Discovery to identify threats [use-case-incident-reporting-use-attack-discovery-to-identify-threats]

Attack Discovery can detect a wide range of threats by finding relationships among alerts that may indicate a coordinated attack. This enables you to comprehend how threats move through and affect your systems. Attack Discovery generates a detailed summary of each potential threat and can highlight avenues for further investigation. Learn how to [get started with Attack Discovery](/solutions/security/ai/attack-discovery/index.md).

:::{important}
To ensure that Attack Discovery analyzes related alerts together (and can therefore identify their connections), pay attention to the [alert filtering](/solutions/security/ai/attack-discovery/index.md) settings. This allows you to target Attack Discovery at specific groups of alerts, such as those related to a particular host, user, date and time, incident, or customer.

:::

:::{image} /solutions/images/security-attck-disc-11-alerts-disc.png
:alt: An Attack Discovery card showing an attack with 11 related alerts
:::

In this example, Attack Discovery found connections between thirteen alerts, and used them to identify and describe an attack chain.

After Attack Discovery outlines your threat landscape, use AI chat to analyze a threat in detail.

## Use {{agent-builder}} to analyze a threat [use-case-incident-reporting-agent-builder-analyze]

```{applies_to}
stack: ga 9.4+
serverless:
  security: ga
```

To start a conversation with a discovery as context, click **Add to chat** on a discovery on the **Attack Discovery** page. {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` Or, from the [**Attacks** view](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md), select **Take actions** → **Add to chat** on an attack.

The [Elastic AI Agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#elastic-ai-agent) can compile essential data and suggest next steps to help you plan an effective response. Ask it questions such as:

* "How can I remediate this threat?"
* "What {{esql}} query would isolate actions taken by this user?"
* "What are the risk scores for the hosts and users involved?" (requires [entity risk scoring](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md))

The agent uses [Security skills](/solutions/security/ai/agent-builder/skills-use-cases.md) such as `alert-analysis`, `entity-analytics`, and `threat-hunting` to answer. To learn more about using {{agent-builder}} for {{esql}}, refer to [Generate, customize, and learn about {{esql}} queries](/solutions/security/ai/generate-customize-learn-about-esorql-queries.md).

{applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` You can also start in chat and have the agent run Attack Discovery for you, for example "Investigate lateral movement involving host-12 over the last 24 hours." Refer to [Run Attack Discovery from {{agent-builder}}](/solutions/security/ai/attack-discovery/run-attack-discovery-from-agent-builder.md).

## Document the incident in a case [use-case-incident-reporting-agent-builder-case]

```{applies_to}
stack: ga 9.4+
serverless:
  security: ga
```

[Cases](/solutions/security/investigate/security-cases.md) centralize relevant details in one place for easy sharing with stakeholders. To add a discovery and its alerts to a case, select **Take action** → **Add to new case** or **Add to existing case** on the discovery. {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` Or, on the **Attacks** view, select **Take actions** → **Add to new case** or **Add to existing case** on the attack.

Ask the agent for an incident report, remediation steps, or a summary, then add them to the case.

{applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview` You can also ask the agent to create the case or add its findings to an existing one, for example "Add these remediation steps as a comment on the case for this attack." The agent uses the [`cases-management`](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md#agent-builder-cases-management-skill) skill.

## Translate incident information to a different language [use-case-incident-reporting-agent-builder-translate]

```{applies_to}
stack: ga 9.4+
serverless:
  security: ga
```

The agent can translate its findings into other human languages, helping to enable collaboration among global security teams, and making it easier to operate within multilingual organizations.

After the agent provides information in one language, ask it to translate its response. For example, if it provides remediation steps for an incident, ask it to "Translate these remediation steps into Japanese." You can then add the translated output to a case.

::::{note}
All LLMs can make mistakes, so review translations before you share them.
::::

## Use AI Assistant (deprecated) [use-case-incident-reporting-ai-assistant]

```{applies_to}
stack: ga 9.0-9.5, deprecated 9.6+
serverless:
  security: deprecated
```

### Use AI Assistant to analyze a threat [use-case-incident-reporting-use-ai-assistant-to-analyze-a-threat]

From a discovery on the **Attack Discovery** page, click **View in AI Assistant** or **Add to chat** to start a chat that includes the discovery as context.

:::{image} /solutions/images/security-attck-disc-remediate-threat.gif
:alt: A dialog with AI Assistant that has the discovery as context
:::

AI Assistant can quickly compile essential data and provide suggestions to help you generate an incident report and plan an effective response. You can ask it to provide relevant data or answer questions, such as “How can I remediate this threat?” or “What {{esql}} query would isolate actions taken by this user?”

:::{image} /solutions/images/security-attck-disc-esql-query-gen-example.png
:alt: An AI Assistant dialog in which the user asks for a purpose-built {{esql}} query
:::

This image shows an {{esql}} query generated by AI Assistant in response to a user prompt. Learn more about [using AI Assistant for {{esql}}](/solutions/security/ai/generate-customize-learn-about-esorql-queries.md).

At any point in a conversation with AI Assistant, you can add data, narrative summaries, and other information from its responses to {{elastic-sec}}'s case management system to generate incident reports.

### Generate reports [use-case-incident-reporting-create-a-case-using-ai-assistant]

From the AI Assistant dialog window, click **Add to case** (![Add to case icon](/solutions/images/security-icon-add-to-case.png "title =20x20")) next to a message to add the information in that message to a [case](/solutions/security/investigate/security-cases.md). Cases help centralize relevant details in one place for easy sharing with stakeholders.

If you add a message that contains a discovery to a case, AI Assistant automatically adds the attack summary and all associated alerts to the case. You can also add AI Assistant messages that contain remediation steps and relevant data to the case.

### Translate incident information to a different human language using AI Assistant [use-case-incident-reporting-translate]

:::{image} /solutions/images/security-attck-disc-translate-japanese.png
:alt: An AI Assistant dialog in which the assistant translates from English to Japanese
:::

AI Assistant can translate its findings into other human languages, helping to enable collaboration among global security teams, and making it easier to operate within multilingual organizations.

After AI Assistant provides information in one language, you can ask it to translate its responses. For example, if it provides remediation steps for an incident, you can instruct it to “Translate these remediation steps into Japanese.” You can then add the translated output to a case. This can help team members receive the same information and insights regardless of their primary language.

::::{note}
In our internal testing, AI Assistant translations preserved the accuracy of the original content. However, all LLMs can make mistakes, so use caution.
::::
