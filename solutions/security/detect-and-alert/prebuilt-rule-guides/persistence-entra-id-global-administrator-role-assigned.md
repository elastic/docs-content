---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Entra ID Global Administrator Role Assigned" prebuilt detection rule.
---

# Entra ID Global Administrator Role Assigned

## Triage and analysis

### Investigating Entra ID Global Administrator Role Assigned

Microsoft Entra ID's Global Administrator role grants comprehensive access to manage Microsoft Entra ID and associated services. Adversaries may exploit this by assigning themselves or others to this role, ensuring persistent control over resources. The detection rule identifies such unauthorized assignments by monitoring specific audit logs for role changes, focusing on the addition of members to the Global Administrator role, thus helping to mitigate potential security breaches.

### Possible investigation steps

- Review the Microsoft Entra ID audit logs to identify the user account that performed the "Add member to role" operation, focusing on the specific event dataset and operation name.
- Verify the identity of the user added to the Global Administrator role by examining the modified properties in the audit logs, specifically the new_value field indicating "Global Administrator".
- Check the history of role assignments for the identified user to determine if this is a recurring pattern or a one-time event.
- Investigate the source IP address and location associated with the role assignment event to assess if it aligns with expected user behavior or if it indicates potential unauthorized access.
- Review any recent changes or activities performed by the newly assigned Global Administrator to identify any suspicious actions or configurations that may have been altered.
- Consult with the organization's IT or security team to confirm if the role assignment was authorized and aligns with current administrative needs or projects.
- Correlate with Microsoft Entra ID sign-in logs to check for any unusual login patterns or failed login attempts associated with the user who assigned the role.
- Review the reported device to determine if it is a known and trusted device or if it raises any security concerns such as unexpected relationships with the source user.

### False positive analysis

- Routine administrative tasks may trigger alerts when legitimate IT staff are assigned the Global Administrator role temporarily for maintenance or configuration purposes. To manage this, create exceptions for known IT personnel or scheduled maintenance windows.
- Automated scripts or third-party applications that require elevated permissions might be flagged if they are configured to add users to the Global Administrator role. Review and whitelist these scripts or applications if they are verified as safe and necessary for operations.
- Organizational changes, such as mergers or restructuring, can lead to legitimate role assignments that appear suspicious. Implement a review process to verify these changes and exclude them from triggering alerts if they align with documented organizational changes.
- Training or onboarding sessions for new IT staff might involve temporary assignment to the Global Administrator role. Establish a protocol to document and exclude these training-related assignments from detection alerts.

### Response and remediation

- Immediately remove any unauthorized users from the Global Administrator role to prevent further unauthorized access and control over Azure AD resources.
- Conduct a thorough review of recent audit logs to identify any additional unauthorized changes or suspicious activities associated with the compromised account or role assignments.
- Reset the credentials of the affected accounts and enforce multi-factor authentication (MFA) to enhance security and prevent further unauthorized access.
- Notify the security operations team and relevant stakeholders about the incident for awareness and further investigation.
- Implement conditional access policies to restrict Global Administrator role assignments to specific, trusted locations or devices.
- Review and update role assignment policies to ensure that only a limited number of trusted personnel have the ability to assign Global Administrator roles.
- Enhance monitoring and alerting mechanisms to detect similar unauthorized role assignments in the future, ensuring timely response to potential threats.

