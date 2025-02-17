native
:   Users are stored in a dedicated {{es}} index. This realm supports an authentication token in the form of username and password, and is available by default when no realms are explicitly configured. The users are managed via the [user management APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-security). See [Native user authentication](native.md).

file
:   Users are defined in files stored on each node in the {{es}} cluster. This realm supports an authentication token in the form of username and password and is always available. See [File-based user authentication](file-based.md).