---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS SSM Inventory Reconnaissance by Rare User" prebuilt detection rule.
---

# AWS SSM Inventory Reconnaissance by Rare User

## Triage and analysis

### Investigating AWS SSM Inventory Reconnaissance by Rare User

AWS Systems Manager (SSM) Inventory provides detailed information about managed EC2 instances, including installed 
applications, network configurations, OS details, and patch compliance status. Threat actors, including Scattered 
Spider (LUCR-3), leverage these APIs to discover targets for lateral movement.

This rule detects the first time a specific user (identified by `cloud.account.id` and `user.name`) accesses SSM 
inventory reconnaissance APIs or runs inventory collection commands. These APIs are typically used by automation 
systems, not interactively by humans.

### Possible investigation steps

- **Verify User Identity**: Check `aws.cloudtrail.user_identity.arn` or `user.name` to determine who performed the action.
    - Is this a service account, automation role, or human user?
    - Does this user typically interact with SSM or EC2 infrastructure?
- **Review Source Context**: Examine `source.ip` and `source.geo` to determine where the request originated.
    - Does the source IP match expected locations for this user?
    - Is the source IP from an EC2 instance (potentially compromised) or an external location?
- **Analyze User Agent**: Check `user_agent.original` for suspicious values.
    - AWS CLI, SDK, or CloudShell usage from unexpected users is suspicious.
    - Custom or unusual user agents may indicate attacker tooling.
- **Correlate with Other Events**: Look for other reconnaissance or lateral movement activity from the same user.
    - Check for `StartSession`, `SendCommand`, or other SSM execution APIs.
    - Look for `GetCallerIdentity` calls which often precede reconnaissance.
- **Review Timeline**: Investigate activity 30 minutes before and after this event.
    - Was there an initial access event (e.g., console login, `AssumeRole`)?
    - Did the user proceed to access secrets or attempt lateral movement?

### False positive analysis

- Automation and Monitoring: Legitimate monitoring tools, asset management systems, or compliance scanners may query SSM inventory regularly. These should use dedicated service accounts.
- Administrator Activity: Cloud administrators may occasionally query inventory for troubleshooting. Verify with the user whether this was intentional.
- CI/CD Pipelines: Deployment pipelines may check patch compliance before deployments.
- SSM Associations: The `AWS-GatherSoftwareInventory` document is normally deployed via IaC tools (Terraform, CloudFormation) or the AWS Console during initial setup. Interactive `CreateAssociation` calls outside of these contexts warrant investigation.

### Response and remediation

- Immediate Verification: Contact the user to verify whether they performed this action intentionally.
- Review Permissions: If unauthorized, review and restrict the user's IAM permissions following least privilege.
- Investigate Credential Compromise: If the user did not perform this action, treat their credentials as compromised.
    - Rotate access keys and session tokens.
    - Review recent activity for data exfiltration or privilege escalation.
- Enhanced Monitoring: Add the user or role to enhanced monitoring if suspicious activity is confirmed.

### Additional information
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **[AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/)**

