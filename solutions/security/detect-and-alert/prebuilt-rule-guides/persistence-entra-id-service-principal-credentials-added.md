---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Entra ID Service Principal Credentials Created by Unusual User" prebuilt detection rule.'
---

# Entra ID Service Principal Credentials Created by Unusual User

## Triage and analysis

### Investigating Entra ID Service Principal Credentials Created by Unusual User

This rule identifies the addition of new credentials (client secrets or certificates) to a Microsoft Entra ID (formerly Azure AD) service principal by a user who has not previously performed this operation in the last 10 days. Adversaries who obtain temporary or persistent access to a user account may add rogue credentials to service principals in order to maintain unauthorized access to cloud resources.

This is a [New Terms](https://www.elastic.co/guide/en/security/current/rules-ui-create.html#create-new-terms-rule) rule that detects rare users performing sensitive identity-related actions in Entra ID.

#### Possible Investigation Steps
- Identify the Actor: Review the `azure.auditlogs.properties.initiated_by.user.user_principal_name` and `azure.auditlogs.properties.initiated_by.user.id` fields to identify the user account performing the action. Determine if this user typically manages service principals.
- Check for Known Admin or Automation Context: Validate if the action was expected (e.g., part of a deployment pipeline or credential rotation process). Investigate whether this is a known administrative account or an automated service principal maintainer.
- Inspect Credential Type: Determine if a certificate or client secret was added, and assess its expiration time, usage scope, and whether it aligns with internal practices.
- Correlate with Other Events: Look for surrounding events such as creation of new service principals, assignment of roles or permissions, or suspicious application sign-ins that could indicate persistence or privilege escalation.
- Analyze Source of Activity: Review `source.ip` and `user_agent.original` fields to assess whether the request came from a trusted network or device. Unexpected geolocations, hosting providers, or Linux CLI-based user agents may indicate unauthorized activity.

### False Positive Analysis
- Routine Administrative Tasks: This alert may trigger when legitimate administrators or DevOps engineers rotate credentials for service principals as part of normal operations.
- First-Time Actions by Known Accounts: If a new user joins the team or an existing user is performing this task for the first time in the observed period, it may be expected behavior. Verify with the relevant team.

### Response and Remediation
- Revoke Unauthorized Credentials: If suspicious, disable or delete the newly added service principal credential immediately.
- Investigate User Account: Review the login history, IP address usage, and other activity from the initiating user to determine whether the account is compromised.
- Audit Affected Service Principal: Evaluate the permissions granted to the service principal to understand the potential impact of misuse.
- Review RBAC and Least Privilege: Ensure that only authorized identities have permission to add credentials to service principals. Tighten IAM role definitions if necessary.
- Enable Just-in-Time or Approval-Based Access: Consider implementing access control policies that require approvals for modifying service principals or adding credentials.
