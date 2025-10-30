# Sundries

A collection of assorted markdown formatting.

## Inline text formatting

Note that there should be no space between the enclosing markers and the text.

| Syntax         | Result                  |
| ------------------- | --------------------------- |
| \*\*strong\*\*  | **strong**    |
| \_emphasis\_           | _emphasis_ |
| \`literal text\`  |`literal text`    |
| \~\~strikethrough\~\~           | ~~strikethrough~~ |
| `\*escaped symbols\*`           | \*escaped symbols\* |

## Subscript & Superscript
 
::::{tab-set}

:::{tab-item} Output
H~2~O
:::

:::{tab-item} Markdown
```markdown
H~2~O 
```
:::

::::

::::{tab-set}

:::{tab-item} Output
4^th^ of July
:::

:::{tab-item} Markdown
```markdown
4^th^ of July
```
:::

::::

## Quotation

Here is a quote. The attribution is added using the block attribute `attribution`.

{attribution="Hamlet act 4, Scene 5"}
> We know what we are, but know not what we may be.

## Thematic break

Same as using `<hr>` HTML tag:
***
