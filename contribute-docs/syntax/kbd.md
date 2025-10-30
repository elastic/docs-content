# Keyboard shortcuts

You can represent keyboard keys and shortcuts in your documentation using the `{kbd}` role. This is useful for showing keyboard commands and shortcuts in a visually consistent way. See the full list of [available keys](#available-keys).

## Basic usage

To display a keyboard key, use the syntax `` {kbd}`key-name` ``. For example, writing `` {kbd}`enter` `` will render as a styled keyboard key.

::::{tab-set}

:::{tab-item} Output
Press {kbd}`enter` to submit.
:::

:::{tab-item} Markdown
```markdown
Press {kbd}`enter` to submit.
```
:::

::::

## Combining keys

For keyboard shortcuts involving multiple keys, you can combine them within a single `{kbd}` role by separating the key names with a `+`. Keys are always visually separated, even when using the combined syntax.

::::{tab-set}

:::{tab-item} Output
Use {kbd}`cmd+shift+enter` to execute the command.
:::

:::{tab-item} Markdown
```markdown
Use {kbd}`cmd+shift+enter` to execute the command.
```
:::

::::

## Alternative keys

To display alternative keys for a shortcut, use `|` to separate the alternate keys within the same `{kbd}` role. This is useful for showing platform-specific shortcuts, such as `ctrl` on Windows and `cmd` on macOS.

::::{tab-set}

:::{tab-item} Output
Use {kbd}`ctrl|cmd + c` to copy text.
:::

:::{tab-item} Markdown
```markdown
Use {kbd}`ctrl|cmd + c` to copy text.
```
:::

::::

## Reserved characters

The `+` and `|` characters have special meaning for combining keys and specifying alternatives. To render them as literal keys, you must use their keyword equivalents.

- To display the {kbd}`plus` key, use `` `{kbd}`plus` ``.
- To display the {kbd}`pipe` key, use `` `{kbd}`pipe` ``.

## Common shortcuts by platform

The platform-specific examples below demonstrate how to combine special keys and regular characters.

::::{tab-set}

:::{tab-item} Output

| Mac              | Windows/Linux     | Description                 |
|------------------|-------------------|-----------------------------|
| {kbd}`cmd+c`     | {kbd}`ctrl+c`     | Copy                        |
| {kbd}`cmd+v`     | {kbd}`ctrl+v`     | Paste                       |
| {kbd}`cmd+z`     | {kbd}`ctrl+z`     | Undo                        |
| {kbd}`cmd+enter` | {kbd}`ctrl+enter` | Run a query                 |
| {kbd}`cmd+/`     | {kbd}`ctrl+/`     | Comment or uncomment a line |

:::

:::{tab-item} Markdown
```markdown
| Mac              | Windows/Linux     | Description                 |
|------------------|-------------------|-----------------------------|
| {kbd}`cmd+c`     | {kbd}`ctrl+c`     | Copy                        |
| {kbd}`cmd+v`     | {kbd}`ctrl+v`     | Paste                       |
| {kbd}`cmd+z`     | {kbd}`ctrl+z`     | Undo                        |
| {kbd}`cmd+enter` | {kbd}`ctrl+enter` | Run a query                 |
| {kbd}`cmd+/`     | {kbd}`ctrl+/`     | Comment or uncomment a line |
```
:::

::::

## Available keys

The `{kbd}` role recognizes a set of special keywords for modifier, navigation, and function keys. Any other text will be rendered as a literal key.

Here is the full list of available keywords:

| Syntax                  | Rendered Output  |
|-------------------------|------------------|
| `` {kbd}`shift` ``      | {kbd}`shift`     |
| `` {kbd}`ctrl` ``       | {kbd}`ctrl`      |
| `` {kbd}`alt` ``        | {kbd}`alt`       |
| `` {kbd}`option` ``     | {kbd}`option`    |
| `` {kbd}`cmd` ``        | {kbd}`cmd`       |
| `` {kbd}`win` ``        | {kbd}`win`       |
| `` {kbd}`up` ``         | {kbd}`up`        |
| `` {kbd}`down` ``       | {kbd}`down`      |
| `` {kbd}`left` ``       | {kbd}`left`      |
| `` {kbd}`right` ``      | {kbd}`right`     |
| `` {kbd}`space` ``      | {kbd}`space`     |
| `` {kbd}`tab` ``        | {kbd}`tab`       |
| `` {kbd}`enter` ``      | {kbd}`enter`     |
| `` {kbd}`esc` ``        | {kbd}`esc`       |
| `` {kbd}`backspace` ``  | {kbd}`backspace` |
| `` {kbd}`del` ``        | {kbd}`delete`    |
| `` {kbd}`ins` ``        | {kbd}`insert`    |
| `` {kbd}`pageup` ``     | {kbd}`pageup`    |
| `` {kbd}`pagedown` ``   | {kbd}`pagedown`  |
| `` {kbd}`home` ``       | {kbd}`home`      |
| `` {kbd}`end` ``        | {kbd}`end`       |
| `` {kbd}`f1` ``         | {kbd}`f1`        |
| `` {kbd}`f2` ``         | {kbd}`f2`        |
| `` {kbd}`f3` ``         | {kbd}`f3`        |
| `` {kbd}`f4` ``         | {kbd}`f4`        |
| `` {kbd}`f5` ``         | {kbd}`f5`        |
| `` {kbd}`f6` ``         | {kbd}`f6`        |
| `` {kbd}`f7` ``         | {kbd}`f7`        |
| `` {kbd}`f8` ``         | {kbd}`f8`        |
| `` {kbd}`f9` ``         | {kbd}`f9`        |
| `` {kbd}`f10` ``        | {kbd}`f10`       |
| `` {kbd}`f11` ``        | {kbd}`f11`       |
| `` {kbd}`f12` ``        | {kbd}`f12`       |
| `` {kbd}`plus` ``       | {kbd}`plus`      |
| `` {kbd}`fn` ``         | {kbd}`fn`        |
| `` {kbd}`pipe` ``       | {kbd}`pipe`      |
