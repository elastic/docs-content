---
navigation_title: Test and validate
description: Test the migrated solution with representative clients and decide whether to refine, recreate, or keep the Serverless destination.
applies_to:
  serverless: ga
products:
  - id: cloud-serverless
type: how-to
---

# Test and validate the destination [migrate-to-serverless-validation]

**Serverless migration process**

:::{image} /deploy-manage/images/serverless-migration-navigation-grouped-test-and-validate.svg
:alt: Assess, create project, prepare and test, and switch to production. The preparation cycle runs from Prepare to Transfer data to Test and validate and back to Prepare. Test and validate is the current procedure.
:::

Previous: [Prepare destination](migrate-to-serverless-prepare.md) · Next: [Switch to production](migrate-to-serverless-production.md)

Verify the complete solution before changing production connections, then use the results to decide whether to refine, recreate, or keep the destination project.

% TBD: now that test and validate has its own document we can structure it better (pending)

:::::{stepper}

::::{step} Verify the solution with test clients
:anchor: migrate-to-serverless-test

The checks for each asset confirm that individual resources are ready. Use test clients to verify that they work together as a solution before changing production connections. Apply the following checklist to the features you use, using representative data from the copies already transferred and from test ingestion:

- [ ] **Client connections and permissions:** Test at least one instance of each client type used in the source. Run a test application for each client library you use, enroll a test {{agent}} in a destination policy, and test your Beats and Logstash configurations where applicable. Confirm that each client connects, authenticates, and performs its required operations with the intended permissions. Check that transient `429` responses trigger retries with exponential backoff and that persistent failures are reported.
- [ ] **Serverless client compatibility:** Remove custom `routing` parameters from requests and replace any application behavior that depends on them. If browser applications send requests directly to {{es}}, route them through a backend service because CORS is unavailable. Refer to [Serverless architectural differences](differences-from-other-elasticsearch-offerings.md#architectural-differences).
- [ ] **Indexing and processing:** Send representative documents and confirm that they reach the intended indices or data streams with the expected fields and values. Include examples that exercise enrich, inference, and failure handling where applicable. To investigate pipeline processing, use [the simulate pipeline API]({{es-serverless-apis}}operation/operation-ingest-simulate) with documents as they arrive before processing. Test `@custom` extensions through the integration pipeline that calls them.
- [ ] **Application queries:** Run the searches, filters, and aggregations your applications use. Compare source and destination results for the same transferred dataset and time range, accounting for any intentional changes.
- [ ] **Kibana experience:** Open the dashboards and views your users rely on in each required space. Check that they show the expected data and that filters, links, and navigation work with the migrated resources.
- [ ] **Solution features:** Run controlled tests of the rules, workflows, machine learning jobs, and inference features you use. Confirm the expected results and use test destinations for notifications or other external actions.
- [ ] **Performance testing (optional):** If performance is critical to your migration decision, consider additional load testing based on your requirements and testing resources. Include queries over recent and historical data. For {{es}} projects, test with the intended [Search Power and Search Boost Window settings](project-settings.md#elasticsearch-manage-project-search-ai-lake-settings), which affect search resources and the volume of data kept search-ready.

Record the results, unresolved issues, and any scenarios you have not tested. Use this record to [decide how to proceed](#migrate-to-serverless-reuse).

::::

::::{step} Evaluate the destination and decide how to proceed
:anchor: migrate-to-serverless-reuse

Use the test results to decide your next action:

- **Continue preparing:** If the solution needs changes, return to the relevant [preparation steps](migrate-to-serverless-prepare.md) and repeat the affected tests.
- **Recreate the project:** If you want to start from a clean destination, [create a new project](migrate-to-serverless-create-project.md) using the setup you tested, repeat [preparation](migrate-to-serverless-prepare.md), and verify it again.
- **Keep the tested project:** If you intend to use it for production, identify test data and provisional copies to remove, verified copies of stable data to retain, and any configuration to update.

Once the destination is validated and you have identified the data and configuration still to transfer, continue to [Complete the migration and switch to production](migrate-to-serverless-production.md).

::::

:::::
