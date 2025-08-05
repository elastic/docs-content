---
navigation_title: Triage alerts
applies_to:
  serverless:
    security: preview
---

# Triage alerts in EASE

Once you've ingested your alerts to Elastic AI SOC Engine (EASE), you can view, track, and analyze them from the **Alert summary** page.

:::{image} /solutions/images/security-ease-alerts-summary.png
:alt: The Alert summary page of an EASE project
:::

## View alert details

An alert's details flyout shows its basic information, highlighted fields, and any associated attack discoveries. It also enables you to generate an AI summary of the alert, or collaborate with AI Assistant to continue your investigation. 

To open the alert details flyout, select the **Expand** button ({icon}`expand`) from the alert's row in the alerts table.

:::{image} /solutions/images/security-ease-alert-flyout.png
:alt: The Alert summary page of an EASE project
:::

You can take several actions from the alert details flyout:

- **Generate insights**: To generate an AI description of the alert with recommended actions, click **Generate insights**. (The connector used here is the default LLM for your project. To update it, navigate to the **Advanced settings** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), and update the **Default AI Connector**.)

   :::{note}
   The recommended actions are informed by any relevant custom knowledge you may have added to the AI Assistant's [knowledge base](/solutions/security/ai/ai-assistant-knowledge-base.md). For example, if you have specified a particular teammate is responsible for a particular type of alert of part of your infrastructure, it would recommend contacting that person. 
   :::

- **Ask AI Assistant**: To start a conversation with [AI Assistant](/solutions/security/ai/ai-assistant.md), select one of the suggested prompts or click **Ask AI Assistant**. 
- **Add to case**: To add an alert to a new or existing case, scroll to the bottom and click **Take action**, then **Add to existing case** or **Add to new case**. 
- **Apply alert tags**: To add tags to an alert, scroll to the bottom of its flyout and click **Take action**, then **Apply alert tags**. (To create new tags, navigate to the **Advanced settings** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), and update the **Alert tagging options**.)