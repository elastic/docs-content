---
description: Review the privileges that Elastic Security features require, including Elastic Defend, detections, and Attack Discovery.
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Access control

Control what each user can view and do by assigning privileges to their roles. Each feature has its own privileges, so review them when you turn on a new feature, or when your team or its responsibilities change.

In {{stack}}, you create roles and assign {{kib}} feature privileges, index privileges, and cluster privileges to them. In {{serverless-short}}, you assign a predefined Security user role, or create a custom role with the privileges you need.

## How {{elastic-sec}} privileges work

Most {{elastic-sec}} features use {{kib}} feature privileges, which you set to **All**, **Read**, or **None** for each feature. Some features also need index privileges on the indices that store their data, such as the alert indices for your space.

Keep these points in mind when you create roles:

- **{{elastic-defend}} uses sub-feature privileges**: Selecting **All** for the **Security** feature doesn't grant access to {{elastic-defend}} features such as endpoint management, host isolation, or trusted applications. To grant them, turn on **Customize sub-feature privileges** and set each one.
- {applies_to}`stack: ga 9.4+` **Rules and alerts have separate privileges**: New custom roles need explicit **Rules and Exceptions** and **Alerts** privileges. After you upgrade, check that existing custom roles still have the access to alerts that you expect.
- {applies_to}`stack: ga 9.1` **Privileges can apply per space**: You can assign {{elastic-defend}} privileges for each {{kib}} space. To manage artifacts that apply to all policies, users need the **Global Artifact Management** privilege.

## Where to start

| Your goal | Start here |
|---|---|
| Give users access to endpoint management, response actions, and artifacts | [{{elastic-defend}} feature privileges](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md) |
| Give users access to detection rules, alerts, and exceptions | [Detections privileges](/solutions/security/detect-and-alert/detections-privileges.md) |
| Give users access to Attack Discovery and its schedules | [Attack Discovery privileges](/solutions/security/ai/attack-discovery/grant-access.md) |
| {applies_to}`stack: preview 9.1` Understand how spaces scope {{elastic-defend}} policies, artifacts, and response actions | [Spaces and {{elastic-defend}} FAQ](/solutions/security/get-started/spaces-defend-faq.md) |
| Check what you need for cloud security features | [CSPM privilege requirements](/solutions/security/cloud/cspm-privilege-requirements.md) or [CNVM privilege requirements](/solutions/security/cloud/cnvm-privilege-requirements.md) |
| Check what you need for entity analytics | [Entity analytics requirements](/solutions/security/advanced-entity-analytics/entity-analytics-requirements.md) |

## Next steps

After you set up roles, you can:

- [Configure workspace settings](/solutions/security/manage/configure-workspace-settings.md) to organize security content into spaces.
- Learn how to [manage {{kib}} roles](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) in {{stack}}, or [custom roles](/deploy-manage/users-roles/cloud-organization/user-roles.md) in {{serverless-short}}.
