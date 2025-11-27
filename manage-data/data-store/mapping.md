---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-mapper.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Mapping

% What needs to be done: Refine

% GitHub issue: docs-projects#370

% Scope notes: Use the content in the linked source and add links to the relevent reference content.

% Use migrated content from existing pages that map to this page:

% - [x] ./raw-migrated-files/elasticsearch/elasticsearch-reference/mapping.md
% - [x] ./raw-migrated-files/elasticsearch/elasticsearch-reference/index-modules-mapper.md
%      Notes: redirect only

% Internal links rely on the following IDs being on this page (for example, as a heading ID, paragraph ID, and so on):

$$$mapping-limit-settings$$$

$$$updating-field-mappings$$$

$$$mapping-manage-update$$$

$$$mapping-dynamic$$$

$$$mapping-explicit$$$

Mapping is the process of defining how a document and the fields it contains are stored and indexed.

Each document is a collection of fields, which each have their own [data type](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md). When mapping your data, you create a mapping definition, which contains a list of fields that are pertinent to the document. A mapping definition also includes [metadata fields](elasticsearch://reference/elasticsearch/mapping-reference/document-metadata-fields.md), like the `_source` field, which customize how a document’s associated metadata is handled.

Depending on where you are in your data journey, use *dynamic mapping* and *explicit mapping* to define your data. For example, you can explicitly map fields where you don’t want to use the defaults, or to gain greater control over which fields are created. Then you can allow {{es}} to dynamically map other fields. Using a combination of dynamic and explicit mapping on the same index is especially useful when you have a mix of known and unknown fields in your data.

::::{note}
Before 7.0.0, the mapping definition included a type name. {{es}} 7.0.0 and later no longer accept a default mapping. [Removal of mapping types](/manage-data/data-store/mapping/removal-of-mapping-types.md) provides more information.
::::

## Dynamic mapping [mapping-dynamic]

When you use [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md), {{es}} automatically detects the data types of fields in your documents and creates mappings for you. If you index additional documents with new fields, {{es}} will add these fields automatically. You can add fields to the top-level mapping, and to inner [`object`](elasticsearch://reference/elasticsearch/mapping-reference/object.md) and [`nested`](elasticsearch://reference/elasticsearch/mapping-reference/nested.md) fields. Dynamic mapping helps you get started quickly, but might yield suboptimal results for your specific use case due to automatic field type inference.

Use [dynamic templates](/manage-data/data-store/mapping/dynamic-templates.md) to define custom mappings that are applied to dynamically added fields based on the matching condition.

## Explicit mapping [mapping-explicit]

Use [explicit mapping](/manage-data/data-store/mapping/explicit-mapping.md) to define mappings by specifying data types for each field. This is recommended for production use cases, because you have full control over how your data is indexed to suit your specific use case.

Defining your own mappings enables you to:

* Define which string fields should be treated as full-text fields.
* Define which text field can be automatically vectorized by a semantic search machine learning model. 
* Define which fields contain numbers, dates, or geolocations.
* Use data types that cannot be automatically detected (such as `geo_point` and `geo_shape`.)
* Choose date value [formats](elasticsearch://reference/elasticsearch/mapping-reference/mapping-date-format.md), including custom date formats.
* Create custom rules to control the mapping for [dynamically added fields](/manage-data/data-store/mapping/dynamic-mapping.md).
* Optimize fields for partial matching.
* Perform language-specific text analysis.

::::{tip}
It’s often useful to index the same field in different ways for different purposes. For example, you might want to index a string field as both a text field for full-text search and as a keyword field for sorting or aggregating your data. Or, you might choose to use more than one language analyzer to process the contents of a string field that contains user input.

::::

## Runtime fields [runtime-fields]

Use [runtime fields](/manage-data/data-store/mapping/runtime-fields.md) to make schema changes without reindexing. You can use runtime fields in conjunction with indexed fields to balance resource usage and performance. Your index will be smaller, but with slower search performance.

::::{admonition} Experiment with mapping options
[Define runtime fields in a search request](/manage-data/data-store/mapping/define-runtime-fields-in-search-request.md) to experiment with different mapping options, and also fix mistakes in your index mapping values by overriding values in the mapping during the search request.
::::

## Manage and update mappings [mapping-manage-update]

Explicit mappings should be defined at index creation for fields you know in advance. You can still add new fields to mappings at any time, as your data evolves.

Use the [Update mapping API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-mapping) to update an existing mapping.

In most cases, you can’t change mappings for fields that are already mapped. These changes require [reindexing](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex).

However, you can update mappings under certain conditions:

* You can add new fields to an existing mapping at any time, dynamically or explicitly.
* You can add new [multi-fields](elasticsearch://reference/elasticsearch/mapping-reference/multi-fields.md) for existing fields.

    * Documents indexed before the mapping update will not have values for the new multi-fields until they are updated or reindexed. Documents indexed after the mapping change will automatically have values for the new multi-fields.

* Some [mapping parameters](elasticsearch://reference/elasticsearch/mapping-reference/mapping-parameters.md) can be updated for existing fields of certain [data types](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md).


## Prevent mapping explosions [mapping-limit-settings]

Defining too many fields in an index can lead to a mapping explosion, which can cause out of memory errors and difficult situations from which to recover.

Consider a situation where every new document inserted introduces new fields, such as with [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md). Each new field is added to the index mapping, which can become a problem as the mapping grows.

Use the [mapping limit settings](elasticsearch://reference/elasticsearch/index-settings/mapping-limit.md) to limit the number of field mappings (created manually or dynamically) and prevent documents from causing a mapping explosion.
