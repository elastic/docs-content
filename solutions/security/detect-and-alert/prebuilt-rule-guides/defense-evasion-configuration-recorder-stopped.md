---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS Configuration Recorder Stopped" prebuilt detection rule.
---

# AWS Configuration Recorder Stopped

## Triage and analysis

### Investigating AWS Configuration Recorder Stopped

AWS Config provides continuous visibility into resource configuration changes and underpins many security, compliance,
and audit workflows. Stopping the configuration recorder prevents new changes from being captured and can create blind
spots in detection and forensic timelines.

This behavior is uncommon in steady-state production environments and should be carefully reviewed, especially when
performed outside approved maintenance windows or by unexpected principals.

### Possible investigation steps

**Identify the actor**
- Review `aws.cloudtrail.user_identity.arn` and `aws.cloudtrail.user_identity.access_key_id`
  to determine who initiated the `StopConfigurationRecorder` action. Confirm whether this principal typically administers AWS Config or performs security and compliance operations.

**Examine the request context**
- Review `user_agent.original` to determine whether the request originated from the AWS Console, CLI, SDK, or automation tooling.
- Inspect `source.ip` and any available geo context to assess whether the request originated from an expected network or region.

**Determine scope and impact**
- Identify which configuration recorder was stopped and which regions or resources were affected.
- Determine how long the recorder remained disabled and whether any configuration changes occurred during that window.
- Assess whether AWS Config rules, Security Hub controls, or downstream monitoring systems were impacted.

**Correlate with related activity**
- Look for surrounding CloudTrail activity from the same principal, including:
  - Deletion or modification of Config rules, delivery channels, or conformance packs.
  - IAM changes, credential activity, or other security control modifications.
- Check for signs of follow-on activity that may have relied on reduced visibility, such as resource creation, policy changes,
  or network reconfiguration.

**Validate intent**
- Confirm with the platform, security, or compliance teams whether the recorder stoppage was intentional and approved.
- Compare the timing against change management records, infrastructure deployments, or account bootstrapping workflows.

### False positive analysis

- Planned maintenance or controlled configuration changes may require temporarily stopping the recorder.
- Automated account provisioning, teardown, or remediation tooling may stop and restart the recorder as part of normal workflows.

### Response and remediation

- Immediately restart the AWS Config recorder to restore configuration visibility.
- Review CloudTrail logs for activity that occurred while the recorder was stopped and assess potential security or compliance impact.
- If the action was unauthorized, rotate or disable credentials associated with the initiating principal and investigate for compromise.
- Review IAM permissions to ensure only a minimal set of trusted roles can stop or modify AWS Config components.
- Implement guardrails such as AWS Config rules, SCPs, or automated remediation to detect and respond to recorder stoppage.
- Update monitoring, alerting, and incident response runbooks to explicitly cover AWS Config visibility loss scenarios.

### Additional information
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **[AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/)**

