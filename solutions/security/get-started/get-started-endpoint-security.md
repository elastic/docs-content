---
navigation_title: Protect your hosts with endpoint security
description: A quick start guide to securing your hosts with endpoint security.
applies_to:
  serverless:
    security: all
  stack:
products:
  - id: security
---

# Quickstart: Protect your hosts with endpoint security

In this guide, you’ll learn how to use {{elastic-sec}} to protect your hosts from malware, ransomware, and other threats.

## Prerequisites 

* You can follow this guide using any deployment. To get up and running quickly, we recommend [](/solutions/security/elastic-security-serverless.md) with the **Security Analytics Complete** [feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md#elastic-sec-project-features). For a complete list of deployment options, refer to [](/deploy-manage/deploy.md#choosing-your-deployment-type). 
* Ensure you have the minimum [system requirements](/solutions/security/configure-elastic-defend/elastic-defend-requirements.md) to install {{elastic-defend}}.  
* Ensure you grant the appropriate [{{elastic-defend}} sub-feature privileges](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md).  We recommend granting them all, but you need at least `All` access for the **Endpoint List** and **Elastic Defend Policy Management** sub-features. 

## Install {{elastic-defend}}

:::::{stepper}
::::{step} Install the Elastic Defend integration

{{elastic-defend}} detects and protects endpoints from malicious activity and provides automated response options before damage and loss occur. 

:::{note}
If you're installing {{elastic-defend}} on macOS, the following instructions apply to hosts without a Mobile Device Management (MDM) profile. If your host has an MDM profile, refer to [Deploy Elastic Defend on macOS with mobile device management](/solutions/security/configure-elastic-defend/deploy-on-macos-with-mdm.md). 
:::

:::{dropdown} Steps to install {{elastic-defend}}
1. On the **Get started** home page, in the **Ingest your data** section, select **{{elastic-defend}}**, then click **Add {{elastic-defend}}**.  
2. On the next page that says, "Ready to add your first integration?", click **Add integration only (skip agent installation)**. The integration configuration page appears.
3. Give the {{elastic-defend}} integration a name and enter an optional description.
4. Select the type of environment you want to protect — **Traditional Endpoints** or **Cloud Workloads**. For this guide, we'll select **Traditional Endpoints**. 
5. Select a configuration preset, which will differ based on your prior selection. Each preset comes with different default settings for {{agent}}, which you can further customize later by [configuring the {{elastic-defend}} integration policy](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md). For optimal endpoint protection, we recommend selecting **Complete EDR (Endpoint, Detection & Response)**. 
6. Enter a name for the agent policy in the **New agent policy name** field.
7. Click **Save and continue**. Next, click **Add {{agent}} to your hosts**. 
:::
::::

::::{step} Add the Elastic Agent

{{agent}} is a single, unified way to add monitoring for logs, metrics, and other types of data to a host. 

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

After you install the {{agent}} with {{elastic-defend}}, several endpoint protections—such as preventions against malware, ransomware, memory threats, and other malicious behavior—are automatically turned on for protected hosts. If any of these behaviors are detected, {{elastic-defend}} generates an alert, and by default, prevents the malicious activity from completing. However, you can tailor the policy configuration to meet your organization’s security needs.

:::{tip}
You may want to consider analyzing which and how many alerts are generated over a specific time period to identify common patterns or anomalies before you make any policy changes. Check out the [SIEM quick start guide](/solutions/security/get-started/get-started-detect-with-siem.md) to learn more about how to monitor alerts. 
:::

:::{dropdown} Steps to modify an integration policy
1. From the left navigation menu, go to **Assets** → **Endpoints** → **Policies**. 
2. From the list, select the policy you want to configure. The integration policy configuration page appears.
3. On the **Policy settings** tab, review and configure the protection, event collection, and antivirus settings as appropriate. 
4. Once you're finished making changes, click **Save** in the lower-right corner to update the policy.  
5. (Optional) You can click the **Trusted applications**, **Event filters**, **Host isolation exceptions**, and **Blocklist** tabs to review and manage those artifacts assigned to the policy, but we'll cover how to manage these in the next section.    

:::{note}
For a comprehensive explanation of all endpoint protections and policy settings, refer to [Configure an integration policy](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md).
::: 

% insert image
:::
::::
:::::

## Manage endpoints 
Now that you've turned on endpoint protection, it's important not only to monitor your environment for alerts, but to manage your hosts to ensure they're healthy and have all appropriate security settings. 

:::{{note}}
You must have `admin` privileges to manage endpoints. 
:::

To view all endpoints running {{elastic-defend}}, go to **Assets** → **Endpoints**. From here, you can view details such as agent and policy status, associated policy and IP address, or perform specific actions on the endpoint. For more information, refer to our documentation on [managing endpoints](/solutions/security/manage-elastic-defend/endpoints.md). 

:::{image} /solutions/images/security-gs-endpoint-endpoints-pg.png
:alt: Endpoints page in Elastic Security
:screenshot:
:::

Here are some other features {{elastic-sec}} provides to help manage host configuration: 

* [Endpoint response actions](/solutions/security/endpoint-response-actions.md): Perform response actions on an endpoint using a terminal-like interface. For example, isolating or releasing a host, getting a list of processes, or suspending a running process. 

   :::{tip}
   You can also automate some responses when an event meets the rule's criteria. Refer to [Automated response actions](/solutions/security/endpoint-response-actions/automated-response-actions.md) for more information. 
   :::

* [Trusted applications](/solutions/security/manage-elastic-defend/trusted-applications.md): Add Windows, macOS, and Linux applications that should be trusted so that {{elastic-defend}} doesn't monitor them.
* [Blocklist](/solutions/security/manage-elastic-defend/blocklist.md): Prevent specified applications from running on hosts to extend the list of processes that {{elastic-defend}} considers malicious. This adds an extra layer of protection by ensuring that known malicious processes aren’t accidentally executed by end users. 
* [Host isolation exceptions](/solutions/security/manage-elastic-defend/host-isolation-exceptions.md): Add specific IP addresses that isolated hosts are still allowed to communicate with, even when blocked from the rest of your network.

:::{tip}
You can apply trusted applications, blocklist entries, and host isolation exceptions to a single policy, or to all policies. 
::: 

## Next steps 

After your hosts are secure and your environment has all the appropriate security settings configured, we recommend taking these next steps: 

* Check out the [Hosts page](/solutions/security/explore/hosts-page.md) for a comprehensive overview of all hosts and host-related security events. This page is also useful to identify uncommon processes and anomalies discovered by {{ml}} jobs. 
*  Install and turn on prebuilt detection rules. You're already set to receive endpoint threat alerts from {{elastic-defend}}, but did you know {{elastic-sec}} ships with several out-of-the-box rules you can turn on? Check out our [SIEM quick start guide](/solutions/security/get-started/get-started-detect-with-siem.md#add-elastic-prebuilt-detection-rules) or our [documentation](/solutions/security/detect-and-alert/install-manage-elastic-prebuilt-rules.md#load-prebuilt-rules).  
* Discover all the other tools available to [manage {{elastic-defend}}](/solutions/security/manage-elastic-defend.md). 
