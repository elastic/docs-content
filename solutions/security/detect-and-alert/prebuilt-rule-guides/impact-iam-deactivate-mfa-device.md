---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS IAM Deactivation of MFA Device" prebuilt detection rule.
---

# AWS IAM Deactivation of MFA Device

## Triage and analysis

### Investigating AWS IAM Deactivation of MFA Device

This rule detects successful deactivation of a Virtual MFA device in AWS IAM. 
Deactivation removes MFA enforcement from an IAM user, significantly lowering account resilience against credential theft or unauthorized access. 
Since MFA devices must be deactivated before deletion, this represents the earliest and most critical opportunity to detect potential account compromise or persistence activity.

For more information about using MFA in AWS, access the [official documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html).

#### Possible investigation steps

- **Identify the actor and context**
  - Review `aws.cloudtrail.user_identity.arn` and `aws.cloudtrail.user_identity.access_key_id` to determine who initiated the deactivation.
  - Check whether the actor typically manages MFA or has the IAM permissions to perform such actions.
  - Review `user_agent.original` to confirm if the operation was performed via the AWS Console, CLI, or SDK.

- **Review the source and location**
  - Investigate `source.ip` and `source.geo` fields for unusual origins or unrecognized locations.
  - Determine if this request originated from known automation infrastructure, internal IP ranges, or a personal endpoint.

- **Correlate with other related activity**
  - Look for preceding API calls such as `ListMFADevices`, `GetSessionToken`, or `ListUsers`, which may indicate reconnaissance or IAM enumeration.
  - Search for subsequent `DeleteVirtualMFADevice` calls to confirm whether the deactivated device was later deleted — a common follow-up action.
  - Check for any privilege changes, credential creations (`CreateAccessKey`, `AttachUserPolicy`), or unexpected login attempts following the deactivation.

- **Validate authorization**
  - Confirm with IAM or security administrators whether the action was part of an authorized device rotation or remediation.
  - If not documented or approved, escalate as a potential credential compromise or persistence attempt.

### False positive analysis

- **Legitimate device rotation**
  - When replacing an MFA device, AWS requires deactivation of the existing device before the new one can be enabled.
- **Administrative maintenance**
  - IAM administrators or automation pipelines may deactivate MFA as part of account management or recovery workflows.

### Response and remediation

- **Containment**
  - Re-enable MFA for the affected IAM user (`EnableMFADevice`) or temporarily disable their login access until legitimacy is confirmed.
  - Revoke temporary credentials or tokens associated with the actor to prevent further misuse.

- **Investigation and scoping**
  - Review CloudTrail history for additional IAM configuration changes or access key creation events tied to the same principal.
  - Determine whether sensitive resources were accessed after MFA removal.
  - Identify whether multiple users had MFA devices deactivated in a short timeframe — an indicator of broader compromise.

- **Recovery and hardening**
  - Require MFA for all privileged IAM users and enforce it using service control policies (SCPs).
  - Enable GuardDuty or Security Hub findings for IAM anomaly detection related to account takeover or configuration changes.

### Additional information
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **[DeactivateMFADevice API Reference](https://docs.aws.amazon.com/IAM/latest/APIReference/API_DeactivateMFADevice.html)**  
- **[Managing MFA Devices in IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html)** 

