# Setting passwords for native and built-in users [change-passwords-native-users]

After you implement security, you might need or want to change passwords for different users. You can use the [`elasticsearch-reset-password`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/command-line-tools/reset-password.md) tool or the [change passwords API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-change-password) to change passwords for native users and [built-in users](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md), such as the `elastic` or `kibana_system` users.

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

