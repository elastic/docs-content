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

::::{step} Add data using {{elastic-defend}}
Before you can start using {{elastic-sec}}, you need to choose an integration to start collecting and analyzing your data. For this guide, we're going to use the {{elastic-defend}} integration. {{elastic-defend}} detects and protects endpoints from malicious activity and provides automated response options before damage and loss occur. 

:::{note}
Before you install {{elastic-defend}}, if you’re using macOS, some versions may require you to grant Full Disk Access to different kernels, system extensions, or files. Refer to [Elastic Defend requirements](/solutions/security/configure-elastic-defend/elastic-defend-requirements.md) for more information.
:::

1. On the Get started home page, in the **Ingest your data** section, select **Elastic Defend**, then click **Add Elastic Defend**. 
2. On the next screen that says, "Ready to add your first integration?", click **Install {{agent}}** in the lower-right corner. Although you *can* skip agent installation, for optimal event collection and threat detection, we recommend that you do not skip it. 
3. Select the appropriate operating system tab, then copy the commands. 
4. On the host, open a command-line interface and navigate to the directory where you want to install {{agent}}. Paste and run the commands to download, extract, enroll, and start {{agent}}. Once the agent is installed successfully, you'll see an "Agent enrollment confirmed" message. 
5. Click


::::