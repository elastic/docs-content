`applies_to` accepts the following version formats:

* `Major.Minor`
* `Major.Minor.Patch`

Regardless of the version format used in the source file, the version number is always rendered in the `Major.Minor.Patch` format.

:::{note}
**Automatic Version Sorting**: When you specify multiple versions for the same product, the build system automatically sorts them in descending order (highest version first) regardless of the order you write them in the source file. For example, `stack: preview =9.0, ga 9.1-9.7, deprecated =9.8, removed 9.9+` will be displayed as `stack: removed 9.9+, deprecated =9.8, ga 9.1-9.7, preview =9.0`. Items without versions (like `ga` without a version or `all`) are sorted last.
:::