---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS S3 Static Site JavaScript File Uploaded" prebuilt detection rule.
---

# AWS S3 Static Site JavaScript File Uploaded

## Triage and Analysis

### Investigating AWS S3 Static Site JavaScript File Uploaded

An S3 `PutObject` action that targets a path like `static/js/` and uploads a `.js` file is a potential signal for web content modification. If done by an unexpected IAM user or outside of CI/CD workflows, it may indicate a compromise.

#### Possible Investigation Steps

- **Identify the Source User**: Check `aws.cloudtrail.user_identity.arn`, access key ID, and session type (`IAMUser`, `AssumedRole`, etc).
- **Review File Content**: Use the S3 `GetObject` or CloudTrail `requestParameters` to inspect the uploaded file for signs of obfuscation or injection.
- **Correlate to Other Events**: Review events from the same IAM user before and after the upload (e.g., `ListBuckets`, `GetCallerIdentity`, IAM activity).
- **Look for Multiple Uploads**: Attackers may attempt to upload several files or modify multiple directories.

### False Positive Analysis

- This behavior may be expected during app deployments. Look at:
  - The `user_agent.original` to detect legitimate CI tools (like Terraform or GitHub Actions).
  - Timing patterns—does this match a regular release window?
  - The origin IP and device identity.

### Response and Remediation

- **Revert Malicious Code**: Replace the uploaded JS file with a clean version and invalidate CloudFront cache if applicable.
- **Revoke Access**: If compromise is confirmed, revoke the IAM credentials and disable the user.
- **Audit IAM Policies**: Ensure that only deployment users can modify static site buckets.
- **Enable Bucket Versioning**: This can allow for quick rollback and historical review.

