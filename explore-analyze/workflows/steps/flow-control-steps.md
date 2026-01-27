---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn about flow control steps for controlling workflow execution order and logic.
---

# Flow control steps

Flow control steps allow you to add logic, conditionals, and loops to your workflows, making them dynamic and responsive to data. Use them to run different steps based on conditions, process items in bulk, or control timing.

The following flow control steps are available:

* **Conditional execution** (`if`): Run different steps based on boolean or {{kib}} Query Language (KQL) expressions
* **Loops and iteration** (`foreach`): Iterate over arrays or collections
* **Execution control** (`wait`): Pause step execution for a specified duration

## If

The `if` step evaluates a boolean or KQL expression and runs different steps based on whether the condition is true or false.

```yaml
steps:
  - name: conditionalStep
    type: if
    condition: <KQL expression>
    steps:
      # Steps to run if condition is true
    else:
      # Steps to run if condition is false (optional)
```

Refer to [](/explore-analyze/workflows/steps/if.md) for more information.

## Foreach

The `foreach` step iterates over an array, running a set of steps for each item in the collection.

```yaml
steps:
  - name: loopStep
    type: foreach
    foreach: <array expression>
    steps:
      # Steps to run for each item
      # Current item is available as 'foreach.item'
```

Refer to [](/explore-analyze/workflows/steps/foreach.md) for more information.

## Wait

The `wait` step pauses workflow execution for a specified duration before continuing to the next step.

```yaml
steps:
  - name: waitStep
    type: wait
    with:
      duration: "5s"
```

Refer to [](/explore-analyze/workflows/steps/wait.md) for more information.
