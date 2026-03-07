---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS EC2 Route Table Modified or Deleted" prebuilt detection rule.
---

# AWS EC2 Route Table Modified or Deleted

## Triage and Analysis

### Investigating AWS EC2 Route Table Modified or Deleted

This rule detects modifications or deletions of AWS route tables using actions such as `ReplaceRoute`, `ReplaceRouteTableAssociation`, `DeleteRouteTable`, `DeleteRoute`, or `DisassociateRouteTable`. These actions may indicate legitimate administrative activity, but they can also be abused by attackers to disrupt network traffic, reroute communications, or maintain persistence in a compromised environment.

#### Possible Investigation Steps

- **Review Request Parameters:**
   - Check the `aws.cloudtrail.request_parameters` field. The sub-fields may vary depending on the `event.action` (e.g., `routeTableId` for `DeleteRouteTable`, `destinationCidrBlock` for `ReplaceRoute`).
   - Validate the affected route table, routes, or associations based on the API call:
     - For `ReplaceRoute`: Look for changes in specific routes using `destinationCidrBlock`.
     - For `ReplaceRouteTableAssociation`: Review the new association details (e.g., subnet ID).
     - For `DeleteRouteTable`: Confirm the `routeTableId` of the deleted table.
     - For `DisassociateRouteTable`: Verify the disassociated resources.

- **Review User Context**:
  - **User Identity**: Inspect the `aws.cloudtrail.user_identity.arn` field to determine the user or role initiating the action. Investigate whether this user is authorized to perform these operations.
  - **Access Key ID**: Check the `aws.cloudtrail.user_identity.access_key_id` field to identify if the access key used was expected or potentially compromised.
  - **Access Patterns**: Validate whether the user or role has a history of performing route table modifications and whether this aligns with their expected responsibilities.

- **Analyze Request Details**:
  - **Action Type**: Verify the specific API call in the `event.action` field (e.g., `ReplaceRoute`, `DeleteRouteTable`) to understand the nature of the modification.
  - **Source IP and Geolocation**: Examine the `source.ip` and `source.geo` fields to confirm whether the request originated from a trusted location. Suspicious geolocations or IPs may indicate adversarial activity.
  - **User Agent**: Review the `user_agent.original` field to determine the tool used for the request (e.g., AWS CLI, Terraform). Unusual or custom user agents may indicate malicious intent.

- **Correlate with Other Activity**:
  - **Concurrent API Calls**: Look for related API calls (e.g., `CreateRoute`, `AuthorizeSecurityGroupIngress`, or `ModifyInstanceAttribute`) from the same user or IP to detect broader attack patterns.
  - **IAM Changes**: Investigate whether any IAM policy updates or privilege escalation attempts preceded this activity.
  - **Unusual Volume of Changes**: Check if the user has performed multiple route table modifications or deletions in a short timeframe.

- **Validate the Intent**:
  - **Planned Changes**: Confirm with administrators whether the route table changes were part of a planned update or maintenance activity.
  - **Permissions and Justification**: Ensure that the user or role has the least privilege necessary for these actions and that there is a valid reason for modifying the route table.

### False Positive Analysis

- **Routine Administration**: Route table modifications are often part of routine administrative tasks, such as creating new routes, updating associations, or removing unused resources.
- **Automation Tools**: Automated workflows, such as those executed by Terraform or CloudFormation, may trigger these events. Verify whether the `user_agent.original` field or source IP matches known automation tools.
- **Maintenance or Scaling**: Confirm whether these actions align with maintenance activities or scaling events (e.g., adding or removing subnets).

### Response and Remediation

- **Revoke Unauthorized Permissions**: If unauthorized, remove permissions for related actions from the user or role. You can use the managed [AWSDenyAll](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSDenyAll.html) policy.
- **Restore the Route Table**:
  - If critical networking was impacted, restore the route table or reapply previous configurations from backups or Terraform state files.
  - Verify connectivity to affected subnets or instances to ensure no disruptions to services.
- **Audit IAM Policies**:
  - Limit route table modification permissions to specific trusted users, roles, or automation accounts.
  - Implement conditions in IAM policies, such as source IP restrictions, to reduce the risk of unauthorized access.
- **Monitor and Alert**:
  - Set up additional alerts for unexpected route table modifications or deletions.
  - Use VPC flow logs and CloudTrail to monitor for related suspicious activity.
- **Secure Automation**: Ensure automation tools, such as Terraform or CloudFormation, are configured securely and that their credentials are stored in secure locations like AWS Secrets Manager.

