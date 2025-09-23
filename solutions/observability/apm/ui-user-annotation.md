---
navigation_title: Create an annotation user
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-app-annotation-user-create.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# Applications UI annotation user [apm-app-annotation-user-create]

::::{note}
By default, the `viewer` and `editor` built-in roles provide read access to Observability annotations. You only need to create an annotation user to write to the annotations index ([`xpack.observability.annotations.index`](kibana://reference/configuration-reference/apm-settings.md)).
::::

## Annotation user [apm-app-annotation-user]

View deployment annotations in the Applications UI.

1. Create a new role, named something like `annotation_user`, and assign the following privileges:

    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | Index | `read` on `{{ANNOTATION_INDEX}}`1 | Read-only access to the observability annotation index |
    | Index | `view_index_metadata` on `{{ANNOTATION_INDEX}}`1 | Read-only access to observability annotation index metadata |

    1 `{{ANNOTATION_INDEX}}` should be the index name you’ve defined in [`xpack.observability.annotations.index`](kibana://reference/configuration-reference/apm-settings.md).

2. Assign the `annotation_user` created previously, and the roles and privileges necessary to create a [full](/solutions/observability/apm/ui-user-reader.md#apm-app-reader-full) or [partial](/solutions/observability/apm/ui-user-reader.md#apm-app-reader-partial) APM reader to any users that need to view annotations in the Applications UI

## Annotation API [apm-app-annotation-api]

See [Create an API user](/solutions/observability/apm/ui-user-api.md).

