---
navigation_title: Secure your cloud assets with cloud security posture management
description: A quick start guide to securing your cloud assets using {{elastic-sec}}.
applies_to:
  serverless:
    security: all
  stack:
products:
  - id: security
---

# Quickstart: Secure your cloud assets with cloud security posture management

In this quickstart guide, you'll learn how to get started with Elastic Security for Cloud Security so you can monitor, detect, and investigate anomalous activity within cloud environments.

## Prerequisites 

* You can follow this guide using any deployment. To get up and running quickly, we recommend [](/solutions/security/elastic-security-serverless.md) with the **Security Analytics Complete** [feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md#elastic-sec-project-features). For a complete list of deployment options, refer to [](/deploy-manage/deploy.md#choosing-your-deployment-type).
* An admin account for the cloud service provider (CSP) you want to use.  


## Add the Cloud Security Posture Management integration 

The Cloud Security Posture Management (CSPM) integration helps you identify and remediate configuration risks that could undermine the confidentiality, integrity, and availability of your cloud data.

To add the CSPM integration: 

1. On the **Get Started** home page, in the **Ingest your data** section, select the **Cloud** tab. 
2. Select **Cloud Security Posture Management (CSPM)**, then click Add **Cloud Security Posture Management (CSPM)**. The integration configuration page displays. 
3. For this guide, we'll be using a single AWS account. Select these options in the **Configure integration** section. 
4. Give the integration a name and enter an optional description. 
5. Next, choose your deployment option. An agent-based deployment requires you to deploy and manage {{agent}} in the cloud account you want to monitor, whereas an agentless deployment allows you to collect cloud posture data without managing the {{agent}} deployment in your cloud. For simplicity, select **Agentless**.
6. Next, in the **Setup Access** section, choose your preferred authentication method—direct access keys (recommended) or temporary keys. For this guide, we'll use direct access keys. 
7. Expand the Steps to Generate AWS Account Credentials, and follow the instructions. 
8. Once you've generated an access key ID and secret access key and pasted the credentials, click **Save and continue** to complete deployment. Your data should start to appear within a few minutes.

:::{image} /solutions/images/security-gs-cloudsec-cspm.png
:alt: Cloud Security Posture management integration
:screenshot:
:::

:::{{{note}}}
Consider adding the Cloud Native Vulnerability Management (CNVM) integration, which identifies vulnerabilities in your cloud workloads.
:::

## View the Cloud Security Posture dashboard

The Cloud Posture dashboard summarizes your cloud infrastructure's overall performance against security guidelines defined by the Center for Internet Security (CIS). It shows configuration risk metrics for all your monitored cloud accounts and Kubernetes clusters and groups them by specific parameters. All configuration risks the integration identifies are called benchmark rules and are listed on the **Findings** page. 

The dashboard also shows your overall compliance score and your compliance score for each CIS section. Use these scores to determine how securely configured your overall cloud environment is. To learn more, refer to our [documentation](/solutions/security/cloud/cspm-dashboard.md).

:::{image} /solutions/images/security-gs-cspm-dashboard.png
:alt: Cloud Security Posture dashboard
:screenshot:
:::

To access the Cloud Security Posture dashboard, go to **Dashboards** → **Cloud Security Posture**. 


## Analyze Findings 

After you install the CSPM integration, it evaluates the configuration of resources in your environment every 24 hours. It lists the results and whether a given resource passed or failed evaluation against a specific security guideline on the **Findings** page, which you can access from the navigation menu. By default, the Findings page lists all findings without grouping or filtering. However, we recommend [filtering the data](/solutions/security/cloud/findings-page.md#cspm-findings-page-filter-findings) for failed findings. You can also [customize](/solutions/security/cloud/findings-page.md#cspm-customize-the-findings-table) the table to control which columns appear.  

To remediate a failed finding, click the arrow to the left of a failed finding to open the findings flyout, then follow the steps under **Remediation**. 

:::{image} /solutions/images/security-gs-cloudsec-findings-flyout.gif
:alt: Findings flyout
:screenshot:
:::

:::{{tip}}
On the Cloud Security Posture dashboard, click one of the "View all failed findings" links to display a filtered view. 
:::

### Set up alerts 

To monitor your configuration more closely, we recommend creating detection rules to detect specific failed findings, which, if found, generate an alert. 

You can create a detection rule directly from the **Findings** page: 

1. Click the arrow to the left of a finding to open the findings flyout.
2. Click **Take action**, then **Create a detection rule**. 
3. To review or customize the new rule, click **View rule**. For example, you might want to set up a rule action—like an email or Slack notification—when alerts are generated. To learn more about rule actions, refer to [](/solutions/security/detect-and-alert/create-detection-rule.md#rule-notifications).   

## More resources 

Now that you've configured CSPM, check out these other Cloud Security resources: 

* [CSPM for Google Cloud Posture (GCP)](/solutions/security/cloud/get-started-with-cspm-for-gcp.md) and [Azure](/solutions/security/cloud/get-started-with-cspm-for-azure.md) 
* [Kubernetes security posture management](/solutions/security/cloud/kubernetes-security-posture-management.md)
* [Cloud native vulnerability management](/solutions/security/cloud/cloud-native-vulnerability-management.md)
* [Cloud workload protection for VMs](/solutions/security/cloud/cloud-workload-protection-for-vms.md)