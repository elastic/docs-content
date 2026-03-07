---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS EC2 Encryption Disabled" prebuilt detection rule.
---

# AWS EC2 Encryption Disabled

## Triage and analysis

### Investigating AWS EC2 Encryption Disabled

Amazon Elastic Block Store (EBS) encryption ensures that all new EBS volumes and snapshots are encrypted at rest using AWS KMS keys.  
When encryption by default is disabled, new EBS volumes in the region will no longer inherit automatic encryption.  
This action can have serious security implications as it can weaken the organization’s data protection posture, violate compliance requirements, or enable adversaries to read or exfiltrate sensitive information without triggering encryption-based access controls.

#### Possible investigation steps

**Identify the initiator and context**
- Review the `aws.cloudtrail.user_identity` fields to determine who or what performed the `DisableEbsEncryptionByDefault` action.  
  - Examine the `user_identity.type` (e.g., IAMUser, AssumedRole, Root, FederatedUser).  
  - Validate whether the actor is authorized to modify account-level encryption defaults.
- Check `source.ip` and `user_agent.original` to identify the origin of the request and whether it came from a known administrative system, automation process, or an unfamiliar host.
- Correlate with recent IAM activity such as `AttachUserPolicy`, `UpdateAccountPasswordPolicy`, or `PutAccountSetting` to identify potential privilege escalation or account misuse.

**Review the timing and scope**
- Compare the event `@timestamp` with other CloudTrail management events to determine if the encryption change occurred alongside other administrative modifications.  
- Investigate if similar actions were executed in other AWS regions, disabling encryption regionally may be part of a broader campaign.
- Review AWS Config or Security Hub findings to determine whether compliance controls or data protection standards (e.g., CIS, PCI-DSS, ISO 27001) have been violated.

**Assess data exposure risk**
- Identify newly created or modified EBS volumes after the timestamp of this change.  
  - Query CloudTrail for `CreateVolume` or `CreateSnapshot` events without `Encrypted:true`.  
- Determine whether sensitive workloads, such as production databases or applications, rely on unencrypted EBS volumes.  
- Check for `CopySnapshot` or `ModifySnapshotAttribute` activity that could indicate data staging or exfiltration.

**Correlate related security events**
- Look for concurrent detections or GuardDuty findings involving IAM privilege misuse, credential exposure, or configuration tampering.  
- Review CloudTrail logs for any `DisableKeyRotation` or `ScheduleKeyDeletion` events related to the KMS key used for EBS encryption. These may indicate attempts to disrupt encryption mechanisms entirely.
- Review AWS Config timeline to confirm whether encryption-by-default was re-enabled or remained off.

### False positive analysis

- **Administrative changes**: System or cloud administrators may disable default encryption temporarily for troubleshooting or migration. Verify if the user identity, role, or automation process is part of a legitimate change.  
- **Infrastructure testing**: Non-production environments may disable encryption for cost or performance benchmarking. These should be tagged and excluded.  
- **Service misconfiguration**: Some provisioning frameworks or scripts may unintentionally disable encryption defaults during environment setup. Ensure automation code uses explicit encryption flags when creating resources.

If confirmed as expected, document the change request, implementation window, and user responsible for traceability.

### Response and remediation

**Containment and restoration**
- Re-enable EBS encryption by default in the affected region to restore protection for new volumes:
  - Via AWS Console: EC2 → Account Attributes → EBS encryption → Enable by default.  
  - Or via CLI/API: `enable-ebs-encryption-by-default`.  
- Audit recently created EBS volumes and snapshots.  
  - Identify any unencrypted resources and re-encrypt them using KMS keys or snapshot-copy encryption workflows.  
- Verify that AWS Config rules and Security Hub controls related to EBS encryption (`ec2-ebs-encryption-by-default-enabled`) are enabled and compliant.

**Investigate and scope**
- Review IAM policies to ensure only designated administrators have the `ec2:DisableEbsEncryptionByDefault` permission.  
- Check for other regional encryption settings (e.g., S3 default encryption) that may have been modified by the same user or automation role.  
- Examine whether any new IAM roles or policies were added that allow similar encryption or security modifications.

**Long-term hardening**
- Enable organization-level service control policies (SCPs) to prevent future disabling of encryption-by-default across accounts.  
- Establish AWS Config conformance packs or Security Hub standards to continuously monitor this setting.  
- Integrate detection correlation (e.g., link EBS encryption disablement with subsequent unencrypted `CreateVolume` events) for improved alert fidelity.
- Educate administrators on data protection implications and require change approvals for encryption-related settings.

**Recovery validation**
- After restoring encryption-by-default, validate the change in CloudTrail and AWS Config timelines.  
- Confirm that subsequent EBS volumes are created with `Encrypted:true`.  
- Conduct a short post-incident review to document root cause, impact, and lessons learned for compliance audits.

### Additional information

- **[AWS Incident Response Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)**: guidance for investigating unauthorized access to modify account settings.  
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/)**: Example framework for customers to create, develop, and integrate security playbooks in preparation for potential attack scenarios when using AWS services
- **AWS Documentation: [EBS Encryption at Rest](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html)**

