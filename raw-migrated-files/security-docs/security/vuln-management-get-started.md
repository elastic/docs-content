# Get started with CNVM [vuln-management-get-started]

This page explains how to set up Cloud Native Vulnerability Management (CNVM).

::::{admonition} Requirements
* CNVM is available to all {{ecloud}} users. On-premise deployments require an [Enterprise subscription](https://www.elastic.co/pricing).
* Requires {{stack}} and {{agent}} version 8.8 or higher.
* Only works in the `Default` {{kib}} space. Installing the CNVM integration on a different {{kib}} space will not work.
* CNVM can only be deployed on ARM-based VMs.
* To view vulnerability scan findings, you need at least `read` privileges for the following indices:

    * `logs-cloud_security_posture.vulnerabilities-*`
    * `logs-cloud_security_posture.vulnerabilities_latest-*`

* You need an AWS user account with permissions to perform the following actions: run CloudFormation templates, create IAM Roles and InstanceProfiles, and create EC2 SecurityGroups and Instances.

::::


::::{note}
CNVM currently only supports AWS EC2 Linux workloads.
::::



## Set up CNVM for AWS [vuln-management-setup]

To set up the CNVM integration for AWS, install the integration on a new {{agent}} policy, sign into the AWS account you want to scan, and run the [CloudFormation](https://docs.aws.amazon.com/cloudformation/index.md) template.

::::{important}
Do not add the integration to an existing {{agent}} policy. It should always be added to a new policy since it should not run on VMs with existing workloads. For more information, refer to [How CNVM works](../../../solutions/security/cloud/cloud-native-vulnerability-management.md#vuln-management-overview-how-it-works).
::::



### Step 1: Add the CNVM integration [vuln-management-setup-step-1]

1. Find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Search for **Cloud Native Vulnerability Management**, then click on the result.
3. Click **Add Cloud Native Vulnerability Management**.
4. Give your integration a name that matches its purpose or the AWS account region you want to scan for vulnerabilities (for example, `uswest2-aws-account`.)

    :::{image} ../../../images/security-cnvm-setup-1.png
    :alt: The CNVM integration setup page
    :::

5. Click **Save and continue**. The integration will create a new {{agent}} policy.
6. Click **Add {{agent}} to your hosts**.


### Step 2: Sign in to the AWS management console [vuln-management-setup-step-2]

1. Open a new browser tab and use it to sign into your AWS management console.
2. Switch to the cloud region with the workloads that you want to scan for vulnerabilities.

::::{important}
The integration will only scan VMs in the region you select. To scan multiple regions, repeat this setup process for each region.
::::



### Step 3: Run the CloudFormation template [vuln-management-setup-step-3]

1. Switch back to the tab where you have {{kib}} open.
2. Click **Launch CloudFormation**. The CloudFormation page appears.

    :::{image} ../../../images/security-cnvm-cloudformation.png
    :alt: The cloud formation template
    :::

3. Click **Create stack**.  To avoid authentication problems, you can only make configuration changes to the VM InstanceType, which you could make larger to increase scanning speed.
4. Wait for the confirmation that {{agent}} was enrolled.
5. Your data will start to appear on the **Vulnerabilities** tab of the [Findings page](https://www.elastic.co/guide/en/security/current/vuln-management-findings.html).
