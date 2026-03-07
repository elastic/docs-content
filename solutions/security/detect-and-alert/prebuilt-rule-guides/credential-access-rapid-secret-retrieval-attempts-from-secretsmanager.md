---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS Secrets Manager Rapid Secrets Retrieval" prebuilt detection rule.
---

# AWS Secrets Manager Rapid Secrets Retrieval

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. 
> While every effort has been made to ensure its quality, validate and adapt it for your operational needs.

### Investigating AWS Secrets Manager Rapid Secrets Retrieval

AWS Secrets Manager stores sensitive credentials such as database passwords, API keys, OAuth tokens, and service 
configuration values. In credential compromise scenarios, attackers frequently attempt to retrieve as many secrets as 
possible in a short timeframe to escalate privileges or move laterally across the environment.

This threshold rule triggers when a single user identity successfully retrieves 20 or more unique secrets using 
`GetSecretValue` or `BatchGetSecretValue` within a short timespan. Retrieval of many different secrets in rapid succession is highly unusual and strongly associated with reconnaissance, secret harvesting, or compromised automation.

Note: `BatchGetSecretValue` API calls the `GetSecretValue` API for each secret value; this alert only captures the `GetSecretValue` calls rather than the `BatchGetSecretValue` call itself.

#### Possible investigation steps

- **Identify the user or role**
  - Review `aws.cloudtrail.user_identity.arn`, `user.name`, and `aws.cloudtrail.user_identity.type`.
  - Determine whether the identity normally accesses Secrets Manager or is tied to a known automation workload.

- **Analyze the set of secrets retrieved**
  - Expand the alert in Timeline and review `aws.cloudtrail.request_parameters` for all `SecretId` values in the grouped threshold event.
  - Identify whether the accessed secrets include:
    - Privileged database credentials  
    - IAM user or service account credentials  
    - Production application secrets  
    - Rarely accessed or high-sensitivity secrets  

- **Assess the runtime context**
  - Investigate `source.ip`, `source.geo.location`, and `user_agent.original`.
  - Validate whether the calls originated from known internal automation (e.g., ECS task, Lambda runtime, EC2 instance profile) 
    or from an unexpected IP or user agent.

- **Correlate with other activity from the same identity**
  - Look for related reconnaissance or credential-access events:
    - `ListSecrets`, `DescribeSecret`
    - IAM enumeration (`ListUsers`, `GetCallerIdentity`)
    - Role-chaining or unusual `AssumeRole` flows  
  - Check for subsequent use of exposed credentials (RDS login attempts, API activity, abnormal resource access).

- **Determine whether unusual automation or deployment activity is occurring**
  - Confirm with application owners whether a new deployment, config reload, or migration might explain the multi-secret access.

### False positive analysis

- Legitimate application initialization or rollouts may retrieve many secrets once on startup.
- CI/CD pipelines or configuration management tools may enumerate secrets as part of environment bootstrapping.

To reduce noise, consider exceptions based on:
- Known service roles  
- Expected source IP ranges  
- Specific application identities tied to secret orchestration  

### Response and remediation

- **Containment**
  - Immediately revoke or disable the IAM user, role session, or instance profile if compromise is suspected.
  - Quarantine EC2/ECS/Lambda resources originating suspicious calls.

- **Investigation**
  - Identify all secrets accessed in the grouped alert and determine where those credentials are used.
  - Review CloudTrail for any suspicious follow-on activity using the retrieved secrets.
  - Assess whether additional identities or workloads show similar enumeration behavior.

- **Recovery and hardening**
  - Rotate all accessed secrets and update dependent systems.
  - Rotate IAM access keys or temporary credentials for the impacted identity.
  - Restrict permissions to Secrets Manager following least privilege.
  - Review automation and application behavior to ensure secrets are accessed only when required.

