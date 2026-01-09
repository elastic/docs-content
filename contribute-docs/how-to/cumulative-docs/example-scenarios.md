---
navigation_title: Example scenarios
---

# Cumulative docs example scenarios

:::{note}
This content is still in development.
If you have questions about how to write cumulative documentation while contributing,
reach out to **@elastic/docs** in the related GitHub issue or PR.
:::

Browse common scenarios you might run into as a docs contributor that require different approaches to labeling cumulative docs.

:::{note}
Screenshots might not exactly match the example pages linked to.
:::

## Content applies to both stateful and serverless [stateful-serverless]

If an entire page is primarily about using or interacting with both Elastic Stack components and
the Serverless UI, add both the `stack` and `serverless` keys to the `applies_to` in the frontmatter.

### If released in Serverless, but not yet released in Elastic Stack

:::{include} /contribute-docs/_snippets/stack-serverless-lifecycle-example.md
:::


## Section applicability differs from page-level applicability [page-section-varies]

When a section has different applicability than the applicability indicated at the
page level in the frontmatter, use section-level `applies_to` badges.

### If labeling serverless vs. stateful [page-section-varies-product]

<!--
TO DO: Consider other alternative titles:
* If labeling versioned products or serverless vs. stateful.
* If labeling available vs. unavailable.
-->

