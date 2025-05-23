---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/anonymous-access.html
applies_to:
  deployment:
    ess:
    ece:
    eck:
    self:
products:
  - id: elasticsearch
---

# Anonymous access [anonymous-access]

::::{tip} 
To embed {{kib}} dashboards or grant access to {{kib}} without requiring credentials, use {{kib}}'s [anonymous authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-authentication.md) feature instead.
::::


Incoming requests to {{es}} are considered to be *anonymous* if no authentication token can be extracted from the incoming request. By default, anonymous requests are rejected and an authentication error is returned (status code `401`).

To enable anonymous access, you assign one or more roles to anonymous users in the [`elasticsearch.yml`](/deploy-manage/stack-settings.md) configuration file. For example, the following configuration assigns anonymous users `role1` and `role2`:

```yaml
xpack.security.authc:
  anonymous:
    username: anonymous_user <1>
    roles: role1, role2 <2>
    authz_exception: true <3>
```

1. The username/principal of the anonymous user. Defaults to `_es_anonymous_user` if not specified.
2. The roles to associate with the anonymous user. If no roles are specified, anonymous access is disabled—anonymous requests will be rejected and return an authentication error.
3. When `true`, a 403 HTTP status code is returned if the anonymous user does not have the permissions needed to perform the requested action and the user will NOT be prompted to provide credentials to access the requested resource. When `false`, a 401 HTTP status code is returned if the anonymous user does not have the necessary permissions and the user is prompted for credentials to access the requested resource. If you are using anonymous access in combination with HTTP, you might need to set `authz_exception` to `false` if your client does not support preemptive basic authentication. Defaults to `true`.


