---
navigation_title: "Create an APM reader user"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-app-reader.html
---



# APM reader user [apm-app-reader]


APM reader users typically need to view the Applications UI and dashboards and visualizations that use APM data. These users might also need to create and edit dashboards, visualizations, and machine learning jobs.


## APM reader [apm-app-reader-full] 

To create an APM reader user:

1. Create a new role, named something like `read-apm`, and assign the following privileges:

    <div class="tabs" data-tab-group="apm-app-reader">
      <div role="tablist" aria-label="Applications UI reader">
        <button role="tab"
              aria-selected="true"
              aria-controls="data-streams-tab"
              id="data-streams">
          Data streams
        </button>
        <button role="tab"
                aria-selected="false"
                aria-controls="classic-indices-tab"
                id="classic-indices"
                tabindex="-1">
          Classic APM indices
        </button>
      </div>
      <div tabindex="0"
           role="tabpanel"
           id="data-streams-tab"
           aria-labelledby="data-streams">
    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | Index | `read` on `logs-apm*` | Read-only access to `logs-apm*` data |
    | Index | `view_index_metadata` on `logs-apm*` | Read-only access to `logs-apm*` index metadata |
    | Index | `read` on `metrics-apm*` | Read-only access to `metrics-apm*` data |
    | Index | `view_index_metadata` on `metrics-apm*` | Read-only access to `metrics-apm*` index metadata |
    | Index | `read` on `traces-apm*` | Read-only access to `traces-apm*` data |
    | Index | `view_index_metadata` on `traces-apm*` | Read-only access to `traces-apm*` index metadata |

      </div>
      <div tabindex="0"
           role="tabpanel"
           id="classic-indices-tab"
           aria-labelledby="classic-indices"
           hidden="">
    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | Index | `read` on `apm-*` | Read-only access to `apm-*` data |
    | Index | `view_index_metadata` on `apm-*` | Read-only access to `apm-*` index metadata |

      </div>
    </div>

2. Assign the `read-apm` role created in the previous step, and the following built-in roles to any APM reader users:

    | Role | Purpose |
    | --- | --- |
    | `kibana_admin` | Grants access to all features in Kibana. |
    | `machine_learning_admin` | Grants the privileges required to create, update, and view machine learning jobs |



## Partial APM reader [apm-app-reader-partial] 

In some instances, you may wish to restrict certain Kibana apps that a user has access to.

1. Create a new role, named something like `read-apm-partial`, and assign the following privileges:

    <div class="tabs" data-tab-group="apm-app-reader">
      <div role="tablist" aria-label="Applications UI reader">
        <button role="tab"
              aria-selected="true"
              aria-controls="data-streams-tab"
              id="data-streams">
          Data streams
        </button>
        <button role="tab"
                aria-selected="false"
                aria-controls="classic-indices-tab"
                id="classic-indices"
                tabindex="-1">
          Classic APM indices
        </button>
      </div>
      <div tabindex="0"
           role="tabpanel"
           id="data-streams-tab"
           aria-labelledby="data-streams">
    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | Index | `read` on `logs-apm*` | Read-only access to `logs-apm*` data |
    | Index | `view_index_metadata` on `logs-apm*` | Read-only access to `logs-apm*` index metadata |
    | Index | `read` on `metrics-apm*` | Read-only access to `metrics-apm*` data |
    | Index | `view_index_metadata` on `metrics-apm*` | Read-only access to `metrics-apm*` index metadata |
    | Index | `read` on `traces-apm*` | Read-only access to `traces-apm*` data |
    | Index | `view_index_metadata` on `traces-apm*` | Read-only access to `traces-apm*` index metadata |

      </div>
      <div tabindex="0"
           role="tabpanel"
           id="classic-indices-tab"
           aria-labelledby="classic-indices"
           hidden="">
    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | Index | `read` on `apm-*` | Read-only access to `apm-*` data |
    | Index | `view_index_metadata` on `apm-*` | Read-only access to `apm-*` index metadata |

      </div>
    </div>

2. Assign feature privileges to any Kibana feature that the user needs access to. Here are two examples:

    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | Kibana | `Read` or `All` on the APM and User Experience feature | Allow the use of the the Applications and User Experience UIs |
    | Kibana | `Read` or `All` on Dashboards and Discover | Allow the user to view, edit, and create dashboards, as well as browse data. |

3. Finally, assign the following role if a user needs to enable and edit machine learning features:

    | Role | Purpose |
    | --- | --- |
    | `machine_learning_admin` | Grants the privileges required to create, update, and view machine learning jobs |


