---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/synthetics-create-test.html
  - https://www.elastic.co/guide/en/serverless/current/observability-synthetics-create-test.html
---

# Write a synthetic test [synthetics-create-test]

After [setting up a Synthetics project](../../../solutions/observability/apps/create-monitors-with-project-monitors.md), you can start writing synthetic tests that check critical actions and requests that an end-user might make on your site.


## Syntax overview [synthetics-syntax]

To write synthetic tests for your application, you’ll need to know basic JavaScript and [Playwright](https://playwright.dev/) syntax.

::::{tip}
[Playwright](https://playwright.dev/) is a browser testing library developed by Microsoft. It’s fast, reliable, and features a modern API that automatically waits for page elements to be ready.
::::


The synthetics agent exposes an API for creating and running tests, including:

`journey`
:   Tests one discrete unit of functionality. Takes two parameters: a `name` (string) and a `callback` (function). Learn more in [Create a journey](../../../solutions/observability/apps/write-synthetic-test.md#synthetics-create-journey).

`step`
:   Actions within a journey that should be completed in a specific order. Takes two parameters: a `name` (string) and a `callback` (function). Learn more in [Add steps](../../../solutions/observability/apps/write-synthetic-test.md#synthetics-create-step).

`expect`
:   Check that a value meets a specific condition. There are several supported checks. Learn more in [Make assertions](../../../solutions/observability/apps/write-synthetic-test.md#synthetics-make-assertions).

`beforeAll`
:   Runs a provided function once, before any `journey` runs. If the provided function is a promise, the runner will wait for the promise to resolve before invoking the `journey`. Takes one parameter: a `callback` (function). Learn more in [Set up and remove a global state](../../../solutions/observability/apps/write-synthetic-test.md#before-after).

`before`
:   Runs a provided function before a single `journey` runs. Takes one parameter: a `callback` (function). Learn more in [Set up and remove a global state](../../../solutions/observability/apps/write-synthetic-test.md#before-after).

`afterAll`
:   Runs a provided function once, after all the `journey` runs have completed. Takes one parameter: a `callback` (function). Learn more in [Set up and remove a global state](../../../solutions/observability/apps/write-synthetic-test.md#before-after).

`after`
:   Runs a provided function after a single `journey` has completed. Takes one parameter: a `callback` (function). Learn more in [Set up and remove a global state](../../../solutions/observability/apps/write-synthetic-test.md#before-after).

`monitor`
:   The `monitor.use` method allows you to determine a monitor’s configuration on a journey-by-journey basis. If you want two journeys to create monitors with different intervals, for example, you should call `monitor.use` in each of them and set the `schedule` property to different values in each. Note that this is only relevant when using the `push` command to create monitors in {{kib}} an Observability Serverless project. Learn more in [Configure individual monitors](../../../solutions/observability/apps/configure-individual-browser-monitors.md).


## Create a journey [synthetics-create-journey]

Create a new file using the `.journey.ts` or `.journey.js` file extension or edit one of the example journey files.

A *journey* tests one discrete unit of functionality. For example, logging into a website, adding something to a cart, or joining a mailing list.

The journey function takes two parameters: a `name` and a `callback`. The `name` helps you identify an individual journey. The `callback` argument is a function that encapsulates what the journey does. The callback provides access to fresh Playwright `page`, `params`, `browser`, and `context` instances.

```js
journey('Journey name', ({ page, browser, context, params, request }) => {
  // Add steps here
});
```


### Arguments [synthetics-journey-ref]

**`name`** (*string*)
:   A user-defined string to describe the journey.

**`callback`** (*function*)
:   A function where you will add steps.

    **Instances**:

    `page`
    :   A [page](https://playwright.dev/docs/api/class-page) object from Playwright that lets you control the browser’s current page.

    `browser`
    :   A [browser](https://playwright.dev/docs/api/class-playwright) object created by Playwright.

    `context`
    :   A [browser context](https://playwright.dev/docs/api/class-browsercontext) that doesn’t share cookies or cache with other browser contexts.

    `params`
    :   User-defined variables that allow you to invoke the Synthetics suite with custom parameters. For example, if you want to use a different homepage depending on the `env` (`localhost` for `dev` and a URL for `prod`). See [Work with params and secrets](../../../solutions/observability/apps/work-with-params-secrets.md) for more information.

    `request`
    :   A request object that can be used to make API requests independently of the browser interactions. For example, to get authentication credentials or tokens in service of a browser-based test. See [Make API requests](../../../solutions/observability/apps/write-synthetic-test.md#synthetics-request-param) for more information.



## Add steps [synthetics-create-step]

A journey consists of one or more *steps*. Steps are actions that should be completed in a specific order. Steps are displayed individually in the Synthetics UI along with screenshots for convenient debugging and error tracking.

A basic two-step journey would look like this:

```js
journey('Journey name', ({ page, browser, client, params, request }) => {
    step('Step 1 name', () => {
      // Do something here
    });
    step('Step 2 name', () => {
      // Do something else here
    });
});
```

Steps can be as simple or complex as you need them to be. For example, a basic first step might load a web page:

```js
step('Load the demo page', () => {
  await page.goto('https://elastic.github.io/synthetics-demo/'); <1>
});
```

1. Go to the [`page.goto` reference](https://playwright.dev/docs/api/class-page#page-goto) for more information.



### Arguments [synthetics-step-ref]

|     |     |
| --- | --- |
| **`name`** (*string*) | A user-defined string to describe the journey. |
| **`callback`** (*function*) | A function where you simulate user workflows using Synthetics and [Playwright](../../../solutions/observability/apps/write-synthetic-test.md#synthetics-playwright) syntax. |

::::{note}

If you want to generate code by interacting with a web page directly, you can use the **Synthetics Recorder**.

The recorder launches a [Chromium browser](https://www.chromium.org/Home/) that will listen to each interaction you have with the web page and record them internally using Playwright. When you’re done interacting with the browser, the recorder converts the recorded actions into JavaScript code that you can use with Elastic Synthetics or {{heartbeat}}.

For more details on getting started with the Synthetics Recorder, refer to [Use the Synthetics Recorder](../../../solutions/observability/apps/use-synthetics-recorder.md).

::::



### Playwright syntax [synthetics-playwright]

Inside the callback for each step, you’ll likely use a lot of Playwright syntax. Use Playwright to simulate and validate user workflows including:

* Interacting with the [browser](https://playwright.dev/docs/api/class-browser) or the current [page](https://playwright.dev/docs/api/class-page) (like in the example above).
* Finding elements on a web page using [locators](https://playwright.dev/docs/api/class-locator).
* Simulating [mouse](https://playwright.dev/docs/api/class-mouse), [touch](https://playwright.dev/docs/api/class-touchscreen), or [keyboard](https://playwright.dev/docs/api/class-keyboard) events.
* Making assertions using [`@playwright/test`'s `expect` function](https://playwright.dev/docs/test-assertions). Read more in [Make assertions](../../../solutions/observability/apps/write-synthetic-test.md#synthetics-make-assertions).

Visit the [Playwright documentation](https://playwright.dev/docs) for information.

::::{note}
Do not attempt to run in headful mode (using `headless:false`) when running through Elastic’s global managed testing infrastructure or Private Locations as this is not supported.

::::


However, not all Playwright functionality should be used with Elastic Synthetics. In some cases, there are alternatives to Playwright functionality built into the Elastic Synthetics library. These alternatives are designed to work better for synthetic monitoring. Do *not* use Playwright syntax to:

* **Make API requests.** Use Elastic Synthetic’s `request` parameter instead. Read more in [Make API requests](../../../solutions/observability/apps/write-synthetic-test.md#synthetics-request-param).

There is also some Playwright functionality that is not supported out-of-the-box in Elastic Synthetics including:

* [Videos](https://playwright.dev/docs/api/class-video)
* The [`toHaveScreenshot`](https://playwright.dev/docs/api/class-locatorassertions#locator-assertions-to-have-screenshot-1) and [`toMatchSnapshot`](https://playwright.dev/docs/api/class-snapshotassertions) assertions

::::{note}
Captures done programmatically via [`screenshot`](https://playwright.dev/docs/api/class-page#page-screenshot) or [`video`](https://playwright.dev/docs/api/class-page#page-video) are not stored and are not shown in the Synthetics application. Providing a `path` will likely make the monitor fail due to missing permissions to write local files.

::::



## Make assertions [synthetics-make-assertions]

A more complex `step` might wait for a page element to be selected and then make sure that it matches an expected value.

Elastic Synthetics uses `@playwright/test`'s `expect` function to make assertions and supports most [Playwright assertions](https://playwright.dev/docs/test-assertions). Elastic Synthetics does *not* support [`toHaveScreenshot`](https://playwright.dev/docs/api/class-locatorassertions#locator-assertions-to-have-screenshot-1) or any [Snapshot Assertions](https://playwright.dev/docs/api/class-snapshotassertions).

For example, on a page using the following HTML:

```html
<header class="header">
  <h1>todos</h1>
  <input class="new-todo"
    autofocus autocomplete="off"
    placeholder="What needs to be done?">
</header>
```

You can verify that the `input` element with class `new-todo` has the expected `placeholder` value (the hint text for `input` elements) with the following test:

```js
step('Assert placeholder text', async () => {
  const input = await page.locator('input.new-todo'); <1>
  expect(await input.getAttribute('placeholder')).toBe(
    'What needs to be done?'
  ); <2>
});
```

1. Find the `input` element with class `new-todo`.
2. Use the assertion library provided by the Synthetics agent to check that the value of the `placeholder` attribute matches a specific string.



## Make API requests [synthetics-request-param]

You can use the `request` parameter to make API requests independently of browser interactions. For example, you could retrieve a token from an HTTP endpoint and use it in a subsequent webpage request.

```js
step('make an API request', async () => {
  const response = await request.get(params.url);
  // Do something with the response
})
```

The Elastic Synthetics `request` parameter is similar to [other request objects that are exposed by Playwright](https://playwright.dev/docs/api/class-apirequestcontext) with a few key differences:

* The Elastic Synthetics `request` parameter comes built into the library so it doesn’t have to be imported separately, which reduces the amount of code needed and allows you to make API requests in [inline journeys](../../../solutions/observability/apps/create-monitors-in-synthetics-app.md#synthetics-get-started-ui-add-a-browser-monitor).
* The top level `request` object exposed by Elastic Synthetics has its own isolated cookie storage unlike Playwright’s `context.request` and `page.request`, which share cookie storage with the corresponding [`BrowserContext`](https://playwright.dev/docs/api/class-browsercontext).
* If you want to control the creation of the `request` object, you can do so by passing options via [`--playwright-options`](../../../solutions/observability/apps/use-synthetics-cli.md#elastic-synthetics-command) or in the [`synthetics.config.ts` file](../../../solutions/observability/apps/configure-synthetics-projects.md).

For a full example that shows how to use the `request` object, refer to the [Elastic Synthetics demo repository](https://github.com/elastic/synthetics-demo/blob/main/advanced-examples/journeys/api-requests.journey.ts).

::::{note}
The `request` parameter is not intended to be used for writing pure API tests. Instead, it is a way to support writing plain HTTP requests in service of a browser-based test.
::::



## Set up and remove a global state [before-after]

If there are any actions that should be done before or after journeys, you can use `before`, `beforeAll`, `after`, or `afterAll`.

To set up global state or a server that will be used for a **single** `journey`, for example, use a `before` hook. To perform this setup once before **all** journeys, use a `beforeAll` hook.

```js
before(({ params }) => {
  // Actions to take
});

beforeAll(({ params }) => {
  // Actions to take
});
```

You can clean up global state or close a server used for a **single** `journey` using an `after` hook. To perform this cleanup once after all journeys, use an `afterAll` hook.

```js
after(({ params }) => {
  // Actions to take
});

afterAll(({ params }) => {
  // Actions to take
});
```


## Import NPM packages [synthetics-import-packages]

You can import and use other NPM packages inside journey code. Refer to the example below using the external NPM package `is-positive`:

```js
import { journey, step, monitor, expect } from '@elastic/synthetics';
import isPositive from 'is-positive';

journey('bundle test', ({ page, params }) => {
  step('check if positive', () => {
    expect(isPositive(4)).toBe(true);
  });
});
```

When you [create a monitor](../../../solutions/observability/apps/create-monitors-with-project-monitors.md) from a journey that uses external NPM packages, those packages will be bundled along with the journey code when the `push` command is invoked.

However there are some limitations when using external packages:

* Bundled journeys after compression should not be more than 800 Kilobytes.
* Native node modules will not work as expected due to platform inconsistency.


## Sample synthetic test [synthetics-sample-test]

A complete example of a basic synthetic test might look like this:

```js
import { journey, step, expect } from '@elastic/synthetics';

journey('Ensure placeholder is correct', ({ page }) => {
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

You can find more complex examples in the [Elastic Synthetics demo repository](https://github.com/elastic/synthetics-demo/blob/main/advanced-examples/journeys/api-requests.journey.ts).


## Test locally [synthetics-test-locally]

As you write journeys, you can run them locally to verify they work as expected. Then, you can create monitors to run your journeys at a regular interval.

To test all the journeys in a Synthetics project, navigate into the directory containing the Synthetics project and run the journeys in there. By default, the `@elastic/synthetics` runner will only run files matching the filename `*.journey.(ts|js)*`.

```sh
# Run tests on the current directory. The dot `.` indicates
# that it should run all tests in the current directory.
npx @elastic/synthetics .
```


### Test an inline monitor [synthetics-test-inline]

To test an inline monitor’s journey locally, pipe the inline journey into the `npx @elastic/synthetics` command.

Assume, for example, that your inline monitor includes the following code:

```js
step('load homepage', async () => {
    await page.goto('https://www.elastic.co');
});
step('hover over products menu', async () => {
    await page.hover('css=[data-nav-item=products]');
});
```

To run that journey locally, you can save that code to a file and pipe the file’s contents into `@elastic-synthetics`:

```sh
cat path/to/sample.js | npx @elastic/synthetics --inline
```

And you’ll get a response like the following:

```sh
Journey: inline
   ✓  Step: 'load homepage' succeeded (1831 ms)
   ✓  Step: 'hover over products menu' succeeded (97 ms)

 2 passed (2511 ms)