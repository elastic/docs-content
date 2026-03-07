---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS Sign-In Root Password Recovery Requested" prebuilt detection rule.'
---

# AWS Sign-In Root Password Recovery Requested

## Triage and analysis

### Investigating AWS Sign-In Root Password Recovery Requested

In AWS, a `PasswordRecoveryRequested` event from `signin.amazonaws.com` is only generated for the root user during the “Forgot your password?” workflow. Other identity types (IAM or federated users) do not trigger this event. A root password recovery request is a critical identity security event that could indicate a legitimate recovery by the account owner or a malicious attempt to gain full administrative access.

### Possible investigation steps

- **Verify the event details.**  
  Review the alert fields (`source.ip`, `user_agent.original`, `cloud.region`, and `@timestamp`) to confirm when and from where the request originated.

- **Confirm legitimacy.**  
  Contact the account owner or credential custodian to verify whether they initiated the password recovery.  
  AWS will also send an email notification to the root account email address, check whether the owner received and acknowledged this.

- **Check CloudTrail for related events.**  
  Search for any subsequent `ConsoleLogin` events for the root user, or IAM changes (for example, `CreateAccessKey`, `CreateUser`, or `AttachUserPolicy`) shortly after the recovery request.

- **Assess IP reputation and location.**  
  Validate whether the `source.ip` aligns with known admin networks or expected geographies.  
  Suspicious indicators include foreign IPs, anonymization services, or unfamiliar user agents.

- **Correlate with other alerts.**  
  Review other AWS security detections (for example, root logins, MFA disablement, or IAM policy changes) around the same timeframe.

### False positive analysis

- **Expected maintenance activity.**  
  If the root account owner confirms that the password reset was intentional (for example, for account recovery or planned credential rotation), the alert may be safely dismissed.  
- **Testing or account verification.**  
  Security or compliance teams occasionally test password recovery flows. Confirm via ticketing or planned maintenance documentation.

### Response and remediation

**Immediate actions**
- **If confirmed legitimate:**  
  - Ensure that MFA is enabled and operational for the root account.  
  - Encourage rotation of the root password if not recently updated.  
- **If unconfirmed or suspicious:**  
  - Immediately reset the root password using the legitimate AWS recovery email link.  
  - Review the AWS account’s email for password-recovery notifications and secure that inbox (change its password, enable MFA).  
  - Check for new successful root logins or unexpected IAM changes since the recovery attempt.  

**Evidence preservation**
- Export the `PasswordRecoveryRequested` event from CloudTrail (±30 minutes).  
- Preserve all `signin.amazonaws.com` and root `ConsoleLogin` events for the next 24 hours.  
- Store this evidence in a restricted S3 bucket with Object Lock enabled.

**Scoping and investigation**
- Review all root-level activities within the past 24–48 hours.  
  Focus on administrative actions such as `CreateAccessKey`, `UpdateAccountPasswordPolicy`, or `DisableMFA`.  
- Correlate with GuardDuty findings and AWS Config change history for any unauthorized modifications.

**Recovery and hardening**
- Confirm MFA is enforced on the root account.  
- Rotate all root credentials and ensure no access keys exist for the root user (root keys should never be active).  
- Secure the associated email account (password reset notifications are sent there).  
- Enable Cloudtrail, GuardDuty, Security Hub, and AWS Config across all regions.  
- Review account recovery procedures to ensure multiple custodians are aware of the legitimate process.

### Additional information

- **AWS Incident Response Playbooks:**    
  and [`IRP-Credential-Compromise.md`](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/IRP-CredCompromise.md) for procedures related to root account credential recovery and unauthorized access attempts.  
- **AWS Customer Playbook Framework:**  
  See [`Compromised_IAM_Credentials.md`](https://github.com/aws-samples/aws-customer-playbook-framework/blob/a8c7b313636b406a375952ac00b2d68e89a991f2/docs/Compromised_IAM_Credentials.md) for guidance on containment, evidence collection, and recovery validation.  
- **AWS Documentation:** [AWS account root user best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html).  
- **Security Best Practices:** [AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/).
