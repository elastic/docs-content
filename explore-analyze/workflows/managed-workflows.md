---
navigation_title: Managed workflows
applies_to:
  stack: ga 9.5+
  serverless: ga
description: Understand managed workflows — Elastic-shipped workflow definitions that install automatically and power product features.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Managed workflows [workflows-managed-workflows]

A *managed workflow* is a workflow definition that Elastic ships and installs automatically. Managed workflows power product features. They are distinct from the workflows you author yourself.

| | Managed workflow | User-authored workflow |
|---|---|---|
| Who creates it | Elastic (installed automatically) | You |
| Who maintains the YAML | Elastic | You |
| Editing and deleting | YAML is read-only; you can't delete the workflow | Full edit and delete |
| Typical use | Back product functionality (for example, Security alert analysis) | Custom automation you build |

Managed workflows appear with a **Managed** badge in {{kib}}. By default they are hidden from the Workflows list. To show them, turn on [**Show managed workflows**](kibana://reference/advanced-settings.md#kibana-workflows-settings) in Advanced Settings and grant the managed workflow read privileges. Refer to [](/explore-analyze/workflows/get-started/setup.md#workflows-managed-visibility) for more information.

Configure managed workflows from the settings for the feature that owns them, not by editing their YAML on the **Workflows** page. For example, configure Attack Discovery's managed workflows from [Attack discovery settings](/solutions/security/ai/attack-discovery/configure-alert-retrieval-from-attacks-page.md) on the **Attacks** view. You can't edit or delete managed workflow YAML.

:::{important}
Turning a managed workflow off on the **Workflows** page can stop the feature that depends on it from running. For example, disabling an Attack Discovery generation or retrieval managed workflow can break or interrupt Attack Discovery runs that rely on it.
:::
