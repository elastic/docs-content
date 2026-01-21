---
navigation_title: Create an API user
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-app-api-user.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# Applications UI API user [apm-app-api-user]

## Central configuration API [apm-app-api-config-manager]

Users can list, search, create, update, and delete central configurations via the Applications UI API.

1. Assign the following Kibana feature privileges:

    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | Kibana | `all` on the APM and User Experience feature | Allow all access to the Applications and User Experience UIs |

## Central configuration API reader [apm-app-api-config-reader]

Sometimes a user only needs to list and search central configurations via the Applications UI API.

1. Assign the following Kibana feature privileges:

    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | Kibana | `read` on the APM and User Experience feature | Allow read access to the Applications and User Experience UIs |

## Annotation API [apm-app-api-annotation-manager]

Users can use the annotation API to create annotations on their APM data.

1. Create a new role, named something like `annotation_role`, and assign the following privileges:

    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | Index | `manage` on `observability-annotations` index | Check if the `observability-annotations` index exists |
    | Index | `read` on `observability-annotations` index | Read the `observability-annotations` index |
    | Index | `create_index` on `observability-annotations` index | Create the `observability-annotations` index |
    | Index | `create_doc` on `observability-annotations` index | Create new annotations in the `observability-annotations` index |

2. Assign the `annotation_role` created previously, and the following Kibana feature privileges to any annotation API users:

    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | Kibana | `all` on the APM and User Experience feature | Allow all access to the Applications and User Experience UIs |

