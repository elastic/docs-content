---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Insecure AWS EC2 VPC Security Group Ingress Rule Added" prebuilt detection rule.
---

# Insecure AWS EC2 VPC Security Group Ingress Rule Added

## Triage and analysis

### Investigating Insecure AWS EC2 VPC Security Group Ingress Rule Added

This rule detects the addition of ingress rules to a VPC security group that allow traffic from any IP address (`0.0.0.0/0` or `::/0`) to sensitive ports commonly used for remote access, such as SSH (port 22) and RDP (port 3389). This configuration change can significantly increase the exposure of EC2 instances to potential threats, making it crucial to understand the context and legitimacy of such changes.

#### Possible Investigation Steps:

- **Identify the Actor**: Review the `aws.cloudtrail.user_identity.arn` and `aws.cloudtrail.user_identity.access_key_id` fields to identify who made the change. Investigate whether this actor has the necessary permissions and typically performs these actions.
- **Review the Request Details**: Examine the `aws.cloudtrail.request_parameters` to understand exactly what changes were made to the security group. Check for any unusual parameters that could suggest a misconfiguration or malicious intent.
- **Analyze the Source of the Request**: Look at the `source.ip` and `source.geo` fields to determine the geographical origin of the request. An external or unusual location could indicate compromised credentials.
- **Contextualize with Timestamp**: Use the `@timestamp` field to check when the change occurred. Modifications outside of typical business hours might warrant additional scrutiny.
- **Correlate with Other Activities**: Search for related CloudTrail events before and after this change to see if the same actor engaged in other potentially suspicious activities.

### False Positive Analysis:

- **Legitimate Administrative Actions**: Verify if the ingress rule change aligns with scheduled updates, maintenance activities, or legitimate administrative tasks documented in change management tickets or systems.
- **Consistency Check**: Compare the action against historical data of similar actions performed by the user or within the organization. Consistency with past legitimate actions might indicate a false alarm.
- **Verify through Outcomes**: Check the `aws.cloudtrail.response_elements` and the `event.outcome` to confirm if the change was successful and intended as per policy.

### Response and Remediation:

- **Immediate Review and Reversal if Necessary**: If the change was unauthorized, revert the security group rules to their previous state to close any unintended access.
- **Enhance Monitoring and Alerts**: Adjust monitoring systems to alert on similar security group changes, especially those that open access to well-known ports from any IP address.
- **Educate and Train**: Provide additional training to users with administrative rights on the importance of security best practices concerning security group management.
- **Audit Security Groups and Policies**: Conduct a comprehensive audit of all security groups and associated policies to ensure they adhere to the principle of least privilege.
- **Incident Response**: If there's an indication of malicious intent or a security breach, initiate the incident response protocol to mitigate any damage and prevent future occurrences.

### Additional Information:

For further guidance on managing security group rules and securing AWS environments, refer to the [Amazon VPC Security Groups documentation](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) and AWS best practices for security.


