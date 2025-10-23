---
navigation_title: Checklist
---

# API docs checklist

Use this checklist to verify the quality, completeness, and consistency of your API docs contributions.

## Structure, organization, and metadata
- Include required [OpenAPI document info](./organize-annotate.md#add-open-api-document-info)
- Include [OpenAPI specification version](./organize-annotate.md#add-openapi-specification-version)
- Define unique [operation identifiers](./organize-annotate.md#add-operation-identifiers) using camelCase
- Use consistent [tags](./organize-annotate.md#group-apis-with-tags) to group related operations
- Document [API lifecycle status](./organize-annotate.md#specify-api-lifecycle-status) (availability, stability, version information)
- Mark deprecated APIs and properties with appropriate notices
- Document [required permissions](./organize-annotate.md#document-required-permissions) for each operation

## Content quality and completeness

- Write clear [summaries](./guidelines.md#write-summaries) (between 5-45 characters)
- Write detailed [descriptions](./guidelines.md#write-descriptions) for operations, parameters, properties, tags etc.
- Document all [parameters](./guidelines.md#document-parameters) and explain how changing defaults affects behavior
- Provide descriptions for non-obvious [enum values](./guidelines.md#document-enum-values)
- Specify [default values](./guidelines.md#set-default-values) for optional parameters
- Include realistic [examples](./guidelines.md#add-examples) with helpful descriptions
- Add [links](./guidelines.md#add-links) to related operations and documentation

## Quality assurance

- Preview your changes locally before submitting (see [Contribute locally: Elasticsearch quickstart](./quickstart.md))
- [Lint your API docs](./guidelines.md#lint-your-api-docs) to identify and fix issues
- Check all links to ensure they work correctly
- Ensure examples are realistic and error-free