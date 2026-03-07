---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Excessive AWS S3 Object Encryption with SSE-C" prebuilt detection rule.'
---

# Excessive AWS S3 Object Encryption with SSE-C

## Triage and analysis

### Investigating Excessive AWS S3 Object Encryption with SSE-C
This rule identifies a high volume of objects being encrypted using Server-Side Encryption with Customer-Provided Keys (SSE-C) in AWS S3. This could indicate malicious activity, such as ransomware encrypting objects, rendering them inaccessible without the corresponding encryption keys.

### Possible investigation steps

**Identify the user and source**:
   - Review the `aws.cloudtrail.user_identity.arn` to identify the IAM user or role performing the operation.
   - Cross-check the `source.ip` and `user_agent.original` fields for unusual IPs or user agents that could indicate unauthorized access.
   - Review the `aws.cloudtrail.user_identity.access_key_id` to identify the access key used. This could be a compromised key.

**Examine the targeted resources**:
   - Check `aws.cloudtrail.request_parameters` to identify the bucket involved.
   - Analyze the object key from `aws.cloudtrail.request_parameters`.

**Evaluate encryption behavior**:
   - Confirm the encryption details in `aws.cloudtrail.request_parameters` and `aws.cloudtrail.additional_eventdata`.
   - Note if `SSEApplied` is `SSE-C`, which confirms encryption using a customer-provided key.

**Correlate with recent events**:
   - Look for any suspicious activity in proximity to the encryption event, such as new access key creation, policy changes, or unusual access patterns from the same user or IP.
   - Identify `ListBucket` or `GetObject` operations on the same bucket to determine all affected objects.
   - For `PutObject` events, identify any other unusual objecs uploaded such as a ransom note.

**Validate access permissions**:
   - Check the IAM policies and roles associated with the user to verify if they had legitimate access to encrypt objects.

**Assess impact**:
   - Identify the number of encrypted objects in the bucket by examining other similar events.
   - Determine if this encryption aligns with standard business practices or constitutes a deviation.

### False positive analysis

- Confirm if SSE-C encryption is part of regular operations for compliance or data protection.
- Cross-reference known processes or users authorized for SSE-C encryption in the affected bucket.

### Response and remediation

**Immediate actions**:
   - Disable access keys or permissions for the user if unauthorized behavior is confirmed.
   - Rotate the bucket's encryption configuration to mitigate further misuse.

**Data recovery**:
   - Attempt to identify and contact the party holding the SSE-C encryption keys if recovery is necessary.

**Enhance monitoring**:
   - Enable alerts for future SSE-C encryption attempts in critical buckets.
   - Review and tighten IAM policies for roles and users accessing S3.

**Post-Incident review**:
   - Audit logs for additional activities by the same user or IP.
   - Document findings and apply lessons learned to improve preventive measures.
