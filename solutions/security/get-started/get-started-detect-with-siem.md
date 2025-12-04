---
navigation_title: Detect and respond to threats with SIEM
description: An introduction to detecting threats with SIEM in {{elastic-sec}}.
applies_to:
  serverless:
    security: all
  stack:
products:
  - id: security
---

# Quickstart: Detect and respond to threats with SIEM

In this quickstart guide, we'll learn how to use some of {{elastic-sec}}'s SIEM features to detect, investigate, and respond to threats. 

## Prerequisites 

* You can follow this guide using any deployment. To get up and running quickly, we recommend [{{sec-serverless}}](/solutions/security/get-started.md#create-sec-serverless-project) with the **Security Analytics Complete** [feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md#elastic-sec-project-features). For a complete list of deployment options, refer to [](/deploy-manage/deploy.md#choosing-your-deployment-type). 
* If you're using the recommended integration in this guide, {{elastic-defend}}, then: 
  * Ensure you have the minimum [system requirements](/solutions/security/configure-elastic-defend/elastic-defend-requirements.md) to install {{elastic-defend}}. 
  * Ensure you grant the appropriate [{{elastic-defend}} sub-feature privileges](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md). At the least, you need `All` access for the **Endpoint List** and **Elastic Defend Policy Management** sub-features. 
* We recommend `manage` and `write` access to manage rules and alerts. Refer to [Detection requirements](/solutions/security/detect-and-alert/detections-requirements.md#enable-detections-ui) for the required cluster, index, and space privileges. 

## Add data using {{elastic-defend}}

Before you can begin using {{elastic-sec}}, you need to choose an integration to start collecting and analyzing your data. This guide uses the {{elastic-defend}} integration. {{elastic-defend}} collects data from endpoints and provides several features that help protect them against threats.  

:::::{stepper} 
::::{step} Install the Elastic Defend integration

:::{dropdown} Steps to install {{elastic-defend}}
1. On the **Get started** page, in the **Ingest your data** section, select **{{elastic-defend}}**, then click **Add {{elastic-defend}}**. Elastic has several integrations for you to choose from—so you can select one of our recommended integrations or another of your choice. 

    :::{note} 
    If you've added data through another integration besides {{elastic-defend}}, you can skip to [Add Elastic prebuilt detection rules](#add-elastic-prebuilt-detection-rules). 
    ::: 
2. On the next page that says, "Ready to add your first integration?", click **Add integration only (skip agent installation)**. The integration configuration page appears.
3. Give the {{elastic-defend}} integration a name and optional description.
4. Select the type of environment you want to protect—**Traditional Endpoints** or **Cloud Workloads**. For this guide, we'll select **Traditional Endpoints**. 
5. Select a configuration preset. Each preset comes with different default settings for {{agent}}, which you can further customize later by [configuring the {{elastic-defend}} integration policy](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md). For optimal endpoint protection, we recommend selecting **Complete EDR (Endpoint, Detection & Response)**. 
6. Enter a name for the agent policy in the **New agent policy name** field.
7. Click **Save and continue**. Next, click **Add {{agent}} to your hosts**. 
:::{image} /solutions/images/security-gs-siem-defend-flyout.png
:alt: Elastic Defend configuration
:screenshot:
:::
::::

::::{step} Add the Elastic Agent

[{{agent}}](/reference/fleet/index.md#elastic-agent) is a single, unified way to add monitoring for logs, metrics, and other types of data to a host. You'll need to install this component so it can monitor any malicious activity on your hosts. 

:::{dropdown} Steps to add {{agent}}
1. In the **Add agent** flyout that appears after you install the {{elastic-defend}} integration, you'll see the policy selected that you previously added. Leave the default enrollment token selected. 
2. Ensure that the **Enroll in {{fleet}}** option is selected. {{elastic-defend}} cannot be integrated with {{agent}} in standalone mode.
3. Select the appropriate platform or operating system for the host on which you're installing the agent, then copy the provided commands.
4.  On the host, open a command-line interface and navigate to the directory where you want to install {{agent}}. Paste and run the commands from {{fleet}} to download, extract, enroll, and start {{agent}}.
5. (Optional) Return to the **Add agent** flyout, and observe the **Confirm agent enrollment** and **Confirm incoming data** steps automatically checking the host connection. It may take a few minutes for data to arrive in {{es}}.
6. (Optional) After you have enrolled the {{agent}} on your host, you can click **View enrolled agents** to access the list of agents enrolled in {{fleet}}. Otherwise, select **Close**.

    The host will now appear on the **Endpoints** page in the {{security-app}} (**Assets** → **Endpoints**). It may take another minute or two for endpoint data to appear in {{elastic-sec}}.

:::{important}
If you’re using macOS, some versions may require you to grant {{elastic-endpoint}} Full Disk Access to different kernels, system extensions, or files. Refer to [Elastic Defend requirements](/solutions/security/configure-elastic-defend/elastic-defend-requirements.md) for more information.
:::
:::
::::

::::{step} Modify policy configuration settings

After you install the {{agent}} with {{elastic-defend}}, the Endpoint Security ({{elastic-defend}}) detection rule is automatically turned on and can generate detection or protection alerts.
You can also set up endpoint protections—such as preventions against malware, ransomware, memory threats, and other malicious behavior—on protected hosts.
This means that {{elastic-defend}} not only monitors these behaviors and generates an alert when they are detected, but also blocks them. Due to this maximum level of protection, we recommend modifying the policy to _detect_ instead of _prevent_ so that only an alert will be generated, and you can decide how to respond to the threat. Then, closely monitor which alerts and how many are generating over a specific time period before enabling higher protection, if needed. 

:::{dropdown} Steps to modify an endpoint policy
1. From the left navigation menu, go to **Assets** → **Endpoints** → **Policies**. 
2. From the list, select the policy you want to configure. The policy configuration page appears.
3. On the **Policy settings** tab, switch the protection level from `Prevent` to `Detect` for each protection. 
4. Review and configure the event collection and antivirus settings as appropriate. 
5. Once you're finished making changes, click **Save** in the lower-right corner to update the policy.  

:::{note}
For a comprehensive explanation of all endpoint protections and policy settings, refer to [Configure an integration policy](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md). 
:::
:::
:::::

## Add Elastic prebuilt detection rules

Detection rules allow you to monitor your environment by searching for source events, matches, sequences, or {{ml}} job anomaly results that meet their criteria. When a rule’s criteria are met, {{elastic-sec}} generates an alert. Although you can create your own rules tailored for your environment, Elastic ships out-of-the-box prebuilt rules that you can install. Remember that if you installed {{elastic-defend}}, the Endpoint Security rule is already turned on.

:::{dropdown} Steps to install and turn on prebuilt rules
1. On the **Get Started** page, scroll down to the **Configure rules and alerts** section. 
2. Click **Install Elastic rules**, then **Add Elastic rules**. The **Rules** page displays. 
3. At the top of the page, click **Add Elastic rules**. The badge next to it shows the number of prebuilt rules available for installation.  
4. Use the search bar and **Tags** filter to find the rules you want to install. For example, to filter by operating system, search for the appropriate OS (such as `macOS`) from the **Tags** menu. 
5. Once you've filtered the rules, confirm that the rules displayed are the ones you'd like to install. If you'd like to learn more about any rule before installing it, click on the rule name to expand the rule details flyout. Here's an example of one: 

    :::{image} /solutions/images/security-gs-siem-rule-details.png 
    :alt: Rule details flyout
    :screenshot:
    :::

6. Select the check box next to the rules you want to install. To select all rules on the page, select the check box to the left of the **Rule** column heading. We recommend installing all the rules for your operating system, but you can install whichever rules you're comfortable with to start. You can always install more later.  
7. Click ![Vertical boxes button](/solutions/images/serverless-boxesVertical.svg "") → **Install and enable** to install and start running the rules. Alternatively, after a rule is installed, you can turn it on from the installed rules table. Once you turn on a rule, it starts running on its configured schedule.

:::{image} /solutions/images/security-gs-siem-install-rules.png 
:alt: Alerts page with visualizations section collapsed
:screenshot:
:::
    
::::{tip}
{{elastic-sec}} regularly updates prebuilt rules to ensure they detect the latest threats. However, you must manually update these rules to the latest version. To learn how to do this, refer to [Update prebuilt rules](/solutions/security/detect-and-alert/install-manage-elastic-prebuilt-rules.md#update-prebuilt-rules).  To learn how to view and manage all detection rules, refer to [Manage detection rules](/solutions/security/detect-and-alert/manage-detection-rules.md). 
::::

:::

## Visualize and examine alert details 

Now that you've installed and turned on rules, it's time to monitor your {{sec-serverless}} project to see if you receive any alerts. Remember, an alert is generated if any of the rule's criteria are met. {{elastic-sec}} provides several tools for investigating security events:

* **Alerts table:** View all generated alerts in a comprehensive list, apply filters for a customized view, and drill down into details. 
* **Timeline:** Explore alerts in a central, interactive workspace. Create customized queries and collaborate on incident analysis by combining data from various sources.  
* **Visual event analyzer:** View a graphical timeline of processes  leading up to the alert and the events that occurred immediately after.
* **Session View:** Examine Linux process data and real-time data insights. 

To view a quick video tutorial on how to use these features, on the **Get Started** page, scroll down to **View alerts**, select a feature from the list, and click **Play Video** on the right. 

For this guide, let's take a closer look at how to visualize and examine alert details by viewing the **Alerts** page. 

:::{note}
If you don't have any alerts yet in your environment, that's great news! You can use the [Elastic demo server](https://demo.elastic.co/) to explore alerts. 
:::

To access the **Alerts** page, do one of the following: 
* On the **Get Started** page, scroll down to the **View alerts** section, then click **View Alerts** at the bottom. 
* From the left navigation menu, select **Alerts**. 

:::{image} /solutions/images/security-gs-siem-alerts-pg.png 
:alt: Alerts page overview
:screenshot:
:::

At the top of the **Alerts** page are four filter controls—**Status**, **Severity**, **User**, and **Host**—that you can use to filter your alerts view. Except for **Status**, you can [edit and customize](/solutions/security/detect-and-alert/manage-detection-alerts.md#drop-down-filter-controls) these to your preference. 


In the visualization section, you can group alerts by a specific view type: 
* **Summary:** Shows how alerts are distributed across specific indicators.
* **Trend:** Shows the occurrence of alerts over time. 
* **Counts:** Shows the count of alerts in each group. Although there are default values, you can change the `Group by` parameters. 
* **Treemap:** Shows the distribution of alerts as nested, proportionally sized and color-coded tiles based on the number of alerts, and the alert's risk score. This view is useful to quickly pinpoint the most critical alerts.

:::{image} /solutions/images/security-gs-siem-view-type.png
:alt: Alerts page, view by type 
:screenshot:
:::

**View alert details**

At the bottom of the **Alerts** page is the alerts table, which includes a comprehensive list of all generated alerts and inline actions so you can take action directly on the alert. You can customize and filter the table by specific criteria to help drill down and narrow alerts. 

:::{tip} 
Consider [grouping alerts](/solutions/security/detect-and-alert/manage-detection-alerts.md#group-alerts) by other parameters such as rule name, user name, host name, source IP address, or any other field. You can select up to three fields. 
:::

To view specific details about an alert, in the alerts table, click the **View details** button, which opens the alert details flyout. Here, you can view a quick description of the alert, or conduct a deep dive to investigate. Each section of the alert details flyout provides a different insight, and the **Take Action** menu at the bottom provides several options to respond to or interact with the alert. 

:::{image} /solutions/images/security-gs-siem-alert-flyout.png
:alt: Alert details flyout
:screenshot:
:::


For a comprehensive overview of the alert details flyout, refer to [View detection alert details](/solutions/security/detect-and-alert/view-detection-alert-details.md#alert-details-flyout-ui). 

## Next steps 

Once you've had a chance to install detection rules and check out alerts, we recommend exploring the following investigation tools and resources to assist you with threat hunting: 

* View and analyze data with out-of-the-box [dashboards](/solutions/security/dashboards.md). 
* Learn how to reduce your mean time to respond with [Attack Discovery](/solutions/security/ai/attack-discovery.md), an AI threat hunting feature that leverages large language models (LLMs) to analyze alerts in your environment, identify threats, and show how they correspond to the MITRE ATT&CK matrix.
* Learn how to use [Cases](/solutions/security/investigate/cases.md) to track investigation details.  
* Download the "Guide to high-volume data sources for SIEM" [white paper](https://www.elastic.co/campaigns/guide-to-high-volume-data-sources-for-siem?elektra=organic&storm=CLP&rogue=siem-gic). 
* Check out [Elastic Security Labs](https://www.elastic.co/security-labs) for the latest on threat research.  
* Learn how to manage your [data lifecycle](/manage-data/lifecycle.md), including how long data is retained, and how to transition indices through data tiers according to your performance needs and retention policies.