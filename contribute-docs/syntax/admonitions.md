# Admonitions

Admonitions allow you to highlight important information with varying levels of priority. In software documentation, these blocks are used to emphasize risks, provide helpful advice, or share relevant but non-critical details.

## Basic admonitions

Admonitions can span multiple lines and support inline formatting.
Available admonition types include:

- [Note](#note)
- [Warning](#warning)
- [Tip](#tip)
- [Important](#important)
- [Plain](#plain)

### Note

A relevant piece of information with no serious repercussions if ignored.


:::::{tab-set}

::::{tab-item} Output

:::{note}
This is a note.
It can span multiple lines and supports inline formatting.
:::

::::

::::{tab-item} Markdown

```markdown
:::{note}
This is a note.
It can span multiple lines and supports inline formatting.
:::
```

::::

:::::

### Warning

You could permanently lose data or leak sensitive information.

:::::{tab-set}

::::{tab-item} Output

:::{warning}
This is a warning.
:::

::::

::::{tab-item} Markdown

```markdown
:::{warning}
This is a warning.
:::
```

::::

:::::

### Tip

Advice to help users make better choices when using a feature.

You could permanently lose data or leak sensitive information.

:::::{tab-set}

::::{tab-item} Output

:::{tip}
This is a tip.
:::

::::

::::{tab-item} Markdown

```markdown
:::{tip}
This is a tip.
:::
```

::::

:::::

### Important

Ignoring this information could impact performance or the stability of your system.

:::::{tab-set}

::::{tab-item} Output

:::{important}
This is an important notice.
:::

::::

::::{tab-item} Markdown

```markdown
:::{important}
This is an important notice.
:::
```

::::

:::::

### Plain

A plain admonition is a callout with no further styling. Useful to create a callout that does not quite fit the mold of the stylized admonitions.



:::::{tab-set}

::::{tab-item} Output

:::{admonition} This is my callout
It can *span* multiple lines and supports inline formatting.
:::

::::

::::{tab-item} Markdown

```markdown
:::{admonition} This is my callout
It can *span* multiple lines and supports inline formatting.
:::
```

::::

:::::

## Applies to information

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
