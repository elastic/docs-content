---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/role-restriction.html
applies_to:
  stack: all
products:
  - id: elasticsearch
---

# Role restriction [role-restriction]

Role restriction can be used to specify conditions under which a role should be effective. When conditions are not met, the role will be disabled, which will result in access being denied. Not specifying restriction means the role is not restricted and thus always effective. This is the default behavior.

Currently, the role restriction is only supported for [API keys](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key), with limitation that the API key can only have a single role descriptor.


## Workflows [workflows-restriction]

Workflows allow to restrict the role to be effective exclusively when calling certain REST APIs. Calling a REST API that is not allowed by a workflow, will result in the role being disabled. The below section lists workflows that you can restrict the role to:

`search_application_query`
:   This workflow restricts the role to the [Search Application Search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search-application-search) only.

::::{note}
Workflow names are case-sensitive.
::::



### Examples [_examples_5]

The following example creates an API key with a restriction to the `search_application_query` workflow, which allows to call only [Search Application Search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search-application-search):

```console
POST /_security/api_key
{
  "name": "my-restricted-api-key",
  "role_descriptors": {
    "my-restricted-role-descriptor": {
      "indices": [
        {
          "names": ["my-search-app"],
          "privileges": ["read"]
        }
      ],
      "restriction":  {
        "workflows": ["search_application_query"]
      }
    }
  }
}
```


