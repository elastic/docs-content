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

# Find and share cases [find-share-cases]

Locate specific cases using search, copy case IDs to share with colleagues, and push cases to external incident management systems.

## Search cases [search-cases]

The **Cases** page has a search bar for quickly finding cases and case data. You can search for case titles, descriptions, and IDs using keywords and text. 

:::{note}
:applies_to: {stack: ga 9.2+}
Cases are automatically assigned human-readable numeric IDs, which you can use for easier referencing. Each time you create a new case in your [space](docs-content://deploy-manage/manage-spaces.md), the case ID increments by one. 
    
IDs are assigned to cases by a background task that runs every 10 minutes, which can cause a delay in ID assignment, especially in spaces with many cases. You can find the case ID after the case's name and can use it while searching the Cases table.
:::

Note the following rules for search:

* **Keywords**: Searches for keywords (like case and alert IDs) must be exact.
* **Text**: Text searches (such as case titles and descriptions) are case-insensitive.
* **Syntax**: No special syntax is required when entering your search criteria.

{applies_to}`stack: ga 9.3` You can also search for alert and event IDs, observable values, case comments, and custom fields (text type only). For example, you can search for a specific IP address that's been specified as an observable, a colleague's comment, or the ID of an alert that's attached to the case.

## Filter cases [filter-cases]

To find cases that were created during a specific time range, use the date time picker above the Cases table. The default time selection is the last 30 days. Clicking **Show all cases** displays every case in your space. The action also adjusts the starting time range to the date of when the first case was created.

## Find the case UUID [cases-find-case-uuid]

Each case has a universally unique identifier (UUID) that you can copy and share. To copy a case's UUID to a clipboard, go to the **Cases** page and select **Actions** → **Copy Case ID** for the case you want to share. Alternatively, go to a case's details page, then from the **More actions** menu (…), select **Copy Case ID**.

## Send cases to external systems [send-cases-external]

To send a case to an external system, select the push button in the **External incident management system** section of the individual case page. This information is not sent automatically. If you make further changes to the shared case fields, you should push the case again.

For more information about configuring connections to external incident management systems, refer to [Configure case settings](manage-cases-settings.md).