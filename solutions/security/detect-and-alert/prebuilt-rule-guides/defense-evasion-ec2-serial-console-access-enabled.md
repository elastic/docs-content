---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS EC2 Serial Console Access Enabled" prebuilt detection rule.
---

# AWS EC2 Serial Console Access Enabled

## Triage and analysis

### Investigating AWS EC2 Serial Console Access Enabled

The EC2 Serial Console provides a direct connection to an instance's serial port, allowing access even when network connectivity is unavailable. This feature operates completely outside the network layer, meaning traffic does not traverse VPCs, security groups, NACLs, or any network-based monitoring tools. Enabling serial console access at the account level is a prerequisite for using this feature on individual instances.

This rule detects successful `EnableSerialConsoleAccess` API calls, which may indicate an adversary attempting to establish an out-of-band access channel. In most production environments, serial console access should remain disabled unless actively troubleshooting specific issues.

### Possible investigation steps

- **Identify the actor**
  - Review `aws.cloudtrail.user_identity.arn` and `aws.cloudtrail.user_identity.type` to determine who enabled serial console access.
  - Verify whether this principal has a legitimate need for troubleshooting access.

- **Review request context**
  - Check `source.ip`, `source.geo`, and `user_agent.original` for anomalous access patterns.
  - Determine whether this action occurred during normal business hours or maintenance windows.

- **Check for follow-on activity**
  - Search for `SendSerialConsoleSSHPublicKey` API calls, which indicate actual usage of the serial console.
  - Review whether any EC2 instances show serial console sessions after this enablement.

- **Correlate with other suspicious activity**
  - Look for preceding credential theft indicators (e.g., `GetSecretValue`, `CreateAccessKey`).
  - Check for other defense evasion actions such as GuardDuty modifications, CloudTrail changes, or security group modifications.

- **Verify business justification**
  - Confirm with the identified user or team whether there was a legitimate troubleshooting need.
  - Check for related incident tickets or change requests.

### False positive analysis

- **Legitimate troubleshooting**
  - Serial console may be enabled temporarily to troubleshoot instances with SSH access issues or boot failures.
  - Verify this corresponds to known incidents and ensure it was disabled afterward.

- **Automated infrastructure provisioning**
  - Some IaC tools may enable serial console access during instance setup. Validate against CI/CD logs.

### Response and remediation

- **Immediate containment**
  - If unauthorized, immediately disable serial console access using `DisableSerialConsoleAccess`.
  - Review any instances that may have been accessed via serial console.

- **Investigation**
  - Audit CloudTrail for all serial console-related API calls (`EnableSerialConsoleAccess`, `DisableSerialConsoleAccess`, `SendSerialConsoleSSHPublicKey`, `GetSerialConsoleAccessStatus`).
  - Check for any data exfiltration or lateral movement that occurred during the enabled period.

- **Hardening**
  - Restrict `ec2:EnableSerialConsoleAccess` permissions to a limited set of administrative roles.
  - Implement AWS Config rules or Security Hub controls to alert on serial console access state changes.
  - Consider using SCPs to prevent serial console enablement in production accounts.

### Additional information
- **[AWS Documentation: EC2 Serial Console](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-serial-console.html)**
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)**
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)**

