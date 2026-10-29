---
navigation_title: Triage alerts with AI
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/assistant-triage.html
  - https://www.elastic.co/guide/en/serverless/current/security-triage-alerts-with-elastic-ai-assistant.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Triage alerts

[{{agent-builder}}](/solutions/security/ai/agent-builder/agent-builder.md) helps you triage alerts faster. Attach an alert to a conversation, and the agent pulls its details, finds related alerts that share hosts, users, or IP addresses, checks entity risk, correlates with {{elastic-sec}} Labs threat intelligence, and recommends a disposition. You can then ask follow-up questions and generate a report for your case.

If you use AI Assistant, refer to [Use AI Assistant (deprecated)](#triage-alerts-ai-assistant).

## Triage alerts with {{agent-builder}} [triage-alerts-agent-builder]

```{applies_to}
stack: ga 9.4+
serverless:
  security: ga
```

These steps use the [Elastic AI Agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#elastic-ai-agent) with the [`alert-analysis`](/solutions/security/ai/agent-builder/skills-use-cases.md#alert-triage-and-investigation) skill. For more example prompts, refer to [Security use cases for {{agent-builder}}](/solutions/security/ai/agent-builder/skills-use-cases.md).

### Triage a specific alert [triage-alerts-agent-builder-single]

1. From the Alerts table, click an alert's **View details** button.
2. In the alert details flyout, click **Add to chat**. {{agent-builder}} opens a new conversation with the alert attached and a suggested prompt that asks for a structured alert summary.
3. Send the suggested prompt, or edit it first. The agent analyzes the alert and its context, then recommends whether it's a true positive, benign true positive, false positive, or needs more data.
4. Ask follow-up questions, add information, or request clarification. For example:

   * "Find alerts related to this one over the last 7 days."
   * "Should we escalate this alert?"

{applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview` To control which alert field values are anonymized before they're sent to the LLM, go to **Stack Management** → **AI** → **Anonymization**.

### Triage multiple alerts [triage-alerts-agent-builder-multiple]

```{applies_to}
stack: ga 9.5+
serverless:
  security: ga
```

Select up to 100 alerts in the Alerts table, then click **Selected *x* alerts** → **Add to chat**. The agent can then assess the alerts together and identify which ones to prioritize. For details, refer to [Add alerts to chat](/solutions/security/detect-and-alert/manage-detection-alerts.md#add-alerts-to-chat).

### Generate triage reports [triage-alerts-agent-builder-reports]

After the agent analyzes one or more alerts, ask it to document the incident for stakeholders. For example:

* "Generate a detailed report about this incident including timeline, impact analysis, and response actions."
* "Generate a summary of this incident and the related alerts."
* "Provide more details on the mitigation strategies used."

To keep a record for your team, add the alert to a [case](/solutions/security/investigate/security-cases.md): in the alert details flyout, click **Take action** → **Add to existing case** or **Add to new case**.

{applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview` You can also ask the agent to create a case or add its findings to an existing one, for example "Add this report as a comment on the case for this alert." The agent uses the [`cases-management`](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md#agent-builder-cases-management-skill) skill.

### Example alert triage workflow [triage-alerts-agent-builder-example]

**Scenario:** You're investigating an alert: "Multiple Failed Logins Followed by Success - user: jsmith"

:::::{stepper}

::::{step} Attach the alert and get an initial analysis
1. From the **Alerts** table, click **View details**.
2. Click **Add to chat**. The alert is attached to a new conversation.
3. Send the suggested prompt. The agent returns an initial assessment of the alert.
::::

::::{step} Assess criticality and context
Ask the agent:

- "Is user jsmith typically logging in from this IP address?"
- "Are there other suspicious activities from this user in the last 24 hours?"
- "What are the risk scores for user jsmith and the host they logged in to?"
::::

::::{step} Investigate related activity
If the agent flags concerns, investigate further. Ask it to:

- "Hunt for all recent activity from user jsmith."
- "Find other users logging in from this IP address."
::::

::::{step} Make a determination
Based on the agent's analysis, determine whether you're dealing with a potential threat:

- **False positive**: User was traveling, this is expected behavior.
  - Immediate action: Add a note to the alert, and close it as a false positive.
  - Future action: Add a rule exception to prevent similar alerts.

- **True positive**: Behavior indicates a potential attack. In response:
  - Escalate according to your organization's incident response plan.
  - Create a case to track the investigation.
::::

::::{step} Document your findings
1. In the alert details flyout, click **Take action** → **Add to existing case** or **Add to new case**.
2. Ask the agent for a report, then add it to the case. {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview` You can ask the agent to add it for you.
3. Change the alert's status to `Acknowledged`.
::::

:::::

## Use AI Assistant (deprecated) [triage-alerts-ai-assistant]

```{applies_to}
stack: ga 9.0-9.5, deprecated 9.6+
serverless:
  security: deprecated
```

::::{include} /solutions/_snippets/security-ai-assistant-deprecated.md
::::

Elastic AI Assistant can help you enhance and streamline your alert triage workflows by assessing multiple recent alerts in your environment, and helping you interpret an alert and its context.

When you view an alert in {{elastic-sec}}, details such as related documents, hosts, and users appear alongside a synopsis of the events that triggered the alert. This data provides a starting point for understanding a potential threat. AI Assistant can answer questions about this data and offer insights and actionable recommendations to remediate the issue.

To enable AI Assistant to answer questions about alerts, you need to provide alert data as context for your prompts. You can either provide multiple alerts using the [Knowledge Base](/solutions/security/ai/ai-assistant-knowledge-base.md) feature, or provide individual alerts directly.

### Use AI Assistant to triage multiple alerts [ai-assistant-triage-alerts-knowledge-base]

Enable the [Knowledge Base](/solutions/security/ai/ai-assistant-knowledge-base.md) **Alerts** setting to send AI Assistant data for up to 500 alerts as context for each of your prompts. Use the slider on the Security AI settings' **Knowledge Base** tab to select the number of alerts to send to AI Assistant.

For more information, refer to [Knowledge Base](/solutions/security/ai/ai-assistant-knowledge-base.md).

### Use AI Assistant to triage a specific alert [ai-assistant-triage-alerts-instructions]

Once you have chosen an alert to investigate:

1. Click its **View details** button from the Alerts table.
2. In the alert details flyout, click **Chat** to launch the AI assistant. Data related to the selected alert is automatically added to the prompt.
3. Click **Alert (from summary)** to view which alert fields will be shared with AI Assistant.

   :::{note}
   For more information about selecting which fields to send, and to learn about anonymizing your data, refer to [AI Assistant](/solutions/security/ai/ai-assistant.md).
   :::

4. (Optional) Click a quick prompt to use it as a starting point for your query, for example **Alert summarization**. Improve the quality of AI Assistant’s response by customizing the prompt and adding detail.

   Once you’ve submitted your query, AI Assistant will process the information and provide a detailed response. Depending on your prompt and the alert data that you included, its response can include a thorough analysis of the alert that highlights key elements such as the nature of the potential threat, potential impact, and suggested response actions.

5. (Optional) Ask AI Assistant follow-up questions, provide additional information for further analysis, and request clarification. The response is not a static report.

### Generate triage reports [ai-triage-reportgen]

Elastic AI Assistant can streamline the documentation and report generation process by providing clear records of security incidents, their scope and impact, and your remediation efforts. You can use AI Assistant to create summaries or reports for stakeholders that include key event details, findings, and diagrams. Once AI Assistant has finished analyzing one or more alerts, you can generate reports by using prompts such as:

* “Generate a detailed report about this incident including timeline, impact analysis, and response actions. Also, include a diagram of events.”
* “Generate a summary of this incident/alert and include diagrams of events.”
* “Provide more details on the mitigation strategies used.”

After you review the report, click **Add to existing case** at the top of AI Assistant’s response. This allows you to save a record of the report and make it available to your team.

:::{image} /solutions/images/security-ai-triage-add-to-case.png
:alt: An AI Assistant dialogue with the add to existing case button highlighted
:screenshot:
:::

### Example alert triage workflow [triage-alerts-ai-assistant-example]

This section shows an example workflow for triaging a specific alert.

**Scenario:** You are investigating an alert: "Multiple Failed Logins Followed by Success - user: jsmith"

:::::{stepper}

::::{step} Open Alert and Generate Initial Analysis
1. From the **Alerts** table, click **View details**. 
2. Click **Chat** to open AI Assistant. The alert information is automatically attached.
3. Click the **Alert summarization** quick prompt. AI Assistant shared an initial alert assessment.
::::

::::{step} Assess Criticality and Context
Ask AI Assistant:

- "Is user jsmith typically logging in from [this IP/location]?"
- "Are there other suspicious activities from this user in the last 24 hours?"
- "What's the risk score for the source IP?"
::::

::::{step} Investigate Related Activity
If AI Assistant flags concerns, investigate further. Ask AI Assistant to:

- "Generate an {{esql}} query to find all recent activity from user jsmith".
- "Generate an {{esql}} query to find other users logging in from this IP".
::::

::::{step} Make a Determination
Based on your initial AI-assisted analysis, determine whether you're dealing with a potential threat:

- **False Positive**: User was traveling, this is expected behavior.
  - Immediate action: Add note to alert, close as false positive.
  - Future action: Add a rule exception to prevent similar alerts.

- **True Positive**: Behavior indicates a potential attack. In response:
  - Escalate according to your organization's incident response plan.
  - Create a case to track the investigation.
::::

::::{step} Document Your Findings
1. From AI Assistant, click **Add to case** on key messages.
2. Go to **Cases**, add your case notes.
3. Go back to the alert and change its status to `Acknowledged`.
::::

:::::

## Related: Automate triage with workflows [ai-triage-related-workflows]

The interactive flow above is one way to triage; you can also encode the same job as a declarative automation that runs without an analyst in the loop:

- [Triage a security alert into a case](/explore-analyze/workflows/use-cases/security/automate-security-operations/alert-triage-with-case.md): Enrich an alert, open a case, attach observables, isolate the host, and notify the on-call analyst.
- [Triage alerts with an AI agent](/explore-analyze/workflows/use-cases/security/automate-security-operations/ai-driven-alert-triage.md): Invoke an {{agent-builder}} agent on each Attack Discovery alert, attach the analysis to a case, and post a Slack summary.
