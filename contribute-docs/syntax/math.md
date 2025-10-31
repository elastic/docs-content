# Math

The `math` directive renders mathematical expressions using LaTeX syntax. Mathematical expressions are rendered client-side using KaTeX for fast, accurate display.

## Basic usage

:::::{tab-set}

::::{tab-item} Preview

:::{math}
S(doc) = exp(\lambda \cdot max(0, |fieldvalue_{doc} - origin| - offset))
:::

::::

::::{tab-item} Markdown

```markdown
:::{math}
S(doc) = exp(\lambda \cdot max(0, |fieldvalue_{doc} - origin| - offset))
:::
```

::::

:::::

## Display math

For block-level mathematical expressions, use display math syntax:

:::::{tab-set}

::::{tab-item} Preview

:::{math}
\[
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
\]
:::

::::

::::{tab-item} Markdown

```markdown
:::{math}
\[
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
\]
:::
```

::::

:::::

The directive automatically detects display math based on:
- LaTeX display delimiters: `\[` and `\]`
- TeX display delimiters: `$$` and `$$`
- LaTeX environments: `\begin{...}` and `\end{...}`
- Multi-line expressions
- Complex expressions containing `\frac`, `\sum`, `\int`, `\lim`, etc.

## Adding labels

Label mathematical expressions for cross-referencing:

:::::{tab-set}

::::{tab-item} Preview

:::{math}
:label: einstein-equation
E = mc^2
:::

::::

::::{tab-item} Markdown

```markdown
:::{math}
:label: einstein-equation
E = mc^2
:::
```

::::

:::::

This creates an element with `id="einstein-equation"` that can be referenced elsewhere in the document.

## Complex expressions

The math directive supports complex LaTeX expressions:

:::::{tab-set}

::::{tab-item} Preview

:::{math}
\begin{align}
\frac{\partial f}{\partial x} &= \lim_{h \to 0} \frac{f(x+h) - f(x)}{h} \\
\nabla \cdot \vec{E} &= \frac{\rho}{\epsilon_0}
\end{align}
:::

::::

::::{tab-item} Markdown

```markdown
:::{math}
\begin{align}
\frac{\partial f}{\partial x} &= \lim_{h \to 0} \frac{f(x+h) - f(x)}{h} \\
\nabla \cdot \vec{E} &= \frac{\rho}{\epsilon_0}
\end{align}
:::
```

::::

:::::

## Supported LaTeX features

The math directive supports most common LaTeX mathematical notation:

- **Fractions**: `\frac{numerator}{denominator}`
- **Superscripts and subscripts**: `x^2`, `x_i`
- **Integrals**: `\int`, `\iint`, `\iiint`
- **Sums and products**: `\sum`, `\prod`
- **Limits**: `\lim`, `\limsup`, `\liminf`
- **Greek letters**: `\alpha`, `\beta`, `\gamma`, etc.
- **Matrices**: `\begin{matrix}`, `\begin{pmatrix}`, etc.
- **Aligned equations**: `\begin{align}`, `\begin{eqnarray}`
- **Roots**: `\sqrt{x}`, `\sqrt[n]{x}`
- **Operators**: `\sin`, `\cos`, `\log`, `\exp`, etc.
