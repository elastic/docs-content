---
navigation_title: Submit requests on behalf of other users
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/run-as-privilege.html
applies_to:
  deployment:
    ece:
    eck:
    ess:
    self:
products:
  - id: elasticsearch
---

# Submitting requests on behalf of other users [run-as-privilege]

{{es}} roles support a `run_as` privilege that enables an authenticated user to submit requests on behalf of other users. For example, if your external application is trusted to authenticate users, {{es}} can authenticate the external application and use the *run as* mechanism to issue authorized requests as other users without having to re-authenticate each user.

To "run as" (impersonate) another user, the first user (the authenticating user) must be authenticated by a mechanism that supports run-as delegation. The second user (the `run_as` user) must be authorized by a mechanism that supports delegated run-as lookups by username.

The `run_as` privilege essentially operates like a secondary form of [delegated authorization](realm-chains.md#authorization_realms). Delegated authorization applies to the authenticating user, and the `run_as` privilege applies to the user who is being impersonated.

## Authenticating user

For the authenticating user, the following realms (plus API keys) all support `run_as` delegation: [native](/deploy-manage/users-roles/cluster-or-deployment-auth/native.md), [file](/deploy-manage/users-roles/cluster-or-deployment-auth/file-based.md), [Active Directory](/deploy-manage/users-roles/cluster-or-deployment-auth/active-directory.md), [JWT](/deploy-manage/users-roles/cluster-or-deployment-auth/jwt.md), [Kerberos](/deploy-manage/users-roles/cluster-or-deployment-auth/kerberos.md), [LDAP](/deploy-manage/users-roles/cluster-or-deployment-auth/ldap.md), and [PKI](/deploy-manage/users-roles/cluster-or-deployment-auth/pki.md).

Service tokens, the {{es}} token service, SAML, and OIDC do not support `run_as` delegation.

## `run_as` user

{{es}} supports `run_as` for any realm that supports user lookup. Not all realms support user lookup. Refer to the list of [supported realms](looking-up-users-without-authentication.md) and ensure that the realm you wish to use is configured in a manner that supports user lookup.

The `run_as` user must be retrieved from a [realm](authentication-realms.md) - it is not possible to run as a [service account](service-accounts.md), [API key](token-based-authentication-services.md#token-authentication-api-key) or [access token](token-based-authentication-services.md#token-authentication-access-token).

To submit requests on behalf of other users, you need to have the `run_as` privilege in your [roles](defining-roles.md). For example, the following request creates a `my_director` role that grants permission to submit request on behalf of `jacknich` or `redeniro`:

```console
POST /_security/role/my_director?refresh=true
{
  "cluster": ["manage"],
  "indices": [
    {
      "names": [ "index1", "index2" ],
      "privileges": [ "manage" ]
    }
  ],
  "run_as": [ "jacknich", "rdeniro" ],
  "metadata" : {
    "version" : 1
  }
}
```

To submit a request as another user, you specify the user in the `es-security-runas-user` request header. For example:

```sh
curl -H "es-security-runas-user: jacknich" -u es-admin -X GET http://localhost:9200/
```

The `run_as` user passed in through the `es-security-runas-user` header must be available from a realm that supports delegated authorization lookup by username. Realms that don’t support user lookup can’t be used by `run_as` delegation from other realms.

For example, JWT realms can authenticate external users specified in JWTs, and execute requests as a `run_as` user in the `native` realm. {{es}} will retrieve the indicated `runas` user and execute the request as that user using their roles.

## Apply the `run_as` privilege to roles [run-as-privilege-apply]

You can apply the `run_as` privilege when creating roles with the [role management API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role), or using the [role management UI](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) in {{kib}}. Users who are assigned a role that contains the `run_as` privilege inherit all privileges from their role, and can also submit requests on behalf of the indicated users.

::::{note} 
Roles for the authenticated user and the `run_as` user are not merged. If a user authenticates without specifying the `run_as` parameter, only the authenticated user’s roles are used. If a user authenticates and their roles include the `run_as` parameter, only the `run_as` user’s roles are used.
::::

After a user successfully authenticates to {{es}}, an authorization process determines whether the user behind an incoming request is allowed to run that request. If the authenticated user has the `run_as` privilege in their list of permissions and specifies the run-as header, {{es}} *discards* the authenticated user and associated roles. It then looks in each of the configured realms in the realm chain until it finds the username that’s associated with the `run_as` user, and uses those roles to execute any requests.

### Example

Consider an admin role and an analyst role. The admin role has higher privileges, but might also want to submit requests as another user to test and verify their permissions.

This example uses the role management API, but a similar configuration can be set up using the [Create users](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) and [Users](/deploy-manage/users-roles/cluster-or-deployment-auth/native.md#managing-native-users) pages in {{kib}}. 

1.  Create an admin role named `my_admin_role`. This role has `manage` [privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md) on the entire cluster, and on a subset of indices. This role also contains the `run_as` privilege, which enables any user with this role to submit requests on behalf of the specified `analyst_user`.

    You can set up a similar role using the [role management UI](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) in {{kib}} by selecting an `analyst_user` from the **Run As privileges** dropdown menu in the **Elasticsearch** section.

    ```console
    POST /_security/role/my_admin_role?refresh=true
    {
      "cluster": ["manage"],
      "indices": [
        {
          "names": [ "index1", "index2" ],
          "privileges": [ "manage" ]
        }
      ],
      "applications": [
        {
          "application": "myapp",
          "privileges": [ "admin", "read" ],
          "resources": [ "*" ]
        }
      ],
      "run_as": [ "analyst_user" ],
      "metadata" : {
        "version" : 1
      }
    }
    ```

2. Create an analyst role named `my_analyst_role`, which has more restricted `monitor` cluster privileges and `manage` privileges on a subset of indices.

    ```console
    POST /_security/role/my_analyst_role?refresh=true
    {
      "cluster": [ "monitor"],
      "indices": [
        {
          "names": [ "index1", "index2" ],
          "privileges": ["manage"]
        }
      ],
      "applications": [
        {
          "application": "myapp",
          "privileges": [ "read" ],
          "resources": [ "*" ]
        }
      ],
      "metadata" : {
        "version" : 1
      }
    }
    ```

3. Create an administrator user and assign them the role named `my_admin_role`, which allows this user to submit requests as the `analyst_user`.

      ```console
      POST /_security/user/admin_user?refresh=true
      {
        "password": "l0ng-r4nd0m-p@ssw0rd",
        "roles": [ "my_admin_role" ],
        "full_name": "Eirian Zola",
        "metadata": { "intelligence" : 7}
      }
      ```

4. Create an analyst user and assign them the role named `my_analyst_role`.

      ```console
      POST /_security/user/analyst_user?refresh=true
      {
        "password": "l0nger-r4nd0mer-p@ssw0rd",
        "roles": [ "my_analyst_role" ],
        "full_name": "Monday Jaffe",
        "metadata": { "innovation" : 8}
      }
      ```

5. You can then authenticate to {{es}} as the `admin_user` or `analyst_user`. However, the `admin_user` could optionally submit requests on behalf of the `analyst_user`. 
   
    The following request authenticates to {{es}} with a `Basic` authorization token and submits the request as the `analyst_user`:

    ```sh
    curl -s -X GET -H "Authorization: Basic YWRtaW5fdXNlcjpsMG5nLXI0bmQwbS1wQHNzdzByZA==" -H "es-security-runas-user: analyst_user" https://localhost:9200/_security/_authenticate
    ```

    The response indicates that the `analyst_user` submitted this request, using the `my_analyst_role` that’s assigned to that user. When the `admin_user` submitted the request, {{es}} authenticated that user, discarded their roles, and then used the roles of the `run_as` user.

    ```sh
    {"username":"analyst_user","roles":["my_analyst_role"],"full_name":"Monday Jaffe","email":null,
    "metadata":{"innovation":8},"enabled":true,"authentication_realm":{"name":"native",
    "type":"native"},"lookup_realm":{"name":"native","type":"native"},"authentication_type":"realm"}
    %
    ```

    The `authentication_realm` and `lookup_realm` in the response both specify the `native` realm because both the `admin_user` and `analyst_user` are from that realm. If the two users are in different realms, the values for `authentication_realm` and `lookup_realm` are different (such as `pki` and `native`).
