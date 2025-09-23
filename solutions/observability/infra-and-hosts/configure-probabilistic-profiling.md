---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/profiling-probabilistic-profiling.html
applies_to:
  stack: ga
products:
  - id: observability
---

# Configure probabilistic profiling [profiling-probabilistic-profiling]

Probabilistic profiling allows you to reduce storage costs by collecting a representative sample of profiling data. This method decreases storage costs with a visibility trade-off, as not all Profiling Host Agents will have profile collection enabled at all times.

Profiling Events linearly correlate with the probabilistic profiling value. The lower the value, the fewer events are collected.


## Configure probabilistic profiling [_configure_probabilistic_profiling]

To configure probabilistic profiling,  set the `-probabilistic-threshold` and `-probabilistic-interval` options.

Set the `-probabilistic-threshold` option to a unsigned integer between 1 and 99 to enable probabilistic profiling. At every probabilistic interval, a random number between 0 and 99 is chosen. If the probabilistic threshold that you’ve set is greater than this random number, the agent collects profiles from this system for the duration of the interval. The default value is 100.

Set the `-probabilistic-interval` option to a time duration to define the time interval for which probabilistic profiling is either enabled or disabled. The default value is 1 minute.


## Example [_example]

The following example shows how to configure the Universal Profiling agent with a threshold of 50 and an interval of 2 minutes and 30 seconds:

```bash
sudo pf-host-agent/pf-host-agent -probabilistic-threshold=50 -probabilistic-interval=2m30s
```

It is also possible to use the environment variables `PRODFILER_PROBABILISTIC_THRESHOLD=50` and `PRODFILER_PROBABILISTIC_INTERVAL=2m30s` to set this configuration.

