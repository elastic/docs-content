# Cloud security posture management [security-cspm]

The Cloud Security Posture Management (CSPM) feature discovers and evaluates the services in your cloud environment — like storage, compute, IAM, and more — against configuration security guidelines defined by the [Center for Internet Security](https://www.cisecurity.org/) (CIS) to help you identify and remediate risks that could undermine the confidentiality, integrity, and availability of your cloud data.

This feature currently supports agentless and agent-based deployments on Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft Azure. For step-by-step getting started guides, refer to [Get started with CSPM for AWS](../../../solutions/security/cloud/get-started-with-cspm-for-aws.md), [Get started with CSPM for GCP](../../../solutions/security/cloud/get-started-with-cspm-for-gcp.md), or [Get started with CSPM for Azure](../../../solutions/security/cloud/get-started-with-cspm-for-azure.md).

::::{admonition} Requirements
:class: note

* CSPM only works in the `Default` {{kib}} space. Installing the CSPM integration on a different {{kib}} space will not work.
* CSPM is supported only on AWS, GCP, and Azure commercial cloud platforms, and AWS GovCloud. Other government cloud platforms are not supported ([request support](https://github.com/elastic/kibana/issues/new/choose)).

::::



## How CSPM works [cspm-how-it-works] 

Using the read-only credentials you will provide during the setup process, it will evaluate the configuration of resources in your environment every 24 hours. After each evaluation, the integration sends findings to Elastic. A high-level summary of the findings appears on the [Cloud Security Posture dashboard](../../../solutions/security/dashboards/cloud-security-posture-dashboard.md), and detailed findings appear on the [Findings page](../../../solutions/security/cloud/findings-page.md).









