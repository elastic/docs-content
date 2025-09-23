---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/profiling-self-managed-install-next-steps.html
applies_to:
  stack: ga
products:
  - id: observability
---

# Step 5: Next steps [profiling-self-managed-install-next-steps]

With the backend installed, we recommend testing the backend and reading the documentation on operating the backend


## Test the backend [_test_the_backend]

Follow the steps described in [Install the Universal Profiling Agent](get-started-with-universal-profiling.md#profiling-install-profiling-agent) to install the Universal Profiling Agent on a machine, and verify that the backend is working as expected.

The agent logs will show that the agent is sending data to the backend, and navigating to Kibana you should be able to see data in the **Stacktraces** view. Inspect the backend services logs to verify that the data is being received and ingested. If needed, re-configure the backend services with `verbose: true` to get more detailed logs.

If you find issues in the logs, refer to [Troubleshooting Universal Profiling backend](/troubleshoot/observability/troubleshoot-your-universal-profiling-agent-deployment/troubleshoot-universal-profiling-backend.md).


## Operating the backend [_operating_the_backend]

Next we recommend reading [Operating the Universal Profiling backend](operate-universal-profiling-backend.md) to learn how to monitor and scale the backend on each platform.
