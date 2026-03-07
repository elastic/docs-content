---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS IAM SAML Provider Created" prebuilt detection rule.'
---

# AWS IAM SAML Provider Created

## Triage and analysis

### Investigating AWS IAM SAML Provider Created

SAML (Security Assertion Markup Language) providers in AWS IAM enable federated authentication, allowing users from external identity providers to access AWS resources without separate AWS credentials. Creating a SAML provider establishes a trust relationship between AWS and the external IdP.

This rule detects successful `CreateSAMLProvider` API calls. In most environments, SAML provider creation is extremely rare—typically only occurring during initial SSO setup or major infrastructure changes. An unauthorized SAML provider creation could enable an attacker to maintain persistent access by forging SAML assertions from an IdP they control.

### Possible investigation steps

- **Identify the actor**
  - Review `aws.cloudtrail.user_identity.arn` to determine who created the SAML provider.
  - Verify whether this principal is authorized to manage identity federation.

- **Review the SAML provider details**
  - Examine `aws.cloudtrail.request_parameters` for the SAML provider name and metadata document.
  - Identify the external IdP URL and signing certificate in the metadata.

- **Validate business justification**
  - Confirm with identity management or platform teams whether this aligns with planned SSO integration.
  - Check for related change tickets or infrastructure-as-code deployments.

- **Check for follow-on activity**
  - Search for `CreateRole` or `UpdateAssumeRolePolicy` calls that reference the new SAML provider.
  - Look for `AssumeRoleWithSAML` calls using the newly created provider.

- **Correlate with other suspicious activity**
  - Check for preceding privilege escalation or credential access events.
  - Look for other persistence mechanisms being established concurrently.

### False positive analysis

- **Planned SSO integration**
  - SAML providers are created during initial setup of identity federation with Okta, Azure AD, or other IdPs.
  - Validate against documented SSO integration projects.

- **Infrastructure-as-code deployments**
  - Terraform, CloudFormation, or other IaC tools may create SAML providers as part of automated deployments.
  - Confirm via CI/CD logs.

### Response and remediation

- **Immediate containment**
  - If unauthorized, delete the SAML provider using `DeleteSAMLProvider`.
  - Review and remove any IAM roles that trust the rogue provider.

- **Investigation**
  - Audit CloudTrail for any `AssumeRoleWithSAML` calls using this provider.
  - Review all IAM roles with SAML trust relationships.

- **Hardening**
  - Restrict `iam:CreateSAMLProvider` permissions to a limited set of administrative roles.
  - Implement SCPs to control SAML provider creation in member accounts.
  - Enable AWS Config rules to monitor identity provider configurations.

### Additional information
- **[AWS IAM SAML Providers Documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html)**
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)**
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)**
