---
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

Elastic AI Assistant can help you enhance and streamline your alert triage workflows by assessing multiple recent alerts in your environment, and helping you interpret an alert and its context.

When you view an alert in {{elastic-sec}}, details such as related documents, hosts, and users appear alongside a synopsis of the events that triggered the alert. This data provides a starting point for understanding a potential threat. AI Assistant can answer questions about this data and offer insights and actionable recommendations to remediate the issue.

To enable AI Assistant to answer questions about alerts, you need to provide alert data as context for your prompts. You can either provide multiple alerts using the [Knowledge Base](/solutions/security/ai/ai-assistant-knowledge-base.md) feature, or provide individual alerts directly.


## Use AI Assistant to triage multiple alerts [ai-assistant-triage-alerts-knowledge-base]

Enable the [Knowledge Base](/solutions/security/ai/ai-assistant-knowledge-base.md) **Alerts** setting to send AI Assistant data for up to 500 alerts as context for each of your prompts. Use the slider on the Security AI settings' **Knowledge Base** tab to select the number of alerts to send to AI Assistant.

For more information, refer to [Knowledge Base](/solutions/security/ai/ai-assistant-knowledge-base.md).


## Use AI Assistant to triage a specific alert [ai-assistant-triage-alerts-instructions]

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

## Generate triage reports [ai-triage-reportgen]

Elastic AI Assistant can streamline the documentation and report generation process by providing clear records of security incidents, their scope and impact, and your remediation efforts. You can use AI Assistant to create summaries or reports for stakeholders that include key event details, findings, and diagrams. Once AI Assistant has finished analyzing one or more alerts, you can generate reports by using prompts such as:

* “Generate a detailed report about this incident including timeline, impact analysis, and response actions. Also, include a diagram of events.”
* “Generate a summary of this incident/alert and include diagrams of events.”
* “Provide more details on the mitigation strategies used.”

After you review the report, click **Add to existing case** at the top of AI Assistant’s response. This allows you to save a record of the report and make it available to your team.

:::{image} /solutions/images/security-ai-triage-add-to-case.png
:alt: An AI Assistant dialogue with the add to existing case button highlighted
:screenshot:
:::


## Example alert triage workflow

This section shows an example workflow for triaging a specific alert.

**Scenario:** You are investigating an alert: "Multiple Failed Logins Followed by Success - user: jsmith"

**Step 1: Open Alert and Generate Initial Analysis**
1. From the **Alerts** table, click **View details**. 
2. Click **Chat** to open AI Assistant. The alert information is automatically attached.
3. Click the **Alert summarization** quick prompt. AI Assistant shared an initial alert assessment.

**Step 2: Assess Criticality and Context**
Ask AI Assistant:
- "Is user jsmith typically logging in from [this IP/location]?"
- "Are there other suspicious activities from this user in the last 24 hours?"
- "What's the risk score for the source IP?"

**Step 3: Investigate Related Activity**
If AI Assistant flags concerns, investigate further. Ask AI Assistant to:
- "Generate an {{esql}} query to find all recent activity from user jsmith".
- "Generate an {{esql}} query to find other users logging in from this IP".

**Step 4: Make a Determination**
Based on your initial AI-assisted analysis, determine whether you're dealing with a potential threat:

- **False Positive**: User was traveling, this is expected behavior.
  - Immediate action: Add note to alert, close as false positive.
  - Future action: Add a rule exception to prevent similar alerts.
  
- **True Positive**: Behavior indicates a potential attack.
In response to a potential credential compromise, immediately:
  - Escalate according to your organization's incident response plan.
  - Create a case to track the investigation.

**Step 5: Document Your Findings**
1. From AI Assistant, click **Add to case** on key messages.
2. Go to **Cases**, add your case notes.
3. Go back to the alert and change its status to `Acknowledged`.