---
navigation_title: Anomaly detection jobs with AI
description: Create anomaly detection jobs with an AI agent in Elastic Agent Builder. It tests a setup on historical data, then creates real-time jobs after you approve.
applies_to:
  serverless: experimental
  stack: experimental 9.6
type: how-to
products:
  - id: machine-learning
  - id: kibana
---

# Create {{anomaly-jobs}} with AI in chat

If you have time series data and want to catch unusual behavior in it, but you're not sure how to set up an {{anomaly-job}}, you can describe your data and your goal to an AI agent in {{agent-builder}}. The agent asks follow-up questions in everyday language, tests a proposed setup on your historical data, and creates real-time jobs only after you've reviewed the results.

Because the agent uses a large language model, its questions and the setup it proposes can vary between conversations. Nothing runs in real time, and no job is deleted, until you approve it.

## Before you begin

* Turn on the `agentBuilder:experimentalFeatures` [advanced setting](/explore-analyze/ai-features/agent-builder/get-started.md#enable-experimental-features-optional). The `anomaly-detection` skill doesn't appear without it.
* Use an agent that has the [`anomaly-detection` skill](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md#agent-builder-anomaly-detection-skill). The default Elastic AI Agent has it because [Elastic capabilities](/explore-analyze/ai-features/agent-builder/agent-builder-agents.md#elastic-capabilities) are on by default. For a custom agent, turn on Elastic capabilities or assign the skill to the agent.
* Make sure your user has the {{kib}} and {{es}} privileges to create and run {{anomaly-jobs}}. Refer to [Setting up machine learning](../setting-up-machine-learning.md#setup-privileges).
* Have time series data in {{es}}. The agent reads the data through a {{dfeed}}, so it can't create jobs for data outside {{es}}.
* To see the inline charts in the conversation, you need a Platinum or later license.

## Create jobs with the agent

1. [Start a chat](/explore-analyze/ai-features/agent-builder/chat.md) with an agent that has the `anomaly-detection` skill. Describe what you want to detect and where your data is. For example: `Detect unusual error rates per host in my nginx access logs.`

   Before it asks you anything, the agent checks your data to see which fields and time range are available. If a prebuilt {{ml}} configuration matches your data, the agent starts from it.

2. Answer the agent's questions. It asks about your goal, not about {{ml}} settings, for example what a bad day looks like, how quickly you need to know about a problem, and whether planned events such as deployments or holidays would look unusual without being a real problem. The agent turns your answers into a job configuration and chooses the job structure itself.

3. Review the proposed setup. The agent validates the configuration, estimates how much memory the jobs need, and summarizes in plain language the time range it will analyze, the approximate number of records, and how long the run is expected to take. It also shows the full job and {{dfeed}} definitions. To try the setup on your historical data before going live, which the agent recommends, confirm the batch run.

4. Wait while the agent runs the analysis on your historical data. When it's done, the agent summarizes what it found, such as how many anomalies, the highest score, and the time and entity behind the strongest one. If you have a Platinum or later license, it also shows an anomaly swim lane, anomaly charts, and a single metric viewer for the top anomaly in the conversation, with a link that opens the jobs in the **Anomaly Explorer**.

   If the agent finds no anomalies, it says so and offers to widen the time range, try a different field or function, or adjust the sensitivity. Zero anomalies can mean your data is very consistent or that the setup needs adjusting.

5. Tell the agent whether the results look right.

   * **If they do**, the agent creates a second set of jobs with the same configuration that runs on incoming data from now on. These jobs get a new ID, for example the original ID with `-realtime` added, so they don't replace the historical ones. The agent then offers to delete the historical jobs, which it only does after you confirm. It also offers to create an alerting rule that notifies you about anomalies.
   * **If they don't**, tell the agent what looked wrong, for example too many false alerts, the wrong entities, missing events, or the wrong time scale. The agent goes back to your answers, adjusts the setup, and runs it again.

To check the outcome, open the **Anomaly Detection Jobs** page. The new real-time jobs are listed there, and they're open with their {{dfeeds}} started. The historical jobs are also listed until you delete them. The model keeps learning what's normal for your data over the following weeks, so the results become more accurate over time.

## Temporary jobs and cleanup

The jobs the agent runs on your historical data are temporary. It adds them to the `ml-agent-scratch` group so it can find them again. The real-time jobs don't carry that group.

When you approve the results, the agent names every historical job it wants to delete and waits for your confirmation. It only deletes jobs in the `ml-agent-scratch` group. If you decline, the historical jobs stay in place, and you can delete them yourself later. Keep them if you want to look at the historical results again.

## Alerting rules

If you ask for alerting, the agent lets you pick one of two {{kib}} rule types:

* **{{anomaly-detect-cap}}**: Notifies you when a job's results match the conditions you define. The agent proposes a default severity threshold of 75 and asks whether you want to change it.
* **{{anomaly-detect-cap}} jobs health**: Notifies you when a job has an operational problem, such as a stopped {{dfeed}} or a memory limit error.

Refer to [Generating alerts for {{anomaly-jobs}}](ml-configuring-alerts.md) to learn how these rules work.

## Next steps

* To adjust a job the agent created, or to explore its results, open it in the **Anomaly Explorer**. Refer to [View the results](ml-ad-view-results.md).
* To ask the agent about existing jobs, such as which entity caused a spike, why a score is high or low, or why a {{dfeed}} stopped, use the same `anomaly-detection` skill. Refer to its entry in the [built-in skills reference](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md#agent-builder-anomaly-detection-skill).

## Related pages

* [Run a job](ml-ad-run-jobs.md)
* [Tutorial: Getting started with {{anomaly-detect}}](ml-getting-started.md)
* [Skills in {{agent-builder}}](/explore-analyze/ai-features/agent-builder/skills.md)
