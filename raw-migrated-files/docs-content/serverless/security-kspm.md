# Kubernetes security posture management [security-kspm]


## Overview [kspm-overview]

The Kubernetes Security Posture Management (KSPM) integration allows you to identify configuration risks in the various components that make up your Kubernetes cluster. It does this by evaluating your Kubernetes clusters against secure configuration guidelines defined by the Center for Internet Security (CIS) and generating findings with step-by-step instructions for remediating potential security risks.

This integration supports Amazon EKS and unmanaged Kubernetes clusters. For setup instructions, refer to [Get started with KSPM](../../../solutions/security/cloud/get-started-with-kspm.md).

::::{admonition} Requirements
:class: note

* KSPM only works in the `Default` {{kib}} space. Installing the KSPM integration on a different {{kib}} space will not work.
* KSPM is not supported on EKS clusters in AWS GovCloud ([request support](https://github.com/elastic/kibana/issues/new/choose)).
* To view posture data, ensure you have the appropriate user role to read the following {{es}} indices:
* `logs-cloud_security_posture.findings_latest-*`
* `logs-cloud_security_posture.scores-*`
* `logs-cloud_security_posture.findings`

::::



## How KSPM works [kspm-how-kspm-works]

1. When you add a KSPM integration, it generates a Kubernetes manifest. When applied to a cluster, the manifest deploys an {{agent}} as a [DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset) to ensure all nodes are evaluated.
2. Upon deployment, the integration immediately assesses the security posture of your Kubernetes resources. The evaluation process repeats every four hours.
3. After each evaluation, the integration sends findings to {{es}}. Findings appear on the [Cloud Security Posture dashboard](../../../solutions/security/dashboards/cloud-security-posture-dashboard.md) and the [findings](../../../solutions/security/cloud/findings-page.md) page.


## Use cases [kspm-use-cases]

The KSPM integration helps you to:

* Identify and remediate `failed` findings
* Identify the most misconfigured resources
* Identify risks in particular CIS benchmark sections


### Identify and remediate failed findings [kspm-remediate-failed-findings]

To identify and remediate failed failed findings:

1. Go to the [Cloud Security Posture dashboard](../../../solutions/security/dashboards/cloud-security-posture-dashboard.md).
2. Click **View all failed findings**, either for an individual cluster or for all monitored clusters.
3. Click a failed finding. The findings flyout opens.
4. Follow the steps under **Remediation** to correct the misconfiguration.

    ::::{note}
    Remediation steps typically include commands for you to execute. These sometimes contain placeholder values that you must replace before execution.

    ::::



### Identify the most misconfigured Kubernetes resources [kspm-identify-misconfigured-resources]

To identify the Kubernetes resources generating the most failed findings:

1. Go to the [Findings](../../../solutions/security/cloud/findings-page.md) page.
2. Click the **Group by** menu near the search box and select **Resource** to view a list of resources sorted by their total number of failed findings.
3. Click a resource ID to view the findings associated with that resource.


### Identify configuration risks by CIS section [kspm-identify-config-risks-by-section]

To identify risks in particular CIS sections:

1. Go to the [Cloud Security Posture dashboard](../../../solutions/security/dashboards/cloud-security-posture-dashboard.md).
2. In the Failed findings by CIS section widget, click the name of a CIS section to view all failed findings for that section.

Alternatively:

1. Go to the Findings page.
2. Filter by the `rule.section` field. For example, search for `rule.section : API Server` to view findings for benchmark rules in the API Server category.
