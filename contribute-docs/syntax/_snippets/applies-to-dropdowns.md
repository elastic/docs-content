You can add an applies_to badge to the dropdown title by specifying the `:applies_to:` option. This displays a badge indicating which deployment types, versions, or other applicability criteria the dropdown content applies to.

**Source**

```markdown
:::{dropdown} Dropdown Title
:applies_to: stack: ga 9.0
Dropdown content for Stack GA 9.0
:::
```

**Rendering**

:::{dropdown} Dropdown Title
:applies_to: stack: ga 9.0
Dropdown content for Stack GA 9.0
:::

You can also specify multiple definitions in the same `:applies_to:` parameter. For example, `:applies_to: { ece:, ess: }` renders both ECE and ECH badges.