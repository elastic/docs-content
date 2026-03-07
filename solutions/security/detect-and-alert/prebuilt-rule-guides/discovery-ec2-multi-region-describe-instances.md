---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS EC2 Multi-Region DescribeInstances API Calls" prebuilt detection rule.'
---

# AWS EC2 Multi-Region DescribeInstances API Calls

## Triage and analysis

### Investigating AWS EC2 Multi-Region DescribeInstances API Calls

This rule flags when the `DescribeInstances` API is executed across multiple AWS regions within a short timeframe. While benign in some cases (e.g., asset inventory, legitimate multi-region management), this pattern can indicate a reconnaissance phase in which an adversary enumerates EC2 instances in all regions to identify potential targets across the environment.

Because the signal can generate significant noise in dynamic or large AWS environments, this rule should be treated as a Building Block Rule (BBR), not a stand-alone alert requiring immediate incident response. Instead, it is best used for hunting, enrichment, correlation, and escalation when combined with other signals.

### How to use this rule (hunting & correlation guide)

This rule is most effective when paired with other detection rules or data sources. Use it to answer questions such as:

- Did a newly created or unknown principal call `DescribeInstances` across many regions? Pair this with a new terms or first-time principal rule (e.g., `GetCallerIdentity`, `AssumeRole`, or `aws.cloudtrail.user_identity.session_context.session_issuer.arn`).  
- Was the same principal also observed making other discovery or enumeration calls (e.g., `DescribeSnapshots`, `DescribeVolumes`, `DescribeImages`, `DescribeSecurityGroups`) in a short timeframe?  
- Did the multi-region calls precede or coincide with higher-risk actions such as:  
  - Snapshot creation or shared snapshot modifications (`CreateSnapshot`, `ModifySnapshotAttribute`)  
  - AMI export/copy operations (`ExportImage`, `CopyImage`)  
  - Access key creation, role assumption, or IAM permission changes  
  - Unexpected S3 bucket or data transfer activity (e.g., large data egress, new S3 bucket writes)  
- Did the activity span regions normally unused or outside the organization's typical operational footprint?

#### Possible investigation steps:

- **Review the principal and session trace**:  
  - Identify `aws.cloudtrail.user_identity.arn`, `aws.cloudtrail.user_identity.access_key_id`, and determine whether the principal is known, recently onboarded, or unusual (e.g., a service role used in rare cases).  
  - Examine `user_agent.original` and `source.ip` for anomalies (e.g., new CLI/SDK versions, IAM roles from unexpected hosts, geolocation outside expected range).

- **Evaluate region distribution and timing**:  
  - Inspect the regions contacted by `DescribeInstances` within the alert window. Are some regions rarely used in your org?  
  - Look at the timeline: did the calls occur in rapid succession or spread out? A burst suggests automated reconnaissance rather than manual usage.

- **Correlate with other detection signals & data access patterns**:  
  - Query for other CloudTrail events by the same principal in the ±30 minutes window: enumeration APIs (`Describe*`), snapshot/AMI events, `CopySnapshot`, `ExportImage`, `StartInstances`, etc.  
  - Cross-validate with SIEM or data egress logs: did large volumes of data leave the environment after the enumeration?  
  - Review IAM activity for privilege elevation, new access keys, or role chaining that could support the enumeration action.

- **Assess intent and operational context**:  
  - Determine whether the enumeration aligns with known asset-inventory or management tasks (Recurring scans, DevOps automation, IT health checks).  
  - If this principal is known for asset management, verify the timing, region list, and audit logs for existing tickets/change-records.  
  - If the activity is unexpected, low legitimacy, or tied to other suspicious events, escalate.

### False positive analysis:

Because many organizations have legitimate multi-region cloud operations, this rule may generate false positives. Common benign scenarios include:

- DevOps or cloud-ops automation that inventories EC2 instances across all regions (for cost, compliance, or multi-region deployment verification).  
- Large-scale migrations or disaster-recovery tests that touch many regions in a short time.  
- Security or audit team enumeration of the environment (e.g., internal red-team, internal asset scanning).  
- Cross-account management tools in AWS Organizations that routinely query multiple regions.

To manage these, consider:  
- Whitelisting known automation roles/principals (with caution).  
- Tagging and excluding known “inventory scan” sessions (based on user agent, IP range, timing).  
- Using this rule only as a correlation trigger and not as a direct alert.

### Response and escalation:

Because this rule is a BBR, its detection alone does not usually warrant full incident response. Instead:

- **Document the finding** in your hunt log, noting principal, regions, timestamp, and correlation flags (other events).  
- If correlation reveals additional suspicious activity (e.g., snapshot share, data export, IAM privilege change) escalate to full incident response.  
- If the enumeration is determined benign (e.g., approved internal scan), add context (ticket number, owner, justification) and suppress/annotate this principal in future hunts for a defined interval.  
- Update your detection playbooks to reflect this rule’s role as a recon-indicator, and train analysts to use it as a pivot point.

### Additional information

For further information on AWS `DescribeInstances` permissions and best practices, refer to the [AWS DescribeInstances API documentation](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeInstances.html).
