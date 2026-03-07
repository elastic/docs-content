---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS Bedrock Detected Multiple Validation Exception Errors by a Single User" prebuilt detection rule.
---

# AWS Bedrock Detected Multiple Validation Exception Errors by a Single User

## Triage and analysis

### Investigating AWS Bedrock Detected Multiple Validation Exception Errors by a Single User

Amazon Bedrock is AWS’s managed service that enables developers to build and scale generative AI applications using large foundation models (FMs) from top providers.

Bedrock offers a variety of pretrained models from Amazon (such as the Titan series), as well as models from providers like Anthropic, Meta, Cohere, and AI21 Labs.

#### Possible investigation steps

- Identify the user account that caused validation errors in accessing the Amazon Bedrock models.
- Investigate other alerts associated with the user account during the past 48 hours.
- Consider the time of day. If the user is a human (not a program or script), did the activity take place during a normal time of day?
- Examine the account's attempts to access Amazon Bedrock models in the last 24 hours.
- If you suspect the account has been compromised, scope potentially compromised assets by tracking Amazon Bedrock model access, prompts generated, and responses to the prompts by the account in the last 24 hours.

### False positive analysis

- Verify the user account that that caused validation errors is a legitimate misunderstanding by users on accessing the bedrock models.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Disable or limit the account during the investigation and response.
- Identify the possible impact of the incident and prioritize accordingly; the following actions can help you gain context:
    - Identify the account role in the cloud environment.
    - Identify if the attacker is moving laterally and compromising other Amazon Bedrock Services.
    - Identify any regulatory or legal ramifications related to this activity.
    - Identify if any implication to resource billing.
- Review the permissions assigned to the implicated user group or role behind these requests to ensure they are authorized and expected to access bedrock and ensure that the least privilege principle is being followed.
- Determine the initial vector abused by the attacker and take action to prevent reinfection via the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

