---
navigation_title: Real user monitoring
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/user-experience.html
applies_to:
  stack: all
products:
  - id: observability
---

# Real user monitoring (User Experience) [user-experience]

{{user-experience}} provides a way to quantify and analyze the perceived performance of your web application. Unlike testing environments, {{user-experience}} data reflects real-world user experiences. Drill down further by looking at data by URL, operating system, browser, and location — all of which can impact how your application performs on end-user machines.

Powered by the APM Real user monitoring (RUM) agent, all it takes is a few lines of code to begin surfacing key user experience metrics.

:::{image} /solutions/images/observability-user-experience-tab.png
:alt: {{user-experience}} tab
:screenshot:
:::

## Why is {{user-experience}} important? [why-user-experience]

Search engines are placing increasing importance on user experience when organically ranking websites. Elastic makes it easy to view your website data in the context of Google Core Web Vitals — metrics that score three key areas of user experience: loading performance, visual stability, and interactivity. These Core Web Vitals are set to become the main performance measurement in Google ranking factors. If you’re a content-based site that wants to appear in the “Top Stories” section of Google search results, you must have good Core Web Vitals.

## How does {{user-experience}} work? [how-user-experience-works]

{{user-experience}} metrics are powered by the [APM Real User Monitoring (RUM) agent](apm-agent-rum-js://reference/index.md). The RUM agent uses browser timing APIs, like [Navigation Timing](https://w3c.github.io/navigation-timing/), [Resource Timing](https://w3c.github.io/resource-timing/), [Paint Timing](https://w3c.github.io/paint-timing/), and [User Timing](https://w3c.github.io/user-timing/), to capture {{user-experience}} metrics every time a user hits one of your pages. This data is stored in {{es}}, where it can be visualized using {{kib}}.

The RUM agent can be installed as a dependency to your application, or with just a few lines of JavaScript. It only takes a few minutes to [get started](/solutions/observability/apm/apm-agents/real-user-monitoring-rum.md).

## {{user-experience}} in {{kib}} [user-experience-tab]

### Page load duration [user-experience-page-load]

This high-level overview is your analysis starting point and answers questions like: How long is my server taking to respond to requests? How much time is spent parsing and painting that content? How many page views has my site received?

You won’t be able to fix any problems from viewing these metrics alone, but you’ll get a sense of the big picture as you dive deeper into your data.

:::{image} /solutions/images/observability-page-load-duration.png
:alt: {{user-experience}} page load duration metrics
:screenshot:
:::

### {{user-experience}} metrics [user-experience-metrics]

{{user-experience}} metrics help you understand the perceived performance of your website. For example, first contentful paint is the timestamp when the browser begins rendering content. In other words, it’s around this time that a user first gets feedback that the page is loading.

:::{image} /solutions/images/observability-user-exp-metrics.png
:alt: {{user-experience}} metrics
:screenshot:
:::

::::{dropdown} Metric reference
First contentful paint
:   Focuses on the initial rendering and measures the time from when the page starts loading to when any part of the page’s content is displayed on the screen. The agent uses the [Paint timing API](https://www.w3.org/TR/paint-timing/#first-contentful-paint) available in the browser to capture the timing information.[^1^](#footnote-1)

Total blocking time
:   The sum of the blocking time (duration above 50 ms) for each long task that occurs between the First contentful paint and the time when the transaction is completed. Total blocking time is a great companion metric for [Time to interactive](https://web.dev/tti/) (TTI) which is lab metric and not available in the field through browser APIs. The agent captures TBT based on the number of long tasks that occurred during the page load lifecycle.[^2^](#footnote-2)

`Long Tasks`
:   A long task is any user activity or browser task that monopolize the UI thread for extended periods (greater than 50 milliseconds) and block other critical tasks (frame rate or input latency) from being executed.[^3^](#footnote-3)

Number of long tasks
:   The number of long tasks.

Longest long task duration
:   Duration of the longest long task on the page.

Total long tasks duration
:   Total duration of all long tasks

::::

These metrics tell an important story about how users experience your website. But developers shouldn’t have to become experts at interpreting and acting on these signals; they should spend their time reacting to the opportunities that these metrics present. For that reason (and many others), Elastic has embraced Google Core Web Vitals.

#### Core Web Vitals [user-experience-core-vitals]

[Core Web Vitals](https://web.dev/vitals/) is a recent initiative from Google to introduce a new set of metrics that better categorize good and bad sites by quantifying the real-world user experience. This is done by looking at three key metrics: loading performance, visual stability, and interactivity:

Largest contentful paint (LCP)
:   Loading performance. LCP is the timestamp when the main content of a page has likely loaded. To users, this is the *perceived* loading speed of your site. To provide a good user experience, Google recommends an LCP of fewer than 2.5 seconds.[^4^](#footnote-4)

Interaction to next paint (INP)
:   Responsiveness to user interactions. The INP value comes from measuring the latency of all click, tap, and keyboard interactions that happen throughout a single page visit and choosing the longest interaction observed. To provide a good user experience, Google recommends an INP of fewer than 200 milliseconds.[^5^](#footnote-5)

::::{note}
Previous {{kib}} versions included the metric [First input delay (FID)](https://web.dev/fid/) in the User Experience app. Starting with version 8.12, FID was replaced with *Interaction to next paint (INP)*. The APM RUM agent started collecting INP data in version 5.16.0. If you use an earlier version of the RUM agent with {{kib}} version 8.12 or later, it will *not* capture INP data and there will be *no data* to show in the User Experience app:

|  | **Kibana version ≥ 8.12** | **Kibana version < 8.12** |
| --- | --- | --- |
| **RUM agent version ≥ 5.16.0** | INP data will be visible. | FID data will be visible. |
| **RUM agent version < 5.16.0** | The INP section will be empty. | FID data will be visible. |

RUM agent version ≥ 5.16.0 will continue to collect FID metrics so, while FID metrics are not shown in the User Experience app in {{kib}} versions 8.12 and later, you can choose to visualize FID metrics in a [custom dashboard](/explore-analyze/dashboards/create-dashboard-of-panels-with-web-server-data.md) or using [Lens](/explore-analyze/visualize/lens.md).

::::

Cumulative layout shift (CLS)
:   Visual stability. Is content moving around because of `async` resource loading or dynamic content additions? CLS measures these frustrating unexpected layout shifts. To provide a good user experience, Google recommends a CLS score of less than `.1`.[^6^](#footnote-6)

::::{tip}
[Beginning in May 2021](https://webmasters.googleblog.com/2020/11/timing-for-page-experience.md), Google will start using Core Web Vitals as part of their ranking algorithm and will open up the opportunity for websites to rank in the "top stories" position without needing to leverage [AMP](https://amp.dev/).[^7^](#footnote-7)
::::

### Load/view distribution [user-experience-distribution]

Operating system, browser family, and geographic location can all have a massive impact on how visitors experience your website. This data can help you understand when and where your users are visiting from, and can help you prioritize optimizations — for example, prioritizing improvements for the most popular browsers visiting your site.

Don’t forget, this data also influences search engine page rankings and placement in top stories for content sites — without requiring the use of AMP.

:::{image} /solutions/images/observability-visitor-breakdown.png
:alt: {{user-experience}} visitor breakdown
:screenshot:
:::

### Error breakdown [user-experience-errors]

JavaScript errors can be detrimental to a users experience on your website. But variation in users' software and hardware makes it nearly impossible to test for every combination. And, as JavaScript continues to get more and more complex, the need for user experience monitoring and error reporting only increases. Error monitoring makes this visible by surfacing JavaScript errors that are occurring on your website in production.

:::{image} /solutions/images/observability-js-errors.png
:alt: {{user-experience}} JavaScript errors
:screenshot:
:::

Open error messages in APM for additional analysis tools, like occurrence rates, transaction ids, user data, and more.

### Feedback and troubleshooting [user-experience-feedback]

Have a question? Want to leave feedback? Visit the [{{user-experience}} discussion forum](https://discuss.elastic.co/c/observability/user-experience/87).

#### References [user-experience-references]

^1^ $$$footnote-1$$$ More information: [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Glossary/First_contentful_paint)<br>
^2^ $$$footnote-2$$$ More information: [web.dev](https://web.dev/tbt/)<br>
^3^ $$$footnote-3$$$ More information: [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/API/Long_Tasks_API)<br>
^4^ $$$footnote-4$$$ Source: [web.dev](https://web.dev/lcp/)<br>
^5^ $$$footnote-5$$$ Source: [web.dev](https://web.dev/articles/inp)<br>
^6^ $$$footnote-6$$$ Source: [web.dev](https://web.dev/cls/)<br>
^7^ $$$footnote-7$$$ Source: [webmasters.googleblog.com](https://webmasters.googleblog.com/2020/05/evaluating-page-experience.md)<br>