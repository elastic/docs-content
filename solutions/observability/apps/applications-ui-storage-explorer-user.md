---
navigation_title: "Create a storage explorer user"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-app-storage-explorer-user-create.html
---



# Applications UI storage explorer user [apm-app-storage-explorer-user-create]



## Storage Explorer user [apm-app-storage-explorer-user]

View the **Storage Explorer** in the Applications UI.

1. Create a new role, named something like `storage-explorer_user`, and assign the following privileges:

    ::::{tab-set}
    :group: datastreams-classic

    :::{tab-item} Data streams
    :sync: datastreams

    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | Cluster | `monitor` | Monitor the disk space used by APM data streams |
    | Index | `monitor` on `logs-apm*` | Monitor access to `logs-apm*` for storage explorer |
    | Index | `monitor` on `metrics-apm*` | Monitor access to `metrics-apm*` for storage explorer |
    | Index | `monitor` on `traces-apm*` | Monitor access to `traces-apm*` for storage explorer |

    :::

    :::{tab-item} Classic APM indices
    :sync: classic

    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | Cluster | `monitor` | Monitor the disk space used by APM indices |
    | Index | `monitor` on `apm-*` | Monitor access to `apm-*` for storage explorer |

    :::

    ::::

2. Assign the `storage-explorer_user` created previously, and the roles and privileges necessary to create a [full](apm-reader-user.md#apm-app-reader-full) or [partial](apm-reader-user.md#apm-app-reader-partial) APM reader to any users that need to view **Storage Explorer** in the Applications UI.
