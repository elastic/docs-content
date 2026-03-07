---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS EC2 Security Group Configuration Change" prebuilt detection rule.'
---

# AWS EC2 Security Group Configuration Change

## Triage and analysis

### Investigating AWS EC2 Security Group Configuration Change

This rule identifies any changes to an AWS Security Group, which functions as a virtual firewall controlling inbound and outbound traffic for resources like EC2 instances. Modifications to a security group configuration could expose critical assets to unauthorized access. Threat actors may exploit such changes to establish persistence, exfiltrate data, or pivot within an AWS environment.

#### Possible Investigation Steps

**Identify the Modified Security Group**:
   - **Security Group ID**: Check the `aws.cloudtrail.request_parameters` field to identify the specific security group affected.
   - **Rule Changes**: Review `aws.cloudtrail.response_elements` to determine the new rules or configurations, including any added or removed IP ranges, protocol changes, and port specifications.

**Review User Context**:
   - **User Identity**: Inspect the `aws.cloudtrail.user_identity.arn` field to determine which user or role made the modification. Verify if this is an authorized administrator or a potentially compromised account.
   - **Access Patterns**: Analyze whether this user regularly interacts with security group configurations or if this event is out of the ordinary for their account.

**Analyze the Configuration Change**:
   - **Egress vs. Ingress**: Determine if the change affected inbound (ingress) or outbound (egress) traffic by reviewing fields like `isEgress` in the `securityGroupRuleSet`. Unauthorized changes to outbound traffic can indicate data exfiltration attempts.
   - **IP Ranges and Ports**: Assess any added IP ranges, especially `0.0.0.0/0`, which exposes resources to the internet. Port changes should also be evaluated to ensure only necessary ports are open.

**Check User Agent and Source IP**:
   - **User Agent Analysis**: Examine the `user_agent.original` field to identify the tool or application used, such as `AWS Console` or `Terraform`, which may reveal if the action was automated or manual.
   - **Source IP and Geolocation**: Use `source.address` and `source.geo` fields to verify if the IP address and geolocation match expected locations for your organization. Unexpected IPs or regions may indicate unauthorized access.

**Evaluate for Persistence Indicators**:
   - **Repeated Changes**: Investigate if similar changes were recently made across multiple security groups, which may suggest an attempt to maintain or expand access.
   - **Permissions Review**: Confirm that the user’s IAM policies are configured to limit changes to security groups only as necessary.

**Correlate with Other CloudTrail Events**:
   - **Cross-Reference Other Security Events**: Look for related actions like `AuthorizeSecurityGroupIngress`, `CreateSecurityGroup`, or `RevokeSecurityGroupIngress` that may indicate additional or preparatory steps for unauthorized access.
   - **Monitor for IAM or Network Changes**: Check for IAM modifications, network interface changes, or other configuration updates in the same timeframe to detect broader malicious activities.

### False Positive Analysis

- **Routine Security Changes**: Security group modifications may be part of regular infrastructure maintenance. Verify if this action aligns with known, scheduled administrative activities.
- **Automated Configuration Management**: If you are using automated tools like `Terraform` or `CloudFormation`, confirm if the change matches expected configuration drift corrections or deployments.

### Response and Remediation

- **Revert Unauthorized Changes**: If unauthorized, revert the security group configuration to its previous state to secure the environment.
- **Restrict Security Group Permissions**: Remove permissions to modify security groups from any compromised or unnecessary accounts to limit future access.
- **Quarantine Affected Resources**: If necessary, isolate any affected instances or resources to prevent further unauthorized activity.
- **Audit IAM and Security Group Policies**: Regularly review permissions related to security groups to ensure least privilege access and prevent excessive access.

### Additional Information

For more details on managing AWS Security Groups and best practices, refer to the [AWS EC2 Security Groups Documentation](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/ec2-security-groups.html) and AWS security best practices.
