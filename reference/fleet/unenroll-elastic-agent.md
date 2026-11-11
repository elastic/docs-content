---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/unenroll-elastic-agent.html
description: Unenroll Elastic Agents from Fleet, and learn what happens to agents and their data after a regular or force unenroll.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Unenroll Elastic Agents [unenroll-elastic-agent]

You can unenroll {{agent}}s to invalidate the API key used to connect to {{es}}.

1. In {{fleet}}, select **Agents**.
2. To unenroll a single agent, open the **Actions** menu next to the agent you want to unenroll, and then select:

    * {applies_to}`serverless: ga` {applies_to}`stack: ga 9.3+` **Security and removal** → **Unenroll agent**
    * {applies_to}`stack: ga 9.0-9.2` **Unenroll agent**

3. To unenroll multiple agents, bulk select the agents, open the **Actions** menu, and then select:

    * {applies_to}`serverless: ga` {applies_to}`stack: ga 9.3+` **Security and removal** → **Unenroll *N* agents**
    * {applies_to}`stack: ga 9.0-9.2` **Unenroll *N* agents**

    *N* is the number of selected agents.

    Unable to select multiple agents? Confirm that your subscription level supports **selective agent unenrollment** in {{fleet}}. For more information, refer to [Elastic subscriptions](https://www.elastic.co/subscriptions).

When you unenroll an agent, {{fleet}} sends it an unenroll action. When the agent receives the action, it stops its inputs and no longer sends data. {{fleet}} invalidates the agent's API keys after the agent acknowledges the action. The {{agent}} process continues to run, but it's no longer managed by {{fleet}}.

Enrollment works differently for {{agent}} in a containerized environment. For details, refer to [Enrollment handling for containerized agents](/reference/fleet/enrollment-handling-containerized-agent.md).

## Force unenroll an agent [force-unenroll-elastic-agent]

If unenrollment hangs because the agent is offline or can't be reached, you can force unenroll it. Force unenroll invalidates all API keys related to the agent and changes its status to **Unenrolled**, so that the agent no longer appears in {{fleet}}.

A force-unenrolled agent doesn't receive the unenroll action, so it keeps running its last policy and keeps trying to check in with {{fleet}}. It can no longer send data to the {{es}} cluster where {{fleet}} runs, and it logs an invalid API key error. However, it can continue sending data to outputs that don't use the invalidated API keys, such as Kafka, {{ls}}, or remote {{es}} outputs. To stop it, you need to [uninstall {{agent}}](/reference/fleet/uninstall-elastic-agent.md) on the host.

::::{warning}
Force unenroll is a last resort, and you can't undo it from {{fleet}}. Use it only for agents that are offline or can't be reached, or for compromised agents whose API keys you need to revoke immediately.
::::

To force unenroll an agent, do one of the following:

* If the agent's unenrollment hangs, open the **Actions** menu next to the agent and select **Force unenroll**. This option replaces **Unenroll agent** while unenrollment is in progress.
* In the unenroll dialog, select **Remove agent immediately** under **Force unenroll agent**.