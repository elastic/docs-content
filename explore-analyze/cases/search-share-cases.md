---
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
---

# Search and share cases [search-share-cases]

Quickly locate relevant cases and share them with colleagues or external ticketing systems to streamline collaboration and handoffs.

## Search cases [search-cases]

The **Cases** page has a search bar for quickly finding cases and case data. You can search for case titles, descriptions, and IDs using keywords and text. 

Note the following rules for search:

* **Keywords**: Searches for keywords (like case and alert IDs) must be exact.
* **Text**: Text searches (such as case titles and descriptions) are case-insensitive.
* **Syntax**: No special syntax is required when entering your search criteria.

{applies_to}`stack: ga 9.3` You can also search for alert and event IDs, observable values, case comments, and custom fields (text type only). For example, you can search for a specific IP address that's been specified as an observable, a colleague's comment, or the ID of an alert that's attached to the case.

## Filter cases [filter-cases]

You can filter cases by attributes such as assignees, categories, severity, status, and tags. 

{applies_to}`stack: ga 9.3` To find cases created during a specific time range, use the date time picker above the Cases table. The default selection is the last 30 days—click **Show all cases** to display every case in your space.

## Send cases to external systems [send-cases-external]

To send a case to an external system, select the push button in the **External incident management system** section of the individual case page. This information is not sent automatically. If you make further changes to the shared case fields, you should push the case again.

For more information about configuring connections to external incident management systems, refer to [Configure case settings](configure-case-settings.md).

## Use case identifiers [case-identifiers]

Cases have two types of identifiers:

* {applies_to}`stack: ga 9.2+` **Numeric ID**: A short, human-readable number that appears after the case name. Use it for quick reference in conversations or searches. Numeric IDs increment by one for each new case in your [space](docs-content://deploy-manage/manage-spaces.md) and are assigned by a background task that runs every 10 minutes.
* **UUID**: A longer alphanumeric identifier for the [cases API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-cases). Copy it from **Actions** → **Copy Case ID** on the Cases page or from the action menu {icon}`boxes_horizontal` in a case.