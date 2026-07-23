---
navigation_title: Security
applies_to:
  stack: ga 9.5+
  serverless: ga
description: Named security.* workflow action steps for Elastic Security operations such as attack triage.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Security action steps [workflows-security-steps]

Security action steps (`security.*`) provide named, schema-validated operations for {{elastic-sec}}. Prefer these over a generic [`kibana.request`](/explore-analyze/workflows/steps/kibana.md#kibana-request) call when a named step exists for the task.

These steps are authenticated automatically using the permissions or API key of the identity executing the workflow, the same model as the [`kibana.*`](/explore-analyze/workflows/steps/kibana.md) and [`cases.*`](/explore-analyze/workflows/steps/cases.md) steps.

## Attack triage

Attack triage steps manage the alert and attack lifecycle you work with on the [Attacks page](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md): status, assignees, and tags on individual alerts and on the correlated attacks that group them.

Use them to:

* Set alert status and manage alert tags and assignees (`security.setAlertStatus`, `security.setAlertTags`, `security.assignAlert`)
* Set attack status and manage attack tags and assignees (`security.setAttackStatus`, `security.setAttackTags`, `security.assignAttack`)

Refer to [Attack triage action steps](/explore-analyze/workflows/steps/attack-triage.md) for shared conventions, parameters, and YAML examples.

## Related

- [Attack triage action steps](/explore-analyze/workflows/steps/attack-triage.md): Status, assignee, and tag management for alerts and attacks.
- [Kibana action steps](/explore-analyze/workflows/steps/kibana.md): Generic `kibana.request` and older PascalCase alert steps.
- [Cases action steps](/explore-analyze/workflows/steps/cases.md): Hand off a triaged alert or attack to a case.
- [Step type index](/explore-analyze/workflows/reference/step-types.md): Alphabetical lookup of every step type.
