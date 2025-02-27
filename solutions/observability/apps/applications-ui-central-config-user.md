---
navigation_title: "Create a central config user"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-app-central-config-user.html
---



# Applications UI central config user [apm-app-central-config-user]



## Central configuration manager [apm-app-central-config-manager]

Central configuration users need to be able to view, create, update, and delete APM agent configurations.

1. Create a new role, named something like `central-config-manager`, and assign the following privileges:

    ::::{tab-set}
    :group: datastreams-classic

    :::{tab-item} Data streams
    :sync: datastreams

    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | Index | `read` on `apm-agent-configuration` | Read-only access to `apm-agent-configuration` data |
    | Index | `view_index_metadata` on `apm-agent-configuration` | Read-only access to `apm-agent-configuration` index metadata |
    | Index | `read` on `logs-apm*` | Read-only access to `logs-apm*` data |
    | Index | `view_index_metadata` on `logs-apm*` | Read-only access to `logs-apm*` index metadata |
    | Index | `read` on `metrics-apm*` | Read-only access to `metrics-apm*` data |
    | Index | `view_index_metadata` on `metrics-apm*` | Read-only access to `metrics-apm*` index metadata |
    | Index | `read` on `traces-apm*` | Read-only access to `traces-apm*` data |
    | Index | `view_index_metadata` on `traces-apm*` | Read-only access to `traces-apm*` index metadata |

    :::

    :::{tab-item} Classic APM indices
    :sync: classic

    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | Index | `read` on `apm-*` | Read-only access to `apm-*` data |
    | Index | `view_index_metadata` on `apm-*` | Read-only access to `apm-*` index metadata |

    :::

    ::::

    ::::{tip}
    Using the deprecated APM Server binaries? Add the privileges under the **Classic APM indices** tab above.
    ::::

2. Assign the `central-config-manager` role created in the previous step, and the following Kibana feature privileges to anyone who needs to manage central configurations:

    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | Kibana | `All` on the APM and User Experience feature | Allow full use of the Applications and User Experience UIs |



## Central configuration reader [apm-app-central-config-reader]

In some instances, you may wish to create a user that can only read central configurations, but not create, update, or delete them.

1. Create a new role, named something like `central-config-reader`, and assign the following privileges:

    ::::{tab-set}
    :group: datastreams-classic

    :::{tab-item} Data streams
    :sync: datastreams

    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | Index | `read` on `apm-agent-configuration` | Read-only access to `apm-agent-configuration` data |
    | Index | `view_index_metadata` on `apm-agent-configuration` | Read-only access to `apm-agent-configuration` index metadata |
    | Index | `read` on `logs-apm*` | Read-only access to `logs-apm*` data |
    | Index | `view_index_metadata` on `logs-apm*` | Read-only access to `logs-apm*` index metadata |
    | Index | `read` on `metrics-apm*` | Read-only access to `metrics-apm*` data |
    | Index | `view_index_metadata` on `metrics-apm*` | Read-only access to `metrics-apm*` index metadata |
    | Index | `read` on `traces-apm*` | Read-only access to `traces-apm*` data |
    | Index | `view_index_metadata` on `traces-apm*` | Read-only access to `traces-apm*` index metadata |

    :::

    :::{tab-item} Classic APM indices
    :sync: classic

    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | Index | `read` on `apm-*` | Read-only access to `apm-*` data |
    | Index | `view_index_metadata` on `apm-*` | Read-only access to `apm-*` index metadata |

    :::

    ::::

    ::::{tip}
    Using the deprecated APM Server binaries? Add the privileges under the **Classic APM indices** tab above.
    ::::

2. Assign the `central-config-reader` role created in the previous step, and the following Kibana feature privileges to anyone who needs to read central configurations:

    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | Kibana | `read` on the APM and User Experience feature | Allow read access to the Applications and User Experience UIs |



## Central configuration API [apm-app-central-config-api]

See [Create an API user](applications-ui-api-user.md).
