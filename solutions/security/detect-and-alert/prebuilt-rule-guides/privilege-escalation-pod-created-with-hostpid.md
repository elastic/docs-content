---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Kubernetes Pod Created With HostPID" prebuilt detection rule.'
---

# Kubernetes Pod Created With HostPID

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kubernetes Pod Created With HostPID

Kubernetes allows pods to share the host's process ID (PID) namespace, enabling visibility into host processes. While useful for debugging, this can be exploited by attackers to escalate privileges, especially when combined with privileged containers. The detection rule identifies attempts to create or modify pods with HostPID enabled, excluding known safe images, to flag potential privilege escalation activities.

### Possible investigation steps

- Review the Kubernetes audit logs to identify the user or service account responsible for the pod creation or modification attempt. Look for the `kubernetes.audit.user.username` field to determine who initiated the action.
- Examine the `kubernetes.audit.requestObject.spec.containers.image` field to identify the container images used in the pod. Verify if any unknown or suspicious images are being deployed.
- Check the `kubernetes.audit.annotations.authorization_k8s_io/decision` field to confirm that the action was allowed and investigate the context or reason for this decision.
- Investigate the `kubernetes.audit.objectRef.resource` and `kubernetes.audit.verb` fields to understand the specific action taken (create, update, or patch) and the resource involved.
- Assess the necessity and legitimacy of using HostPID in the pod's configuration by consulting with the relevant development or operations teams. Determine if there is a valid use case or if it was potentially misconfigured or maliciously set.
- Review any recent changes in the Kubernetes environment or related configurations that might have led to this alert, focusing on changes around the time the alert was triggered.

### False positive analysis

- Known safe images like "docker.elastic.co/beats/elastic-agent:8.4.0" are already excluded, but other internal tools or monitoring agents that require HostPID for legitimate reasons might trigger false positives. Review and identify such images and add them to the exclusion list.
- Development or testing environments often use HostPID for debugging purposes. Consider creating a separate rule or exception for these environments to prevent unnecessary alerts.
- Some system maintenance tasks might require temporary use of HostPID. Document these tasks and schedule them during known maintenance windows, then adjust the rule to exclude these specific time frames.
- Regularly review audit logs to identify patterns of benign HostPID usage. Use this information to refine the rule and reduce false positives by updating the exclusion criteria.
- Collaborate with development and operations teams to understand legitimate use cases for HostPID in your environment, and adjust the rule to accommodate these scenarios without compromising security.

### Response and remediation

- Immediately isolate the affected pod to prevent further interaction with the host processes. This can be done by cordoning the node or deleting the pod if necessary.
- Review and revoke any unnecessary permissions or roles that may have allowed the creation of pods with HostPID enabled. Ensure that only trusted users and service accounts have the ability to create such pods.
- Conduct a thorough investigation of the container images used in the pod to ensure they are from trusted sources and have not been tampered with. Remove any untrusted or suspicious images from the registry.
- Check for any unauthorized access or changes to the host system's processes and files. If any malicious activity is detected, take steps to restore affected systems from backups and patch any vulnerabilities.
- Implement network segmentation to limit the communication between pods and the host system, reducing the risk of lateral movement by an attacker.
- Enhance monitoring and logging to capture detailed audit logs of Kubernetes API activities, focusing on changes to pod specifications and the use of HostPID. This will aid in detecting similar threats in the future.
- Escalate the incident to the security operations team for further analysis and to determine if additional security measures or incident response actions are required.

## Setup

The Kubernetes Fleet integration with Audit Logs enabled or similarly structured data is required to be compatible with this rule.
