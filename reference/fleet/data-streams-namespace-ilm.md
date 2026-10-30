---
navigation_title: Apply an ILM policy to a namespace
description: Apply an index lifecycle management policy to every data stream in one namespace of a Fleet integration, from the integration policy editor or the Fleet API.
applies_to:
  stack: ga 9.5+
  serverless: unavailable
products:
  - id: fleet
  - id: elastic-agent
---

# Apply an {{ilm-init}} policy to an integration namespace [data-streams-namespace-ilm]

**Data retention settings** in the integration policy editor lets you choose an [index lifecycle management](/manage-data/lifecycle/index-lifecycle-management.md) ({{ilm-init}}) policy for a namespace, instead of editing component templates by hand. {{fleet}} applies your choice to every data stream the integration defines in that namespace.

The {{ilm-init}} policy is tied to an `(integration, namespace)` pair rather than to a single integration policy. Every integration policy that uses the same integration and namespace shares one {{ilm-init}} policy, and different namespaces can use different policies. Use this feature when you want one retention policy for a whole environment, such as `production`.

## Before you begin [data-streams-namespace-ilm-prereqs]

* [Namespace index templates](/reference/fleet/data-streams-namespace-custom.md) must be enabled for the namespace. Until they are, **Data retention settings** stays unavailable.
* The {{ilm-init}} policy must already exist. [Create it](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md) on the **Index Lifecycle Policies** page first. You can't create a policy from the integration policy editor.
* You need the `manage_ilm` cluster privilege. {{fleet}} enforces this privilege in the UI and in the API.
* You can't change **Data retention settings** on a managed integration policy.

## Apply an {{ilm-init}} policy in the UI [data-streams-namespace-ilm-ui]

1. Find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the integration you want, then:
   * To create an integration policy, click **Add <integration>**.
   * To edit an existing one, open the **Integration policies** tab and select the policy.
3. In the **Integration settings** section, expand **Advanced options**.
4. In the **Namespace** field, enter the namespace you want a custom {{ilm-init}} policy for.
5. Turn on **Use dedicated index templates for this namespace**, if it isn't on already.
6. From **Data retention settings**, select an {{ilm-init}} policy.
7. Save the policy.

You can complete these steps in a single pass. You don't need to save the integration policy before you select an {{ilm-init}} policy.

**Data retention settings** lists the {{ilm-init}} policies you created. Built-in policies that {{es}} manages, such as `logs` and `metrics`, and internal policies whose names begin with a dot, aren't listed.

::::{note}
**Data retention settings** appears only in the integration policy editor. The integration's **Settings** tab manages the namespace opt-in list, but it doesn't include the {{ilm-init}} policy selection.
::::

## Apply an {{ilm-init}} policy with the API [data-streams-namespace-ilm-api]

Use the {{fleet}} update package API to apply an {{ilm-init}} policy to a namespace:

```console
PUT kbn:/api/fleet/epm/packages/system
{
  "namespace_customization_settings": {
    "production": { "ilm_policy": "my-retention-policy" }
  }
}
```

To clear the policy for a namespace, pass an empty object for it:

```console
PUT kbn:/api/fleet/epm/packages/system
{
  "namespace_customization_settings": {
    "production": {}
  }
}
```

::::{important}
`namespace_customization_settings` merges per namespace: namespaces you leave out of the request keep their current settings. This differs from `namespace_customization_enabled_for`, which replaces the entire opt-in list. Send only the namespaces you want to change.
::::

{{fleet}} rejects the request in these cases:

* The namespace isn't opted in for namespace index templates.
* The {{ilm-init}} policy doesn't exist.
* You don't have the `manage_ilm` cluster privilege.
* The namespace doesn't match the allowed namespace prefixes for your {{kib}} space.

{{fleet}} applies the changes asynchronously after the request succeeds. For the full request schema, refer to the [update package API]({{kib-apis}}operation/operation-put-fleet-epm-packages-pkgname).

## How {{fleet}} applies the policy [data-streams-namespace-ilm-how]

For each data stream, {{fleet}} creates a managed component template that holds the `index.lifecycle.name` setting. These component templates are named using the same pattern as the namespace index templates:

