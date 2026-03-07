---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS EC2 Deprecated AMI Discovery" prebuilt detection rule.'
---

# AWS EC2 Deprecated AMI Discovery

## Triage and analysis

### Investigating AWS EC2 Deprecated AMI Discovery

This rule detects when a user queries AWS for deprecated Amazon Machine Images (AMIs). While deprecated AMIs are not inherently malicious, their use can introduce vulnerabilities or misconfigurations. Adversaries may exploit deprecated AMIs in search of outdated or unpatched systems. Investigating these queries can help identify potential risks or misconfigurations.

### Possible investigation steps

**Identify the user**:
   - Review the `aws.cloudtrail.user_identity.arn` field to determine the AWS user or role making the request.
   - Check `aws.cloudtrail.user_identity.type` and `aws.cloudtrail.user_identity.access_key_id` to verify the type of access (e.g., IAM user, role, or federated identity).

**Analyze the source**:
   - Review the `source.ip` field to determine the IP address of the source making the request.
   - Check `source.geo` for the geographic location of the IP address.
   - Analyze the `user_agent.original` field to determine the client or tool used (e.g., AWS CLI, SDK).

**Validate the query context**:
   - Inspect the `aws.cloudtrail.request_parameters` field 
   - Determine if the request is part of legitimate activity, such as:
     - Security assessments or vulnerability scans.
     - Maintenance or testing of legacy systems.
   - Check if the query aligns with recent changes in the AWS environment, such as new configurations or services.

**Correlate with other events**:
   - Investigate additional AWS API calls from the same user or IP address for signs of reconnaissance or exploitation.
   - Review logs for related actions, such as launching instances from deprecated AMIs (`RunInstances` API call).

**Assess security risks**:
   - Evaluate the use of deprecated AMIs within your environment and their associated vulnerabilities.
   - Ensure that deprecated AMIs are not being used in production environments or systems exposed to external threats.

### False positive analysis

- Users may query for deprecated AMIs for testing or compatibility purposes.
- Security or compliance tools might query deprecated AMIs as part of regular assessments.
- Legacy systems may rely on deprecated AMIs for compatibility, leading to legitimate queries.

### Response and remediation

**Immediate actions**:
   - Verify the intent of the user querying for deprecated AMIs.
   - Restrict IAM permissions to prevent unauthorized access to deprecated AMIs.

**Mitigation steps**:
   - Identify and replace deprecated AMIs in use with supported and updated AMIs.
   - Update AWS IAM policies to minimize permissions for querying or using deprecated AMIs.

**Enhance monitoring**:
   - Enable alerts for future queries involving deprecated AMIs or other unusual API activity.
   - Monitor CloudTrail logs for additional reconnaissance or suspicious behavior.

**Security audits**:
   - Conduct a review of all AMIs in use across your environment to identify outdated or deprecated images.
   - Remove any deprecated AMIs from production environments and restrict their usage to isolated testing.

**Add rule exceptions**:
   - Create exceptions for legitimate use cases or automated tools that query for deprecated AMIs.
   - Document and communicate the exceptions to relevant teams to avoid future alerts.

### Additional resources

- [AWS Documentation: AMI Lifecycle Management](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html)
- [AWS Documentation: Deprecated AMIs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ami-deprecate.html)
