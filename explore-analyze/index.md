---
applies_to:
  stack: ga
  serverless: ga
mapped_urls:
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-explore-your-data.html
  - https://www.elastic.co/guide/en/kibana/current/introduction.html#visualize-and-analyze
  - https://www.elastic.co/guide/en/kibana/current/get-started.html
  - https://www.elastic.co/guide/en/kibana/current/accessibility.html
---

# Explore and analyze

% What needs to be done: Write from scratch

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/docs-content/serverless/elasticsearch-explore-your-data.md
% - [ ] ./raw-migrated-files/kibana/kibana/introduction.md

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):

$$$elasticsearch-explore-your-data-visualizations-save-to-the-visualize-library$$$

The Elasticsearch platform and its UI, also known as Kibana, provide a comprehensive suite of tools to help you search, interact with, explore, and analyze your data effectively. These features empower you to gain deep insights, uncover trends, and take actionable steps based on your findings. This page is an overview of the key capabilities.

:::{dropdown} Accessibility statement

Elastic is committed to ensuring digital accessibility for people with disabilities. We are continually improving the user experience, and strive toward ensuring our tools are usable by everyone.

**Measures to support accessibility**
Elastic takes the following measures to ensure accessibility of Kibana:

* Maintains and incorporates an [accessible component library](https://elastic.github.io/eui/).
* Provides continual accessibility training for our staff.
* Employs a third-party audit.

**Conformance status**
Kibana aims to meet [WCAG 2.1 level AA](https://www.w3.org/WAI/WCAG21/quickref/?currentsidebar=%23col_customize&levels=aaa&technologies=server%2Csmil%2Cflash%2Csl) compliance. Currently, we can only claim to partially conform, meaning we do not fully meet all of the success criteria. However, we do try to take a broader view of accessibility, and go above and beyond the legal and regulatory standards to provide a good experience for all of our users.

**Feedback**
We welcome your feedback on the accessibility of Kibana. Please let us know if you encounter accessibility barriers on Kibana by either emailing us at `accessibility@elastic.co` or opening [an issue on GitHub](https://github.com/elastic/kibana/issues/new?labels=Project%3AAccessibility&template=Accessibility.md&title=%28Accessibility%29).

**Technical specifications**
Accessibility of Kibana relies on the following technologies to work with your web browser and any assistive technologies or plugins installed on your computer:

* HTML
* CSS
* JavaScript
* WAI-ARIA

**Limitations and alternatives**
Despite our best efforts to ensure accessibility of Kibana, there are some limitations. Please [open an issue on GitHub](https://github.com/elastic/kibana/issues/new?labels=Project%3AAccessibility&template=Accessibility.md&title=%28Accessibility%29) if you observe an issue not in this list.

Known limitations are in the following areas:

* **Charts**: We have a clear plan for the first steps of making charts accessible. We’ve opened this [Charts accessibility ticket on GitHub](https://github.com/elastic/elastic-charts/issues/300) for tracking our progress.
* **Maps**: Maps might pose difficulties to users with vision disabilities. We welcome your input on making our maps accessible. Go to the [Maps accessibility ticket on GitHub](https://github.com/elastic/kibana/issues/57271) to join the discussion and view our plans.
* **Tables**: Although generally accessible and marked-up as standard HTML tables with column headers, tables rarely make use of row headers and have poor captions. You will see incremental improvements as various applications adopt a new accessible component.
* **Color contrast**: Modern Kibana interfaces generally do not have color contrast issues. However, older code might fall below the recommended contrast levels. As we continue to update our code, this issue will phase out naturally.

To see individual tickets, view our [GitHub issues with label "`Project:Accessibility`"](https://github.com/elastic/kibana/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc+label%3AProject%3AAccessibility).

**Assessment approach**
Elastic assesses the accessibility of Kibana with the following approaches:

* **Self-evaluation**: Our employees are familiar with accessibility standards and review new designs and implemented features to confirm that they are accessible.
* **External evaluation**: We engage external contractors to help us conduct an independent assessment and generate a formal VPAT. Please email `accessibility@elastic.co` if you’d like a copy.
* **Automated evaluation**: We are starting to run [axe](https://www.deque.com/axe/) on every page. See our current progress in the [automated testing GitHub issue](https://github.com/elastic/kibana/issues/51456).

Manual testing largely focuses on screen reader support and is done on:

* VoiceOver on MacOS with Safari, Chrome and Edge
* NVDA on Windows with Chrome and Firefox

:::

## Querying and filtering

Elasticsearch’s robust query capabilities enable you to retrieve specific data from your datasets. Using the Query DSL (Domain Specific Language), you can build powerful, flexible queries that support:

* Full-text search
* Boolean logic
* Fuzzy matching
* Proximity searches
* Semantic search
* …and more.

These tools simplify refining searches and pinpointing relevant information in real-time.

### Aggregations

Aggregations provide advanced data analysis, enabling you to extract actionable insights. With aggregations, you can calculate statistical metrics (for example, sums, averages, medians), group data into buckets (histograms, terms, and so on), or perform nested and multi-level analyses. Aggregations transform raw data into structured insights with ease.

## Geospatial Analysis

The geospatial capabilities enable analysis of location-based data, including distance calculations, polygon and bounding box queries, and geohash grid aggregations. This functionality is necessary for logistics, real estate, and IoT industries, where location matters.

## Machine Learning

Elasticsearch integrates machine learning for proactive analytics, helping you to:
* Detect anomalies in time-series data
* Forecast future trends
* Analyze seasonal patterns
* Perform powerful NLP operations such as semantic search
* Machine learning models simplify complex predictive tasks, unlocking new opportunities for optimization.

## Scripting

Scripting makes custom data manipulation and transformation possible during search and aggregation processes. Using scripting languages like Painless, you can calculate custom metrics, perform conditional logic, or adjust data dynamically in search time. This flexibility ensures tailored insights specific to your needs.

## Explore with Discover [explore-the-data]

[Discover](/explore-analyze/discover.md) lets you interact directly with raw data. Use Discover to:

* Browse documents in your indices
* Apply filters and search queries
* Visualize results in real-time

It’s the starting point for exploratory analysis.

## Visualize the data [view-and-analyze-the-data]

Create a variety of visualizations and add them to a dashboard.

### Dashboards
[Dashboards](/explore-analyze/dashboards.md) serve as centralized hubs for visualizing and monitoring data insights. With Dashboards, you can:

* Combine multiple visualizations into a single, unified view
* Display data from multiple indices or datasets for comprehensive analysis
* Customize layouts to suit specific workflows and preferences

Dashboards provide an interactive and cohesive environment with filtering capabilities and controls to explore trends and metrics at a glance.

### Panels and visualizations

[Panels and visualizations](/explore-analyze/visualize.md) are the core elements that populate your dashboards, enabling dynamic data representation. They support diverse chart types, Interactive filtering, and drill-down capabilities to explore data further. These building blocks transform raw data into clear, actionable visuals, allowing users to analyze and interpret results effectively.

## Reporting and sharing

You can share your work and findings with colleagues and stakeholders or generate reports. Report generation can be scheduled or on-demand. You can choose from multiple formats (for example, PDF, CSV). These tools ensure that actionable insights reach the right people at the right time.
Alerting
You can set up alerts to monitor your data continuously. Alerts notify you when specific conditions are met. This ensures timely action on critical issues.

## Bringing it all together

Elasticsearch's features integrate seamlessly, offering an end-to-end solution for exploring, analyzing, and acting on data. If you want to explore any of the listed features in greater depth, refer to their respective documentation pages and check the provided hands-on examples and tutorials.

If you'd like to explore some features but don't have data ready yet, some sample data sets are available in {{kib}} for you to install and play with.

### Add sample data [gs-get-data-into-kibana]

Sample data sets come with sample visualizations, dashboards, and more to help you explore {{kib}} before you ingest or add your own data.

1. Open the **Integrations** page from the navigation menu or using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the list of integrations, select **Sample Data**.
3. On the page that opens, select **Other sample data sets**.
4. Install the sample data sets that you want.

Once installed, you can access the sample data in the various {{kib}} apps available to you.
