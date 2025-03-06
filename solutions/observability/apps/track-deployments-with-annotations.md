---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/apm-transactions-annotations.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-track-deployments-with-annotations.html

navigation_title: "Track deployments with annotations"
---

# Track deployments with annotations [apm-transactions-annotations]

::::{note}

**For Observability Serverless projects**, the **Admin** role or higher is required to create and manage annotations. To learn more, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::

:::{image} ../../../images/observability-apm-transaction-annotation.png
:alt: Example view of transactions annotation in the Applications UI
:class: screenshot
:::

For enhanced visibility into your deployments, we offer deployment annotations on all transaction charts. This feature enables you to easily determine if your deployment has increased response times for an end-user, or if the memory/CPU footprint of your application has changed. Being able to quickly identify bad deployments enables you to rollback and fix issues without causing costly outages.

By default, automatic deployment annotations are enabled. This means APM will create an annotation on your data when the `service.version` of your application changes.

Alternatively, you can explicitly create deployment annotations with our annotation API. The API can integrate into your CI/CD pipeline, so that each time you deploy, a POST request is sent to the annotation API endpoint.

Refer to the [annotation API reference](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-apm-annotations) for more information.

::::{note}
If custom annotations have been created for the selected time period, any derived annotations, i.e., those created automatically when `service.version` changes, will not be shown.

::::