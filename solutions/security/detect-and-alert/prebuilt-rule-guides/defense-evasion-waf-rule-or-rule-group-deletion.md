---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS WAF Rule or Rule Group Deletion" prebuilt detection rule.
---

# AWS WAF Rule or Rule Group Deletion

## Triage and analysis

### Investigating AWS WAF Rule or Rule Group Deletion

AWS WAF rules and rule groups define the security boundary for web applications by blocking malicious inputs,
enforcing rate-based protections, and applying managed or custom signatures. Deleting a rule or rule group immediately
weakens this boundary. Adversaries who obtain sufficient permissions may delete these protections to remove detection of malicious payloads prior to exploitation or erase defenses protecting high-value APIs. 

This rule detects successful `DeleteRule` or `DeleteRuleGroup` API calls in CloudTrail.

### Possible investigation steps

**Identify the actor**
- Review `aws.cloudtrail.user_identity.arn` and `user_identity.access_key_id` to determine which principal performed the deletion.
- Determine whether the principal normally manages WAF resources or appears anomalous (new key, unused IAM role, unexpected federation source).

**Inspect the request context**
- Review `source.address`, `source.geo` fields, and `user_agent.original` to determine if the request originated from a known enterprise IP range, a CI/CD runner or automation tool, an unfamiliar network, region, or browser/CLI pattern.

**Understand what was deleted**
- Review `aws.cloudtrail.request_parameters` for `RuleId` or `RuleGroupId`, any referenced WebACLs using the rule, metadata indicating whether the deleted rule was part of production traffic control. 

**Correlate surrounding activity**
- Look for adjacent CloudTrail events:
  - modifications to WebACLs (`UpdateWebACL`)
  - creation of permissive rules (`CreateRule`, `PutRule`) after deletion  
  - IAM privilege escalation events  
  - unusual S3, API Gateway, or ALB access patterns immediately after the rule deletion  
- Determine if deletion preceded or followed exploit attempts visible in application logs.

**Establish operational context**
- Confirm whether the deletion aligns with a deployment pipeline, scheduled maintenance, rule tuning by security teams. If not, treat the event as potentially malicious.

**Engage relevant owners**
- Contact application security or platform engineering teams to verify whether the rule or rule group deletion was authorized.

### False positive analysis

- **Authorized deployment workflows**  
  Some organizations rebuild WAF rules programmatically during deployments. Validate expected CI/CD service roles and event timing.

- **Automated rule regeneration**  
  Certain WAF-as-code approaches temporarily delete and recreate rules. Confirm if the event corresponds to an expected automation cycle.

- **Security team testing**  
  Teams may temporarily disable or remove rules during testing of new signatures or rate controls. Verify scheduling and ownership.

- **Non-production environments**  
  Development or staging accounts may routinely alter WAF rules. Tune the rule by account, environment tags, or namespaces to reduce noise.

### Response and remediation

- **Contain the incident**
  - Immediately verify whether the deletion was intentional.
  - If unauthorized, revoke active access keys or disable implicated IAM roles/sessions.

- **Reinstate protections**
  - Restore the deleted rule or rule group from infrastructure-as-code definitions, backups, or documented configuration.
  - Inspect associated WebACLs to ensure no additional rules were removed or modified.

- **Investigate follow-on activity**
  - Review application logs for suspicious requests following WAF rule removal.
  - Investigate potential exploitation attempts (SQLi, XSS, API abuse, authentication bypass).

- **Harden IAM and WAF governance**
  - Limit WAF deletion operations to tightly controlled IAM roles.
  - Enforce MFA and short session durations for privileged accounts.
  - Consider guardrails using AWS Config or SCPs to prevent deletion of production WAF rules.

- **Post-incident improvements**
  - Update runbooks to track planned WAF changes.
  - Strengthen CI/CD guardrails to prevent unauthorized rule manipulation.
  - Enhance alerting for other high-risk WAF configuration changes.

### Additional information

- **DeleteRule API (WAF Classic & Regional)**  
  https://docs.aws.amazon.com/waf/latest/APIReference/API_waf_DeleteRule.html  
- **DeleteRuleGroup API (WAFv2)**  
  https://docs.aws.amazon.com/waf/latest/APIReference/API_waf_DeleteRuleGroup.html   
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **[AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/)**

