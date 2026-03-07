---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS SNS Topic Created by Rare User" prebuilt detection rule.
---

# AWS SNS Topic Created by Rare User

## Triage and Analysis

### Investigating AWS SNS Topic Created by Rare User

This rule detects the creation of an AWS Simple Notification Service (SNS) topic by a user who does not typically perform this action. Adversaries may create SNS topics to facilitate data exfiltration or other malicious activities.

This is a [New Terms](https://www.elastic.co/guide/en/security/current/rules-ui-create.html#create-new-terms-rule) rule that only flags when this behavior is observed for the first time by a user or role.

### Possible investigation steps

**Identify the actor and context**
  - Examine `aws.cloudtrail.user_identity.arn` to determine **who** created the SNS topic.
  - Identify whether the actor assumed a privileged IAM role (`aws.cloudtrail.user_identity.type: "AssumedRole"`) or used a long term access keys (`aws.cloudtrail.user_identity.access_key_id`).
  - Check `user_agent.original` to determine if this action was performed via the AWS CLI, SDK, or Console.
  - If `aws-cli` was used, review whether it aligns with typical automation or administrative behavior.
  - Review `source.ip` and `source.geo` fields to confirm if the request originated from a trusted or unexpected location.

**Evaluate the SNS topic creation**
  - Check `aws.cloudtrail.request_parameters` for the SNS topic name and determine whether it appears suspicious (e.g., random strings, unusual keywords).
  - Verify `cloud.region` and `cloud.account.id` to ensure the SNS topic was created in an expected environment.
  - Identify additional actions **before or after** this event using `event.action` values like:
    - `Subscribe`
    - `Publish`
    - `SetTopicAttributes`
  - These may indicate follow-up steps taken to misuse the SNS topic.

**Analyze potential malicious intent**
  - Check if this user has previously created SNS topics using historical CloudTrail logs.
  - Look for multiple topic creations in a short period, which may suggest an automation script or malicious behavior.
  - If `aws.cloudtrail.user_identity.arn` references an EC2 instance role, verify whether that instance typically performs SNS operations.
  - Review whether new subscriptions were added (`Subscribe` API action) to forward data externally.
  - If an SNS topic was configured to trigger Lambda functions or S3 events, it may indicate an attempt to persist in the environment.

### False positive analysis
- Check whether the SNS topic creation aligns with known DevOps, automation, or monitoring activities.
- If the user typically interacts with SNS, consider allowlisting expected IAM roles for this action.
- Some AWS services may auto-create SNS topics for alerts and monitoring. Confirm whether the creation was system-generated.

### Response and remediation
- **Confirm Authorization**:
  - If the user was not expected to create SNS topics, verify whether their IAM permissions should be restricted.
  - If unauthorized, disable the access keys or IAM role associated with the event.
- **Monitor for Further SNS Modifications**:
  - Set up additional monitoring for SNS Publish or Subscription events (`Publish`, `Subscribe`).
- **Investigate for Persistence**:
  - Check whether the SNS topic is being used as a notification channel for Lambda, S3, or other AWS services.
- **Enhance IAM Policy Controls**:
  - Consider enforcing least privilege IAM policies and enabling multi-factor authentication (MFA) where applicable.

