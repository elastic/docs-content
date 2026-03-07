---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS Route 53 Domain Transferred to Another Account" prebuilt detection rule.
---

# AWS Route 53 Domain Transferred to Another Account

## Triage and analysis

### Investigating AWS Route 53 Domain Transferred to Another Account

Transferring a Route 53 domain to another AWS account is a high-impact administrative action. A successful transfer enables the
recipient account to fully manage the domain and all associated DNS resources. Unauthorized transfers can result in loss of
visibility and control, traffic redirection, service outages, or domain hijacking for phishing, credential harvesting, or command-and-control.

This rule detects successful calls to `TransferDomainToAnotherAwsAccount`. These events are rare and should be considered
high-risk unless explicitly documented and approved.

### Possible investigation steps

- **Identify the actor and authentication context**
  - Review `aws.cloudtrail.user_identity.arn` and `aws.cloudtrail.user_identity.access_key_id` to determine who initiated the transfer. Determine whether the actor typically performs Route 53 administrative actions or if this represents anomalous behavior.

- **Review request details and target account**
  - Inspect `aws.cloudtrail.request_parameters` for: `DomainName`, `AccountId` receiving the transfer, Request tokens or validation parameters. Validate whether the destination AWS account is recognized, trusted, or documented in ownership transfer procedures.

- **Assess environment and timing**
  - Compare `@timestamp` against maintenance windows, deployment pipelines, or approved domain operations. Review the region and endpoint used; domain transfers occurring from unexpected regions may indicate unauthorized access.

- **Analyze source and execution context**
  - Review `source.ip`, `source.geo.country_iso_code`, and `user_agent.original` to determine:
    - If the request originated from known networks, Whether it matches typical administrator access patterns or if suspicious automation tools, outdated SDK versions, or unknown agents were used.

- **Correlate with broader activity**
  - Pivot on the same IAM principal or access key ID to identify:
    - Recent IAM policy changes or privilege escalation
    - `DisableDomainTransferLock`, which normally precedes domain transfers
    - AWS console sign-ins from new geolocations or ASNs
    - API calls involving certificate requests, hosted zone changes, or DNS record edits
  - Look for evidence of lateral movement or credential theft preceding the transfer.

- **Validate with business owners**
  - Confirm with domain owners, development teams, or asset managers whether The transfer was intentional.

### False positive analysis

- **Expected domain migrations**
  - Organizations with multi-account strategies may transfer domains between operational, security, or sandbox accounts.
- **Business events**
  - Mergers, acquisitions, or contractual transitions between managed service providers often involve bulk domain transfers.
- **Automated administrative tooling**
  - Domain lifecycle automation or infrastructure-as-code pipelines may trigger transfers if misconfigured.
  
### Response and remediation

- **Contain and revoke access**
  - If unauthorized, immediately invalidate the IAM session or access keys used in the transfer.
  - Rotate credentials for the implicated IAM user or role and require MFA for privileged operations.

- **Reverse or halt the transfer**
  - Contact AWS Support as soon as possible to request assistance reversing or blocking the transfer if it was not approved.
  - Re-enable transfer lock (`DisableDomainTransferLock=false`) to prevent further modifications.

- **Investigate the extent of compromise**
  - Review CloudTrail to identify all actions performed by the actor before and after the transfer.
  - Check for additional changes to hosted zones, DNS records, certificates, or registrar contact details.

- **Restore operational integrity**
  - Validate DNS routing, certificate issuance, and application endpoints for signs of redirection or tampering.
  - Communicate with impacted teams and external stakeholders if customer-facing domains were affected.

- **Hardening and long-term improvements**
  - Restrict domain transfer permissions to a minimal set of roles using IAM Conditions such as `aws:PrincipalArn` and `aws:MultiFactorAuthPresent`
  - Consider SCPs to block domain-transfer APIs in production accounts.
  - Add change-management tracking for domain ownership modifications.

### Additional information
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **[AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/)**

