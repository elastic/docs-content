---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS IAM API Calls via Temporary Session Tokens" prebuilt detection rule.'
---

# AWS IAM API Calls via Temporary Session Tokens

## Triage and analysis

### Investigating AWS IAM API Calls via Temporary Session Tokens

Temporary session credentials in AWS (identified by access keys beginning with "ASIA") are typically short-lived tokens 
issued by the AWS Security Token Service (STS). While they are legitimate and often used by developers or automation pipelines, 
their use in direct IAM management or privilege modification is highly unusual and may indicate credential misuse.

Attackers who compromise IAM users, roles, or federated identities can obtain session tokens to blend in with normal operations. 
They may then execute sensitive IAM API actions such as `CreateAccessKey`, `PutUserPolicy`, or `UpdateAssumeRolePolicy` to 
establish persistence, escalate privileges, or disable protections.

### Possible investigation steps

- **Identify the actor**
  - Review `aws.cloudtrail.user_identity.arn` and `aws.cloudtrail.user_identity.type` to determine the originating user or role.
  - This rule automatically filters out console login sessions using `aws.cloudtrail.session_credential_from_console`, so alerts indicate non-console temporary credential usage.
  - Examine `aws.cloudtrail.user_identity.session_context.mfa_authenticated` — absence of MFA may indicate token misuse.

- **Analyze the API context**
  - Review `event.action` and `aws.cloudtrail.request_parameters` for the exact IAM operation performed.
  - Identify whether the action modifies roles, user policies, trust relationships, or credentials.
  - Determine if this session token was associated with prior `sts:GetSessionToken`, `sts:AssumeRole`, or `AWS SSO` events.

- **Evaluate source and behavior**
  - Inspect `source.ip` and `user_agent.original` for unexpected origins or tools.
  - Check if the request came from known infrastructure (e.g., CI/CD nodes, bastion hosts) or an anomalous network.
  - Compare `@timestamp` against normal operating hours or deployment schedules.

- **Correlate related activity**
  - Look for subsequent or preceding activity using the same access key:
    - IAM changes (`CreateUser`, `AttachUserPolicy`, `EnableMFADevice`)
    - STS operations (`AssumeRole`, `GetCallerIdentity`)
    - CloudTrail or GuardDuty configuration changes (possible defense evasion)
  - If applicable, search for multiple users exhibiting similar patterns, a sign of large-scale token misuse.

### False positive analysis

- **Expected automation**
  - Some CI/CD pipelines, monitoring tools, or AWS SDK-based automation may perform IAM operations using temporary credentials.
  - Validate whether the IAM user or assumed role performing these actions belongs to an authorized automation workflow.
- **Administrative operations**
  - Security or DevOps engineers may temporarily use session credentials for maintenance or testing.
  - Cross-reference with recent change tickets or known operations schedules.
- **Federated identity scenarios**
  - Federated logins (via AWS SSO or external IdPs) can also generate temporary "ASIA" credentials. Verify if the source identity 
    aligns with expected roles or groups.
- **Console Login Session**
  - Console login sessions are automatically filtered out by this rule using the `aws.cloudtrail.session_credential_from_console` field.

### Response and remediation

- **Containment**
  - If activity is unauthorized, immediately revoke the temporary session by invalidating the associated IAM credentials.
  - Rotate long-term credentials (access keys, passwords) for the parent IAM user or role.

- **Investigation**
  - Search for all actions linked to the same `access_key_id` to assess potential persistence or lateral movement.
  - Examine the creation of new users, keys, or policies during or shortly after the detected session.

- **Recovery and hardening**
  - Require MFA for all privileged actions using `aws:MultiFactorAuthPresent` conditions.
  - Implement detection coverage for follow-on persistence actions such as:
    - `iam:CreateAccessKey`
    - `iam:PutUserPolicy`
    - `iam:UpdateAssumeRolePolicy`
  - Educate administrative users and developers on secure token handling and the risks of shared credential reuse.

### Additional information

For more information on detecting and mitigating session token abuse:
- **[AWS Security Token Service (STS) Documentation](https://docs.aws.amazon.com/STS/latest/APIReference/Welcome.html)**
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **Security Best Practices:** [AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/).
