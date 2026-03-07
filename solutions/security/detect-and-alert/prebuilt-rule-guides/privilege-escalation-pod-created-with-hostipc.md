---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Kubernetes Pod Created With HostIPC" prebuilt detection rule.
---

# Kubernetes Pod Created With HostIPC

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kubernetes Pod Created With HostIPC

Kubernetes allows pods to share the host's IPC namespace, enabling inter-process communication. While useful for legitimate applications, adversaries can exploit this to access shared memory and IPC mechanisms, potentially leading to data exposure or privilege escalation. The detection rule identifies suspicious pod creation or modification events that enable host IPC, excluding known benign images, to flag potential security threats.

### Possible investigation steps

- Review the Kubernetes audit logs to identify the specific pod creation or modification event that triggered the alert, focusing on the event.dataset field with the value "kubernetes.audit_logs".
- Examine the kubernetes.audit.annotations.authorization_k8s_io/decision field to confirm that the action was allowed, and verify the identity of the user or service account that initiated the request.
- Investigate the kubernetes.audit.objectRef.resource field to ensure the resource involved is indeed a pod, and check the kubernetes.audit.verb field to determine if the action was a create, update, or patch operation.
- Analyze the kubernetes.audit.requestObject.spec.hostIPC field to confirm that host IPC was enabled, and cross-reference with the kubernetes.audit.requestObject.spec.containers.image field to ensure the image is not part of the known benign list.
- Check for any other pods or processes on the host that might be using the host's IPC namespace, and assess if there is any unauthorized access or data exposure risk.
- Look for any suspicious activity or anomalies in the /dev/shm directory or use the ipcs command to identify any IPC facilities that might be exploited.

### False positive analysis

- Pods using hostIPC for legitimate inter-process communication may trigger alerts. Review the pod's purpose and verify if hostIPC is necessary for its function.
- Known benign images, such as monitoring or logging agents, might use hostIPC. Update the exclusion list to include these images if they are verified as non-threatening.
- Development or testing environments often use hostIPC for debugging purposes. Consider excluding these environments from the rule or creating a separate rule with a higher threshold for alerts.
- Automated deployment tools might temporarily use hostIPC during setup. Ensure these tools are recognized and excluded if they are part of a controlled and secure process.
- Regularly review and update the exclusion list to reflect changes in your environment, ensuring that only verified and necessary uses of hostIPC are excluded.

### Response and remediation

- Immediately isolate the affected pod to prevent further access to the host's IPC namespace. This can be done by cordoning the node or deleting the pod if necessary.
- Review and revoke any unnecessary permissions or roles that allowed the pod to be created or modified with hostIPC enabled. Ensure that only trusted entities have the capability to modify pod specifications.
- Conduct a thorough audit of other pods and configurations in the cluster to identify any additional instances where hostIPC is enabled without a valid justification.
- Implement network policies to restrict communication between pods and the host, limiting the potential impact of any unauthorized access to the host's IPC mechanisms.
- Escalate the incident to the security operations team for further investigation and to determine if any data exposure or privilege escalation occurred.
- Update security policies and configurations to prevent the use of hostIPC in future pod deployments unless explicitly required and approved.
- Enhance monitoring and alerting to detect similar attempts in the future, ensuring that any unauthorized use of hostIPC is promptly flagged and addressed.

## Setup

The Kubernetes Fleet integration with Audit Logs enabled or similarly structured data is required to be compatible with this rule.
