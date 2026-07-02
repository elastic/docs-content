<!--
This snippet is in use in the following locations:
- deploy-manage/api-keys.md
- deploy-manage/app-connections.md
-->
Application connections are the OAuth equivalent of a [serverless project API key](/deploy-manage/api-keys/serverless-project-api-keys.md) for external access to your {{serverless-short}} project's data on a user's behalf. Both are scoped to one project and let an external application work with that project as the consenting user.

During technical preview, application connections support MCP clients only. For MCP hosts, browser consent replaces creating a project API key with [{{agent-builder}} application privileges](/explore-analyze/ai-features/agent-builder/mcp-server.md#api-key-application-privileges) and adding it to the host configuration.

Application connections do not replace [{{ecloud}} API keys](/deploy-manage/api-keys/elastic-cloud-api-keys.md) for organization or multi-project API access, or other uses of serverless project API keys for direct [{{es}}]({{es-serverless-apis}}) and [{{kib}}]({{kib-serverless-apis}}) API calls.
