---
navigation_title: Search and share
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/manage-cases.html
  - https://www.elastic.co/guide/en/security/current/cases-open-manage.html
  - https://www.elastic.co/guide/en/observability/current/manage-cases.html
  - https://www.elastic.co/guide/en/serverless/current/security-cases-open-manage.html
  - https://www.elastic.co/guide/en/serverless/current/observability-create-a-new-case.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: security
  - id: observability
  - id: cloud-serverless
description: Search, filter, and share cases with colleagues or external ticketing systems.
---

# Search and share cases [search-share-cases]

Quickly locate relevant cases and share them with others or external ticketing systems to streamline collaboration and handoffs.

## Search cases [search-cases]

The **Cases** page has a search bar for quickly finding cases and case data. You can search for case titles, descriptions, and IDs using keywords and text.

Note the following rules for search:

* **Keywords**: Searches for keywords (like case and alert IDs) must be exact.
* **Text**: Text searches (such as case titles and descriptions) are case-insensitive.
* **Multi-word terms**: If a term contains spaces, wrap it in quotation marks so it's treated as a single term. For example, `"Needs review"`.
* **Multiple criteria**: To search on more than one criterion at once, separate each term with a space.
* **Syntax**: No special syntax is required for general keyword and text searches. {applies_to}`stack: ga 9.5+` To target a field library field, use `label:value` syntax (described later).

### Search alerts, comments, and observables [search-case-related-data]

```{applies_to}
stack: ga 9.3+
```

You can also search for alert and event IDs, observable values, and case comments. For example, in {{elastic-sec}} you can search for a specific IP address that's been specified as an observable, a colleague's comment, or the ID of an alert that's attached to the case.

* {applies_to}`stack: ga 9.3-9.4` You can also search custom fields (text type only).
* {applies_to}`stack: ga 9.5+` For field library fields, see [Search template and field library values](#search-case-field-values).

### Search template and field library values [search-case-field-values]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

You can search by the values of [field library](create-case-field-library.md) fields (including values set by a [case template](manage-case-templates.md)). Use each field's **label** as it appears on the case, not its internal `name`. The `name` is what you use in YAML (for example, with `$ref`). Number, date, checkbox, and user-selection fields all support search, including numeric and date ranges.

To target a specific field, use `label:value` syntax. The left side is the field's label as it appears on the case; the right side is the value to match. For example, the following finds cases where the field labeled `Team` is set to `A1`:

```text
"Team":"A1"
```

Unlike general text search, `label:value` searches are case-sensitive. For example, `"Team":"A1"` matches `A1`, not `a1`. You can mix `label:value` pairs with free-text terms in the same query:

```text
"Team":"A1" "Priority":"High" phishing "Escalation reason"
```

Substring matches also work. For example, `"Summary":"network"` matches a text area whose value contains "network".

## Filter cases [filter-cases]

You can filter cases by attributes such as assignees, categories, severity, status, and tags. 

{applies_to}`stack: ga 9.3+` To find cases created during a specific time range, use the date time picker above the Cases table. The default selection is the last 30 days—click **Show all cases** to display every case in your space.

## Send cases to external systems [send-cases-external]

To send a case to an external system, select the push button in the **External incident management system** section of the individual case page. This information is not sent automatically. If you make further changes to the shared case fields, you should push the case again.

For more information about configuring connections to external incident management systems, refer to [Configure case settings](configure-case-settings.md).

## Use case identifiers [case-identifiers]

Cases have two types of identifiers:

* {applies_to}`stack: ga 9.2+` **Numeric ID**: A short, human-readable number that appears after the case name. Use it for quick reference in conversations or searches. Numeric IDs increment by one for each new case in your [space](docs-content://deploy-manage/manage-spaces.md) and are assigned by a background task that runs every 10 minutes.
* **UUID**: A longer alphanumeric identifier for the [cases API]({{kib-apis}}group/endpoint-cases). Copy it from **Actions** → **Copy Case ID** on the Cases page or from the action menu {icon}`boxes_horizontal` in a case.