```text
<type>-<dataset>@namespace.<namespace>
```

Each namespace index template references its component template in `composed_of`, after the `<namespace>@custom` component template and before the data stream-level `@custom` template. For example, `logs-system.application@namespace.production` contains:

```json
[
  "logs@mappings",
  "logs@settings",
  "logs-system.application@package",
  "logs@custom",
  "system@custom",
  "production@custom",
  "logs-system.application@namespace.production",
  "logs-system.application@custom",
  "ecs@mappings",
  ".fleet_globals-1",
  ".fleet_agent_id_verification-1"
]
```

Because the data stream-level `@custom` template comes later in the list, it takes precedence. If you set `index.lifecycle.name` in `logs-system.application@custom`, that setting wins over the {{ilm-init}} policy you apply here.

{{fleet}} creates a component template for every data stream the integration defines, including data streams that no integration policy has enabled yet. A data stream you enable later uses the same {{ilm-init}} policy.

To verify the managed component template and the reference to it:

```console
GET _component_template/logs-system.application@namespace.production
```

```console
GET _index_template/logs-system.application@namespace.production
```

To check which {{ilm-init}} policy a data stream uses:

```console
GET _data_stream/logs-system.application-production
```

## When changes take effect [data-streams-namespace-ilm-rollover]

{{fleet}} applies your changes with a background task, so the component templates can take a few seconds to appear after you save. The task also triggers a rollover for the affected data streams on a best-effort basis.

{{ilm-init}} policies take effect when new backing indices are created. Existing backing indices keep the policy they were created with. If the automatic rollover didn't happen, you can roll over a data stream yourself with the [{{es}} rollover API]({{es-apis}}operation/operation-indices-rollover):

```console
POST logs-system.application-production/_rollover
```

## Change or clear the {{ilm-init}} policy [data-streams-namespace-ilm-clear]

* To use a different {{ilm-init}} policy, select it in **Data retention settings** on any integration policy that uses that integration and namespace. The change applies to all integration policies for the pair.
* To stop using a custom {{ilm-init}} policy while the namespace keeps its dedicated index templates, select **None (use default)**. {{fleet}} deletes the managed component templates, and the data streams return to the {{ilm-init}} policy defined by the integration's base index templates. The `<namespace>@custom` component template and any settings or mappings in it stay in place.
* If you turn off **Use dedicated index templates for this namespace**, or remove the namespace from **Namespaces with dedicated index templates** on the integration's **Settings** tab, {{fleet}} also clears the {{ilm-init}} policy for that namespace. You don't need to clear it first. This removes the namespace index templates as well, so use **None (use default)** if you want to keep your other namespace-level customizations.

As with any other {{ilm-init}} change, existing backing indices keep the policy they were created with until the data stream rolls over.

## Limitations [data-streams-namespace-ilm-limitations]

* You can apply only one {{ilm-init}} policy per `(integration, namespace)` pair. Two integration policies that use the same integration and namespace can't use different {{ilm-init}} policies.
* The {{ilm-init}} policy applies to every data stream the integration defines. To target a single data stream, apply the policy to [specific data streams across all namespaces](/reference/fleet/data-streams-scenario2.md), or to [one data stream in one namespace](/reference/fleet/data-streams-scenario3.md).
* You can select {{ilm-init}} policies only. To use a [data stream lifecycle](/manage-data/lifecycle/data-stream.md) instead, configure it outside of {{fleet}}.
* An `index.lifecycle.name` setting in a data stream-level `@custom` component template overrides the policy you apply here.

## Related pages [data-streams-namespace-ilm-related]

* [Customize data streams with namespace index templates](/reference/fleet/data-streams-namespace-custom.md)
* [Customize data retention policies for integrations](/reference/fleet/data-streams-ilm-tutorial.md)
* [Index lifecycle management ({{ilm-init}})](/reference/fleet/data-streams.md#data-streams-ilm)
* [Create an {{ilm-init}} policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md)
* [Manage lifecycle policies for integrations data](/manage-data/lifecycle/index-lifecycle-management/manage-lifecycle-integrations-data.md)
