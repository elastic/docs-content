---
applies_to:
  serverless:
products:
  - id: cloud-serverless
---

# Update a connection alias for a project

Connection aliases for your projects enable you to have predictable, human-readable URLs that can be shared easily. The connection alias must be unique for each region, across all accounts.

New projects are assigned a default alias derived from the project name.

To modify the connection alias for a project:

1. From the **Serverless projects** menu, select a project and click **Manage**.
2. Locate **Connection alias**, click **Edit**.
3. Define a new alias. Make sure you choose something meaningful to you.

    ::::{tip}
    Make the alias as unique as possible to avoid collisions. Aliases might have been already claimed by other users for projects in the region.
    ::::

4. Select **Update alias**.

::::[important]
Renaming connection aliases may cause disruptions to applications and services that rely on these endpoints. Ensure that you update any references to the old alias to prevent issues.
::::
