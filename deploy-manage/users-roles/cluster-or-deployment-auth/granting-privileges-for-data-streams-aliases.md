---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/securing-aliases.html
---

# Granting privileges for data streams and aliases [securing-aliases]

{{es}} {{security-features}} allow you to secure operations executed against [data streams](../../../manage-data/data-store/index-types/data-streams.md) and [aliases](../../../manage-data/data-store/aliases.md).

## Data stream privileges [data-stream-privileges]

Use [index privileges](elasticsearch-privileges.md#privileges-list-indices) to control access to a data stream. Granting privileges on a data stream grants the same privileges on its backing indices.

For example, `my-data-stream` consists of two backing indices: `.ds-my-data-stream-2099.03.07-000001` and `.ds-my-data-stream-2099.03.08-000002`.

A user is granted the `read` privilege to `my-data-stream`.

```js
{
  "names" : [ "my-data-stream" ],
  "privileges" : [ "read" ]
}
```

Because the user is automatically granted the same privileges to the stream’s backing indices, the user can retrieve a document directly from `.ds-my-data-stream-2099.03.08-000002`:

```console
GET .ds-my-data-stream-2099.03.08-000002/_doc/2
```

Later `my-data-stream` [rolls over](../../../manage-data/data-store/index-types/use-data-stream.md#manually-roll-over-a-data-stream). This creates a new backing index: `.ds-my-data-stream-2099.03.09-000003`. Because the user still has the `read` privilege for `my-data-stream`, the user can retrieve documents directly from `.ds-my-data-stream-2099.03.09-000003`:

```console
GET .ds-my-data-stream-2099.03.09-000003/_doc/2
```


## Alias privileges [index-alias-privileges]

Use [index privileges](elasticsearch-privileges.md#privileges-list-indices) to control access to an [alias](../../../manage-data/data-store/aliases.md). Privileges on an index or data stream do not grant privileges on its aliases. For information about managing aliases, see [*Aliases*](../../../manage-data/data-store/aliases.md).

::::{important} 
Don’t use [filtered aliases](../../../manage-data/data-store/aliases.md#filter-alias) in place of [document level security](controlling-access-at-document-field-level.md). {{es}} doesn’t always apply alias filters.
::::


For example, the `current_year` alias points only to the `2015` index. A user is granted the `read` privilege for the `2015` index.

```js
{
  "names" : [ "2015" ],
  "privileges" : [ "read" ]
}
```

When the user attempts to retrieve a document from the `current_year` alias, {{es}} rejects the request.

```console
GET current_year/_doc/1
```

To retrieve documents from `current_year`, the user must have the `read` index privilege for the alias.

```js
{
  "names" : [ "current_year" ],
  "privileges" : [ "read" ]
}
```


