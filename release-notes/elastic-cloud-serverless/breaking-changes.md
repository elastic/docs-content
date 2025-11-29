---
navigation_title: Breaking changes
products:
  - id: cloud-serverless
---

# {{serverless-full}} breaking changes [elastic-cloud-serverless-breaking-changes]

## October 27, 2025 [serverless-changelog-10272025-breaking]

:::{dropdown} Implement native synthetic source for normalized keywords

This adds a new mapping parameter `normalizer_skip_store_original_value` to keyword fields. When this parameter is set and `synthetic_source` is enabled, keyword fields with configured normalizers will not store the original non-normalized value in `_ignored_source` and will instead use the normalized value to reconstruct the source.
This parameter enabled by default for the built-in `lowercase` normalizer and is disabled by default for other custom normalizers.

**Impact:**

Keyword fields using the `lowercase` normalizer will return the normalized value in the source when synthetic source is enabled.

For more information, view [#136915](https://github.com/elastic/elasticsearch/pull/136915).
:::



## August 25, 2025 [elastic-cloud-serverless-08252025-breaking]

* Allows partial results by default in {{esql}} [#125060](https://github.com/elastic/elasticsearch/pull/125060)
:::{dropdown} Don't enable norms for fields of type text when the index mode is LogsDB or TSDB

This changes the default behavior for norms on `text` fields in logsdb and tsdb indices.
Prior to this change, norms were enabled by default, with the option to disable them via manual configurations.
After this change, norms will be disabled by default.
Note, because we dont support enabling norms from a disabled state, users will not be able to enable norms on `text` fields in logsdb and tsdb indices.

**Impact:**

Text fields will no longer be normalized by default in LogsDB and TSDB indicies.
  
For more information, view [#131317](https://github.com/elastic/elasticsearch/pull/131317).

## August 11, 2025 [elastic-cloud-serverless-08112025-breaking]

* Improves advanced settings management APIs privilege checks [#230067]({{kib-pull}}230067)

## June 23, 2025 [serverless-changelog-06232025]

* {{esql}}: Disallows mixed quoted/unquoted patterns in `FROM` commands [#127636]({{es-pull}}127636)
