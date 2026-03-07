---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS IAM Roles Anywhere Trust Anchor Created with External CA" prebuilt detection rule.
---

# AWS IAM Roles Anywhere Trust Anchor Created with External CA

## Triage and analysis

### Investigating AWS IAM Roles Anywhere Trust Anchor Created with External CA

AWS IAM Roles Anywhere allows workloads outside AWS (such as on-premises servers or CI/CD agents) to assume AWS IAM roles by presenting X.509 certificates. A trust anchor defines which certificate authority (CA) AWS trusts to validate 
these external identities. Normally, organizations use AWS Certificate Manager Private CA (ACM PCA) to control issuance 
and revocation. 

This detection rule identifies when a trust anchor is created using an **external CA** (`sourceType= "CERTIFICATE_BUNDLE" or "SELF_SIGNED_REPOSITORY"`) rather than an ACM-managed CA (`sourceType="AWS_ACM_PCA"`). This can indicate an adversary establishing persistent external access, enabling them to authenticate using certificates signed by their own CA.

#### Possible investigation steps

- **Identify the actor**
  - Review `aws.cloudtrail.user_identity.arn` and `aws.cloudtrail.user_identity.access_key_id`.
  - Determine whether this user or role is normally responsible for IAM configuration or Roles Anywhere setup.

- **Review the trust anchor details**
  - In `aws.cloudtrail.request_parameters`, confirm the `sourceType` and inspect the certificate chain.
  - Look for non-AWS issuer names, custom organization fields, or self-signed CA certificates.

- **Assess the scope and risk**
  - Identify which IAM roles are linked to this trust anchor via `Profile` associations.
  - Determine whether any of those roles provide privileged or cross-account access.
  - Check for subsequent API calls like `CreateProfile`, `CreateRole`, or `AssumeRoleWithCertificate` to gauge whether 
    the external CA has been used.

- **Correlate related activity**
  - Search for preceding reconnaissance or setup activity:
    - `ListTrustAnchors`, `ListProfiles`, `GetRole`
    - Attempts to create additional credential paths (`CreateAccessKey`, `CreateOpenIDConnectProvider`)
  - Investigate other actions by the same user identity, particularly IAM role or trust policy modifications.

- **Validate legitimacy**
  - Confirm with identity management or security engineering teams whether the external CA is an approved authority.
  - Review internal PKI or certificate inventories to ensure this CA is registered in the organization’s trust chain.

### False positive analysis

- **Legitimate external CA use**
  - Some organizations integrate trusted third-party PKI providers (e.g., Venafi, DigiCert, Entrust) for workload identity management. Validate whether the CA is part of your documented PKI ecosystem.
- **Testing and lab accounts**
  - Development or testing environments may temporarily use self-signed certificates to validate Roles Anywhere integrations.
  - Confirm that such activity occurs in isolated accounts and not in production.
- **Expected administrative setup**
  - Initial configuration by security engineers or platform teams may trigger this rule. Verify via change tickets or 
    deployment logs before treating as suspicious.

### Response and remediation

- **Containment**
  - If the CA is unauthorized, immediately delete the trust anchor using 
    `aws rolesanywhere delete-trust-anchor --trust-anchor-id <id>`.
  - Review for any certificates already used to assume roles and revoke those certificates from the external CA.

- **Investigation**
  - Identify all IAM Roles Anywhere profiles linked to the trust anchor (`ListProfiles`).
  - Check CloudTrail for any successful `AssumeRoleWithCertificate` calls associated with the external CA.
  - Assess whether lateral movement or data exfiltration occurred after the trust anchor creation.

- **Recovery and hardening**
  - Replace unauthorized CAs with ACM PCA-managed ones.
  - Restrict `rolesanywhere:CreateTrustAnchor` permissions to security administrators only.
  - Monitor for new trust anchor creations and external certificate sources via AWS Config rules or Security Hub findings.
  - Implement GuardDuty or Security Hub integrations to detect anomalous IAM and Roles Anywhere behavior.

### Additional information

- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **Security Best Practices:** [AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/).

