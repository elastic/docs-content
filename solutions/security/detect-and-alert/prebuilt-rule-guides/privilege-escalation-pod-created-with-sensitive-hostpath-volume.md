---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Kubernetes Pod Created with a Sensitive hostPath Volume" prebuilt detection rule.
---

# Kubernetes Pod Created with a Sensitive hostPath Volume

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kubernetes Pod Created with a Sensitive hostPath Volume

Kubernetes allows containers to access host filesystems via hostPath volumes, which can be crucial for certain applications. However, if a container is compromised, adversaries can exploit these mounts to access sensitive host data or escalate privileges. The detection rule identifies when pods are created or modified with hostPath volumes pointing to critical directories, signaling potential misuse or security risks.

### Possible investigation steps

- Review the Kubernetes audit logs to identify the specific pod creation or modification event that triggered the alert, focusing on the event.dataset field with the value "kubernetes.audit_logs".
- Examine the kubernetes.audit.requestObject.spec.volumes.hostPath.path field to determine which sensitive hostPath was mounted and assess the potential risk associated with that specific path.
- Check the kubernetes.audit.annotations.authorization_k8s_io/decision field to confirm that the action was allowed, and verify the legitimacy of the authorization decision.
- Investigate the kubernetes.audit.requestObject.spec.containers.image field to identify the container image used, ensuring it is not a known or suspected malicious image, and cross-reference with any known vulnerabilities or security advisories.
- Analyze the context of the pod creation or modification by reviewing the kubernetes.audit.verb field to understand whether the action was a create, update, or patch operation, and correlate this with recent changes or deployments in the environment.
- Assess the potential impact on the cluster by identifying other pods or services that might be affected by the compromised pod, especially those with elevated privileges or access to sensitive data.

### False positive analysis

- Development environments often use hostPath volumes for testing purposes, which can trigger this rule. To manage this, create exceptions for specific namespaces or labels associated with development workloads.
- Monitoring tools or agents may require access to certain host paths for legitimate reasons. Identify these tools and exclude their specific container images from the rule, similar to the exclusion of the elastic-agent image.
- Backup or logging applications might need access to host directories to perform their functions. Review these applications and consider excluding their specific hostPath configurations if they are deemed non-threatening.
- Some system maintenance tasks might temporarily use hostPath volumes. Document these tasks and schedule them during known maintenance windows, then create temporary exceptions during these periods.
- Custom scripts or automation tools that interact with Kubernetes may inadvertently trigger this rule. Audit these scripts and tools, and if they are safe, exclude their specific actions or paths from the rule.

### Response and remediation

- Immediately isolate the affected pod to prevent further access to sensitive host data. This can be done by cordoning the node or deleting the pod if necessary.
- Review and revoke any credentials or tokens that may have been exposed through the compromised pod to prevent unauthorized access to other resources.
- Conduct a thorough analysis of the container image and application code to identify any vulnerabilities or malicious code that may have led to the compromise.
- Patch or update the container image and application code to address any identified vulnerabilities, and redeploy the application with the updated image.
- Implement network policies to restrict pod-to-pod and pod-to-node communication, limiting the potential impact of a compromised pod.
- Enhance monitoring and logging for Kubernetes audit logs to ensure timely detection of similar threats in the future, focusing on unauthorized access attempts and privilege escalation activities.
- Escalate the incident to the security operations team for further investigation and to assess the need for additional security measures or incident response actions.

## Setup

The Kubernetes Fleet integration with Audit Logs enabled or similarly structured data is required to be compatible with this rule.
