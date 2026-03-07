---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Kernel Driver Load by non-root User" prebuilt detection rule.'
---

# Kernel Driver Load by non-root User

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kernel Driver Load by non-root User

Kernel modules extend the functionality of the Linux kernel, allowing dynamic loading of drivers or features. Typically, only root users can load these modules due to their potential to alter system behavior. Adversaries may exploit this by loading malicious modules, such as rootkits, to gain control and evade detection. The detection rule identifies non-root users attempting to load modules, signaling potential unauthorized activity.

### Possible investigation steps

- Review the alert details to identify the non-root user (user.id) involved in the kernel module loading attempt.
- Check the system logs and audit logs for any additional context around the time of the event, focusing on the specific system calls (init_module, finit_module) used.
- Investigate the source and legitimacy of the kernel module being loaded by examining the module's file path and associated metadata.
- Assess the user's recent activity and permissions to determine if there are any signs of privilege escalation or unauthorized access.
- Correlate this event with other security alerts or anomalies on the same host to identify potential patterns of malicious behavior.
- Verify the integrity and security posture of the affected system by running a comprehensive malware and rootkit scan.

### False positive analysis

- Legitimate software or system utilities may occasionally load kernel modules as part of their normal operation. Identify these applications and verify their behavior to ensure they are not malicious.
- Development environments or testing scenarios might involve non-root users loading kernel modules for legitimate purposes. Consider creating exceptions for these specific users or processes after thorough validation.
- Some system management tools or scripts executed by non-root users might trigger this rule. Review these tools and, if deemed safe, add them to an exception list to prevent unnecessary alerts.
- In environments where non-root users are granted specific permissions to load kernel modules, ensure these permissions are documented and monitored. Adjust the rule to exclude these known and authorized activities.
- Regularly review and update the list of exceptions to ensure that only verified and non-threatening behaviors are excluded, maintaining the integrity of the detection rule.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or potential lateral movement by the adversary.
- Terminate any suspicious processes associated with the non-root user attempting to load the kernel module to halt any ongoing malicious activity.
- Conduct a thorough review of the loaded kernel modules on the affected system to identify and remove any unauthorized or malicious modules.
- Reset credentials and review permissions for the non-root user involved in the alert to prevent further unauthorized actions.
- Escalate the incident to the security operations team for a deeper forensic analysis to determine the scope of the compromise and identify any additional affected systems.
- Implement enhanced monitoring and logging for kernel module loading activities across all systems to detect similar threats in the future.
- Review and update security policies to ensure that only authorized users have the necessary permissions to load kernel modules, reducing the risk of unauthorized access.
