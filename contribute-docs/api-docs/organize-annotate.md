---
navigation_title: Organize and annotate docs
---

# Organize and annotate your API docs

This page explains how to organize your API documentation and add technical metadata to help users understand your APIs. You'll find guidance on:

- Adding required OpenAPI document information
- Adding structure with operation IDs and tags
- Documenting API availability and lifecycle status
- Specifying required permissions and privileges
- Extending OpenAPI with custom properties

For guidance on writing effective API content like summaries, descriptions, and examples, see [Core guidelines](./guidelines.md).

## Add Open API document info

The published OpenAPI documents must have the following metadata in the [`info` object](https://spec.openapis.org/oas/latest#info-object):

| **Field**      | **Description** |
| -------------- | --------------- |
| `description`   | A descriptive overview of the API's purpose and functionality. This should be a concise summary that helps users understand what the API does. |
| `license`        | [License information](https://spec.openapis.org/oas/latest#license-object "https://spec.openapis.org/oas/latest#license-object") for the API (which is distinct from the documentation license).<br>Until we have a custom extension, add the documentation license ([Deed - Attribution-NonCommercial-NoDerivatives 4.0 International - Creative Commons](https://creativecommons.org/licenses/by-nc-nd/4.0/)) to `info.description` |
| `title`          | The title of the API |
| `version`        | The version of the document (which is distinct from the OpenAPI specification version and the API implementation version) |
| `x-feedbackLink` | This specialization extension enables us to collect feedback about the document. The URL should take readers to a GitHub issue template so they can create an issue. Refer to [Get feedback from users](https://docs.bump.sh/help/publish-documentation/feedback/) |


## Add OpenAPI specification version

You must specify the version number of the OpenAPI specification that the OpenAPI document uses. This value is not related to the API `version` string in the [document info](#add-open-api-document-info).

[Bump.sh](https://bump.sh/openapi "https://bump.sh/openapi") supports all versions from Swagger 2.0 to OpenAPI 3.1.

Learn more about the [OpenAPI object](https://spec.openapis.org/oas/latest#openapi-object).

## Add operation identifiers

The `operationId` uniquely identifies the operation.

It is case sensitive and must be unique in the OpenAPI document.

When adding operation identifiers:
- Ensure each operation has a unique `operationId`
- Make `operationId`s valid for use in URLs (no special characters)
- Use consistent naming patterns across related operations

## Group APIs with tags

We use [tags](https://swagger.io/docs/specification/v3_0/grouping-operations-with-tags/) to group APIs by feature.

There are two types of tags:

| Tag type | Purpose | Notes |
| --- | --- | --- |
| **Document-level** | Define the available tag categories for the entire API | - Use human-readable names<br>- Add descriptions<br>- Order affects navigation |
| **Operation-level** | Assign each endpoint to a category | - Use tags from document-level list<br>- Each operation needs at least one tag |

**Best practices:**
- Use **consistent tag names** across your entire API
- Use **one tag per operation** for cleaner navigation  
- Use **sentence case** for tag names (use `x-displayName` to override the actual tag name if necessary)
- **Order tags logically** to create intuitive navigation flow

### Examples

::::{tab-set}
:group: implementations

:::{tab-item} OpenAPI
:sync: openapi

```yaml
paths:
  /indices:
    post:
      summary: Create an index
      tags: ["Index management"]
      description: Creates a new index with optional settings and mappings
  /indices/{index}:
    delete:
      summary: Delete an index
      tags: ["Index management"]  
      description: Removes an index and all its data
  /indices/{index}/_settings:
    put:
      summary: Update index settings
      tags: ["Index management"]
      description: Modifies settings for an existing index
```

**Define tag metadata** in the top-level `tags` section. Write a description for each tag to clarify its purpose:

```yaml
tags:
  - name: "Index management"
    description: Operations for creating, configuring, and managing indices
  - name: "Search"
    description: Operations for querying and retrieving documents
  - name: "Document operations"
    description: Operations for creating, updating, and deleting individual documents
```
:::

:::{tab-item} Elasticsearch
:sync: elasticsearch

**Default namespace behavior**

The compiler extracts the namespace from your endpoint name using everything before the first dot:

- `indices.create` → `"indices"` tag
- `search.template` → `"search"` tag  
- `cluster.health` → `"cluster"` tag
- `ping` → `"ping"` tag (no dot, uses full name)

This automatic grouping works well when your namespace matches how users think about the API functionality.

**Overriding defaults with `@doc_tag`**

Use the `@doc_tag` annotation when the automatic namespace doesn't match user expectations or when you want more descriptive groupings:

```ts
/**
 * @rest_spec_name indices.create
 * @doc_tag "Index management"
 */
export interface Request extends RequestBase {
  // ...
}
```

This moves the operation from an "indices" section to an "Index management" section.

**Add new tags**

If you create a new tag value, you must also add it to the [elasticsearch-shared-overlays.yaml](https://github.com/elastic/elasticsearch-specification/blob/main/docs/overlays/elasticsearch-shared-overlays.yaml) file. You can see all existing tag values in that file.

Use **sentence case** for tag names. If you need different casing in the final docs, use the `x-displayName` extension in the overlay file.

:::{note}
Each operation can only have one tag, even though the OpenAPI specification supports multiple tags. This is a deliberate system constraint to keep the docs navigation clean and predictable.
:::
:::

:::::

## Extend OpenAPI documents

Per [OpenAPI Specification v3.0.3](https://spec.openapis.org/oas/v3.0.3#specification-extensions):

_"While the OpenAPI Specification tries to accommodate most use cases, additional data can be added to extend the specification at certain points."_

The extensions properties are implemented as patterned fields that are always prefixed by `x-`. The following extensions are supported by Bump.sh:

| **Field**       | **Description** |
|-----------------|-----------------|
| `x-beta` | Indicates that something is in beta. **Note:** Use `x-state` instead. |
| `x-codeSamples` | Defines code examples and their programming language. [Docs](https://docs.bump.sh/help/specification-support/doc-code-samples/) |
| `x-displayName` | Overrides tag names at the document level to align with documentation standards. |
| `x-feedbackLink` | Adds a link for users to send feedback. [Docs](https://docs.bump.sh/help/publish-documentation/feedback/) |
| `x-model` | Used to abbreviate deeply nested/recursive API sections (e.g., Elasticsearch query DSL). Should include an `externalDocs` link. Currently only applied via overlays. |
| `x-state` | Indicates lifecycle state (e.g., “Technical preview; added in 9.1.0”). Appears next to the operation/property. |
| `x-topics` | Adds extra pages shown below the introduction. [Docs](https://docs.bump.sh/help/enhance-documentation-content/topics/) |

:::{note}
For more information, refer to the [Bump.sh page about Extensions](https://docs.bump.sh/help/specification-support/extensions/)
:::

## Specify API lifecycle status

In OpenAPI, lifecycle status is communicated through extension properties like `x-state` and the standard `deprecated` field. These annotations indicate deployment compatibility, stability level, and version information.

### Examples

::::{tab-set}
:group: implementations

:::{tab-item} OpenAPI
:sync: openapi

**Availability and stability** is specified using the `x-state` extension property:

```yaml
paths:
  /indices/{index}:
    get:
      summary: Get index information
      x-state: "Generally available; Added in 7.10.0"
      # ...

  /ml/anomaly_detection/{jobId}/_forecast:
    post:
      summary: Create anomaly detection forecast
      x-state: "Beta; Added in 8.5.0"
      # ...
```
**Deprecation notices** use the standard OpenAPI `deprecated` boolean field:

```yaml
components:
  schemas:
    IndexSettings:
      type: object
      properties:
        blocks:
          type: object
          deprecated: true
          description: |
            Deprecated in 8.0.0. Use 'index.blocks.read_only' instead.
            Controls read/write blocks on the index.
```
:::

:::{tab-item} Elasticsearch
:sync: elasticsearch

**API availability** is specified using the `@availability` annotation:

```ts
/**
 * @availability stack
 * @availability serverless
 */
class FooRequest {
  bar: string
  /**
   * @availability stack
   * @availability serverless
   */
  baz: string
  faz: string
}
```

**When to use parameter/property-level availability**

Parameter and property-level `@availability` annotations are necessary in specific scenarios:

1. **Mixed deployment availability**: When an API supports both serverless and stateful deployments, but some parameters/properties are only available in one deployment type
2. **Later additions**: When a parameter or property is added after the initial API release, making its availability later than the API-level availability

**API stability** is indicated using the `stability` parameter:

```ts
/**
 * @availability stack since=8.0.0 stability=beta
 * @availability serverless stability=experimental
 */
class BetaRequest {
  // ...
}
```

The stability values map to the following `x-state` labels:
- **`stability=stable`** (default) → "Generally available" 
- **`stability=beta`** → "Beta"
- **`stability=experimental`** → "Technical preview"

**Deployment-specific APIs** can be restricted to certain deployment types:

```ts
export class Example {
  /**
   * Available in both (default when no annotations)
   */
  fieldBoth1: integer

  /**
   * @availability serverless
   */
  fieldServerlessOnly: integer

  /**
   * @availability stack
   */
  fieldStackOnly: integer
}
```

This example shows a mixed deployment scenario where the API itself is available to both deployment types, but individual parameters have different availability constraints.

**Version information** uses the `since=` parameter:

```ts
/**
 * @availability stack since=7.10.0
 * @availability serverless
 */
class FooRequest {
  /**
   * Added with the original API
   */
  originalField: string
  
  /**
   * @availability stack since=7.11.0
   * @availability serverless
   */
  laterAddition: string
}
```

This example shows the "later addition" scenario where `laterAddition` was added after the initial API release, requiring a parameter-level availability annotation with a later version than the API-level availability.

:::::{important}
The `since` field is only available for `stack`. If the API is introduced in multiple major versions (eg: `8.19.0` and `9.1.0`), use the appropriate value in each branch.
:::::


**Deprecation notices** use the `@deprecated` annotation:

```ts
class Foo {
  bar: string
  /** @deprecated 7.0.0 */
  baz?: string
  faz: string
}
```

You can add an optional description explaining the deprecation:

```ts
class Foo {
  bar: string
  /** @deprecated 7.0.0 'baz' has been deprecated, use 'bar' instead */
  baz?: string
  faz: string
}
```
:::

::::

:::{important}
Since we now only publish API docs for major versions (v8, v9) and not for minor versions (8.1, 8.2, etc.), always include the full version information in your `x-state` labels. For example: `Technical preview; added in 9.1.0".
:::

## Document required permissions

Required permissions aren't part of the standard OpenAPI specification, but they can be documented in operation descriptions or through custom extensions. In Elasticsearch, we use annotations that generate structured permission documentation.

### Examples

::::{tab-set}
:group: implementations

:::{tab-item} OpenAPI
:sync: openapi

Add permission requirements to the operation description using markdown formatting:

```yaml
paths:
  /indices/{index}:
    put:
      summary: Create index
      description: |
        Creates a new index with optional settings and mappings.
        
        ## Required authorization
        
        * Index privileges: `create_index`, `manage`
```

For APIs requiring multiple permission types:

```yaml
paths:
  /indices/{index}/_stats:
    get:
      summary: Get index statistics
      description: |
        Returns statistics about one or more indices.
        
        ## Required authorization
        
        * Index privileges: `monitor`, `view_index_metadata`
        * Cluster privileges: `monitor`
```
:::

:::{tab-item} Elasticsearch
:sync: elasticsearch

**Index-level permissions** use the `@index_privileges` annotation:

```ts
/**
 * @rest_spec_name indices.create
 * @availability stack since=0.0.0 stability=stable
 * @index_privileges create_index, manage
 */
export interface Request extends RequestBase {
 // ...
}
```

This generates the following markdown section in the operation description:

```markdown
## Required authorization

* Index privileges: `create_index`, `manage`
```

**Cluster-level permissions** use the `@cluster_privileges` annotation:

```ts
/**
 * @rest_spec_name cluster.state
 * @availability stack since=1.3.0 stability=stable
 * @cluster_privileges monitor, manage
 */
export interface Request extends RequestBase {
 // ...
}
```

This adds:

```markdown
## Required authorization

* Cluster privileges: `monitor`, `manage`
```

**Combined privileges** use both annotations together:

```ts
/**
 * @rest_spec_name indices.analyze
 * @index_privileges read
 * @cluster_privileges monitor
 */
export interface Request extends RequestBase {
 // ...
}
```

This creates:

```markdown
## Required authorization

* Index privileges: `read`
* Cluster privileges: `monitor`
```

:::{note}
The annotation system doesn't support "OR" relationships between privileges. When multiple privileges are listed, they appear as if all are required. Use only the minimum necessary privileges for each operation to avoid confusion.
:::
:::

::::
