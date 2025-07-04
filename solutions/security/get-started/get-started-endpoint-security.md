---
navigation_title: Secure my hosts with endpoint security
description: A quick start guide to securing your hosts with endpoint security.
applies_to:
  serverless:
products:
  - id: security
---

# Quickstart: Secure my hosts with endpoint security

In this guide below, you’ll learn how to use {{elastic-sec}} to protect your hosts from malware, ransomware, and other threats.

## Prerequisites 

* Log in to your {{sec-serverless}} project. If you don't have one yet, refer to [Create a Security project](/solutions/security/get-started/create-security-project.md) to learn how to create one. 
* Ensure you have the appropriate [{{elastic-defend}} feature privileges](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md). 
* Ensure you have the appropriate user role to configure an integration policy and access the Endpoints page.

:::::{stepper}

::::{step} Add the Elastic Defend integration

{{elastic-defend}} detects and protects endpoints from malicious activity and provides automated response options before damage and loss occur. 

:::{note}
If you're installing {{elastic-defend}} on macOS, the following instructions apply to hosts without a Mobile Device Management (MDM) profile. If your host has an MDM profile, refer to [Deploy Elastic Defend on macOS with mobile device management](/solutions/security/configure-elastic-defend/deploy-on-macos-with-mdm.md). 
:::

1. On the Get started home page, in the **Ingest your data** section, select **Elastic Defend**, then click **Add Elastic Defend**. 
2. On the next page that says, "Ready to add your first integration?", click **Add integration only (skip agent installation)**. The integration configuration page appears.
3. Give the Elastic Defend integration a name and optional description.
4. Select the type of environment you want to protect — **Traditional Endpoints** or **Cloud Workloads**. For this guide , we'll select **Traditional Endpoints**. 
5. Select a configuration preset, which will differ based on your prior selection. Each preset comes with different default settings for {{agent}}, which you can further customize later by [configuring the {{elastic-defend}} integration policy](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md). For optimal endpoint protection, we recommend selecting **Complete EDR (Endpoint, Detection & Response)**. 
6. Enter a name for the agent policy in the **New agent policy name** field.
7. Click **Save and continue**. Next, click **Add {{agent}} to your hosts**. 
::::

::::{step} Add the {{agent}}

{{agent}} is a single, unified way to add monitoring for logs, metrics, and other types of data to a host. 

1. In the **Add agent** flyout that appears after you install the {{elastic-defend}} integration, you'll see the policy selected that you previously added. Leave the default enrollment token selected. 
2. Ensure that the **Enroll in {{fleet}}** option is selected. {{elastic-defend}} cannot be integrated with {{agent}} in standalone mode.
3. Select the appropriate platform or operating system for the host on which you're installing the agent, then copy the provided commands.
4.  On the host, open a command-line interface and navigate to the directory where you want to install {{agent}}. Paste and run the commands from {{fleet}} to download, extract, enroll, and start {{agent}}.
5. (Optional) Return to the **Add agen**t flyout, and observe the **Confirm agent enrollment** and **Confirm incoming data** steps automatically checking the host connection. It may take a few minutes for data to arrive in {{es}}.
6. (Optional) After you have enrolled the {{agent}} on your host, you can click **View enrolled agents** to access the list of agents enrolled in {{fleet}}. Otherwise, select **Close**.

    The host will now appear on the **Endpoints** page in the {{security-app}} (**Assets** → **Endpoints**). It may take another minute or two for endpoint data to appear in {{elastic-sec}}.
7. If you’re using macOS, some versions may require you to grant {{elastic-endpoint}} Full Disk Access to different kernels, system extensions, or files. Refer to [Elastic Defend requirements](/solutions/security/configure-elastic-defend/elastic-defend-requirements.md) for more information.
::::

::::{step} (Optional) Configure an integration policy for Elastic Defend

After you install the {{agent}} with {{elastic-defend}}, several endpoint protections — such as preventions against malware, ransomware, memory threats, and other malicious behavior are automatically enabled on protected hosts. However, you can update the policy configuration to meet your organization’s security needs.

To configure an integration policy:

1. From the left navigation menu, go to Assets → Endpoints → Policies. 
2. From the list, select the policy you want to configure. The integration policy configuration page appears.
3. On the **Policy settings** tab, review and configure the protection, event collection, and antivirus settings as appropriate. 
4. Once you're finished making changes, click **Save** in the lower-right corner to update the policy.  
5. Next, click the **Trusted applications**, **Event filters**, **Host isolation exceptions**, and **Blocklist** tabs to review and manage the endpoint policy artifacts assigned to the policy.   

    For a comprehensive explanation of all endpoint protections and policy settings, refer to [Configure an integration policy](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md). 

%insert image
::::
:::::