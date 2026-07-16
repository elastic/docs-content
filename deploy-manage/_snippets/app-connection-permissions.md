All application connections mirror the permissions of the user that authorizes the connection. If you authorize the connection and you have read and write permissions, then so will your connected application. 

When a user's permissions change, the change applies on the next token refresh; changes to a custom role apply immediately.

You can use a secondary user with limited permissions to restrict what the connected application can access. Permissions follow the user who authorizes the connection, so ensure that user is signed in before authorizing it. This user does not need to be the same account used to create the OAuth client or manage application connections.