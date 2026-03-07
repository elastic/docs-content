---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS EC2 AMI Shared with Another Account" prebuilt detection rule.
---

# AWS EC2 AMI Shared with Another Account

## Triage and analysis

### Investigating AWS EC2 AMI Shared with Another Account

This rule identifies when an Amazon Machine Image (AMI) is shared with another AWS account. While sharing AMIs is a common practice, adversaries may exploit this feature to exfiltrate data by sharing AMIs with external accounts under their control.

#### Possible Investigation Steps

- **Review the Sharing Event**: Identify the AMI involved and review the event details in AWS CloudTrail. Look for `ModifyImageAttribute` actions where the AMI attributes were changed to include additional user accounts.
    - **Request and Response Parameters**: Check the `aws.cloudtrail.request_parameters` and `aws.response.response_elements` fields in the CloudTrail event to identify the AMI ID and the user ID of the account with which the AMI was shared.
- **Verify the Shared AMI**: Check the AMI that was shared and its contents to determine the sensitivity of the data stored within it.
- **Contextualize with Recent Changes**: Compare this sharing event against recent changes in AMI configurations and deployments. Look for any other recent permissions changes or unusual administrative actions.
- **Validate External Account**: Examine the AWS account to which the AMI was shared. Determine whether this account is known and previously authorized to access such resources.
- **Interview Relevant Personnel**: If the share was initiated by a user, verify the intent and authorization for this action with the person or team responsible for managing AMI deployments.
- **Audit Related Security Policies**: Check the security policies governing AMI sharing within your organization to ensure they are being followed and are adequate to prevent unauthorized sharing.

### False Positive Analysis

- **Legitimate Sharing Practices**: AMI sharing is a common and legitimate practice for collaboration and resource management in AWS. Always verify that the sharing activity was unauthorized before escalating.
- **Automation Tools**: Some organizations use automation tools for AMI management which might programmatically share AMIs. Verify if such tools are in operation and whether their actions are responsible for the observed behavior.
- **AWS Services**: Some AWS services, such as WorkSpaces and Backup, automate AMI sharing when users configure cross-account sharing or disaster recovery plans. These will appear in CloudTrail with `userIdentity.invokedBy` and `source.address` fields like `workspaces.amazonaws.com` or `backup.amazonaws.com`. Confirm that such activity aligns with your organization's approved configurations.

### Response and Remediation

- **Review and Revoke Unauthorized Shares**: If the share is found to be unauthorized, immediately revoke the shared permissions from the AMI.
- **Enhance Monitoring of Shared AMIs**: Implement monitoring to track changes to shared AMIs and alert on unauthorized access patterns.
- **Incident Response**: If malicious intent is confirmed, consider it a data breach incident and initiate the incident response protocol. This includes further investigation, containment, and recovery.
- **Policy Update**: Review and possibly update your organization’s policies on AMI sharing to tighten control and prevent unauthorized access.
- **Educate Users**: Conduct training sessions for users involved in managing AMIs to reinforce best practices and organizational policies regarding AMI sharing.

### Additional Information

For more information on managing and sharing AMIs, refer to the [Amazon EC2 User Guide on AMIs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html) and [Sharing AMIs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/sharingamis-explicit.html). Additionally, explore adversarial techniques related to data exfiltration via AMI sharing as documented by Stratus Red Team [here](https://stratus-red-team.cloud/attack-techniques/AWS/aws.exfiltration.ec2-share-ami/).


