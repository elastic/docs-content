---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS IAM CompromisedKeyQuarantine Policy Attached to User" prebuilt detection rule.'
---

# AWS IAM CompromisedKeyQuarantine Policy Attached to User

## Triage and analysis

### Investigating AWS IAM CompromisedKeyQuarantine Policy Attached to User

The AWS IAM `CompromisedKeyQuarantine` and `CompromisedKeyQuarantineV2` managed policies deny certain action and is applied by the AWS team to a user with exposed credentials.
This action is accompanied by a support case which specifies instructions to follow before detaching the policy.

#### Possible Investigation Steps

- **Identify Potentially Compromised Identity**: Review the `userName` parameter of the `aws.cloudtrail.request_parameters` to determine the quarantined IAM entity.
- **Contextualize with AWS Support Case**: Review any information from AWS comtaining additional information about the quarantined account and the reasoning for quarantine.
- **Follow Support Case Instructions**: Do not revert the quarantine policy attachment or delete the compromised keys. Instead folow the instructions given in your support case.
- **Correlate with Other Activities**: Search for related CloudTrail events before and after this change to see if the same actor or IP address engaged in potentially suspicious activities.
- **Interview Relevant Personnel**: If the compromised key belongs to a user, verify the intent and authorization for these correlated actions with the person or team responsible for managing the compromised key.

### False Positive Analysis

- There shouldn't be many false positives related to this action as it is inititated by AWS in response to compromised or publicly exposed credentials.

### Response and Remediation

- **Immediate Review and Reversal**: Update the user IAM permissions to remove the quarantine policy and disable the compromised credentials.
- **Policy Update**: Review and possibly update your organization’s policies on credential storage to tighten control and prevent public exposure.
- **Incident Response**: If malicious intent is confirmed, consider it a data breach incident and initiate the incident response protocol. This includes further investigation, containment, and recovery.

### Additional Information:

For further guidance on managing and securing credentials in AWS environments, refer to the [AWS IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html) regarding security best practices and guidance on [Remediating Potentially Compromised AWS Credentials](https://docs.aws.amazon.com/guardduty/latest/ug/compromised-creds.html).
