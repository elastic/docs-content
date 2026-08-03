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

Namespace index templates are {{fleet}}-managed index templates scoped to one namespace of an installed integration. When you opt a namespace in, {{fleet}} creates one of these templates for each data stream defined by the integration package, and each template references a `<namespace>@custom` component template that you create and manage.

Use this feature when you want the same custom settings or mappings on every data stream in a specific namespace for a given integration, instead of editing each data stream's `@custom` component template separately.

## How namespace index templates work [data-streams-namespace-custom-how]

When you enable namespace index templates for a namespace on an installed integration, {{fleet}} creates one namespace index template for each data stream defined by the package. The templates are named using the following pattern:

```text
<type>-<dataset>@namespace.<namespace>
```

For example, enabling the `production` namespace for the System integration creates templates such as `logs-system.application@namespace.production`.

Each namespace index template is a copy of the integration's base data stream index template, but differs in these ways:

* The `index_patterns` value is scoped to that namespace (for example, `logs-system.application-production*`).
* The priority is `250`, which is higher than the base template priority of `200`, so {{es}} applies the namespace index template for matching data streams.
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
2. Select the integration you want, then create a new integration policy or select an existing integration policy from the **Integration policies** tab.
3. In the **Integration settings** section, expand **Advanced options**.
4. In the **Namespace** field, enter the namespace you want to customize.
5. Turn on **Use dedicated index templates for this namespace**.
6. Save the policy.
:::

After you save, {{fleet}} creates the namespace index templates asynchronously. You can confirm they exist on the integration's **Assets** tab, or in the **Index Management** → **Index Templates** list by searching for `@namespace.`.

::::{important}
Namespace index templates are shared across all integration policies for that integration package and namespace. Enabling or turning them off for one policy updates the opt-in list for the entire integration package.
::::

## Create the namespace `@custom` component template [data-streams-namespace-custom-component]

1. Find **Index Management** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), and open the **Component Templates** tab.
2. Select **Create component template**.
3. Name the template using the pattern `<namespace>@custom` (for example, `production@custom`).
4. Add the index settings, mappings, or aliases you want applied to every data stream in that namespace for opted-in integrations.
5. Create the component template.
6. Roll over the affected data streams so new backing indices pick up the changes. For example:

    ```console
    POST logs-system.application-production/_rollover
    ```

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

## Turn off namespace index templates [data-streams-namespace-custom-disable]

You can remove a namespace from the opt-in list in either of these ways:

* On the integration **Settings** tab, remove the namespace from **Namespaces with dedicated index templates**, then save.
* In the integration policy editor, turn off **Use dedicated index templates for this namespace**, then save.

When you remove a namespace from the opt-in list, {{fleet}} deletes the corresponding namespace index templates. The `<namespace>@custom` component template is left in place so you can reuse it later.

## Overlapping index templates [data-streams-namespace-custom-conflicts]

If you previously duplicated a base data stream index template and gave the copy a higher priority, that copy can overlap with the {{fleet}}-managed namespace index template at priority `250`. When you opt a namespace in, {{fleet}} warns you about overlapping templates and what will happen for each one.

For details and resolution steps, refer to [Resolve overlapping index templates for namespace customization](/reference/fleet/data-streams-template-conflicts.md).

## Related pages [data-streams-namespace-custom-related]

* [{{agent}} data streams for {{fleet}}](/reference/fleet/data-streams.md)
* [Edit the {{es}} index template](/reference/fleet/data-streams.md#data-streams-index-templates-edit)
* [Resolve overlapping index templates for namespace customization](/reference/fleet/data-streams-template-conflicts.md)
