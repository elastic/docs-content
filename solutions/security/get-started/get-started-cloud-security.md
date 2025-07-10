---
navigation_title: Secure your cloud assets with cloud security posture management
description: A quick start guide to securing your cloud assets using {{elastic-sec}}.
applies_to:
  serverless:
products:
  - id: security
---

# Quickstart: Secure your cloud assets with cloud security posture management

## Prerequisites 

* An admin account for the cloud service provider (CSP) you want to use 


## Add the Cloud Security Posture Management integration 

The Cloud Security Posture Management (CSPM) integration helps you identify and remediate configurations risks that could potentially undermine the confidentiality, integrity, and availability of your data in the cloud.

To add the CSPM integration: 

1. On the **Get Started** home page, in the **Ingest your data** section, select the **Cloud** tab. 
2. Select **Cloud Security Posture Management (CSPM)**, then click Add **Cloud Security Posture Management (CSPM)**. The integration configuration page displays. 
3. For this guide, we'll be using AWS single account for configuration. Select these options in the configuration integration section. 
4. Give the integration a name and enter an optional description. 
5. Next, choose your deployment option. An agent-based deployment requires you to deploy and manage {{agent}} in the cloud account you want to monitor, whereas an agentless deployment allows you to collect cloud posture data without having to manage the {{agent}} deployment in your cloud. For simplicity, select **Agentless**.
6. Next, in the **Setup Access** section, choose your preferred authentication method — direct access keys (recommended) or temporary keys. For this guide, we'll use direct access keys. 
7. Expand the Steps to Generate AWS Account Credentials, and follow the instructions. 
8. Once you've generated an Access Key ID and Secret Access Key and pasted the credentials, click **Save and continue** to complete deployment. Your data should start to appear within a few minutes.

% insert image 

Keep in mind that you'll need to do additional configurations if you'd like to enable Cloud Native Vulnerability Management. This isn't needed to get started, but for more information, check out our documentation.

Security cspm - integration installed.png
Cloud Posture Dashboard
The Cloud Posture dashboard summarizes the overall security posture of your cloud environments.

Number of accounts you've enrolled
Number of resources evaluated
Failed findings
Your posture score tells you how securely configured your overall cloud environment is.

Security cspm - dashboard.png

Findings and alerts
The Findings page displays each individual resource evaluated by the CSPM integration and whether the resource passed or failed the secure configuration checks against it, for more information on Findings, such as how to group and filter them, check out our documentation.

Security cspm - findings.png

Some rules, more than others, you may want to monitor closely. You can select a finding for that particular rule and click Take action in the lower right. Then click Create a detection rule.

Security cspm - create rule.png
Next click View rule.

Security cspm - view rules .png
Now, you'll see the detection rule, along with its definition. Now, whenever there is a failed finding for this rule, you'll get an alert. To set up other actions, click Edit rule settings on the upper right of the rule page.

Security cspm - rule details.png
Next you'll select, Actions.

Security cspm - edit rule settings.png

From here, you can set up actions. For example, if a rule fails, you set up a Slack message, Jira ticket, etc., so you get a proactive notification to review the failed finding and remediate the misconfiguration. To learn more about detection rules, check out our documentation.

Security cspm - edit rules.png

Next steps
Congrats on beginning your Elastic Security journey with Elastic Security for Cloud (CSPM). For more information on CSPM, please review the product documentation. As you begin your journey with Elastic, be sure to understand some operational, security, and data components you should manage as a user when you deploy across your environment.

Ready to get started? Spin up a free 14-day trial on Elastic Cloud or try out these 15-minute hands-on learnings on Security 101.