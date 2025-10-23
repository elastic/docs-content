# Add core content

This page covers the core guidelines for excellent API docs. Learn how to write clear summaries and descriptions, create helpful examples, and add useful links.

## Write summaries and descriptions

Most objects in your Open API specification accept both concise summaries and detailed descriptions to help users understand their purpose and usage.

### Write summaries

Clear, single-sentence summaries help users understand the components of your API at a glance. They appear in various contexts like IDEs, search results, and documentation overviews.

Here are some principles for writing effective summaries:

- **Be concise:** Keep summaries short (between 5-45 characters) because they appear in different contexts where space is limited
- **Start with a verb:** Use action words like "Get", "Update", "Delete", "Create"
- **Use simple verbs:** Use simple verbs (Get, Update, Delete) rather than verbose alternatives (Retrieve, Return, List)
- **Include articles:** "Delete a space", "Delete spaces", "Delete all spaces"
- **Use sentence case:** Capitalize only the first word and proper nouns

#### Summary examples

::::{tab-set}
:group: implementations

:::{tab-item} OpenAPI
:sync: openapi

In OpenAPI specifications, summaries are defined in the `summary` field:

```yaml
paths:
  /indices/{index}:
    get:
      summary: Get index information
      description: Retrieve configuration and mapping information...
```
:::

:::{tab-item} Elasticsearch
:sync: elasticsearch

In the Elasticsearch TypeScript definitions, summaries are added as JSDoc comments above class definitions:

```ts
/**
 * Get index information
 */
class GetIndexRequest {
  // ...
}
```

**Notes:**
- Use 30 characters maximum to avoid text wrapping in generated output
- Don't add a period at the end
:::

:::::

### Write descriptions

