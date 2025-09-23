---
navigation_title: ECK managed credentials
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-users-and-roles.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-rotate-credentials.html
applies_to:
  deployment:
    eck:
products:
  - id: cloud-kubernetes
---

# {{eck}} managed credentials

When deploying an {{stack}} application, the operator generates a set of credentials essential for the operation of that application. For example, these generated credentials include the default `elastic` user for {{es}} and the security token for APM Server.

To list all auto-generated credentials in a namespace, run the following command:

```sh
kubectl get secret -l eck.k8s.elastic.co/credentials=true
```

## Default elastic user [k8s-default-elastic-user]

When the {{es}} resource is created, a default user named `elastic` is created automatically, and is assigned the `superuser` role.

Its password can be retrieved in a Kubernetes secret, whose name is based on the {{es}} resource name: `<elasticsearch-name>-es-elastic-user`.

For example, the password of the `elastic` user for an {{es}} cluster named `quickstart` can be retrieved with:

```sh
kubectl get secret quickstart-es-elastic-user -o go-template='{{.data.elastic | base64decode}}'
```

### Disabling the default `elastic` user [k8s_disabling_the_default_elastic_user]

If your prefer to manage all users via SSO, for example using [SAML Authentication](../../../deploy-manage/users-roles/cluster-or-deployment-auth/saml.md) or OpenID Connect, you can disable the default `elastic` superuser by setting the `auth.disableElasticUser` field in the {{es}} resource to `true`:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch-sample
spec:
  version: {{version.stack}}
  auth:
    disableElasticUser: true
  nodeSets:
  - name: default
    count: 1
```

## Rotate auto-generated credentials [k8s-rotate-credentials]

You can force the auto-generated credentials to be regenerated with new values by deleting the appropriate Secret. For example, to change the password for the `elastic` user from the [quickstart example](/deploy-manage/deploy/cloud-on-k8s/elasticsearch-deployment-quickstart.md), use the following command:

```sh
kubectl delete secret quickstart-es-elastic-user
```

::::{warning}
If you are using the `elastic` user credentials in your own applications, they will fail to connect to {{es}} and {{kib}} after you run this command. It is not recommended to use `elastic` user credentials for production use cases. Always [create your own users with restricted roles](../../../deploy-manage/users-roles/cluster-or-deployment-auth/native.md) to access {{es}}.
::::


To regenerate all auto-generated credentials in a namespace, run the following command:

```sh
kubectl delete secret -l eck.k8s.elastic.co/credentials=true
```

::::{warning}
This command regenerates auto-generated credentials of **all** {{stack}} applications in the namespace.
::::

## Creating custom users

{{eck}} provides functionality to facilitate custom user creation through various authentication realms. You can create users using the native realm, file realm, or external authentication methods.

### File realm

ECK supports creating users through Kubernetes secrets referenced in the {{es}} resource. These secrets can contain either file realm content or standard authentication credentials with a username and password.

For more information, refer to [File-based user authentication > Add users](/deploy-manage/users-roles/cluster-or-deployment-auth/file-based.md#add-users), and check the ECK examples.

### Native realm

You can create custom users in the {{es}} native realm using {{es}} user management APIs or {{kib}}.

Refer to [Native user authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/native.md) for more details.

### External authentication realms

You can also configure external authentication realms such as LDAP, OpenID Connect, or SAML in your ECK deployments by providing the appropriate {{es}} or {{kib}} configuration settings and any required [certificates or configuration files](/deploy-manage/deploy/cloud-on-k8s/custom-configuration-files-plugins.md).

For more information, refer to [External authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/external-authentication.md).

## Creating custom roles

ECK facilitates file-based role management through Kubernetes secrets containing the roles specification. Alternatively, you can use the Role management API or the Role management UI in {{kib}}.

Refer to [Managing custom roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md#managing-custom-roles) for details and ECK based examples.