---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/change-passwords-native-users.html
applies_to:
  deployment:
    self:
navigation_title: Change passwords
---
# Set passwords for native and built-in users in self-managed clusters[ change-passwords-native-users]

After you implement security, you might need or want to change passwords for different users. If you want to reset a password for a [built-in user](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md) such as the `elastic` or `kibana_system` users, or a user in the [native realm](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md), you can use the following tools:

* The **Manage users** UI in {{kib}}
* The [`elasticsearch-reset-password`](elasticsearch://reference/elasticsearch/command-line-tools/reset-password.md) tool
* The [change passwords API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-change-password)

:::{{tip}}
This topic describes resetting passwords after the initial bootstrap password is reset. To learn about the users that are used to communicate between {{stack}} components, and about managing bootstrap passwords for built-in users, refer to [](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md).
:::

## Using {{kib}}

Elastic enables you to easily manage users in {{kib}} on the **Stack Management > Security > Users** page. From this page, you can create users, edit users, assign roles to users, and change user passwords. You can also deactivate or delete existing users.

## Using `elasticsearch-reset-password`

For example, the following command changes the password for a user with the username `user1` to an auto-generated value, and prints the new password to the terminal:

```shell
bin/elasticsearch-reset-password -u user1
```

To explicitly set a password for a user, include the `-i` parameter with the intended password.

```shell
bin/elasticsearch-reset-password -u user1 -i <password>
```

If you’re working in {{kib}} or don’t have command-line access, you can use the change passwords API to change a user’s password:

```console
POST /_security/user/user1/_password
{
  "password" : "new-test-password"
}
```
% TEST[continued]

## Using the `user` API [native-users-api]

You can manage users through the Elasticsearch `user` API.

For example, you can change a user's password:

```console
POST /_security/user/user1/_password
{
  "password" : "new-test-password"
}
```
% TEST[continued]

For more information and examples, see [Users](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-security).

