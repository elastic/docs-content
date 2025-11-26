---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/kibana-privileges.html
applies_to:
  stack: all
products:
  - id: kibana
---

# {{kib}} privileges [kibana-privileges]

{{kib}} privileges grant users access to features within {{kib}}. Roles have privileges to determine whether users have write or read access.

To learn how to assign privileges to a role, refer to [](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md).

## Base privileges [_base_privileges]

Assigning a base privilege grants access to all {{kib}} features, such as **Discover**, **Dashboard**, **Visualize Library**, and **Canvas**.

$$$kibana-privileges-all$$$

`all`
:   Grants full read-write access.

`read`
:   Grants read-only access.

### Assigning base privileges [_assigning_base_privileges]

From the role management screen:

:::{image} /deploy-manage/images/kibana-assign-base-privilege.png
:alt: Assign base privilege
:screenshot:
:::

Using the [role APIs](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-roles):

```js
PUT /api/security/role/my_kibana_role
{
  "elasticsearch": {
    "cluster" : [ ],
    "indices" : [ ]
  },
  "kibana": [
    {
      "base": ["all"],
      "feature": {},
      "spaces": ["marketing"]
    }
  ]
}
```



## Feature privileges [kibana-feature-privileges]

Assigning a feature privilege grants access to a specific feature.

`all`
:   Grants full read-write access.

`read`
:   Grants read-only access.

### Sub-feature privileges [_sub_feature_privileges]

Some features allow for finer access control than the `all` and `read` privileges. This additional level of control is a [subscription feature](https://www.elastic.co/subscriptions).


### Assigning feature privileges [_assigning_feature_privileges]

From the role management screen:

:::{image} /deploy-manage/images/kibana-assign-subfeature-privilege.png
:alt: Assign feature privilege
:screenshot:
:::

Using the [role APIs](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-roles):

```js
PUT /api/security/role/my_kibana_role
{
  "elasticsearch": {
    "cluster" : [ ],
    "indices" : [ ]
  },
  "kibana": [
    {
      "base": [],
      "feature": {
        "visualize_v2": ["all"],
        "dashboard_v2": ["read", "url_create"]
      },
      "spaces": ["marketing"]
    }
  ]
}
```



