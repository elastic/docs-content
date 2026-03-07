---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS IAM OIDC Provider Created by Rare User" prebuilt detection rule.'
---

# AWS IAM OIDC Provider Created by Rare User

## Triage and analysis

### Investigating AWS IAM OIDC Provider Created by Rare User

OpenID Connect (OIDC) providers in AWS IAM enable web identity federation, allowing external identity providers to authenticate users who then assume IAM roles. Common legitimate use cases include GitHub Actions accessing AWS resources, Kubernetes pods authenticating to AWS, and web applications using social login.

This rule detects the first time a specific user or role creates an OIDC provider within an account. While OIDC provider creation is common in some environments, a new user creating one for the first time warrants validation to ensure it's authorized.

### Possible investigation steps

- **Identify the actor**
  - Review `aws.cloudtrail.user_identity.arn` to determine who created the OIDC provider.
  - Check if this user has created OIDC providers before in other accounts.

- **Review the OIDC provider details**
  - Examine `aws.cloudtrail.request_parameters` for the provider URL and client IDs.
  - Identify the external IdP (e.g., GitHub, Google, custom provider).

- **Validate business justification**
  - Confirm with DevOps or platform teams whether this aligns with CI/CD pipeline setup.
  - Check for related change tickets or infrastructure-as-code deployments.

- **Check for follow-on activity**
  - Search for `CreateRole` or `UpdateAssumeRolePolicy` calls that trust the new OIDC provider.
  - Look for `AssumeRoleWithWebIdentity` calls using the newly created provider.

- **Correlate with other suspicious activity**
  - Check for preceding privilege escalation or credential access events.
  - Look for other persistence mechanisms being established concurrently.

### False positive analysis

- **CI/CD pipeline integration**
  - GitHub Actions, GitLab CI, and other CI/CD systems commonly use OIDC for AWS authentication.
  - Validate against known DevOps workflows.

- **Kubernetes federation**
  - EKS and self-managed Kubernetes clusters may use OIDC providers for pod identity.
  - Confirm with platform engineering teams.

- **Infrastructure-as-code deployments**
  - Terraform, CloudFormation, or other IaC tools may create OIDC providers.
  - Verify via CI/CD logs.

### Response and remediation

- **Immediate containment**
  - If unauthorized, delete the OIDC provider using `DeleteOpenIDConnectProvider`.
  - Review and remove any IAM roles that trust the rogue provider.

- **Investigation**
  - Audit CloudTrail for any `AssumeRoleWithWebIdentity` calls using this provider.
  - Review all IAM roles with web identity trust relationships.

- **Hardening**
  - Restrict `iam:CreateOpenIDConnectProvider` permissions to authorized roles.
  - Implement SCPs to control OIDC provider creation in member accounts.
  - Enable AWS Config rules to monitor identity provider configurations.

### Additional information
- **[AWS IAM OIDC Providers Documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_oidc.html)**
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)**
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)**
