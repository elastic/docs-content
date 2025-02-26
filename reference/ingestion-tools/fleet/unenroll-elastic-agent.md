---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/unenroll-elastic-agent.html
---

# Unenroll Elastic Agents [unenroll-elastic-agent]

You can unenroll {{agent}}s to invalidate the API key used to connect to {{es}}.

1. In {{fleet}}, select **Agents**.
2. To unenroll a single agent, choose **Unenroll agent** from the **Actions** menu next to the agent you want to unenroll.
3. To unenroll multiple agents, bulk select the agents and click **Unenroll agents**.

    Unable to select multiple agents? Confirm that your subscription level supports selective agent unenrollment in {{fleet}}. For more information, refer to [{{stack}} subscriptions](https://www.elastic.co/subscriptions).


Unenrolled agents will continue to run, but will not be able to send data. They will show this error instead: `invalid api key to authenticate with fleet`.

::::{tip}
If unenrollment hangs, select **Force unenroll** to invalidate all API keys related to the agent and change the status to `inactive` so that the agent no longer appears in {{fleet}}.
::::


