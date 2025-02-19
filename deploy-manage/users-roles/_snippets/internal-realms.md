native
:   Users are stored in a dedicated {{es}} index. This realm supports an authentication token in the form of username and password, and is available by default when no realms are explicitly configured. Users are managed through {{kib}}, or using [user management APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-security). See [Native user authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/native.md).

file
:   Users are defined in files stored on each node in the {{es}} cluster. This realm supports an authentication token in the form of username and password and is always available. See [File-based user authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/file-based.md). Available for {{eck}} and self-managed deployments only.