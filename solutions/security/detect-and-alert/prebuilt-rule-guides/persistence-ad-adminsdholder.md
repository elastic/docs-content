---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AdminSDHolder Backdoor" prebuilt detection rule.'
---

# AdminSDHolder Backdoor

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating AdminSDHolder Backdoor

The AdminSDHolder object in Active Directory is crucial for maintaining consistent permissions across privileged accounts. It ensures that any changes to these accounts are reverted to match the AdminSDHolder's settings. Adversaries exploit this by modifying the AdminSDHolder to create persistent backdoors, regaining administrative privileges. The detection rule identifies such abuses by monitoring specific directory service changes, focusing on modifications to the AdminSDHolder object, thus alerting security teams to potential threats.

### Possible investigation steps

- Review the event logs for entries with event.code:5136 to identify specific changes made to the AdminSDHolder object.
- Examine the winlog.event_data.ObjectDN field to confirm the object path is CN=AdminSDHolder,CN=System* and verify the nature of the modifications.
- Identify the user account responsible for the changes by checking the event logs for the associated user information.
- Investigate the history of the identified user account to determine if there are any other suspicious activities or patterns of behavior.
- Assess the current permissions on the AdminSDHolder object and compare them with the expected baseline to identify unauthorized changes.
- Check for any recent changes in group memberships or permissions of privileged accounts that could indicate exploitation of the AdminSDHolder backdoor.
- Collaborate with the IT or security team to determine if the changes were authorized or if further action is needed to secure the environment.

### False positive analysis

- Routine administrative changes to the AdminSDHolder object can trigger alerts. To manage this, establish a baseline of expected changes and create exceptions for these known activities.
- Scheduled maintenance or updates to Active Directory may result in temporary modifications to the AdminSDHolder object. Document these events and exclude them from triggering alerts during the maintenance window.
- Automated scripts or tools used for Active Directory management might modify the AdminSDHolder object as part of their normal operation. Identify these tools and whitelist their activities to prevent false positives.
- Changes made by trusted security personnel or systems should be logged and reviewed. Implement a process to verify and exclude these changes from alerting if they are part of approved security operations.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or privilege escalation.
- Revert any unauthorized changes to the AdminSDHolder object by restoring it from a known good backup or manually resetting its permissions to the default secure state.
- Conduct a thorough review of all privileged accounts and groups to ensure their permissions align with organizational security policies and have not been altered to match the compromised AdminSDHolder settings.
- Reset passwords for all accounts that were potentially affected or had their permissions altered, focusing on privileged accounts to prevent adversaries from regaining access.
- Implement additional monitoring on the AdminSDHolder object and other critical Active Directory objects to detect any future unauthorized modifications promptly.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine the scope of the breach, including identifying any other compromised systems or accounts.
- Review and update access control policies and security configurations to prevent similar attacks, ensuring that only authorized personnel have the ability to modify critical Active Directory objects.
