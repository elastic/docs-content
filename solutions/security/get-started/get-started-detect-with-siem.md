---
navigation_title: Detect and respond to threats with SIEM
description: An introduction to detecting threats with SIEM in {{elastic-sec}}.
applies_to:
  serverless:
products:
  - id: security
---

# Quickstart: Detect and respond to threats with SIEM

Elastic Security is a unified security solution that brings together SIEM, endpoint security, and cloud security into a single platform. This makes it easier to protect, investigate, and respond to security events from all areas within your environment.

In this guide, we'll learn how to use some of {{elastic-sec}}'s SIEM features to detect, investigate, and respond to threats. 

## Prerequisites 

To get started exploring {{elastic-sec}}, log in to your {{sec-serverless}} project. If you don't have one yet, refer to [Create a Security project](/solutions/security/get-started/create-security-project.md). 

:::::{stepper}

::::{step} Add data using Elastic Defend

Before you can start using {{elastic-sec}}, you need to choose an integration to start collecting and analyzing your data. For this guide, we're going to use the {{elastic-defend}} integration. {{elastic-defend}} detects and protects endpoints from malicious activity and provides automated response options before damage and loss occur. 

1. On the Get started home page, in the **Ingest your data** section, select **Elastic Defend**, then click **Add Elastic Defend**. 
2. On the next page that says, "Ready to add your first integration?", click **Install {{agent}}** in the lower-right corner. Although you *can* skip agent installation, for optimal event collection and threat detection, we recommend that you do not skip it. 

3. Select the appropriate operating system tab, then copy the commands. 
4. On the host, open a command-line interface and navigate to the directory where you want to install {{agent}}. Paste and run the commands to download, extract, enroll, and start {{agent}}. Once the agent is installed successfully, you'll see an "Agent enrollment confirmed" message. 
5. Click **Add the integration**, then Confirm incoming data on the next page.  
    After a few minutes, you should see the agent receiving data.

    :::{image} /solutions/images/security-gs-siem-install-agent.png
    :alt: Alerts page with visualizations section collapsed
    :screenshot:
    :::

:::{important}
If you’re using macOS, some versions may require you to grant {{elastic-endpoint}} Full Disk Access to different kernels, system extensions, or files. Refer to [Elastic Defend requirements](/solutions/security/configure-elastic-defend/elastic-defend-requirements.md) for more information.
:::
::::

::::{step} Add Elastic detection prebuilt rules

Detection rules allow you to proactively monitor your environment by searching for source events, matches, sequences, or machine learning job anomaly results that meet their criteria. When a rule’s criteria are met, {{elastic-sec}} generates an alert. While you can create your own rules tailored for your environment, Elastic ships out-of-the-box prebuilt rules that you can install. 

To install and enable Elastic's prebuilt detection rules: 
1. On the Get Started page, scroll down to the **Configure rules and alerts** section. 
2. At the top of the page, click **Add Elastic rules**. The badge next to it shows the number of prebuilt rules available for installation. 

    The next pages displays the list of rules. Click on a rule name to view its details before you install it.  
3. Use the search bar and **Tags** filter to find the rules you want to install. For example, to filter by operating system, search for the appropriate OS from the **Tags** menu (such as `macOS`). We recommend installing all the rules for your operating system, but you can install whichever rules you're comfortable with to start. You can always install more later.  
4. Select the check box next to rules you want to install. To select all rules on the page, select the check box to the left of the **Rule** column heading. 
5. Click ![Vertical boxes button](/solutions/images/serverless-boxesVertical.svg "") → **Install and enable** to install and start running the rules. Once you enable a rule, it starts running on its configured schedule.

:::{image} /solutions/images/security-gs-siem-install-rules.png 
:alt: Alerts page with visualizations section collapsed
:screenshot:
:::
    
    To learn how to view and manage all detection rules, refer to [Manage detection rules](/solutions/security/detect-and-alert/manage-detection-rules.md). 
::::

::::{step} Visualize and examine alert details 

Now that you've installed and enabled rules, it's time to monitor the {{security-app}} to see if you receive any alerts. Remember, an alert is generated if any of the rule's criteria are met. {{elastic-sec}} provides several tools for investigating security events:

* **Alerts table:** View all generated alerts in a comprehensive list, apply filters for a customized view, and drill down into details. 
* **Timeline:** Explore alerts in a central, interactive workspace. Create customized queries and collaborate on incident analysis by combining data from various sources.  
* **Visual event analyzer:** View a graphical timeline of processes that led up to the alert and the events that occurred immediately after.
* **Session View:** Examine Linux process data and real-time data insights. 

To view a quick video tutorial on how to use these features, on the Get Started page, scroll down to **View alerts**, select an alert tool from the list, and click **Play Video** on the right. 

For this guide, let's take a closer look at how to visualize and examine alert details by viewing the Alerts page. 

:::{note}
If you don't have any alerts yet in your environment, that's great news! You can use the [Elastic demo server](https://demo.elastic.co/) to explore alerts. 
:::

To access the Alerts page, do one of the following: 
* On the Get Started page, scroll down to the View alerts section, then click **View Alerts** at the bottom. 
* From the left navigation menu, select **Alerts**. 

:::{image} /solutions/images/security-gs-siem-alerts-pg.png 
:alt: Alerts page overview
:screenshot:
:::

At the top of the Alerts page are four filter controls: **Status**, **Severity**, **User**, and **Host** that you can use to filter your alerts view. With the exception of **Status**, you can [edit and customize](/solutions/security/detect-and-alert/manage-detection-alerts.md#drop-down-filter-controls) these to your preference. 


In the visualization section, you can group alerts by a specific view type: 
* **Summary:** Shows how alerts are distributed across specific indicators.
* **Trend:** Shows the occurrence of alerts over time. 
* **Counts:** Shows the count of alerts in each group. Although there are default values, you can change the `Group by` parameters. 
* **Treemap:** Shows the distribution of alerts as nested, proportionally-sized and color-coded tiles based on the number of alerts, and the alert's risk score. This view is useful to quickly pinpoint the most critical alerts.

:::{image} /solutions/images/security-gs-siem-view-type.png
:alt: Alerts page, view by type 
:screenshot:
:::

View alert details

At the bottom of the Alerts page is the alerts table, which includes a comprehensive list of all generated alerts, as well as inline actions so you can take action directly on the alert. You can customize and filter the table by specific criteria to help drill down and narrow alerts. 

:::{tip} 
Consider [grouping alerts](/solutions/security/detect-and-alert/manage-detection-alerts.md#group-alerts) by other parameters such as rule name, user name, host name, source IP address, or any other field. You can select up to three fields. 
:::

To view specific details about an alert, in the alerts table, click the **View details** button, which opens the alert details flyout. Here, you can view a quick description of the alert, or conduct a deep dive to investigate. Each section of the alert details flyout provides a different insight, and the **Take Action** menu at the bottom provides several options for interacting with the alert. 

:::{image} /solutions/images/security-gs-siem-alert-flyout.png
:alt: Alert details flyout
:screenshot:
:::


For a comprehensive overview of the alert details flyout, refer to [View detection alert details](/solutions/security/detect-and-alert/view-detection-alert-details.md#alert-details-flyout-ui). 

::::
:::::{stepper}

## Next steps 

Once you've had a chance to install detection rules and check out alerts, we recommend exploring the following investigation tools and resources to assist you with threat hunting: 

* View and analyze data with out-of-the-box [dashboards](/solutions/security/dashboards.md). 
* Explore a graphical timeline of processes that led up to the alert and the events that occurred immediately after with the [visual event analyzer](/solutions/security/investigate/visual-event-analyzer.md).     
* Learn how to use [Cases](/solutions/security/investigate/cases.md) to track investigation details.  
* Download the "Guide to high-volume data sources for SIEM" [white paper](https://www.elastic.co/campaigns/guide-to-high-volume-data-sources-for-siem?elektra=organic&storm=CLP&rogue=siem-gic). 
* Check out [Elastic Security Labs](https://www.elastic.co/security-labs) for the latest on threat research.  
% add endpoint getting started guide when it's done 