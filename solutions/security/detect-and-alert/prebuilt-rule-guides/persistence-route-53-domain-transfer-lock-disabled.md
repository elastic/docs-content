---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS Route 53 Domain Transfer Lock Disabled" prebuilt detection rule.
---

# AWS Route 53 Domain Transfer Lock Disabled

## Triage and analysis

### Investigating AWS Route 53 Domain Transfer Lock Disabled

This rule detects when the `DisableDomainTransferLock` operation succeeds for a managed Route 53 domain. The transfer lock
prevents unauthorized domain transfers, and disabling it is an uncommon operation outside of planned migrations. Because
domains often underpin production workloads (web, API, authentication, email), unauthorized transfer lock changes may
indicate adversary preparation for domain hijacking or service disruption.

This event should be treated with high urgency whenever it occurs unexpectedly.

### Possible investigation steps

- **Review the actor**
  - Examine `aws.cloudtrail.user_identity.arn` and `user_identity.access_key_id` to confirm who
    initiated the change. Validate whether this identity normally performs domain-management tasks.

- **Analyze the request context**
  - Review `aws.cloudtrail.request_parameters` to identify which domain was affected.
  - Confirm no corresponding `operation=TransferDomainToAnotherAwsAccount` or registrar-level modifications occurred
    shortly before or after the lock was disabled.
  - Note the timestamp and evaluate whether the change occurred during maintenance windows or outside business hours.

- **Evaluate activity surrounding the lock disablement**
  - Look for subsequent events such as modifications to contact details, attempted transfers, DNS record changes, or updates to hosted zones. Correlate with unusual IAM role usage, newly issued access keys, or anomalous login behavior.

- **Validate intent with responsible teams**
  - Confirm whether stakeholders (network operations, domain owners, infrastructure leads) initiated or approved the
    transfer lock disablement. If unmanaged or unexpected, treat this as a potentially malicious action.

### False positive analysis

- **Authorized transfer preparation**
  - The most common legitimate case is preparation for a planned transfer of ownership or registrar migration. Ensure the
    change aligns with a ticketed and approved operation.

- **Internal domain restructuring**
  - Organizational changes (e.g., merging AWS accounts, consolidating DNS assets) may require disabling the lock. Check
    for documented work items or migration plans.

- **Automated tooling**
  - Rare but possible: Some internal automation used for domain lifecycle management may disable the lock as part of an
    update. Validate that any automation using administrative API credentials is documented and approved.

### Response and remediation

- **Re-enable the transfer lock immediately if unauthorized**
  - Restore the lock from Route 53 to prevent any pending or future unauthorized transfer attempts.

- **Contain potential credential compromise**
  - If the action is suspicious, rotate credentials for the user or role involved and enforce MFA.

- **Audit for related domain-level modifications**
  - Review CloudTrail logs for:
    - attempted domain transfers,
    - contact profile changes,
    - hosted zone modifications,
    - DNS record updates,
    - IAM privilege escalations.

- **Engage internal owners**
  - Notify domain owners, infosec leadership, and operations teams; determine business impact and next steps.

- **Strengthen governance**
  - Limit domain-management permissions to the minimum set of authorized administrators.
  - Consider implementing AWS Organizations service control policies (SCPs) to prevent domain-level actions except
    through designated accounts.

### Additional information
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **[AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/)**

