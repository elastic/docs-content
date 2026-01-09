`applies_to` accepts the following version formats:

| Format | Syntax | Examples | Badge Display | Description |
|:-------|:-------|:---------|:--------------|:------------|
| **Greater than or equal to** (default) | `x.x+`<br>`x.x`<br>`x.x.x+`<br>`x.x.x` | `ga 9.1`<br>`ga 9.1+` | `9.1+` | Applies from this version onwards |
| **Range** (inclusive) | `x.x-y.y`<br>`x.x.x-y.y.y` | `preview 9.0-9.2` | `9.0-9.2`<br>`9.0+`* | Applies within the specified range |
| **Exact version** | `=x.x`<br>`=x.x.x` | `beta =9.1` | `9.1` | Applies only to this specific version |

\* Range display depends on release status of the second version.

**Important notes:**

- Versions are always displayed as **Major.Minor** (for example, `9.1`) in badges, regardless of whether you specify patch versions in the source.
- Each version statement corresponds to the **latest patch** of the specified minor version (for example, `9.1` represents 9.1.0, 9.1.1, 9.1.6, and so on).
- When critical patch-level differences exist, use plain text descriptions alongside the badge rather than specifying patch versions.

:::{note}
**Automatic Version Sorting**: When you specify multiple versions for the same product, the build system automatically sorts them in descending order (highest version first) regardless of the order you write them in the source file. For example, `stack: preview =9.0, ga 9.1-9.7, deprecated =9.8, removed 9.9+` will be displayed as `stack: removed 9.9+, deprecated =9.8, ga 9.1-9.7, preview =9.0`. Items without versions (like `ga` without a version or `all`) are sorted last.
:::