---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn how to get started creating Elastic workflows. 
---

# Get started with workflows [workflows-get-started]

In this tutorial, you'll create a workflow that indexes and searches through national parks data, demonstrating the core concepts and capabilities of workflows along the way.

## Prerequisites [workflows-prerequisites]

- To use workflows, turn on the Elastic Workflows [advanced setting](kibana://reference/advanced-settings.md#kibana-general-settings) (`workflows:ui:enabled`).   
- You must have the appropriate subscription. Refer to the subscription page for [Elastic Cloud](https://www.elastic.co/subscriptions/cloud) and [Elastic Stack/self-managed](https://www.elastic.co/subscriptions) for the breakdown of available features and their associated subscription tiers.

## Tutorial [workflows-tutorial]

:::::{stepper}

::::{step} Go to Worfklows

To access the **Worfklows** page, find **Workflows** in the navigation menu or using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

::::

::::{step} Create a new workflow

Click **Create a new workflow**. The YAML editor opens.

<!-- TODO: Add screenshot of YAML editor interface -->

::::

::::{step} Define your workflow

Remove the placeholder content and copy and paste the following YAML into the editor:

```yaml
name: 🏔️ National Parks Demo
description: Creates an Elasticsearch index, loads sample national park data using bulk operations, searches for parks by category, and displays the results.
enabled: true
tags: ["demo", "getting-started"]
consts:
  indexName: national-parks
triggers:
  - type: manual
steps:
  - name: get_index
    type: elasticsearch.indices.exists
    with:
      index: "{{ consts.indexName }}"
  - name: check_if_index_exists
    type: if
    condition: 'steps.get_index.output : true'
    steps:
      - name: index_already_exists
        type: console
        with:
          message: "index: {{ consts.indexName }} already exists. Will proceed to delete it and re-create"
      - name: delete_index
        type: elasticsearch.indices.delete
        with:
          index: "{{ consts.indexName }}"
    else:
      - name: no_index_found
        type: console
        with:
          message: "index: {{ consts.indexName }} Not found. Will proceed to create"
       
  - name: create_parks_index
    type: elasticsearch.indices.create
    with:
      index: "{{ consts.indexName }}"
      mappings:
        properties:
          name: { type: text }
          category: { type: keyword }
          description: { type: text }
  - name: bulk_index_park_data
    type: elasticsearch.bulk
    with:
      index: "{{ consts.indexName }}"
      operations:
        - name: "Yellowstone National Park"
          category: "geothermal"
          description: "America's first national park, established in 1872, famous for Old Faithful geyser and diverse wildlife including grizzly bears, wolves, and herds of bison and elk."

        - name: "Grand Canyon National Park"
          category: "canyon"
          description: "Home to the immense Grand Canyon, a mile deep gorge carved by the Colorado River, revealing millions of years of geological history in its colorful rock layers."

        - name: "Yosemite National Park"
          category: "mountain"
          description: "Known for its granite cliffs, waterfalls, clear streams, giant sequoia groves, and biological diversity. El Capitan and Half Dome are iconic rock formations."
         
        - name: "Zion National Park"
          category: "canyon"
          description: "Utah's first national park featuring cream, pink, and red sandstone cliffs soaring into a blue sky. Famous for the Narrows wade through the Virgin River."
         
        - name: "Rocky Mountain National Park"
          category: "mountain"
          description: "Features mountain environments, from wooded forests to mountain tundra, with over 150 riparian lakes and diverse wildlife at various elevations."
  - name: search_park_data
    type: elasticsearch.search
    with:
      index: "{{ consts.indexName }}"
      size: 5
      query:
        term:
          category: "canyon"
  - name: log_results
    type: console
    with:
      message: |-
        Found {{ steps.search_park_data.output.hits.total.value }} parks in category "canyon".
  - name: loop_over_results
    type: foreach
    foreach: "{{steps.search_park_data.output.hits.hits | json}}"
    steps:
      - name: process-item
        type: console
        with:
          message: "{{foreach.item._source.name}}"
```

::::

::::{step} Save your workflow

Click **Save**. Your workflow is now ready to run.

::::

::::{step} Run your workflow

Click the **Run** icon {icon}`play` (next to **Save**) to execute your workflow.

::::

::::{step} Monitor execution

As your workflow runs, execution logs display in a panel next to your workflow. In the panel, you can find:

* **Real-time execution logs**: Each step appears as it executes.
* **Step status indicators**: Green checkmarks for success, timestamps for duration.
* **Expandable step details**: Click any step to see input, output, and timeline.

::::

::::{step} View execution history

To examine past executions:

1. Click the **Executions** tab.
2. View a list of all workflow runs (including pending and in progress runs), along with their status and completion time.
3. Click any execution to see its detailed logs.

<!-- TODO: Add screenshot showing failed execution with error details -->

::::

:::::

## Understand what happened

Let's examine each part of our first workflow to understand how it works.

### Workflow metadata

```yaml
name: 🏔️ National Parks Demo
description: Creates an Elasticsearch index, loads sample national park data using bulk operations, searches for parks by category, and displays the results.
enabled: true
tags: ["demo", "getting-started"]
```

* **`name`**: A unique identifier for your workflow.
* **`description`**: Explains the workflow's purpose.
* **`enabled`**: Controls whether the workflow can be run.
* **`tags`**: Labels for organizing and finding workflows.

### Constants

```yaml
consts:
  indexName: national-parks-data
```

* **`consts`**: Defines reusable values that can be referenced throughout the workflow.
* Accessed using template syntax: `{{ consts.indexName }}`. This promotes consistency and makes the workflow easier to maintain.

### Trigger

```yaml
triggers:
  - type: manual
```

* **`triggers`**: Defines how the workflow starts.
* **`manual`**: Specifies the trigger type. Manual triggers require explicit user action (clicking the **Run** icon {icon}`play`) to start a workflow.

### Step 1: Create index

```yaml
- name: create_parks_index
  type: elasticsearch.indices.create
  with:
    index: "{{ consts.indexName }}"
    settings:
      number_of_shards: 1
      number_of_replicas: 0
    mappings:
      properties:
        name: { type: text }
        category: { type: keyword }
        description: { type: text }
```

* **Step type**: This is an action step that directly interacts with {{es}}.
* **Step purpose**: Establishes the data structure for our park information, ensuring fields are properly typed for searching and aggregation.
* **Key elements**:
    * Uses `elasticsearch.indices.create`, which is a built-in action that maps to the {{es}} Create Index API.
    * Defines mappings to control how data is indexed (`text` for full-text search, `keyword` for exact matching).
    * References the constant `indexName` for consistency.
    * Sets index settings for optimal performance in this demo.

### Step 2: Bulk index documents

```yaml
- name: bulk_index_park_data
  type: elasticsearch.bulk
  with:
    index: "{{ consts.indexName }}"
    operations:
      - name: "Yellowstone National Park"
        category: "geothermal"
        description: "America's first national park, established in 1872..."
      - name: "Grand Canyon National Park"
        category: "canyon"
        description: "Home to the immense Grand Canyon..."
      # ... additional parks
```

* **Step type**: Another internal action step using {{es}}'s bulk API.
* **Step purpose**: Efficiently loads multiple documents in a single operation, populating our index with sample data.
* **Key elements**:
    * The `operations` array contains the documents to index.
    * Each document becomes a searchable record in {{es}}.
    * Uses the field names defined in our mappings (`name`, `category`, `description`).
    * Each document becomes a searchable record with consistent field structure.
    * This step demonstrates how to handle batch operations in workflows.

### Step 3: Search parks

```yaml
- name: search_park_data
  type: elasticsearch.search
  with:
    index: "{{ consts.indexName }}"
    size: 5
    query:
      term:
        category: "canyon"
```

* **Step type**: Internal action step for querying {{es}}.
* **Step purpose**: Retrieves specific data based on criteria, demonstrating how workflows can make decisions based on data.
* **Key elements**:
    * Searches for parks with category `"canyon"` (will find Grand Canyon and Zion).
    * Results are automatically available to subsequent steps via `steps.search_park_data.output`.
    * Limits results to 5 documents for manageable output.
    * Shows how workflows can filter and process data dynamically.

### Step 4: Log results

```yaml
- name: log_results
  type: console
  with:
    message: |-
      Found {{ steps.search_park_data.output.hits.total.value }} parks in category "canyon".
      Top results: {{ steps.search_park_data.output.hits.hits | json(2) }}
```

* **Step type**: A console step for output and debugging.
* **Step purpose**: Presents the results in a human-readable format, demonstrating how to access and format data from previous steps.
* **Key elements**:
    * Template variables access the search results: `{{ steps.search_park_data.output }}`.
    * The `| json(2)` filter formats JSON output with indentation.
    * Uses the exact step name `search_park_data` to reference previous step output.
    * Shows how data flows through the workflow and can be transformed.

## Key concepts demonstrated

This workflow introduces several fundamental concepts:

* **Action steps**: Built-in steps that interact with {{es}} and {{kib}} APIs.
* **Data flow**: How information moves from step to step using outputs and template variables.
* **Constants**: Reusable values that make workflows maintainable.
* **Template syntax**: The `{{ }}` notation for dynamic values.
* **Step chaining**: How each step builds on previous ones to create a complete process.

% ## What's next?

% Now that you have a working workflow, you're ready to explore more advanced features. In the following sections, you'll build upon this National Parks example to demonstrate:

% * [**Triggers**](./triggers.md): Automate when this workflow runs (daily reports, alert responses).
% * [**Stes**](./steps.md): Add conditional logic based on search results and send notifications about park data.
% * [**Data and error handling**](./data.md): Make the workflow resilient to failures.
