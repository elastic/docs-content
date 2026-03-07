---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS Route 53 Private Hosted Zone Associated With a VPC" prebuilt detection rule.'
---

# AWS Route 53 Private Hosted Zone Associated With a VPC

## Triage and analysis

### Investigating AWS Route 53 Private Hosted Zone Associated With a VPC

Route 53 private hosted zones provide internal DNS capabilities accessible only to the VPCs explicitly associated with
them. Associating a new VPC expands DNS visibility and access. If an adversary gains sufficient IAM permissions, they may
attach unauthorized VPCs to privileged hosted zones to perform internal reconnaissance, intercept service discovery,
redirect traffic, or gain persistence by manipulating internal name resolution.

This rule detects successful `AssociateVPCWithHostedZone` events where a hosted zone's visibility scope is modified.

### Possible investigation steps

- **Identify the Actor**
  - Review `aws.cloudtrail.user_identity.arn` and `access_key_id` to determine who initiated the association. Validate whether this identity is expected to manage Route 53 or VPC networking.

- **Review Request Details**
  - Examine `aws.cloudtrail.request_parameters` to confirm which hosted zone and VPC were associated. Determine if the hosted zone contains sensitive internal service records, privileged DNS, or identity service endpoints.

- **Validate the VPC**
  - Identify whether the associated VPC belongs to an authorized environment (e.g., known production, staging, or internal networks). Check for unusual VPC creation events, cross-account VPC behavior, or recently observed anomalous resource provisioning.

- **Assess Source Context**
  - Inspect `source.ip` and `user_agent.original` for geographic anomalies, automation patterns, or suspicious tooling.
  - Look for correlations with unusual IAM activity, privilege escalations, or policy modifications.

- **Correlate With Broader Activity**
  - Search for additional changes involving the same identity, including:
    - Route 53 hosted zone modifications
    - VPC peering creation
    - Network ACL or security group changes
    - IAM privilege modifications
  - Identify whether this association is part of a larger sequence suggesting lateral movement or internal reconnaissance.

- **Engage Relevant Teams**
  - If initiated by a user, confirm intent with networking or cloud infrastructure teams. Validate whether the association aligns with deployment, migration, or environment expansion activities.

### False positive analysis

- **Routine Infrastructure Updates**
  - Associations may occur during normal environment expansions (new VPC for microservices, deployments, region expansion).

- **Automated Tooling**
  - Infrastructure-as-code pipelines (Terraform, CloudFormation, CDK) may regularly modify hosted zone associations.
  - If confirmed legitimate, consider excluding specific automation IAM roles.

- **Migration or Restructuring Events**
  - Large-scale cloud migrations or VPC re-architecture work may trigger frequent legitimate associations.

### Response and remediation

- **Revoke Unauthorized Access**
  - If the association is unauthorized, review and restrict IAM permissions for the actor.
  - Remove the VPC association if it is not intended.

- **Investigate Potential Impact**
  - Review internal DNS query logs and VPC flow logs for any misuse, suspicious lookups, or unauthorized cross-VPC traffic.

- **Strengthen IAM Controls**
  - Limit `route53:AssociateVPCWithHostedZone` to specific administrative roles.
  - Require MFA for accounts with Route 53 and VPC modification permissions.

- **Monitor for Related Activity**
  - Add monitoring for other hosted zone modifications, new VPC creation, and cross-account network configurations.

- **Communicate and Document**
  - Notify cloud networking and security operations of unauthorized changes.
  - Document findings and update policy controls or automation baselines.

### Additional information
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **[AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/)**
