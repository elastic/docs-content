---
navigation_title: Customize data streams with namespace index templates
description: Enable namespace index templates so you can apply shared settings and mappings across a Fleet integration's data streams in one namespace.
applies_to:
  stack: ga 9.5+
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Customize data streams with namespace index templates [data-streams-namespace-custom]

Namespace index templates are {{fleet}}-managed [index templates](/manage-data/data-store/templates.md#index-templates) scoped to one namespace of an installed integration. When you opt a namespace in, {{fleet}} creates one of these templates for each data stream defined by the integration, and each template references a `<namespace>@custom` component template that you create and manage.

Use this feature when you want the same custom settings or mappings on every data stream in a specific namespace for a given integration, instead of editing each data stream's `@custom` component template separately.

Setting up namespace index templates involves these steps:

1. Enable namespace index templates for the namespace, in the [UI](#data-streams-namespace-custom-ui) or with the [API](#data-streams-namespace-custom-api).
2. [Create the `<namespace>@custom` component template](#data-streams-namespace-custom-component) that holds the custom settings and mappings you want applied to every data stream in the namespace.
3. If you have pre-existing index templates that overlap with the {{fleet}}-managed templates, [resolve the overlapping templates](#data-streams-namespace-custom-conflicts).

{applies_to}`stack: ga 9.5+` Opting a namespace in also lets you [apply an {{ilm-init}} policy to it](/reference/fleet/data-streams-namespace-ilm.md) from the integration policy editor.

## How namespace index templates work [data-streams-namespace-custom-how]

When you enable namespace index templates for a namespace on an installed integration, {{fleet}} creates one namespace index template for each data stream defined by the integration. The templates are named using the following pattern:

```text
<type>-<dataset>@namespace.<namespace>
```

For example, enabling the `production` namespace for the System integration creates templates such as `logs-system.application@namespace.production`.

Each namespace index template is a copy of the integration's base data stream index template, but differs in these ways:

* The `index_patterns` value is scoped to that namespace (for example, `logs-system.application-production*`).
* The priority is the base template priority plus 50: `250` for most integrations (base `200`), or `200` for integrations with `dataset_is_prefix: true` data streams (base `150`). Because this is higher than the base template priority, {{es}} applies the namespace index template for matching data streams. If you change this priority manually, {{fleet}} restores the default the next time the integration's templates are reinstalled or resynchronized.
* The `composed_of` list includes a `<namespace>@custom` component template (for example, `production@custom`) after the type-level and package-level `@custom` templates, and before the data stream-level `@custom` template.

Example `composed_of` list for `logs-system.application@namespace.production`:

```json
[
  "logs@mappings",
  "logs@settings",
  "logs-system.application@package",
  "logs@custom",
  "system@custom",
  "production@custom",
  "logs-system.application@custom",
  "ecs@mappings",
  ".fleet_globals-1",
  ".fleet_agent_id_verification-1"
]
```

Later component templates in this list take precedence when the same setting or mapping key appears more than once. From highest to lowest precedence among the `@custom` templates: `logs-system.application@custom`, then `production@custom`, then `system@custom`, then `logs@custom`.

{applies_to}`stack: ga 9.5+` If you also [apply an {{ilm-init}} policy to the namespace](/reference/fleet/data-streams-namespace-ilm.md), {{fleet}} adds a managed component template named `<type>-<dataset>@namespace.<namespace>` to `composed_of`, between `production@custom` and `logs-system.application@custom`. That template holds only the `index.lifecycle.name` setting.

::::{note}
{{fleet}} does not create the `<namespace>@custom` component template. You create and manage that template yourself. Until you create it, the reference in `composed_of` has no effect. The same `<namespace>@custom` template is shared by namespace name across every integration that has that namespace opted in.
::::

The namespaces you opt in for an integration are the same across the whole cluster. The index templates and component templates {{fleet}} creates are also shared across the cluster.

If your {{kib}} space restricts which namespaces are allowed, you can only enable namespace index templates for namespaces that match those restrictions.

## Enable namespace index templates in the UI [data-streams-namespace-custom-ui]

You can enable namespace index templates from the integration settings, or while creating or editing an integration policy.

:::{dropdown} From the integration's Settings tab
:open:

1. Find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Open the **Installed integrations** tab, then select the integration.
3. Open the **Settings** tab.
4. In the **Namespace index templates** section, add the namespace you want to customize.
5. Save your changes.
:::

:::{dropdown} From the integration policy editor
:open:

1. Find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the integration you want, then:
   * To create an integration policy, click **Add <integration>**.
   * To edit an existing one, open the **Integration policies** tab and select the policy.
3. In the **Integration settings** section, expand **Advanced options**.
4. In the **Namespace** field, enter the namespace you want to customize.
5. Turn on **Use dedicated index templates for this namespace**.
6. Save the policy.
:::

After you save, {{fleet}} creates the namespace index templates asynchronously. You can confirm they exist on the integration's **Assets** tab, or in the **Index Management** → **Index Templates** list by searching for `@namespace.`.

::::{important}
Namespace index templates are shared across all integration policies for that integration and namespace. Enabling or turning them off for one policy updates the opt-in list for the entire integration.
::::

After you opt in, [create the `<namespace>@custom` component template](#data-streams-namespace-custom-component) so your customizations take effect.

## Enable namespace index templates with the API [data-streams-namespace-custom-api]

You can also manage opt-in with the {{fleet}} package APIs. Template create and delete operations run asynchronously after the request succeeds.

To enable one or more namespaces for a single installed package:

```console
PUT kbn:/api/fleet/epm/packages/system
{
  "namespace_customization_enabled_for": ["production"]
}
```

::::{note}
For a single package, `namespace_customization_enabled_for` replaces the full opt-in list. To keep existing namespaces, include them in the array. To turn a namespace off, omit it from the array, or pass an empty array to clear the list.
::::

To enable namespaces or remove them from the opt-in list across multiple packages in one request:

```console
POST kbn:/api/fleet/epm/packages/_bulk_namespace_customization
{
  "packages": ["system", "nginx", "apache"],
  "enable": ["production"],
  "disable": ["staging"]
}
```

The bulk endpoint is additive and subtractive: `enable` adds namespaces to each package's opt-in list, and `disable` removes them. It does not replace the full list.

Your customizations only apply after you create the `<namespace>@custom` component template.

## Create the namespace `@custom` component template [data-streams-namespace-custom-component]

1. Find **Index Management** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), and open the **Component Templates** tab.
2. Select **Create component template**.
3. Name the template using the pattern `<namespace>@custom` (for example, `production@custom`).
4. Add the index settings, mappings, or aliases you want applied to every data stream in that namespace for opted-in integrations.
5. Create the component template.
6. Roll over each affected data stream so new backing indices pick up the changes. For example:

    ```console
    POST logs-system.application-production/_rollover
    ```

## Turn off namespace index templates [data-streams-namespace-custom-disable]

You can remove a namespace from the opt-in list in either of these ways:

* On the integration **Settings** tab, remove the namespace from **Namespaces with dedicated index templates**, then save.
* In the integration policy editor, turn off **Use dedicated index templates for this namespace**, then save.

When you remove a namespace from the opt-in list, {{fleet}} deletes the corresponding namespace index templates. The `<namespace>@custom` component template is left in place so you can reuse it later.

{applies_to}`stack: ga 9.5+` If an {{ilm-init}} policy was applied to the namespace, {{fleet}} clears it too. You don't need to clear it before you remove the namespace.

## Overlapping index templates [data-streams-namespace-custom-conflicts]

If you previously duplicated a base data stream index template and gave the copy a higher priority, that copy can overlap with the {{fleet}}-managed namespace index template. When you opt a namespace in, {{fleet}} warns you about overlapping templates and what will happen for each one.

For details and resolution steps, refer to [Resolve overlapping index templates for namespace customization](/reference/fleet/data-streams-template-conflicts.md).

## Related pages [data-streams-namespace-custom-related]

* [Apply an {{ilm-init}} policy to an integration namespace](/reference/fleet/data-streams-namespace-ilm.md)
* [{{agent}} data streams for {{fleet}}](/reference/fleet/data-streams.md)
* [Edit the {{es}} index template](/reference/fleet/data-streams.md#data-streams-index-templates-edit)
* [Resolve overlapping index templates for namespace customization](/reference/fleet/data-streams-template-conflicts.md)
