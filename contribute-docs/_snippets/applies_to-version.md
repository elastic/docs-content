`applies_to` accepts the following version formats:

* `Major.Minor`
* `Major.Minor.Patch`

Regardless of the version format used in the source file, the version number is always rendered in the `Major.Minor.Patch` format.

:::{note}
**Automatic Version Sorting**: When you specify multiple versions for the same product, the build system automatically sorts them in descending order (highest version first) regardless of the order you write them in the source file. For example, `stack: ga 8.18.6, ga 9.1.2, ga 8.19.2, ga 9.0.6` will be displayed as `stack: ga 9.1.2, ga 9.0.6, ga 8.19.2, ga 8.18.6`. Items without versions (like `ga` without a version or `all`) are sorted last.
:::