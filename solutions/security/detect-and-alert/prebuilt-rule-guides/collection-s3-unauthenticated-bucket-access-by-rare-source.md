---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS S3 Unauthenticated Bucket Access by Rare Source" prebuilt detection rule.
---

# AWS S3 Unauthenticated Bucket Access by Rare Source

## Triage and analysis

### Investigating AWS S3 Unauthenticated Bucket Access by Rare Source

This rule detects requests to an AWS S3 bucket by an unauthenticated source, which could indicate a misconfigured bucket policy allowing public access. Adversaries can exploit this misconfiguration by using tools or AWS CLI options like `--no-sign-request` to access bucket contents.

The rule triggers when an unauthenticated IP address retrieves an object, and that IP has not been seen in the last 7 days.

### Possible Investigation Steps

**Identify the Source of the Request**:
    - Review the `source.address` field to determine the IP address of the request source.
    - Check `source.geo` fields for geographic details of the originating IP address.
    - Analyze the `user_agent.original` field to identify the client or tool used (e.g., `Python Requests`, `aws-cli`, browser).

**Review the Accessed Bucket and Object**:
    - Analyze the `aws.cloudtrail.resources.arn` field to identify the S3 bucket and object being accessed.
    - Inspect `aws.cloudtrail.request_parameters` for bucket name and object key to determine which file was retrieved.
    - Review the `even.action` field to identify which API call was made (e.g., `GetObject`, `ListObjects`, `PutObject`, `ListBucket`).

**Validate the Source IP and Context**:
    - Determine if the IP address (`source.address`) has any prior activity in your environment.
    - Correlate the IP with threat intelligence or blocklist databases to check for malicious indicators.
    - Review CloudTrail logs for other activities originating from the same IP.

**Analyze the S3 Bucket Configuration**:
    - Review the S3 bucket's Access Control List (ACL) and bucket policy to check for misconfigurations allowing public or unauthenticated access.
    - Look for overly permissive settings, such as `Principal: *` or `Effect: Allow` rules that expose the bucket.

**Investigate Additional Activity**:
    - Check if there are subsequent actions, such as:
        - **Additional `GetObject` API calls**: Indicating further data exfiltration.
        - **ListObjects requests**: Attempting to enumerate the bucket's contents.
    - Correlate events within the same timeframe to identify related suspicious activity.

**Assess the Data Exposed**:
    - Identify the retrieved object(s) and analyze their content to assess potential data exposure.
    - Determine if the file contains sensitive information, such as credentials, intellectual property, or PII.

### False Positive Analysis

- **Public Buckets by Design**: Some S3 buckets may intentionally allow public access. Verify with the bucket owner if the access was expected.
- **Automated Tools**: Security scanners or legitimate services may generate `GetObject` events to validate bucket configurations.

### Response and Remediation

**Immediate Action**:
    - Restrict or remove public access to the affected S3 bucket.
    - Update the bucket policy to ensure access is restricted to trusted principals.
    - Enable **S3 Block Public Access** settings to prevent unintended public access.

**Monitoring and Detection**:
    - Enable detailed logging and monitoring for all S3 bucket activities.
    - Configure real-time alerts for unauthenticated `GetObject` or `ListObjects` events on sensitive S3 buckets.

**Security Audits**:
    - Regularly audit S3 bucket policies and ACLs to ensure they adhere to AWS security best practices.
    - Use AWS tools like **Trusted Advisor** or **Access Analyzer** to identify and address misconfigurations.

**Investigate for Data Exfiltration**:
    - Analyze historical CloudTrail logs to determine if other sensitive files were accessed or exfiltrated.
    - Assess the scope of the exposure and initiate further response if sensitive data was compromised.

### Additional Resources

- [AWS Documentation: S3 Bucket Policy Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html)
- [AWS S3 Block Public Access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)

