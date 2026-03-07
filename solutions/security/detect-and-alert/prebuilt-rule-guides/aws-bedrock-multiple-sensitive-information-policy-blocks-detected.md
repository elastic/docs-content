---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual High Denied Sensitive Information Policy Blocks Detected" prebuilt detection rule.
---

# Unusual High Denied Sensitive Information Policy Blocks Detected

## Triage and analysis

### Investigating Unusual High Denied Sensitive Information Policy Blocks Detected

Amazon Bedrock Guardrail is a set of features within Amazon Bedrock designed to help businesses apply robust safety and privacy controls to their generative AI applications.

It enables users to set guidelines and filters that manage content quality, relevancy, and adherence to responsible AI practices.

Through Guardrail, organizations can define "sensitive information filters" to prevent the model from generating content on specific, undesired subjects,
and they can establish thresholds for harmful content categories.

#### Possible investigation steps

- Identify the user account that queried sensitive information and whether it should perform this kind of action.
- Investigate other alerts associated with the user account during the past 48 hours.
- Consider the time of day. If the user is a human (not a program or script), did the activity take place during a normal time of day?
- Examine the account's prompts and responses in the last 24 hours.
- If you suspect the account has been compromised, scope potentially compromised assets by tracking Amazon Bedrock model access, prompts generated, and responses to the prompts by the account in the last 24 hours.

### False positive analysis

- Verify the user account that queried denied topics, is not testing any new model deployments or updated compliance policies in Amazon Bedrock guardrails.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Disable or limit the account during the investigation and response.
- Identify the possible impact of the incident and prioritize accordingly; the following actions can help you gain context:
    - Identify the account role in the cloud environment.
    - Identify if the attacker is moving laterally and compromising other Amazon Bedrock Services.
    - Identify any regulatory or legal ramifications related to this activity.
- Review the permissions assigned to the implicated user group or role behind these requests to ensure they are authorized and expected to access bedrock and ensure that the least privilege principle is being followed.
- Determine the initial vector abused by the attacker and take action to prevent reinfection via the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

