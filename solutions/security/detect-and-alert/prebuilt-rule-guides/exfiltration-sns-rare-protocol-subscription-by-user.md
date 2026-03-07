---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS SNS Rare Protocol Subscription by User" prebuilt detection rule.
---

# AWS SNS Rare Protocol Subscription by User

## Triage and analysis

### Investigating AWS SNS Rare Protocol Subscription by User

This rule identifies when an SNS topic is subscribed to by a rare protocol for a particular user. While subscribing to SNS topics is a common practice, adversaries may exploit this feature to collect sensitive information or exfiltrate data via an external email address, mobile number, or cross-account AWS service like Lambda.

This is a [New Terms](https://www.elastic.co/guide/en/security/current/rules-ui-create.html#create-new-terms-rule) rule that only flags when this behavior is observed using a protocol for the first time.

#### Possible Investigation Steps

- **Identify the Actor**: Review the `aws.cloudtrail.user_identity.arn` field to identify the user who requested the subscription. Verify if this actor typically performs such actions and has the necessary permissions. It may be unusual for this activity to originate from certain user types, such as an assumed role or federated user.
- **Review the SNS Subscription Event**: Analyze the specifics of the `Subscribe` action in CloudTrail logs:
  - **Topic**: Look at the `aws.cloudtrail.request_parameters` field to identify the SNS topic involved in the subscription.
  - **Protocol and Endpoint**: Review the `aws.cloudtrail.request_parameters` field to confirm the subscription's protocol and endpoint, if available. Confirm if this endpoint is associated with a known or trusted entity.
  - **Subscription Status**: Check the `aws.cloudtrail.response_elements` field for the subscription's current status, noting if it requires confirmation.
- **Verify Authorization**: Evaluate whether the user typically engages in SNS subscription actions and if they are authorized to do so for the specified topic.
- **Contextualize with Related Events**: Review related CloudTrail logs around the event time for other actions by the same user or IP address. Look for activities involving other AWS services, such as S3 or IAM, that may indicate further suspicious behavior.
- **Check for Publish Actions**: Investigate for any subsequent `Publish` actions on the same SNS topic that may indicate exfiltration attempts or data leakage. If Publish actions are detected, further investigate the contents of the messages.
- **Review IAM Policies**: Examine the user or role's IAM policies to ensure that the subscription action is within the scope of their permissions or should be.

### False Positive Analysis

- **Historical User Actions**: Verify if the user has a history of performing similar actions on SNS topics. Consistent, repetitive actions may suggest legitimate usage.
- **Scheduled or Automated Tasks**: Confirm if the subscription action aligns with scheduled tasks or automated notifications authorized by your organization.

### Response and Remediation

- **Immediate Review and Reversal**: If the subscription was unauthorized, take appropriate action to cancel it and adjust SNS permissions as necessary.
- **Strengthen Monitoring and Alerts**: Configure monitoring systems to flag similar actions involving sensitive topics or unapproved endpoints.
- **Policy Review**: Review and update policies related to SNS subscriptions and access, tightening control as needed to prevent unauthorized subscriptions.
- **Incident Response**: If there is evidence of malicious intent, treat the event as a potential data exfiltration incident and follow incident response protocols, including further investigation, containment, and recovery.

### Additional Information

For further guidance on managing and securing SNS topics in AWS environments, refer to the [AWS SNS documentation](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) and AWS best practices for security.


