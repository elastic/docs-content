---
navigation_title: Configure individual monitors
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/synthetics-monitor-use.html
  - https://www.elastic.co/guide/en/serverless/current/observability-synthetics-monitor-use.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
---

# Configure individual browser monitors [synthetics-monitor-use]

::::{note}
This is only relevant for monitors that are created and managed using a [Synthetics project](/solutions/observability/synthetics/get-started.md#observability-synthetics-get-started-synthetics-project). For more information on configuring browser monitors added in the UI, refer to [Create monitors in the Synthetics UI](/solutions/observability/synthetics/create-monitors-ui.md).

::::

After [writing synthetic journeys](/solutions/observability/synthetics/write-synthetic-test.md), you can use `monitor.use` to configure the browser monitors that will run your tests.

You’ll need to set a few configuration options:

* **Give your monitor a name.** Provide a human readable name and a unique ID for the monitor. This will appear in {{kib}} or your Observability Serverless project where you can view and manage monitors after they’re created.
* **Set the schedule.** Specify the interval at which your tests will run.
* **Specify where the monitors should run.** You can run monitors on Elastic’s global managed testing infrastructure or [create a {{private-location}}](/solutions/observability/synthetics/monitor-resources-on-private-networks.md) to run monitors from your own premises.
* {applies_to}`stack: ga 9.1+` **Choose which spaces the monitor is visible in.** ({{kib}} only) You can make the monitor visible in one or more [spaces](/deploy-manage/manage-spaces.md), or use `'*'` for all spaces. Options set in `monitor.use()` override the project-level `spaces` setting in your [Synthetics project config](/solutions/observability/synthetics/configure-projects.md#synthetics-configuration-monitor).
* **Set other options as needed.** There are several other options you can set to customize your implementation including params, tags, screenshot options, throttling options, and more.

Configure each monitor directly in your `journey` code using `monitor.use`. The `monitor` API allows you to set unique options for each journey’s monitor directly through code. For example:

```js
import { journey, step, monitor, expect } from '@elastic/synthetics';

journey('Ensure placeholder is correct', ({ page, params }) => {
  monitor.use({
    id: 'example-monitor',
    schedule: 10,
    spaces: ['default', 'team-a'],
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

For each journey, you can specify its `schedule`, the `locations` in which it runs, {applies_to}`stack: ga 9.1+` `spaces` ({{kib}} only), and other options. When an option is not set in `monitor.use()`, Synthetics uses the default from the global configuration file. Options set in `monitor.use()` take precedence over the project-level config—for example, `spaces` here overrides the global `monitor.spaces` setting. For more details, refer to [Configure a Synthetics project](/solutions/observability/synthetics/configure-projects.md).
