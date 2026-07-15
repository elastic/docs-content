All application connections mirror the permissions of the user that authorizes the connection. If you approve the connection and you have read and write permissions, then so will your Agent. 

When a user's permissions change, the change applies on the next token refresh; changes to a custom role apply immediately.

It is possible to use a secondary user with limited permissions to limit the permissions of your agent. Permissions follow the user that approves the connection, so ensure that the second user is logged in before approving the connection. This does not need to be the same account that is used to create the OAuth client and manage the application connections.