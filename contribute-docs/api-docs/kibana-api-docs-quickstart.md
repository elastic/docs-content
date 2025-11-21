---
navigation_title: Kibana API docs
---

# Contribute to Kibana API docs locally

## Overview

The Kibana API documentation is created by merging multiple OpenAPI documents. This is a step-by-step local development workflow. While CI runs these steps automatically on PR branches in the `kibana` repo, working locally enables you to validate, preview and debug before submitting your changes.

The workflow you follow depends on which set of APIs you're updating:

::::{tab-set}
:group: kibana-workflow

:::{tab-item} Code-generated
:sync: code-generated

The core Kibana APIs are automatically generated from TypeScript route definitions in the codebase. Edit the `.ts` files in your plugin, and CI will regenerate the OpenAPI files when you push your PR. You can also run the generation locally for validation.
:::

:::{tab-item} Manual YAML
:sync: manual

Some teams, including Security and Observability, work with hand-edited YAML files in their plugin and package directories. For the complete list of files, refer to the [merge scripts](https://github.com/elastic/kibana/tree/main/oas_docs/scripts). 
:::
::::

 For more details, see the {{kib}} [OAS docs README](https://github.com/elastic/kibana/tree/main/oas_docs#kibana-api-reference-documentation).

## Quickstart

Follow these steps to contribute to Kibana API docs locally:

::::::::{stepper}

::::{step} Fork and clone the repository

1. [Fork the Kibana repository](https://github.com/elastic/kibana/fork) to your GitHub account.
2. Clone your fork locally:

    ```bash
    git clone https://github.com/YOUR_USERNAME/kibana.git
    cd kibana
    ```
3. Add the upstream repository as a remote:

    ```bash
    git remote add upstream https://github.com/elastic/kibana.git
    ```
::::

::::{step} Prepare your environment

Run this command to set up your Node.js environment:

```bash
nvm use
```

If you don't have Node.js installed, refer to the [Kibana development getting started guide](https://www.elastic.co/docs/extend/kibana/development-getting-started).
::::

::::{step} Install dependencies

```bash
yarn kbn bootstrap
```

:::{note}
If dependencies are broken or bootstrap fails, run `yarn kbn clean` first. For more troubleshooting guidance, refer to the [Kibana development getting started guide](https://www.elastic.co/docs/extend/kibana/development-getting-started).
:::
::::

::::::{step} Make your docs changes

:::::{tab-set}
:group: kibana-workflow

::::{tab-item} Code-generated
:sync: code-generated
Edit the TypeScript route definitions in your plugin code. Add JSDoc comments, request/response schemas, and examples as needed, per the [checklist](checklist.md).

:::{note}
**CI will automatically regenerate the OpenAPI files when you push your `.ts` changes.** The next two steps show how to capture the snapshot and add examples locally, which is useful for validating changes before pushing or debugging issues.
:::

::::

::::{tab-item} Manual YAML
:sync: manual
Edit the YAML files in the appropriate plugin or package directory. Refer to the README alongside each file for specific guidance on adding summaries, descriptions, tags, metadata, links, and examples.

In these README files, you'll also find instructions for generating intermediate bundle files that capture your changes, and that are later used to generate the full API documentation.

The YAML files with the content changes and the intermediate bundle files are the minimum set of files required for creating a pull request. Without the intermediate bundle files, the automation won't pick up the changes and won't generate the full API documentation.

Review the the [checklist](checklist.md) for best practices.

Once you've made your changes, skip the next two steps and proceed to "Generate docs".
::::

::::::

::::::{step} Add examples to your routes

Beyond schema definitions, providing concrete request and response examples significantly improves API documentation usability.

::::{dropdown} Inline TypeScript examples

For code-generated APIs, you can add examples directly in your route definitions. Examples are type-checked at development time, so shape errors are caught during authoring.

```typescript
.addVersion({
  version: '2023-10-31',
  options: {
    oasOperationObject: () => ({
      requestBody: {
        content: {
          'application/json': {
            examples: {
              fooExample1: {
                summary: 'An example foo request',
                value: {
                  name: 'Cool foo!',
                } as FooResource,
              },
            },
          },
        },
      },
    }),
  },
  // ...
})
```
::::
::::{dropdown} YAML examples

**For code-generated APIs**, reference a YAML file in your route definition:

```typescript
import path from 'node:path';

const oasOperationObject = () => path.join(__dirname, 'foo.examples.yaml');

.addVersion({
  version: '2023-10-31',
  options: {
    oasOperationObject,
  },
  validate: {
    request: {
      body: fooResource,
    },
    response: {
      200: {
        body: fooResourceResponse,
      },
    },
  },
})
```

**For manual YAML**, add examples directly in your YAML files in the appropriate plugin or package directory.

**Example YAML structure:**

```yaml
requestBody:
  content:
    application/json:
      examples: # Use examples (plural), not example (deprecated)
        fooExample:
          summary: Foo example
          description: An example request of creating foo
          value:
            name: 'Cool foo!'
            enabled: true
responses:
  200:
    content:
      application/json:
        examples:
          exampleResponse:
            summary: Successful response
            value:
              id: '12345'
              name: 'Cool foo!'
              enabled: true
```
::::

::::::

::::::{step} (optional) Capture code-generated output

:::::{tab-set}
:group: kibana-workflow

::::{tab-item} Code-generated
:sync: code-generated

:::{note}
**This step is optional.** CI will automatically capture the snapshot when you push your `.ts` changes. Running this locally is useful for validating changes before pushing or debugging issues.
:::

This step captures the OpenAPI specification that {{kib}} generates at runtime from your route definitions. It spins up a local {{es}} and {{kib}} cluster with your code changes. This generates the following output files in the `oas_docs` directory:

- `bundle.json`
- `bundle.serverless.json`

**Prerequisites:**
- [Docker](https://docs.docker.com/get-docker/) must be running
- If you're an Elastician, ensure you're logged into Docker with your Elastic account

To capture all the documented API paths, copy the command from [`capture_oas_snapshot.sh`](https://github.com/elastic/kibana/blob/main/.buildkite/scripts/steps/checks/capture_oas_snapshot.sh). For example:

```bash
node scripts/capture_oas_snapshot \
  --include-path /api/status \
  --include-path /api/alerting/rule/ \
  --include-path /api/alerting/rules \
  --include-path /api/actions \
  --include-path /api/security/role \
  --include-path /api/spaces \
  --include-path /api/streams \
  --include-path /api/fleet \
  --include-path /api/saved_objects/_import \
  --include-path /api/saved_objects/_export \
  --include-path /api/maintenance_window \
  --include-path /api/agent_builder
  --update
```

For faster iteration, you can capture the specific paths you're working on, though this minimized output should not be included in your pull request.
For example:

```bash
node scripts/capture_oas_snapshot --update --include-path /api/your/specific/path
```
::::

::::{tab-item} Manual YAML
:sync: manual

This step is not applicable for Manual YAML. Your YAML files are used directly. Skip to the next step.
::::

:::::
::::::

::::{step} Generate docs

Run these commands to merge the OpenAPI documentation files:

```bash
cd oas_docs
make api-docs
```

This generates the following files:

- `oas_docs/output/kibana.yaml`
- `oas_docs/output/kibana.serverless.yaml`

:::{tip}
Use `make help` to see available commands.
:::
::::

::::{step} Lint your docs

Run this command to lint your OpenAPI files:

```bash
node ../scripts/validate_oas_docs.js
```

You can limit the scope of APIs that the linter checks by using `--path` or `--only` options. For details and examples, add `--help`.

:::{tip}
When you open a pull request to submit API documentation changes, this linter runs in a CI check. It uses the `--assert-no-error-increase` option which causes the check to fail if the number of errors increases compared to the baseline.
:::
::::

::::{step} Preview the API docs

1. Ensure [`bump-cli`](https://www.npmjs.com/package/bump-cli) is installed and up to date:

    ```bash
    npm install -g bump-cli
    ```
2. Run this command to generate a short-lived URL preview hosted on Bump.sh:

    ```bash
    make api-docs-preview
    ```

::::

:::::{step} Open a pull request

Once you're satisfied with your docs changes, create a pull request:

::::{tab-set}
:group: kibana-workflow

:::{tab-item} Code-generated
:sync: code-generated
You have two options:
- Push only your `.ts` changes and let CI regenerate the OpenAPI files automatically
- Push both your `.ts` changes and locally-generated OpenAPI files together

The CI will validate your OpenAPI specs using the linter. Once approved, merge your changes and backport to the appropriate branches if needed.
:::

:::{tab-item} Manual YAML
:sync: manual
Push your edited YAML files. The CI will validate your OpenAPI specs using the linter. Once approved, merge your changes and backport to the appropriate branches if needed.
:::

:::::

::::::::
