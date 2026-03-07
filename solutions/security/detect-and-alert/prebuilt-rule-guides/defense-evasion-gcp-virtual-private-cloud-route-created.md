---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "GCP Virtual Private Cloud Route Creation" prebuilt detection rule.
---

# GCP Virtual Private Cloud Route Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating GCP Virtual Private Cloud Route Creation

In Google Cloud Platform, VPC routes dictate the network paths for traffic from VM instances to various destinations, both within and outside the VPC. Adversaries may exploit this by creating routes to reroute or intercept traffic, potentially disrupting or spying on network communications. The detection rule identifies such activities by monitoring specific audit events related to route creation, aiding in the early detection of unauthorized network modifications.

### Possible investigation steps

- Review the audit logs for the specific event.dataset:gcp.audit and event.action values (v*.compute.routes.insert or "beta.compute.routes.insert") to identify the exact time and user account associated with the route creation.
- Examine the details of the newly created route, including the destination IP range and next hop, to determine if it aligns with expected network configurations or if it appears suspicious.
- Check the IAM permissions and roles of the user account that created the route to assess if they had the necessary privileges and if those privileges are appropriate for their role.
- Investigate any recent changes in the environment that might explain the route creation, such as new deployments or changes in network architecture.
- Correlate the route creation event with other security events or alerts in the same timeframe to identify potential patterns or coordinated activities that could indicate malicious intent.
- Consult with the network or cloud infrastructure team to verify if the route creation was part of an authorized change or if it was unexpected.

### False positive analysis

- Routine network configuration changes by authorized personnel can trigger alerts. To manage this, maintain a list of known IP addresses and users who frequently make legitimate changes and exclude their activities from triggering alerts.
- Automated deployment tools that create or modify routes as part of their normal operation may cause false positives. Identify these tools and their associated service accounts, then configure exceptions for these accounts in the monitoring system.
- Scheduled maintenance activities often involve creating or updating routes. Document these activities and set temporary exceptions during the maintenance window to prevent unnecessary alerts.
- Integration with third-party services might require route creation. Verify these integrations and whitelist the associated actions to avoid false positives.
- Development and testing environments may have frequent route changes. Consider applying different monitoring thresholds or rules for these environments to reduce noise.

### Response and remediation

- Immediately isolate the affected VM instances by removing or disabling the suspicious route to prevent further unauthorized traffic redirection.
- Conduct a thorough review of recent route creation activities in the GCP environment to identify any other unauthorized or suspicious routes.
- Revoke any unauthorized access or permissions that may have allowed the adversary to create the route, focusing on IAM roles and service accounts with route creation privileges.
- Notify the security operations team and relevant stakeholders about the incident for awareness and further investigation.
- Implement network monitoring and logging to detect any future unauthorized route creation attempts, ensuring that alerts are configured for similar activities.
- Review and update the GCP VPC network security policies to enforce stricter controls on route creation and modification, limiting these actions to trusted administrators only.
- If applicable, report the incident to Google Cloud support for further assistance and to understand if there are any additional security measures or advisories.

## Setup

The GCP Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
