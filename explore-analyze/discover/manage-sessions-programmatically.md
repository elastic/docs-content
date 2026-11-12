---
navigation_title: Manage programmatically
description: Create and manage Discover sessions from code with the Discover sessions API, and see how it works with the Dashboards API and the data views APIs.
applies_to:
  serverless: ga
  stack: ga 9.6+
products:
  - id: kibana
type: overview
---

# Manage Discover sessions programmatically [manage-discover-sessions-programmatically]

If you keep your {{kib}} content in version control or deploy it from a pipeline, you can create and manage Discover sessions from code instead of saving each one by hand in **Discover**. Three APIs work together to do that:

| API | {{kib}} API docs | {{kib}} Serverless API docs | When to use it | What you get |
|---|---|---|---|---|
| Discover sessions API | [Open]({{kib-apis}}group/endpoint-discover-sessions) | [Open]({{kib-serverless-apis}}group/endpoint-discover-sessions) | Keeping sessions in version control and deploying them from CI/CD | Saved Discover session |
| Dashboards API | [Open](https://elastic.github.io/dashboards-api-spec/dashboards#tag/Dashboards) | [Open](https://elastic.github.io/dashboards-api-spec/dashboards#tag/Dashboards) | Showing a session on a dashboard that you also manage as code | Dashboard with a Discover session panel |
| Data views v2 API | [Open]({{kib-apis}}group/endpoint-data-views-v2) | [Open]({{kib-serverless-apis}}group/endpoint-data-views-v2) | Creating a saved data view that a session tab can use as its data source, before you deploy the session | Data view |

## Related pages

- [Save and manage Discover sessions](save-open-search.md)
- [Use Discover sessions in dashboards](use-sessions-in-dashboards.md)
- [Create dashboards programmatically](../dashboards/create-dashboards-programmatically.md)
- [Manage dashboards as code](../dashboards/manage-dashboards-as-code.md)
- [{{kib}} data views](../find-and-organize/data-views.md)
