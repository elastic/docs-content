---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/synthetics-monitor-use.html
  - https://www.elastic.co/guide/en/serverless/current/observability-synthetics-monitor-use.html

navigation_title: "Configure individual monitors"
---

# Configure individual browser monitors [synthetics-monitor-use]


::::{note}
This is only relevant for monitors that are created and managed using a [Synthetics project](../../../solutions/observability/apps/get-started.md#observability-synthetics-get-started-synthetics-project). For more information on configuring browser monitors added in the UI, refer to [Create monitors in the Synthetics UI](../../../solutions/observability/apps/create-monitors-in-synthetics-app.md).

::::


After [writing synthetic journeys](../../../solutions/observability/apps/write-synthetic-test.md), you can use `monitor.use` to configure the browser monitors that will run your tests.

You’ll need to set a few configuration options:

* **Give your monitor a name.** Provide a human readable name and a unique ID for the monitor. This will appear in {{kib}} or your Observability Serverless project where you can view and manage monitors after they’re created.
* **Set the schedule.** Specify the interval at which your tests will run.
* **Specify where the monitors should run.** You can run monitors on Elastic’s global managed testing infrastructure or [create a {{private-location}}](../../../solutions/observability/apps/monitor-resources-on-private-networks.md) to run monitors from your own premises.
* **Set other options as needed.** There are several other options you can set to customize your implementation including params, tags, screenshot options, throttling options, and more.

Configure each monitor directly in your `journey` code using `monitor.use`. The `monitor` API allows you to set unique options for each journey’s monitor directly through code. For example:

```js
import { journey, step, monitor, expect } from '@elastic/synthetics';

journey('Ensure placeholder is correct', ({ page, params }) => {
  monitor.use({
    id: 'example-monitor',
    schedule: 10,
    throttling: {
      download: 10,
      upload: 5,
      latency: 100,
    },
  });
  step('Load the demo page', async () => {
    await page.goto('https://elastic.github.io/synthetics-demo/');
  });
  step('Assert placeholder text', async () => {
    const placeholderValue = await page.getAttribute(
      'input.new-todo',
      'placeholder'
    );
    expect(placeholderValue).toBe('What needs to be done?');
  });
});
```

For each journey, you can specify its `schedule` and the `locations` in which it runs. When those options are not set, Synthetics will use the default values in the global configuration file. For more details, refer to [Configure a Synthetics project](../../../solutions/observability/apps/configure-synthetics-projects.md).
