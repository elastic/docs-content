---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Virtual Machine Fingerprinting" prebuilt detection rule.'
---

# Virtual Machine Fingerprinting

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Virtual Machine Fingerprinting

Virtual Machine Fingerprinting involves identifying characteristics of a virtual environment, often to tailor attacks or evade detection. Adversaries exploit this by querying system files for hardware details, a tactic seen in malware like Pupy RAT. The detection rule flags non-root users accessing specific Linux paths indicative of VM queries, signaling potential reconnaissance activities.

### Possible investigation steps

- Review the process execution details to identify the non-root user involved in accessing the specified paths, focusing on the user.name field.
- Examine the process.args field to determine which specific file paths were accessed, as this can indicate the type of virtual machine information being targeted.
- Investigate the parent process and command line arguments to understand the context of the process initiation and whether it aligns with legitimate user activity.
- Check for any related alerts or logs around the same timeframe to identify potential patterns or repeated attempts at virtual machine fingerprinting.
- Assess the system for any signs of compromise or unauthorized access, particularly focusing on the presence of known malware like Pupy RAT or similar threats.
- Correlate the findings with MITRE ATT&CK framework references (TA0007, T1082) to understand the broader tactics and techniques potentially in use by the adversary.

### False positive analysis

- Non-root users running legitimate scripts or applications that query system files for hardware information may trigger the rule. Review the context of the process and user activity to determine if it aligns with expected behavior.
- System administrators or developers using automated tools for inventory or monitoring purposes might access these paths. Consider creating exceptions for known tools or scripts that are verified as safe.
- Security or compliance audits conducted by non-root users could inadvertently match the rule's criteria. Document and whitelist these activities if they are part of regular operations.
- Development environments where virtual machine detection is part of testing processes may cause false positives. Identify and exclude these environments from the rule's scope if they are consistently flagged.
- Regularly review and update the list of exceptions to ensure that only verified and necessary exclusions are maintained, minimizing the risk of overlooking genuine threats.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further reconnaissance or potential lateral movement by the adversary.
- Terminate any suspicious processes identified in the alert that are attempting to access the specified system files, especially those not initiated by the root user.
- Conduct a thorough review of recent user activity and process logs to identify any unauthorized access or anomalies that may indicate further compromise.
- Reset credentials for any non-root users involved in the alert to prevent unauthorized access, and review user permissions to ensure least privilege principles are enforced.
- Deploy endpoint detection and response (EDR) tools to monitor for similar suspicious activities and enhance visibility into system processes and user actions.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement additional monitoring and alerting for the specific file paths and processes identified in the query to detect and respond to future attempts at virtual machine fingerprinting.
