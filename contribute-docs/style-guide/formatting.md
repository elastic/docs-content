---
navigation_title: Formatting
description: Guidelines for using consistent formatting across Elastic documentation.
---

# Formatting

As technical writers and contributors, it's our job to design our documentation to be user-friendly, accessible, and efficient so users can find what they need quickly and comprehend what they read. Consistent formatting—especially for components that highlight relationships between concepts, such as headings, images, tables, and lists—can help achieve this. 

## Line spacing

Enter a single line break between two elements, for example, between the end of a sentence and a new table. Unless it's required for Asciidoc, Markdown, or MDX syntax, you shouldn't need double spacing or indentation. Our stylesheets control the visual appearance of our docs, like font, colors, and sizing, so you don't have to worry about those, either. 

Use a single line break to control the spacing between paragraphs. In general, try to keep paragraphs short so users aren't overwhelmed with lengthy blocks of text. This is even more imperative if a user is on a mobile device. If your paragraph is more than seven lines, consider dividing it into two paragraphs.   

## Emphasis

Bold, italic, and monospace formatting helps users distinguish words and phrases from the surrounding text and provides visual cues for users. 

Use emphasis only in the text body, and avoid using it in titles and links. All titles must appear uniform so that users can scan them in the table of contents. By default, links are emphasized by rendering in a different color. Avoid applying multiple variations of emphasis to the same text. For example, when link text includes the name of a UI element, avoid using bold.

### Bold / strong

Use bold text formatting to emphasize the names of UI elements so that users can identify interactive components. 

| Element | Example |
| ------- | ------- |
| Apps | **Visualize** allows you to create visualizations of the data in your Elasticsearch indices. |
| Columns | In the **Value** column, go to the value you want to edit and click **Edit**. |
| Interactive UI functions | To use a dark color theme, click **Options** and select **Use dark theme**. |
| Key combinations | Press **Alt+C**. |
| Menu items | In Kibana, open the main menu, then click **Discover**. |
| Page names | The **Hosts** page provides a comprehensive overview of all hosts and host-related security events. |
| Sections | The **Document Summary** section provides general alert details, including any available threat intelligence data. |
| Tables | In the **Value lists** table, click the value list you want to edit. |
| Tabs | The **Overview** tab provides an overview of the alert and shows relevant threat intelligence details. |

:::::{note}
If the name of the UI element isn't explicitly shown in the UI, then don't bold it.
::::{dropdown} Example
The risk summary table shows the category, score, and number of risk inputs that determine the host risk score.
::::
:::::

### Italic / emphasis

Use italic text formatting to emphasize new words and concepts that are introduced to users for the first time, as well as titles of Elastic documentation resources.

| Element | Example |
| ------- | ------- |
| Terms | A Metricbeat *module* defines the basic logic for collecting data from a specific service. |

### Monospace / code

Use monospace text formatting to emphasize technical elements to help users differentiate code and command examples from regular text.

| API endpoints | The endpoints include `/_bulk` and `/INDEX/_bulk`. |
| --- | --- |
| Class names | Date fields are exposed as `ReadableDateTime`, so they support methods like `getYear`. |
| Code blocks | ```sh       GET _tasks       GET _tasks?nodes=nodeId1,nodeId2       GET _tasks?nodes=nodeId1,nodeId2&actions=cluster:*       ``` |
| Command invocations | To create the basic files for your metricset, run `make create-metricset`. |
| Command names |  The `elasticsearch-certutil` command simplifies the creation of certificates. |
| Configuration settings | For example, set `action.auto_create_index` to `+aaa*,-bbb*,+ccc*,-*`. |
| Data types | The example uses a strongly typed `int`. |
| Directory names and paths | The example harvests all files in the `/var/log/*.log` path. |
| Environment variables | Set the `ES_PATH_CONF` environment variable. |
| Error and validation messages | When you receive `Bulk Indexing of signals failed: [parent] Data too large`, the alerts payload is too large to process. |
| Field names | Filter by the `rule.section` field. |
| Function and method names | Date fields are exposed as `ReadableDateTime`, so they support methods like `getYear`. |
| Index names | The `.ml-notifications` index. |
| Inline code | To access the names, use `doc['first'].value` and `doc['last'].value`. |
| Parameter names | The query requires the `type` and `id` parameters. |
| Process names | Verify the `autodetect` process is running. |
| Property names | The following example uses the `DROP` command to omit the `_id` property from the results table. |
| Role names | * The `kibana_system` role is required.        * The `elastic` superuser. |
| User input | In the command line, enter `hello world`. |
| Variables | Access the original source for a field as `ctx._source.<field_name>`. |


