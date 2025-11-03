Admonitions support the `applies_to` property to indicate which products or versions the information applies to.

:::::{tab-set}

::::{tab-item} Output

:::{note}
:applies_to: stack: ga 9.1.0

This note applies to the Elastic Stack GA version 9.1.0.
:::

:::{warning}
:applies_to: serverless: ga

This warning applies to serverless GA.
:::

:::{tip}
:applies_to: { ess:, ece: }

This tip applies to ECH and ECE.
:::

:::{important}
:applies_to: {"stack": "ga 9.2, preview 9.1", "serverless": "ga"}

This important note applies to Elastic Stack GA version 9.2 and Elastic Stack Preview version 9.1. It also applies to serverless GA.
:::

::::

::::{tab-item} Markdown

```markdown
:::{note}
:applies_to: stack: ga 9.1.0

This note applies to the Elastic Stack GA version 9.1.0.
:::

:::{warning}
:applies_to: serverless: ga

This warning applies to serverless GA.
:::

:::{tip}
:applies_to: { ess:, ece: }

This tip applies to ECH and ECE.
:::

:::{important}
:applies_to: {"stack": "ga 9.2, preview 9.1", "serverless": "ga"}

This important note applies to Elastic Stack GA version 9.2 and Elastic Stack Preview version 9.1. It also applies to serverless GA.
:::
```

::::

:::::