---
navigation_title: Entity store
applies_to:
  stack: preview 9.5+
  serverless: preview
description: Reference for the entityStore.* action step that lets workflows set, update, or remove the asset criticality of an entity store entity in Elastic Security.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Entity store action step [workflows-entity-store-steps]

The entity store action step let workflows operate on entities in the {{elastic-sec}} [entity store](/solutions/security/advanced-entity-analytics/entity-store.md). The namespace (`entityStore.*`) provides the [`entityStore.updateAssetCriticality`](#entitystore-updateassetcriticality) step, which sets, updates, or removes the [asset criticality](/solutions/security/advanced-entity-analytics/asset-criticality.md) of an entity and, by default, triggers a [risk score](/solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md) recalculation for it.

This step is automatically authenticated using the permissions or API key of the identity executing the workflow, the same model as the [`kibana.*`](/explore-analyze/workflows/steps/kibana.md) and [`cases.*`](/explore-analyze/workflows/steps/cases.md) steps.

:::{note}
This step lives under the `entityStore.*` step type namespace. It exposes an explicit input schema, so parameters are validated when you save the workflow and are discoverable in the Workflows editor.
:::

:::{include} ../_snippets/schema-location-legend.md
:::

## `entityStore.updateAssetCriticality` [entitystore-updateassetcriticality]

Set, update, or remove the asset criticality level of an entity store entity, identified by its entity type and entity ID (EUID).

To run this step, the workflow's execution identity needs permission to write to the entity store in the target space. The target entity must already exist in the entity store; attempting to set an asset criticality for an entity that isn't in the store fails with an error.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `entity_type` | `with` | string | Yes | The entity store entity type: `user`, `host`, or `service`. |
| `entity_id` | `with` | string | Yes | The entity store entity ID (EUID), for example `host:my-host`. Maximum 1000 characters. |
| `criticality_level` | `with` | string | Yes | The criticality level to assign to the entity: `low_impact`, `medium_impact`, `high_impact`, or `extreme_impact`. Pass `null` to remove the existing criticality level. |
| `recalculate-risk-score` | `top level` | boolean | No (default `true`) | Whether to trigger a risk score recalculation for the entity after updating its criticality. |

**Removing a criticality level.** `criticality_level` is required, but you can pass `null` to clear the current level rather than setting a new one.

**Risk score recalculation.** By default, a successful criticality update triggers a risk score recalculation for the entity. Set `recalculate-risk-score: false` to skip it. Recalculation runs as a side effect of the update, so if it fails (for example, when no risk engine is configured for the space) the step still succeeds and the criticality change is preserved. If recalculation fails or is skipped, the entity's risk score is recalculated on the next scheduled risk scoring engine run.

### Output [entitystore-updateassetcriticality-output]

| Field | Type | Description |
|---|---|---|
| `success` | boolean | Whether the criticality update succeeded. |
| `message` | string | Human-readable summary of what happened, including whether a risk score recalculation ran, was skipped, or failed. |

### Examples [entitystore-updateassetcriticality-examples]

Set the criticality level for a host:

```yaml
- name: set_host_criticalilty
  type: entityStore.updateAssetCriticality
  with:
    entity_type: "host"
    entity_id: "{{ variables.host_entity_id }}"
    criticality_level: "high_impact"
```

Remove the criticality level from a host:

```yaml
- name: clear_host_criticality
  type: entityStore.updateAssetCriticality
  with:
    entity_type: "host"
    entity_id: "{{ variables.host_entity_id }}"
    criticality_level: null
```

Set the criticality level for a user without triggering a risk score recalculation:

```yaml
- name: set_user_criticality
  type: entityStore.updateAssetCriticality
  recalculate-risk-score: false
  with:
    entity_type: "user"
    entity_id: "{{ variables.user_entity_id }}"
    criticality_level: "extreme_impact"
```

## Related

- [Asset criticality](/solutions/security/advanced-entity-analytics/asset-criticality.md): The {{elastic-sec}} feature this step updates.
- [Entity risk scoring](/solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md): Background on the risk score recalculation this step can trigger.
- [{{kib}} action steps](/explore-analyze/workflows/steps/kibana.md): Generic `kibana.request` escape hatch for other {{kib}} APIs.
- [Cases action steps](/explore-analyze/workflows/steps/cases.md): Hand off an entity to a case after changing its criticality.
- [Step type index](/explore-analyze/workflows/reference/step-types.md): Alphabetical lookup of every step type.