## Lists and tables

Lists and tables are an effective way to structure and organize data. Consider the following guidelines when deciding which of these components to use.

Use a list:

* If the order of items is important, such as for step-by-step instructions.
* If the items you're listing don't need to be directly compared.
* When each item includes a short description.

Use a table:

* If users need to compare several items and you want to present their differences and similarities.
* When each item consists of three or more pieces of related data, such as parameter name, type, and description.
* If there isn't a simpler way to present your content, such as in a list or paragraph text.

## Lists

Lists are an excellent way to present related or sequential data that's easy to scan. A list should have at least two list items. Here are some general rules to follow:

* Introduce the list with a heading, a complete sentence, or a fragment that ends with a colon.
* Use parallel structures for list items. For example, don't use a combination of verbs and noun phrases to start each item in a list. Choose one or the other.
* Begin each list item with a capital letter (unless it's case-sensitive, such as a lowercase field or CLI command).
* Don't use a period at the end of list items unless they're complete sentences.
* If a list has run-in headings, end the run-in headings with a period or colon, and use bold formatting for them.

In Elastic documentation, we typically use two types of lists: bulleted and numbered lists.

### Bulleted lists

Use a bulleted list to group related items that can appear in any order or to describe options that users can choose from.

:::{dropdown} Examples

Alert suppression allows you to reduce the number of repeated or duplicate detection alerts created by these detection rule types:

* Custom query
* Threshold
* Indicator match
* Event correlation (non-sequence queries only)
* New terms

---

To create the visualizations in this tutorial, you'll use the following fields:

* `timestamp`
* `bytes`
* `referer.keyword`

---

On the **Dashboards** page, choose one of the following options:

* To start with an empty dashboard, click **Create dashboard**.
* To open an existing dashboard, click the dashboard **Title** you want to open.

---

Templates can include two types of filters:

* **Regular filter**: Like other Kibana KQL filters, defines both the source event field and its value.
* **Template filter**: Only defines the event field and uses a placeholder for the field's value.

:::

### Numbered lists

Use a numbered list for a sequence of steps or a procedure that's performed in a specific order.

:::{dropdown} Examples

Sample data sets come with sample visualizations, dashboards, and more to help you explore Kibana before you ingest or add your own data.

1. On the home page, click **Try sample data**.
1. Click **Other sample data sets**.
1. On the **Sample eCommerce orders** card, click **Add data**.

---

When security is enabled, you grant users access to reporting features with Kibana application privileges.

1. Enable application privileges in **Reporting**.
1. Create the reporting role.
    1. Open the main menu, then click **Stack Management**.
    1. Click **Roles → Create role**.
1. Specify the role settings.
    1. Enter the **Role name**. For example, `custom_reporting_user`.
    1. Specify the **Indices** and **Privileges**.
1. Add the Kibana privileges.
1. Click **Create role**.
1. Assign the reporting role to a user.

---

#### How is risk score calculated?

1. The risk scoring engine runs hourly to aggregate **Open** and **Acknowledged** alerts from the last 30 days.
1. The engine groups alerts by `host.name` or `user.name` and aggregates the individual alert risk scores.
1. The engine then verifies the entity's asset criticality level and updates the risk score based on this value.
1. Based on the two risk inputs, the risk scoring engine generates a single entity risk score of 0-100.

:::

## Tables

We use tables to present structured data, so it's easier for users to scan and compare it. A table should have at least two rows (excluding the header) and at least two columns. Here are some general rules to follow:

* Use a table header to explain what the rows and columns represent.
* Use parallel structures for table entries. For example, don't use a combination of verbs and noun phrases to start each table entry. Choose one or the other.
* Use sentence-style capitalization for table headers and table entries (unless they're case-sensitive, such as lowercase fields or CLI commands).
* Don't use a period at the end of table entries unless they're complete sentences.
* To give users context, introduce a table with a sentence that describes its purpose.
* Avoid overly complex tables with split or merged cells. If possible, use multiple tables instead.

:::{dropdown} Examples

To separate staging and production APM data, we need to create six filtered aliases—three aliases for each service environment:

| Index setting | `production` environment | `staging` environment |
| ------------- | ------------------------ | --------------------- |
| Error | `production-logs-apm` | `staging-logs-apm` |
| Span/transaction | `production-traces-apm` | `staging-traces-apm` |
| Metrics | `production-metrics-apm` | `staging-metrics-apm` |
 
---

Go to **Project Settings** to manage your connectors, data views, and other features.

| API keys | Create and manage keys that can send requests on behalf of users. | * Elasticsearch       * Observability       * Security |
| --- | --- | --- |
| Asset criticality | Bulk assign asset criticality to multiple entities by importing a text file. | Security |
| Connectors | Create and manage reusable connectors for triggering actions. | * Elasticsearch       * Observability       * Security |
| Data views | Manage the fields in the data views that retrieve your data from ((es)). | * Elasticsearch       * Observability       * Security |


:::


## Numbers

Write out numbers 1–9, and numerals for numbers 10 and greater, except for tables, decimals, dimensions, and most percentages. 

When your sentence includes numbers that are both less than and greater than 10, use numerals for consistency. 

:::{dropdown} Examples
  ❌ **Don't**: The watcher thread pool size is now five times the number of processors until 50 threads are reached.

  ✔️ **Do**: There are two ways to create and add panels. 
:::

### Separate large numbers with commas

Use a comma separator to make it easy for users to quickly and easily read large numbers.

:::{dropdown} Examples
  ❌ **Don't**: 1234567 users

  ✔️ **Do**: 1,234,567 users
:::

### Use numerals in tables

When you add numbers to a table, use only numerals so that users can quickly analyze the information.

:::{dropdown} Examples

  ❌ **Don't**:

  | Deployment | Instances | Nodes |
  | ---------- | --------- | ----- |
  | AWS        | 20        | Seven |
  | GCP        | 45        | Three |

  ✔️ **Do**:

  | Deployment | Instances | Nodes |
  | ---------- | --------- | ----- |
  | AWS        | 20        | 7     |
  | GCP        | 45        | 3     |

:::

### Decimals

Use numerals for decimals and pluralize the noun. When decimal numbers are less than one, include the zero before the decimal point. 

:::{dropdown} Examples
  ❌ **Don't**: One pixel

  ✔️ **Do**: 0.5 pixels
:::

### Dimensions

Use numerals for dimensions, separated by a lowercase *x* and without spaces.

:::{dropdown} Examples
  ❌ **Don't**: 16 X 9

  ✔️ **Do**: 16x9
:::

### Percentages

When using a percent in a sentence, use numerals and the percent sign, without a space. When starting a sentence with a percentage, write out the numeral and word percent.

:::{dropdown} Examples
  ❌ **Don't**: 30% of the memory must be free.

  ✔️ **Do**: Odds of a 0.50% increase are slim. 

  ✔️ **Do**: Thirty percent of the memory must be free. 
:::

## Code samples

Good code samples can be extremely valuable in developer documentation. They're a great way to illustrate how to implement specific features or functionality. Whenever possible, provide complete and runnable code samples that users can copy and test out themselves.

In general, follow the formatting rules of the language of the code sample. 

The following guidelines will help to ensure your code samples are clear, readable, and easily understandable.

### Use consistent indentation

Use spaces, not tabs, to indent code. Make sure that indentation is consistent throughout the code sample. For example, use 2 spaces per indentation level for JSON examples.

:::::{tip}

You can use online tools such as [JSON formatter](https://jsonformatter.org) to validate and format your code examples.

:::{dropdown} Example

```json
{
  "rule_id": "process_started_by_ms_office_program_possible_payload",
  "threat": [
    {
      "framework": "MITRE ATT&CK",
      "tactic": {
        "id": "TA0001",
        "reference": "https://attack.mitre.org/tactics/TA0001",
        "name": "Initial Access"
      },
      "technique": [
        {
          "id": "T1193",
          "name": "Spearphishing Attachment",
          "reference": "https://attack.mitre.org/techniques/T1193"
        }
      ]
    }
  ]
}
```
:::
:::::

### Apply syntax highlighting

Syntax highlighting improves readability of code samples by adding color highlighting relevant to the language of the sample. Where applicable, use the appropriate AsciiDoc or Markdown formatting for syntax highlighting.

For AsciiDoc, samples should be preceded by `[source,{format}]`, where `format` is one of:
`console`, `console-result`, `eql`, `esql`, `java`, `js`, `json`, `ruby`, `sh`, `shell`, `term`, `text`, `xml`, `yaml`, `yml`

:::{dropdown} Example

```asciidoc
[source,yaml]
----
path:
  data:
    - /mnt/elasticsearch_1
    - /mnt/elasticsearch_2
    - /mnt/elasticsearch_3
----
```

:::

For Markdown, specify a language next to the backticks that precede the code block.

:::{dropdown} Example

````markdown
```yaml
path:
  data:
    - /mnt/elasticsearch_1
    - /mnt/elasticsearch_2
    - /mnt/elasticsearch_3
```
````

:::

### Add comments and explanations

Where needed, you can include comments in code samples to explain specific parts of the code. To do this, use the comment syntax of the language of your code sample. For example, for single-line comments in Java, use two forward slashes (`//`). Add the comment before the line or group of lines it refers to.

:::{dropdown} Example

```java
WatcherBuild build = watcherStatsResponse.getBuild();

// The current size of the watcher execution queue
long executionQueueSize = watcherStatsResponse.getThreadPoolQueueSize();

// The maximum size the watcher execution queue has grown to
long executionQueueMaxSize = watcherStatsResponse.getThreadPoolQueueSize();

// The total number of watches registered in the system
long totalNumberOfWatches = watcherStatsResponse.getWatchesCount();

// Watcher state (STARTING, STOPPED or STARTED)
WatcherState watcherState = watcherStatsResponse.getWatcherState();
```

:::

For languages that don't support comments natively, such as JSON, you can add explanations about specific lines using [footnotes](./formatting.md).

:::{dropdown} Example

```json
{
  "_tags": [
    "endpoint", [^1]
    "os:windows" [^2]
  ],
  "comments": [],
  "description": "File exception for Windows",
  "entries": [
    {
      "field": "file.hash.sha1",
      "operator": "included",
      "type": "match",
      "value": "27fb21cf5db95ffca43b234affa99becc4023b9d"
    }
  ],
  "item_id": "trusted-windows-file",
  "list_id": "endpoint-exception-container",
  "name": "Trusted Windows file",
  "namespace_type": "agnostic", <3>
  "tags": [],
  "type": "simple"
}
```
1. Indicates this item is for endpoint rules.
2. Relevant OS.
3. Item accessible from all Kibana spaces.

:::

## Footnotes

A footnote is an annotation with additional information usually provided at the end of a page, section, or code sample. In general, avoid footnotes because they aren't accessible. 

Instead of a footnote, consider adding a link or putting the information in an admonition, like a note. If you _must_ use a footnote—for example, if you need to add a comment in a language that doesn't support them natively, like JSON—follow these guidelines:

* Keep footnotes short and concise. 
* If you have more than one footnote, number them in sequential order. 
* Offset the numeral with superscript. 
  
## Redaction of sensitive information

End-user documentation may contain screen captures and examples that show
real or realistic data. To prevent malicious actors from using this information
to attack Elastic systems, employees, partners, or customers, we must avoid
leaking sensitive information.

Sensitive information might include:

* Data about (or provided by) customers, including code samples and logs
* Data about Elastic employees or partners
* Passwords, tokens, or secrets
* Security certificates
* Host/port info about real systems
* Links to internal documents

:::::{tip}
  Fake security information is not considered sensitive, but may trigger alerts during scans.
:::::

Common examples of leaked data include:

* Screen captures that show employee or customer names and details
* Screen captures that expose user credentials or tokens
* Screen captures that show hostnames or IP addresses
* Example access logs that expose real data

### How to protect sensitive information

* Use a blur tool (or similar) to hide or mask sensitive data in screen
captures.
* Replace sensitive data in examples or text with generic, placeholder text.
For example: `myname@example.com:my-api-key`.
* Avoid showing realistic security data that might be flagged during scans. For
example, instead of showing a real web hook, use placeholder text:
`https://hooks.slack.com/services/T00000000/B00000000/<hash_code>`
* When possible, use domain names and IP addresses that are reserved for documentation.
For more information, refer to:
    * [RFC2606 - Reserved Top Level DNS Names](https://datatracker.ietf.org/doc/html/rfc2606)
    * [RFC5737 - IPv4 Address Blocks Reserved for Documentation](https://datatracker.ietf.org/doc/html/rfc5737)
    * [RFC3849 - IPv6 Address Blocks Reserved for Documentation](https://datatracker.ietf.org/doc/html/rfc3849)