<!--
TO DO: Please make this better
-->
When a documentation set or page is primarily about using a product following its own
versioning schema or some combination of Elastic Stack components and the Serverless UI,
it usually includes content that is meant to be used together (i.e. not parallel sections
like in [If labeling deployment modes](#page-section-varies-deployment)), but is only
available in specific versions or either serverless or stateful.

% Contributor experience
In this case, docs contributors should include the following at the page level:

* `stack` with the lowest version that applies to any content (unless it is lower
  than the base version, {{version.stack.base}}, in which case omit the version number altogether).
* `serverless` if applicable.

Then if a section contains content that applies to a different context than what is
defined at the page level, include section-level `applies_to` only with the items
that are different than the page-level `applies_to`.

% Reader experience
The reader should assume that content in a section with a section-level `applies_to`
is applicable to all the contexts included in the page-level `applies_to` unless
explicitly stated.

:::{tip}
**Don’t overload with badges that restate the page-level applicability.**
In content that is primarily about serverless vs. stateful, use `unavailable`
if functionality is not available at all in `serverless` or `stack`.
Do not use `unavailable` for specific `stack` versions.
Instead, include the lifecycle and version and the fact that it is not applicable
to other versions will be implied.
:::

% Example
For example, if a whole page is generally applicable to Elastic Stack 9.0.0 and to Serverless, but one specific section isn’t applicable to Serverless. The content on the [Spaces](https://www.elastic.co/docs/deploy-manage/manage-spaces) page is generally applicable to both Serverless and stateful, but one section only applies stateful:

* In the frontmatter, specify that the content on the page applies to both unless otherwise specified.
* In a section-level annotation, specify that the content is `unavailable` in `serverless`.

:::::{tab-set}
::::{tab-item} Image
:::{image} ./images/page-section-varies-product.png
:screenshot:
:alt:
:::
::::
::::{tab-item} Code
````
---
applies_to:
  stack: ga
  serverless: ga
---

# Spaces

[...]

## Configure a space-level landing page [space-landing-page]

```{applies_to}
serverless: unavailable
```

[...]
````
::::
:::::

:::{tip}
Likewise, when the difference is specific to just one paragraph or list item, the same rules apply.
Just the syntax slightly differs so that it stays inline: `` {applies_to}`serverless: unavailable` ``.
:::

### If labeling deployment modes [page-section-varies-deployment]

<!--
TO DO: Consider other alternative titles:
* If labeling parallel content on a single page.
* If labeling applicable vs. not applicable.
-->

<!--
TO DO: Please make this better
-->
When a documentation set or page is primarily about orchestrating, deploying,
or configuring an installation, it usually includes parallel content about multiple
deployment modes (the reader picks one of several sections that is applicable to them).

% Contributor experience
In this case, docs contributors include all the deployment types that are mentioned
throughout the page in the frontmatter `applies_to`, and in each section they include
only the applicable deployment modes using section-level `applies_to`.

% Reader experience
The reader should assume that content in a section with a section-level `applies_to` is
not applicable to any deployment modes that are omitted.

:::{tip}
**Don’t overload with exclusions unless it is necessary.**
In content that is primarily about deployment modes, we do not include `unavailable` badges
for anything in `applies_to` > `deployment`.
:::

% Example
For example, the content on the [Security](https://www.elastic.co/docs/deploy-manage/security) page is generally applicable to all deployment types, but the first section only applies to Elastic Cloud Hosted and Serverless:

* In the frontmatter, specify that the content on the page applies to all deployment types unless otherwise specified.
* In a section-level annotation, specify that the content only applies to `ech` and `serverless`.

:::::{tab-set}
::::{tab-item} Image
:::{image} ./images/page-section-varies-deployment.png
:screenshot:
:alt:
:::
::::
::::{tab-item} Code
````
---
applies_to:
  deployment: all
---

# Security

[...]

## Managed security in Elastic Cloud

```{applies_to}
deployment:
  ech: ga
serverless: ga
```

[...]
````
::::
:::::

:::{tip}
Likewise, when the difference is specific to just one paragraph or list item, the same rules apply.
Just the syntax slightly differs so that it stays inline: `` {applies_to}`ech: ga` {applies_to}`serverless: ga` ``.
:::

## Functionality is added to an unversioned product [unversioned-added]

When functionality is _first added_ to an unversioned product/deployment mode,
how it is labeled depends on if the functionality is in technical preview, beta, or GA.

### If the section lifecycle is the same as the page level [unversioned-added-same]

For example, on the [Project settings](https://www.elastic.co/docs/deploy-manage/deploy/elastic-cloud/project-settings#obs-serverless-project-features) page we added content about the Observability Logs Essentials feature tier, that was added to Serverless in GA.
Since the page's frontmatter already includes `serverless: ga`, there is no need to label the added content.

However, if the functionality is also applicable to a specific version of a versioned product/deployment mode,
label the content with both versioned and unversioned applicability information.

For example, on the [Lens](https://www.elastic.co/docs/explore-analyze/visualize/lens) page we added information
about a new option that was added to Serverless in GA and the Elastic Stack in GA in 9.1.0.
Even though it is added to Serverless, an unversioned product, in the same lifecycle state as the page-level annotation,
we still include an inline annotation to make it clear that this is not only available in the Elastic Stack.

:::::{tab-set}
::::{tab-item} Image
:::{image} ./images/example-unversioned-added-same-exception.png
:screenshot:
:alt:
:::
::::
::::{tab-item} Code
```
---
applies_to:
  stack: ga
  serverless: ga
---

# Lens [lens]

[...]

#### Tables

**Density** {applies_to}`stack: ga 9.1+` {applies_to}`serverless: ga`
:   Make the table more or less compact. Choose between **Compact**, **Normal** (default), and **Expanded**.
```
::::
:::::

### If the section lifecycle is different than the page level [unversioned-added-different]

For example, on the [Dashboard controls](https://www.elastic.co/docs/explore-analyze/dashboards/add-controls#add-esql-control) page we added content about new ES|QL controls functionality that was added to Serverless in preview.
Since this is different than the page-level applicability in the frontmatter, `serverless: ga`,
label the content about the new functionality with `serverless: preview`.

:::::{tab-set}
::::{tab-item} Image
:::{image} ./images/example-unversioned-added-different.png
:screenshot:
:alt:
:::
::::
::::{tab-item} Code
````
---
serverless: ga
---

# Add filter controls

[...]

## Add ES|QL controls

```{applies_to}
serverless: preview
```

[...]
````
::::
:::::

## Functionality changes lifecycle state [lifecycle-changed]

When the functionality described in any content changes lifecycle state,
how it is labeled varies by whether the product/deployment mode is versioned or unversioned.

For example, the majority of the content on the [Lens](https://www.elastic.co/docs/explore-analyze/visualize/lens)
page was applicable to both Elastic Stack and to Serverless.
One specific section describes functionality that was in technical preview in Elastic Stack 9.0.0 and
Serverless at the time Elastic Stack 9.0.0 was released.
Then, the functionality became generally available in Elastic Stack in 9.1.0 and shortly before the
Elastic Stack 9.1.0 release in Serverless.

* For Elastic Stack, a versioned product, label the section with both lifecycles: `ga 9.1` and `preview 9.0`.
* For Serverless, an unversioned product, update the section label from `serverless: preview` to `serverless: ga`.
  Do _not_ list both lifecycles.

:::::{tab-set}
::::{tab-item} Image
:::{image} ./images/example-lifecycle-changed.png
:screenshot:
:alt:
:::
::::
::::{tab-item} Code
````
---
applies_to:
  stack: ga
  serverless: ga
---

# Lens [lens]

[...]

### Assign colors to terms [assign-colors-to-terms]

```{applies_to}
<<<<<<< Updated upstream
stack: ga 9.1+, preview =9.0,
=======
stack: ga 9.1+, preview =9.0
>>>>>>> Stashed changes
serverless: ga
```

[...]

````
::::
:::::


## Functionality is removed [removed]

When the functionality described in any level of content is removed,
how to handle it varies by which lifecycle it was in before being removed and
whether the product/deployment mode is versioned or unversioned.

### If a GA or deprecated feature is removed from a versioned product

For example, we removed the `securitySolution:enableVisualizationsInFlyout` setting that was described on the
[Configure advanced settings](https://www.elastic.co/docs/solutions/security/get-started/configure-advanced-settings)
page from the Elastic Stack in 9.1.0 and from Serverless around the same time.
Since this this functionality is still available before 9.1.0, we need that content to continue to be
available to users on Elastic Stack earlier versions while communicating to users on newer versions
that it is no longer available.

:::::{tab-set}
::::{tab-item} Image
:::{image} ./images/example-removed-unversioned-exception.png
:screenshot:
:alt:
:::
::::
::::{tab-item} Code
````
---
applies_to:
  stack: all
  serverless:
    security: all
---

# Configure advanced settings for Elastic Security

[...]

## Access the event analyzer and Session View from the event or alert details flyout [visualizations-in-flyout]

```{applies_to}
stack: removed 9.1
serverless: removed
```

[...]
````
::::
:::::

### If a beta or technical preview feature is removed [beta-removed]

If the functionality was only ever available in beta or technical preview before being removed,
you can remove the content altogether regardless of whether it is versioned or unversioned.

### If a feature is removed from an unversioned product

If the functionality was only ever available in an unversioned product or deployment mode,
remove the content altogether.

## Code block content varies [code-block]

Often the content in a code block will vary between situations (versions, deployment types, etc).
There are a couple possible solutions.

### Solution A: Use a code callout [code-block-callout]

Using a code callout is the lightest-touch solution, but might not be sufficient in all cases.

**When to use a code callout**:

* The code block and its callouts fit vertically on a typical laptop screen.
  This will reduce the risk of users copying the code snippet without reading the information in the callout.
* Syntax is either just added or just removed — syntax is not modified.
  It is difficult to communicate that some syntax is needed in more than one situation but varies depending on the situation.
* The code block will not require more than 3 `applies_to`-related callouts.
  At that point, the code becomes more difficult to read and use.

**Best practices**:

* Place the badge at the beginning of the callout.

**Example**: On the [Entity Analytics](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-input-entity-analytics#_configuration_3) page, we added a new option to a code block that was only made available in 9.1.0.

::::{image} ./images/example-code-block-callout.png
:screenshot:
::::

### Solution B: Use applies switch tabs [code-block-tabs]

**When to use applies switch tabs**: If using a [code callout](#code-block-callout) isn't appropriate.

**Best practices**:

* Try to minimize the number of tabs where possible,
  but do not mix applies switch and `applies_to`-related code callouts.
* Try not to include information surrounding a code block in the tabs.
  Make the tab content as small as possible apart from the procedure itself.

**Example**: On the [Upstream OpenTelemetry Collectors and language SDKs](https://www.elastic.co/docs/solutions/observability/apm/upstream-opentelemetry-collectors-language-sdks#apm-connect-open-telemetry-collector) page, we use tabs to show two different code blocks: one for Serverless and one for Elastic Stack (stateful).

::::::{tab-set}
:::::{tab-item} Image
::::{image} ./images/example-code-block-tabs.png
:screenshot:
::::
:::::

:::::{tab-item} Code

Connect your OpenTelemetry Collector instances to Elastic {{observability}} or {{obs-serverless}} using the OTLP exporter:

````
::::{applies-switch}
:::{applies-item} stack: ga

```
[...]
```

:::
:::{applies-item} serverless: ga

```
[...]
```

:::
::::
````

:::::
::::::

## Workflows vary [workflow]

When one or more steps in a process differs.

### Solution A: Use inline `applies_to` [workflow-inline]

Using inline `applies_to` badges to a few line items in an ordered list is the lightest-touch solution,
but might not be sufficient in all cases.

**When to use inline `applies_to`**:

* Workflow steps that vary between situations can be easily isolated.
* Each step that varies, only varies between 3 or fewer situations (deployment types, versions, etc).
* There are no more than 3 steps that need to be split into multiple lines with `applies_to` badges.

**Best practices**:

* Follow the [best practices for ordered and unordered lists](badge-placement.md#ordered-and-unordered-lists)
  including the order of items and the placement of labels.

**Example**: Only one item in an ordered list varies between Serverless and stateful.

:::::{tab-set}

::::{tab-item} Image
:::{image} ./images/workflow-inline.png
:screenshot:
:::
::::

::::{tab-item} Code
```md
1. Get started:
    * {applies_to}`serverless: ga` In your {{obs-serverless}} project, go to **Add Data**.
    * {applies_to}`stack: ga` In {{kib}}, go to the **Observability** UI and click **Add Data**.
1. Under **What do you want to monitor?** select **Host**, and then select **Elastic Agent: Logs & Metrics**.
1. Copy the install command.
```
::::
:::::

### Solution B: Use applies switch tabs [workflow-tabs]

Applies switch tabs are minimally disruptive in many situations.

**When to use applies switch tabs**:

* Using [inline `applies_to` badges](#workflow-inline) isn't appropriate.
* All the tabs fit horizontally on a single row on a typical laptop screen.
  This is usually around a maximum of four tabs.
* The tab with the most content fits vertically on a typical laptop screen.
  This is usually around of 20 lines.

**Best practices**:

* Try to minimize the number of tabs where possible. Try to work around small differences by
  rewording or adding context in prose or in `note` style admonitions.
* Try not to include information surrounding a procedure in the tabs.
  Make the tab content as small as possible apart from the procedure itself.
* Consider breaking up procedures into sets of procedures if only one section differs between contexts.

**Example**: On the [Enable audit logging](https://www.elastic.co/docs/deploy-manage/security/logging-configuration/enabling-audit-logs#enable-audit-logging-procedure) page, we use applies switch tabs to show separate ordered lists outlining the workflow for each deployment type.

::::::{tab-set}

:::::{tab-item} Image
::::{image} ./images/example-workflow-tabs.png
:screenshot:
::::
:::::

:::::{tab-item} Code

```
::::{applies-switch}

:::{applies-item} ess: ga
[...]
:::

:::{applies-item} eck: ga
[...]
:::

:::{applies-item} ece: ga
[...]
:::

:::{applies-item} self: ga
[...]
:::

::::
```

:::::

::::::

### Solution C: Use sibling pages [workflow-sibling-pages]

Sibling pages are a last resort when no other solutions are appropriate.

**When to use sibling pages**:

* Neither [inline `applies_to` badges](#workflow-inline) or [applies switch tabs](#workflow-tabs) are appropriate.
* The workflow has significant differences across multiple procedures.
* There are chained procedures where not all of the procedures are needed for all contexts
  or where the flow across procedures is muddied when versioning context is added.
* The workflow exists in a very complex page that is already heavily using tabs and other tools we use for versioning differences.
  This makes it difficult to add another “layer” of content.
* Product lifecycle state changes like when technical preview or beta transitions to GA.

**Best practices**:

* Use consistent structure and terminology across sibling pages.
* Use redirects when one version becomes the primary approach.

**Example**: We use separate pages for ECH and Serverless billing information:

* [Cloud Hosted deployment billing dimensions](https://elastic.co/docs/deploy-manage/cloud-organization/billing/cloud-hosted-deployment-billing-dimensions)
* [{{serverless-short}} project billing dimensions](https://elastic.co/docs/deploy-manage/cloud-organization/billing/serverless-project-billing-dimensions)

## Screenshots vary [screenshot]

Sometimes the UI differs between versions, deployment types or other conditions.

### Solution A: Use applies switch tabs [screenshot-tabs]

**When to use applies switch tabs**:
* When the screenshot shows significantly different interfaces or workflows for each product, deployment type, or version.
* When the screenshot represents a specific, interactive action, like clicking a button or navigating a UI that changes meaningfully between contexts.

**Best practices**:
* Keep any explanatory text outside the tab unless it's specific to the screenshot inside.

**Example**: As of the Elastic Stack 9.1.0 release, there are no examples of this approach being used in live docs
except for with images used in workflows.

### Solution B: Add a note [screenshot-note]

In cases where only a small visual detail differs (for example, a button label or icon), it’s often more efficient to add a note rather than creating tabbed screenshots.

**When to use a note**:
* When the screenshot is mostly consistent, but includes minor visual or behavioral differences.
* When adding another screenshot would be redundant or distracting.

**Best practices**:
* Keep notes concise, ideally one sentence.
* Place the note directly after the screenshot.
* Use an `applies_to` badge at the start of the note if relevant.

**Example**: As of the Elastic Stack 9.1.0 release, there are no examples of this approach being used in live docs
except for with images used in workflows.

### Solution C: Keep the screenshot aligned with the latest version [screenshot-latest]

In cases where the screenshot is rather conceptually demonstrating a capability, it's fine not to version it.

For example, versioning the screenshot on the [Dashboards](https://www.elastic.co/docs/explore-analyze/dashboards) parent page would not add tremendous value unless the capability drastically evolves.

## Multiple adjacent block elements vary [multiple-block]

### Solution A: Use applies switch tabs [multiple-block-tabs]

**When to use applies switch tabs**:
* When the content is structurally similar but differs in detail — for example, slightly different instructions, outputs, or paths.
* When you want to avoid repeating most of the surrounding content and isolate just the difference.

**Best practices**:
* Only include content that varies inside the tab — don’t wrap entire pages or unrelated information.
* Keep tabs short and focused to reduce cognitive load.
* Label tabs clearly and consistently (e.g., by version or product).

% TO DO: Add example
% **Example**:
% <image>

### Solution B: Use headings [multiple-block-headings]

_Work in progress._

% TO DO: Add all sections
% **When to use headings**:
% **Best practices**:
% **Example**:

## Functionality is added to multiple patch versions [multiple-patch]

Sometimes, features and enhancements slip through into patch versions, and the same functionality might be added for the first time to multiple patch versions at the same time.

- **Standard case**: Our docs are aligned with the latest patch of any given minor version. That means that in most cases, we don't need to call out the exact patch version that introduced a change (that's for the release notes).
- **Exceptions**: In rare cases, it can happen that the change is important enough to be explicitly called out in the docs with a precise patch-level information. In that case, you can add a callout and indicate patch-level versions using plain text to explain the change.

For example, on the [HTTP JSON input](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-input-httpjson) page, the `terminate` helper function was added to a 9.0.x and 9.1.x patch version at the same time. Since the new functionality is available in the latest patch of both 9.0.x and 9.1.x, use the earlier version: 9.0.x.

:::::{tab-set}
::::{tab-item} Image
:::{image} ./images/example-multiple-patch.png
:screenshot:
:alt:
:::
::::
::::{tab-item} Code
```markdown
* `terminate`: exits the template without falling back to the default value
  and without causing an error. It takes a single string argument that is
  logged in debug logging. {applies_to}`stack: ga 9.1.2+!` {applies_to}`stack: ga 9.0.6+!`
```
::::
:::::
