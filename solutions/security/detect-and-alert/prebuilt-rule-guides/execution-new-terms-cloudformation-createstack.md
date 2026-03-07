---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "First Time AWS CloudFormation Stack Creation" prebuilt detection rule.'
---

# First Time AWS CloudFormation Stack Creation

## Triage and analysis

### Investigating First Time AWS CloudFormation Stack Creation

AWS CloudFormation automates the setup of cloud resources using templates, streamlining infrastructure management. Adversaries with access can exploit this to deploy malicious resources, escalating their control. The detection rule identifies unusual activity by flagging the initial use of stack creation APIs by a user or role, helping to spot potential unauthorized actions early.

### Possible investigation steps

- Review `aws.cloudtrail.user_identity.arn` to identify the user or role that initiated the `CreateStack` or `CreateStackInstances` action.
- Verify the IAM permissions of the user or role involved in the event to ensure they have the appropriate level of access and determine if the action aligns with their typical responsibilities.
- Examine the stack template used to identify any unusual or unauthorized resources being provisioned.
- Investigate any related resources that were deployed as part of the stack.
- Correlate the timing of the stack creation with other logs or alerts to identify any suspicious activity or patterns that might indicate malicious intent.
- Investigate the account's recent activity history to determine if there have been any other first-time or unusual actions by the same user or role.

### False positive analysis

- Routine infrastructure updates by authorized users may trigger the rule. To manage this, maintain a list of users or roles that regularly perform these updates and create exceptions for them.
- Automated deployment tools or scripts that use CloudFormation for legitimate purposes can cause false positives. Identify these tools and exclude their associated IAM roles or users from the rule.
- New team members or roles onboarding into cloud management tasks might be flagged. Implement a process to review and whitelist these users after verifying their activities.
- Scheduled or periodic stack creations for testing or development environments can be mistaken for suspicious activity. Document these schedules and exclude the relevant users or roles from the rule.
- Third-party services or integrations that require stack creation permissions could be misidentified. Ensure these services are documented and their actions are excluded from triggering the rule.

### Response and remediation

- Immediately isolate the IAM user or role that initiated the stack creation to prevent further unauthorized actions. This can be done by revoking permissions with a [DenyAll](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSDenyAll.html) permissions policy or disabling the account temporarily.
- Review the created stack for any unauthorized or suspicious resources. Identify and terminate any resources that are not part of the expected infrastructure.
- Conduct a thorough audit of recent IAM activity to identify any other unusual or unauthorized actions that may indicate further compromise.
- If malicious activity is confirmed, escalate the incident to the security operations team for a full investigation and potential involvement of incident response teams.
- Implement additional monitoring and alerting for the affected account to detect any further unauthorized attempts to use CloudFormation or other critical AWS services.
- Review and tighten IAM policies and permissions to ensure that only necessary privileges are granted, reducing the risk of exploitation by adversaries.
