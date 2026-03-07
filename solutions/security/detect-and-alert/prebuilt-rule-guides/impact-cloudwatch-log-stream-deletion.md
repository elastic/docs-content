---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS CloudWatch Log Stream Deletion" prebuilt detection rule.
---

# AWS CloudWatch Log Stream Deletion

## Triage and analysis

### Investigating AWS CloudWatch Log Stream Deletion

CloudWatch log streams contain sequential log events from a single application, service, or AWS resource.  
Deleting a log stream permanently removes its archived log events, which may disable monitoring workflows, eliminate 
critical telemetry, or disrupt forensic visibility.

Adversaries may delete log streams to cover their tracks after unauthorized actions, break ingestion pipelines feeding SIEM, alerting, or anomaly detection or to remove evidence before escalating privileges or moving laterally. This rule detects successful invocations of the `DeleteLogStream` API from CloudTrail.

#### Possible investigation steps

- **Identify the actor**
  - Review `aws.cloudtrail.user_identity.arn` and `aws.cloudtrail.user_identity.access_key_id`.  
  - Confirm whether the user or role normally manages CloudWatch Logs resources.

- **Review request details**
  - Inspect `aws.cloudtrail.request_parameters` to determine which log stream and parent log group were deleted.  
  - Assess the importance of the deleted stream:
    - Was it used for VPC Flow Logs, CloudTrail, Lambda functions, ECS tasks, or application logs?  
    - Did it contain logs used for security detection or compliance auditing?

- **Examine request origin and context**
  - Review `source.ip` and `user_agent.original` for anomalies (e.g., unfamiliar CLI tools, suspicious automation, 
    unknown IP ranges, or external geolocations).
  - Validate whether the request originated from a legitimate automation host or jump box.  
  - Check activity around the same timestamp for related operations such as:
    - `DeleteLogGroup`
    - `StopLogging`, `UpdateTrail`, or `DeleteTrail`
    - GuardDuty detector or CloudWatch alarm deletions
    - IAM policy or role modifications

- **Determine operational justification**
  - Consult change management systems or deployment pipelines to confirm whether the deletion was planned.  
  - Contact application owners or platform teams to determine whether the log stream was part of normal rotation or cleanup.

- **Investigate broader compromise indicators**
  - Look for suspicious activity by the same identity in the past 24–48 hours, such as:
    - Failed authentication attempts  
    - IAM privilege escalations  
    - Unusual STS AssumeRole usage  
    - Access from new geolocations  

### False positive analysis

- **Log rotation and automation**
  - Some systems delete log streams automatically when rolling new deployments or recycling compute resources.
  - CI/CD pipelines managing immutable infrastructure may delete and recreate streams during each deploy.

- **Test and development accounts**
  - Dev/test environments may frequently create and delete log streams as part of iterative work.

- **Bulk cleanup operations**
  - Platform engineering teams may delete obsolete log streams during cost-optimization or log-retention management.

If the rule triggers frequently from known infrastructure accounts or automation hosts, consider adding narrow exceptions using a combination of IAM role, IP range, or user agent.

### Response and remediation

- **Containment**
  - If the deletion is unauthorized, review other CloudWatch resources for additional tampering (alarms, log groups, metric filters).
  - Temporarily restrict permissions for the implicated IAM user or role.

- **Investigation**
  - Reconstruct any missing telemetry from alternative sources (e.g., S3 buckets, application logs, third-party logging systems).
  - Review CloudTrail and Config timelines for preceding suspicious events.
  - Validate whether the deleted log stream contained evidence of prior compromise.

- **Recovery and hardening**
  - Implement IAM least-privilege for `logs:DeleteLogStream`.
  - Enable AWS Config rules to monitor CloudWatch Logs configuration changes.  
  - Ensure that business-critical log groups enforce minimum retention periods and prevent accidental deletion.
  - Integrate log stream lifecycle management into CI/CD to avoid manual deletions.
  - Establish guardrails using Service Control Policies (SCPs) to block log deletions outside designated automation roles.

### Additional information

- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **Security Best Practices:** [AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/).

