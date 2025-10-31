`applies_to` tags are rendered as badges in the documentation output. They reproduce the "key + lifecycle status + version" indicated in the content sources.

Specifically for versioned products, badges will display differently when the `applies_to` key specifies a product version that has not been released to our customers yet.

The following table shows how badges for versioned products are displayed based on the release status for each lifecycle value. Hover over the example badges for the tooltip text.

| Lifecycle   | Release status | Badge text examples                   |
|-------------|----------------|---------------------------------------|
| preview     | prerelease     | {applies_to}`stack: preview 99.99`    |
|             | post-release   | {applies_to}`stack: preview 9.1`      |
| beta        | prerelease     | {applies_to}`stack: beta 99.99`       |
|             | post-release   | {applies_to}`stack: beta 9.1`         |
| ga          | prerelease     | {applies_to}`stack: ga 99.99`         |
|             | post-release   | {applies_to}`stack: ga 9.1`           |
| deprecated  | prerelease     | {applies_to}`stack: deprecated 99.99` |
|             | post-release   | {applies_to}`stack: deprecated 9.1`   |
| removed     | prerelease     | {applies_to}`stack: removed 99.99`    |
|             | post-release   | {applies_to}`stack: removed 9.1`      |

This is computed at build time (there is a docs build every 30 minutes). The documentation team tracks and maintains released versions for these products centrally in [`versions.yml`](https://github.com/elastic/docs-builder/blob/main/config/versions.yml).

When multiple lifecycle statuses and versions are specified in the sources, several badges are shown.

:::{note}
Visuals and wording in the output documentation are subject to changes and optimizations.
:::
