# Cloud security posture management [cspm]

The Cloud Security Posture Management (CSPM) feature discovers and evaluates the services in your cloud environment — like storage, compute, IAM, and more — against configuration security guidelines defined by the [Center for Internet Security](https://www.cisecurity.org/) (CIS) to help you identify and remediate risks that could undermine the confidentiality, integrity, and availability of your cloud data.

This feature currently supports agentless and agent-based deployments on Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft Azure. For step-by-step getting started guides, refer to [Get started with CSPM for AWS](../../../solutions/security/cloud/get-started-with-cspm-for-aws.md), [Get started with CSPM for GCP](../../../solutions/security/cloud/get-started-with-cspm-for-gcp.md), or [Get started with CSPM for Azure](../../../solutions/security/cloud/get-started-with-cspm-for-azure.md).

::::{admonition} Requirements
* CSPM is available to all {{ecloud}} users. On-premise deployments require an [Enterprise subscription](https://www.elastic.co/pricing).
* {{stack}} version 8.10 or greater.
* CSPM only works in the `Default` {{kib}} space. Installing the CSPM integration on a different {{kib}} space will not work.
* CSPM is supported only on AWS, GCP, and Azure commercial cloud platforms, and AWS GovCloud. Other government cloud platforms are not supported. [Click here to request support](https://github.com/elastic/kibana/issues/new/choose).
* `Read` privileges for the following {{es}} indices:

    * `logs-cloud_security_posture.findings_latest-*`
    * `logs-cloud_security_posture.scores-*`

* The following {{kib}} privileges:

    * Security: `Read`
    * Integrations: `Read`
    * Saved Objects Management: `Read`
    * Fleet: `All`


::::



## How CSPM works [cspm-how-it-works] 

Using the read-only credentials you will provide during the setup process, it will evaluate the configuration of resources in your environment every 24 hours. After each evaluation, the integration sends findings to Elastic. A high-level summary of the findings appears on the [Cloud Security Posture dashboard](../../../solutions/security/cloud/cloud-security-posture-dashboard-2.md), and detailed findings appear on the [Findings page](../../../solutions/security/cloud/findings-page-2.md).









