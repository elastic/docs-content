---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS EC2 Full Network Packet Capture Detected" prebuilt detection rule.
---

# AWS EC2 Full Network Packet Capture Detected

## Triage and analysis

### Investigating AWS EC2 Full Network Packet Capture Detected

This alert fires on a successful `CreateTrafficMirrorSession`, which enables full-packet Traffic Mirroring from a
source ENI to a mirror target under a given filter. Because sessions immediately begin sending packets once active,
treat unexpected creations as high priority.

#### Possible investigation steps

**Identify the actor and execution context**
- **Principal**: Review `aws.cloudtrail.user_identity.arn`, `aws.cloudtrail.user_identity.type`, and
  `aws.cloudtrail.user_identity.access_key_id` to determine who created the session (human IAM user vs. assumed role vs. automation).
- **Caller metadata**: Check `user_agent.original`, and `source.ip` for unusual tools, hosts, or locations.
- **Account/Region/Time**: Validate `cloud.account.id`, `cloud.region`, and `@timestamp` against change windows or tickets.

**Extract the session details from the event**
- **Request parameters**: Parse `aws.cloudtrail.request_parameters` for:
  - `NetworkInterfaceId` (mirrored source ENI)  map to the EC2 instance and its business function.
  - `TrafficMirrorTargetId` identify where packets are being sent (ENI vs. NLB).
  - `TrafficMirrorFilterId` check which directions and protocols are allowed (ingress/egress, ports).
  - `SessionNumber`, `Description`, `TagSpecifications` look for operator tags or suspicious notes.
- **Response elements**: Use `aws.cloudtrail.response_elements` to confirm the created `TrafficMirrorSessionId` and
  any resolved resource ARNs/IDs.

**Pivot for related API calls to validate scope and intent**
Look before and after this event (±30–60 minutes) by the same principal / access key / source IP for:
- **Target & Filter lifecycle**: `CreateTrafficMirrorTarget`, `CreateTrafficMirrorFilter`, `CreateTrafficMirrorFilterRule`,
  `ModifyTrafficMirrorSession|Filter|FilterRule`, and `Delete*` calls (rapid create-modify patterns can indicate staging).
- **Session management**: `DeleteTrafficMirrorSession` shortly after creation (test/probe), or repeated creations to different targets.
- **Discovery/positioning**: `DescribeNetworkInterfaces`, `DescribeInstances`, `DescribeVpcs/Subnets/RouteTables` around the same time.
- **Cross-account indicators**: creation of targets that forward to infrastructure not owned by your account (e.g., NLB in shared services).
- **Other suspicious changes**: IAM permission changes, new access keys, or S3/SNS setup that could support exfil/ops.

**Validate the mirror destination and potential data exposure**
- If the target is an ENI: identify the owning instance/application; confirm it is an approved NDR/packet capture host.
- If the target is an NLB target: determine where the NLB sends traffic (could be a collection point in another VPC or account).
- Assess whether mirrored flows include plaintext protocols (internal HTTP, databases, LDAP, etc.) increasing sensitivity.

### False positive analysis

- **Authorized monitoring**: Approved NDR/IDS tooling or troubleshooting playbooks may legitimately create sessions.
- **Ops/diagnostics**: Short-lived sessions during incident handling or performance analysis.
- **Automation**: Infrastructure pipelines that stand up temporary mirroring for validation.

### Response and remediation

**Contain**
- If unauthorized, terminate the session immediately (use the `TrafficMirrorSessionId` from `aws.cloudtrail.response_elements`)
  and block creation permissions for the offending principal.
- Quarantine or restrict egress from the target if you suspect it is forwarding captured traffic outside approved destinations.

**Investigate**
- Enumerate all active sessions in the affected account/region; verify there aren’t additional rogue sessions.
- Review related target and filter resources (and recent `Modify*` calls) to understand captured scope and recipients.
- Trace the source ENI back to the EC2 instance and validate whether sensitive workloads were mirrored.

**Recover & harden**
- Remove or lock down unapproved targets/filters; enforce least privilege on `ec2:CreateTrafficMirrorSession/Target/Filter`.
- Consider SCPs or IAM conditions limiting who/where sessions can be created (e.g., only into designated monitoring VPCs).
- Ensure monitoring targets are controlled, logged, and not internet-reachable.

**Improve**
- Add correlation logic to automatically surface CreateTrafficMirrorSession alongside Create/Modify Target/Filter calls by the same actor.
- Require tags on approved mirroring resources; alert on untagged/unticketed creations.
- Update playbooks to include a standard validation checklist (principal, source ENI, target, filter rules, destination path).


