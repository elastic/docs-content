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

3. To unenroll multiple agents, bulk select the agents, and then select **Actions** → **Unenroll *N* agents**, where *N* is the number of selected agents.

    Unable to select multiple agents? Confirm that your subscription level supports **selective agent unenrollment** in {{fleet}}. For more information, refer to [Elastic subscriptions](https://www.elastic.co/subscriptions).

When you unenroll an agent, {{fleet}} sends it an unenroll action. When the agent receives the action, it stops its inputs and no longer sends data. {{fleet}} invalidates the agent's API keys after the agent acknowledges the action. The {{agent}} process continues to run, but it's no longer managed by {{fleet}}.

If unenrollment hangs, select **Force unenroll** to invalidate all API keys related to the agent and change the status to **Unenrolled** so that the agent no longer appears in {{fleet}}. A force-unenrolled agent doesn't receive the unenroll action, so it keeps running its inputs. It can no longer connect to {{fleet}} or send data to the {{es}} cluster where {{fleet}} runs, and it logs an invalid API key error.

::::{important}
A force-unenrolled agent can continue sending data to outputs that don't use the invalidated API keys, such as Kafka, {{ls}}, or remote {{es}} outputs. To stop all data collection, [uninstall {{agent}}](/reference/fleet/uninstall-elastic-agent.md) from the host.
::::

Enrollment works differently for {{agent}} in a containerized environment. For details, refer to [Enrollment handling for containerized agents](/reference/fleet/enrollment-handling-containerized-agent.md).