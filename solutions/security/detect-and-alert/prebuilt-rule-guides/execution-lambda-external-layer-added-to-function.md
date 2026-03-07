---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS Lambda Layer Added to Existing Function" prebuilt detection rule.'
---

# AWS Lambda Layer Added to Existing Function

## Triage and analysis

### Investigating AWS Lambda Layer Added to Existing Function

Lambda layers introduce external code artifacts into a function’s runtime. Adding a layer to an existing Lambda function
modifies its execution environment and may allow an adversary to run arbitrary code, intercept data, or maintain
persistence without altering the function source itself. This detection highlights successful configuration updates using
`PublishLayerVersion*` or `UpdateFunctionConfiguration*`.

### Possible investigation steps

**Identify the actor**
- Review `aws.cloudtrail.user_identity.arn` and the `access_key_id`. Determine whether the actor normally administers Lambda or has recently exhibited unusual behavior.

**Review what was modified**
- Inspect `aws.cloudtrail.request_parameters` to identify which layer ARN was added, the function name and region, whether multiple layers were applied at once or in rapid succession.
- Compare the added layer version against known and approved layer catalogs.

**Validate the operational context**
- Check the time of the update (`@timestamp`) to see if it aligns with known release pipelines or deployment windows and Normal working hours for the responsible team.
- Determine whether a CI/CD pipeline or IaC tool was expected to update this function.

**Assess where the change came from**
- Review `source.ip` and `user_agent.original` for signs of console access from unusual locations, access via previously unused automation tools, suspicious programmatic access consistent with compromised keys.

**Correlate with additional activity**
- Look for preceding or subsequent events such as:
  - Creation of new Lambda layers (`PublishLayerVersion`).
  - IAM role modifications affecting the Lambda function.
  - Increased invocation volume or unusual invocation patterns after the layer addition.
- Search for other functions modified by the same actor or from the same IP.

### False positive analysis

- Confirm whether the change aligns with a planned deployment, application update, or dependency upgrade.
- Determine whether the user or automation role commonly modifies Lambda function configurations.
- Validate the legitimacy of the added layer by checking internal documentation or release notes.

### Response and remediation

- Remove or roll back the added layer if the modification appears unauthorized or suspicious.
- Review the layer contents, especially for newly published layers, to verify integrity and legitimacy.
- Investigate the IAM role or user responsible for the change and rotate compromised credentials if necessary.
- Tighten permissions by ensuring only approved roles can modify Lambda configurations or publish new layers.
- Implement monitoring for subsequent Lambda configuration changes, invocation anomalies caused by the injected layer, additional persistence techniques targeting serverless infrastructure.

### Additional information
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **[AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/)**