>  **"Documentation can be added almost everywhere using a `description` field".** -  [OpenAPI Specification docs](https://learn.openapis.org/specification/docs.html#providing-long-descriptions-in-yaml)

Most OpenAPI objects accept a `description` field. For best results, add descriptions wherever possible.

Elastic APIs are generally complex, and summaries alone are not enough to explain their purpose and usage.
Descriptions enable you to add detailed explanations of your OpenAPI objects.

They are essential for transforming machine-readable information into nicely formatted, human-readable prose. You can add paragraph breaks, links, or lists to your descriptions.

Here are some principles for effective descriptions:

- **Explain purpose and impact:** What does this operation/parameter do and why would users need it?
- **Provide context:** What are the prerequisites or related concepts users should know?
- **Use formatting:** Use paragraph breaks, lists, and other formatting options to make descriptions readable
- **Reference related operations:** [Link](#add-links) to complementary APIs or prerequisite steps
- **Provide usage guidance:** How should users typically use this parameter or operation?
- **Document constraints:** What are the valid values, formats, or limitations?
- **Explain data relationships:** For list parameters, clarify how multiple values are handled (comma-separated, arrays, etc.)
- **Document special formats:** Include expected formats for timestamps (ISO-8601), patterns for wildcards, etc.
- **Ensure comprehensive coverage:** Ensure all parameters, tags, and information sections include clear descriptions
- **Use inclusive language:** Avoid problematic terminology (blacklist, whitelist, execute, kill, etc.) and use inclusive language throughout

#### Description examples

::::{tab-set}
:group: implementations

:::{tab-item} OpenAPI
:sync: openapi

**Operation descriptions** 

Add descriptions to operation definitions:

```yaml
paths:
  /books:
    get:
      summary: List books
      description: |
        Retrieve a paginated list of books from the library catalog.
        Use query parameters to filter by author, genre, or publication year.
        Results are sorted by title by default.
```

**Parameter descriptions**

Add descriptions to parameter definitions:  

```yaml
parameters:
  - name: author
    in: query
    description: |
      Filter books by author name. Supports partial matching - 
      searching for "smith" will find "John Smith" and "Jane Smithson".
    schema:
      type: string
      example: "Jane Austen"
```

**Schema property descriptions**

Add descriptions directly to schema properties:

```yaml
components:
  schemas:
    Book:
      type: object
      properties:
        publishedDate:
          type: string
          format: date
          description: |
            The date when the book was first published in ISO 8601 format.
            Used for filtering and sorting operations.
```
:::{tip}
Learn more about providing long descriptions in YAML in the [OpenAPI docs](https://learn.openapis.org/specification/docs.html#providing-long-descriptions-in-yaml).
:::
:::

:::{tab-item} Elasticsearch
:sync: elasticsearch

**Operation descriptions** 

Write comments above class definitions:

```ts
/**
 * Get index information
 * 
 * Retrieve configuration and mapping information for one or more indices.
 * You can use this API to check index settings, mappings, and other metadata
 * before performing operations that might affect the index structure.
 */
class GetIndexRequest {
  // ...
}
```

**Parameter descriptions**

Write comments inline:

```ts
class SearchRequest {
  /**
   * A comma-separated list of data streams, indices, and index aliases used to limit the request. 
   * Wildcard expressions (*) are supported.
   */
  index: string
}

class AlertRule {
  /**
   * An ISO-8601 timestamp that indicates when the event was detected.
   */
  detectedAt: string
}
```
:::

::::

## Document parameters

Proper documentation helps users understand what values are expected, how to construct valid requests, and explains the effects of changing defaults.

Here are some principles for documenting parameters:

- **Write clear descriptions:** Follow the general guidance for [writing descriptions](#write-descriptions)
- **Indicate requirement status appropriately:** 
  - Path parameters are always required (`required: true` must be present)
- **Document parameter constraints:** Specify valid formats, patterns, or value ranges
- **Explain parameter relationships:** Clarify how multiple parameters work together and any dependencies between them

### Examples: Path parameters

::::{tab-set}
:group: implementations

:::{tab-item} OpenAPI
:sync: openapi

Define path parameters directly in the path specification:

```yaml
paths:
  /users/{userId}/posts/{postId}:
    get:
      summary: Get a specific post
      parameters:
        - name: userId
          in: path
          required: true
          description: The unique identifier of the user
          schema:
            type: string
            example: "12345"
        - name: postId
          in: path
          required: true
          description: The unique identifier of the post
          schema:
            type: string
            example: "post-abc"
```

For optional variations, create separate paths:

```yaml
paths:
  /books:
    get:
      summary: List all books
  /books/{category}:
    get:
      summary: List books by category
      parameters:
        - name: category
          in: path
          required: true
          description: The book category to filter by
          schema:
            type: string
            example: "fiction"
```
:::

:::{tab-item} Elasticsearch
:sync: elasticsearch

For endpoints that can accept optional parameters, define multiple paths in the `urls` array:

```ts
urls: [
  {
    path: "/{index}/_doc/{id}",
    methods: ["PUT", "POST"]
  },
  {
    path: "/{index}/_doc",
    methods: ["POST"]
  }
]
```

**Notes:**
- The `make transform-to-openapi` output shows these two paths as separate entities
- The `make transform-to-openapi-for-docs` output contains only the most complex variation of the paths (and mentions the others in its description)
:::

::::

## Document enum values

Enumerated types (enums) define a fixed set of allowed values for a property. Well-documented enum values help users understand the purpose of each option and when to use it.

Here are some principles for documenting enum values:

- **Clarify non-obvious meanings:** Document when the purpose isn't clear from the name alone
- **Provide usage guidance:** Explain when to use each option and any performance implications
- **Document special behavior:** Note if some values are deprecated, experimental, or have unique characteristics
- **Keep it concise:** Use brief, focused descriptions that explain the essential differences

:::{tip}
You can skip documenting enum values that are self-explanatory (like `true`/`false`) or follow standard conventions (like HTTP status codes).
:::

### Examples

::::{tab-set}
:group: implementations

:::{tab-item} OpenAPI
:sync: openapi

In OpenAPI specifications, enum descriptions are documented in schema definitions:

```yaml
components:
  schemas:
    SearchType:
      type: string
      enum:
        - query_then_fetch
        - dfs_query_then_fetch
        - query_and_fetch
      description: |
        The search execution strategy:
        - `query_then_fetch`: Searches across all fields using default settings
        - `dfs_query_then_fetch`: Performs distributed frequency scoring before fetching results  
        - `query_and_fetch`: Fetches results immediately without scoring optimization
```
:::

:::{tab-item} Elasticsearch
:sync: elasticsearch

In TypeScript definitions, enum descriptions are added as JSDoc comments above each value:

```ts
export enum SearchType {
  /** Searches across all fields using default settings. */
  query_then_fetch = "query_then_fetch",
  
  /** Performs distributed frequency scoring before fetching results. */
  dfs_query_then_fetch = "dfs_query_then_fetch",
  
  /** Fetches results immediately without scoring optimization. */
  query_and_fetch = "query_and_fetch"
}
```

The compiler automatically extracts these descriptions and formats them as lists in the property documentation:

- `query_then_fetch`: Searches across all fields using default settings
- `dfs_query_then_fetch`: Performs distributed frequency scoring before fetching results
- `query_and_fetch`: Fetches results immediately without scoring optimization
:::

::::


## Add examples

Examples help users understand how to use your API with realistic request and response data. Well-written descriptions transform examples from code snippets into effective learning tools.

Here are some principles for effective examples:

- **Use realistic data:** Provide examples that reflect actual use cases rather than placeholder values
- **Write clear summaries:** Introduce the example with a very brief summary (<45 characters) that explains its purpose (reused as dropdown label in the docs)
- **Write clear descriptions:** Explain what the example accomplishes in more detail and why it's useful
- **Include edge cases:** Show how to handle optional parameters, the error conditions, and the effects of changing defaults
- **Point out key details:** Highlight important aspects users might miss
- **Show variations:** Demonstrate alternative approaches or related concepts
- **Provide realistic response bodies:** Each response body should have a realistic example. It must not contain any sensitive or confidential data
- **Include success responses:** Include at least one example for each success response (HTTP 200)

#### Generated examples

If you don't provide examples, Bump.sh automatically generates them from your API schema. Because it's hard to randomly generate meaningful examples, this has been disabled for Elasticsearch APIs.

It's preferable to include curated examples in your OpenAPI document with a realistic combination of property values. You can provide more than one example object in the examples field, so consider adding examples that reflect the most common use cases.

Bump.sh also generates a single curl example for each API. To override that generated example and optionally provide an equivalent Console or language-specific example, use the `x-codeSamples` extension described in [Custom code examples in Bump.sh](https://docs.bump.sh/help/specification-support/doc-code-samples).

:::{tip}
When you use validation tools to check your API specification, examples are helpful for ensuring that you haven't missed things like nullable data types.

Learn more:

- [The example object](https://spec.openapis.org/oas/latest#example-object)
- [Add examples](https://swagger.io/docs/specification/adding-examples)
:::

### Examples

::::{tab-set}
:group: implementations

:::{tab-item} OpenAPI
:sync: openapi

The OpenAPI specification supports examples in several ways:

**Individual parameter examples** can be defined directly in specifications:

```yaml
components:
  schemas:
    SearchRequest:
      type: object
      properties:
        department:
          type: string
          description: Filter employees by department
          example: "engineering"
        hireDate:
          type: string
          format: date
          description: Minimum hire date in ISO 8601 format
          example: "2020-01-01"
```

For more complex examples, OpenAPI provides the [Example Object](https://spec.openapis.org/oas/v3.0.3#example-object), which can be attached to request bodies, responses, or parameters.
:::

:::{tab-item} Elasticsearch
:sync: elasticsearch

**File-based examples** use a structured folder approach alongside your API specification:

```
/specification/your-api/examples/
  ├── request/
  │   ├── basic-search.yml
  │   └── advanced-filters.yml
  └── response/
      ├── success.yml
      └── error.yml
```

Each example file follows the [OpenAPI Example object specification](https://spec.openapis.org/oas/v3.0.3#example-object) in YAML format:

```yaml
summary: Search with filters
method_request: GET /employees/_search
description: >
  Combine multiple conditions using a bool query. This example finds employees 
  in the engineering department hired after 2020. Notice how the bool query's 
  "must" clause requires both conditions to match.
value: |-
  {
    "query": {
      "bool": {
        "must": [
          {"match": {"department": "engineering"}},
          {"range": {"hire_date": {"gte": "2020-01-01"}}}
        ]
      }
    }
  }
```

**Required fields:**
- `summary` - Brief label that appears in the docs
- `value` - The actual request/response body
- `method_request` - HTTP method and path (request examples only)

:::{warning}
For Elasticsearch APIs, you only need to provide Console examples. Examples for other programming languages (including cURL) are **generated automatically** and added to [docs/examples/languageExamples.json](https://github.com/elastic/elasticsearch-specification/blob/main/docs/examples/languageExamples.json).
:::
:::
:::

::::

## Add links

Links help users navigate between related APIs and find additional context in narrative documentation. Strategic linking improves discoverability and helps users understand how different operations work together.

Here are some principles for effective linking:

- **Link to prerequisite concepts:** Connect APIs to foundational concepts users need to understand first
- **Reference related operations:** Point to complementary APIs that users typically need together
- **Provide narrative context:** Link to guides that explain when and how to use the API effectively
- **Use descriptive link text:** Choose meaningful labels that indicate what users will find
- **Validate link targets:** Ensure links point to current, accurate documentation

### Examples

::::{tab-set}
:group: implementations

:::{tab-item} OpenAPI
:sync: openapi

Use the `externalDocs` field to link to narrative guides in the main Elastic documentation:

```yaml
paths:
  /search:
    post:
      summary: Search documents
      description: Execute a search query against one or more indices
      externalDocs:
        description: Try the hands-on Query DSL tutorial
        url: https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html
```

**Related operation links** can be referenced in descriptions using standard markdown:

```yaml
paths:
  /indices/{index}:
    put:
      summary: Create an index
      description: |
        Creates a new index with optional settings and mappings.
        See also: [Delete Index](delete-index) and [Update Index Sets](update-index-settings).
```
:::

:::{tab-item} Elasticsearch
:sync: elasticsearch

**External documentation links** use the `@ext_doc_id` annotation to connect to narrative guides. This is transformed into an OpenAPI `externalDocs` field in the [compilation process](./overview.md#example-elasticsearch):

```ts
/**
 * @variants container
 * @non_exhaustive
 * @ext_doc_id query-dsl
 */
export class QueryContainer {
  // ...
}
```

**API reference links** use the `@doc_id` annotation for language client generation and Console integration:

```ts
/**
 * @rest_spec_name indices.create
 * @doc_id indices-create-index
 */
export interface CreateIndexRequest extends RequestBase {
  // ...
}
```

Both annotations require corresponding entries in [`specification/_doc_ids/table.csv`](https://github.com/elastic/elasticsearch-specification/blob/main/specification/_doc_ids/table.csv):

:::{note}
Each endpoint can only have one `@ext_doc_id`. For multiple links, use inline markdown in descriptions.
:::
:::

::::

## Set default values

Default values can only be applied to optional parameters or properties in OpenAPI specifications using the `default` field. It's important to explain how changing these defaults affects the behavior of the API in the parameter description.

### Examples

::::{tab-set}
:group: implementations

:::{tab-item} OpenAPI
:sync: openapi

Specify defaults directly in schema definitions:

```yaml
components:
  schemas:
    SearchSettings:
      properties:
        size:
          type: integer
          default: 10
        timeout:
          type: string
          default: "1m"
```

For arrays:

```yaml
parameters:
  - name: fields
    in: query
    schema:
      type: array
      items:
        type: string
      default: ["id", "name", "created"]
```
:::

:::{tab-item} Elasticsearch
:sync: elasticsearch

Use the `@server_default` annotation for optional properties:

```ts
class Foo {
  /** @server_default "hello" */
  baz?: string
  
  /** @server_default ["hello", "world"] */
  tags?: string[]
}
```

:::{note}
Default values only work on optional properties and appear in parameter documentation without affecting client behavior.
:::
:::

::::

## Lint your API docs

Linting your API docs helps ensure consistency, correctness, and adherence to best practices. It catches common issues like missing descriptions, inconsistent naming, and formatting errors.

::::{tab-set}
:group: implementations
::::{tab-item} Elasticsearch
:sync: elasticsearch

The [Elasticsearch API specification](https://github.com/elastic/elasticsearch-specification/tree/main/docs/linters) uses the following linters with custom rules:

- **Spectral**: Configuration in `.spectral.yaml`
- **Redocly**: Configuration in `redocly.yaml`

Refer to [the Elasticsearch quickstart](./quickstart.md#lint-your-docs) to learn how to run the linter locally.

::::
::::
