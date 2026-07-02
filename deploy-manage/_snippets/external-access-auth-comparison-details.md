<!--
This snippet is in use in the following locations:
- deploy-manage/api-keys.md
- deploy-manage/app-connections.md
-->
| | Application connections | Elastic API keys |
| --- | --- | --- |
| Best for | External applications acting on behalf of individual users | Automation, scheduled jobs, and machine-to-machine access |
| Identity | The consenting user's live permissions | Permissions snapshotted at key creation |
| Authorization | Each user grants access in the browser | A key is created once and stored in a config file or secret store |
| Credential lifetime | Short-lived tokens that refresh automatically | Long-lived until the key expires or is revoked |
| Revocation | Revoke one user's connection without affecting others | Revoking the key affects every client that uses it |
