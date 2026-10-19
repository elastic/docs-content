```yaml
##### Required fields #####
title:

# A required string that is a short, user-facing headline
# Max 80 characters

type: 

# A required string that contains the type of change.
# For the acceptable values, refer to https://github.com/elastic/docs-builder/blob/main/src/Elastic.Documentation/ReleaseNotes/ChangelogEntryType.cs
products:

# A required array of objects that denote the affected products.

    - product:

      # A required string with a predefined product ID used for release note routing,
      # filters, and categorization.
      # Refer to https://github.com/elastic/docs-builder/blob/main/config/products.yml for the acceptable values.
      
      versions:

      # A list of concrete release versions or dates this changelog applies to.
      # This field is required when you run the "changelog note" command.
      # Omit when `prs` lists at least one pull request that ships in a product release.
      # Use a YAML list of concrete values such as [9.3.0, 9.4.0], not "*" and not a pipe-separated string.

      lifecycle:

      # An optional string for new features and enhancements that have a specific availability.
      # For the acceptable values, refer to https://github.com/elastic/docs-builder/blob/main/src/Elastic.Documentation/Lifecycle.cs

##### Optional fields #####
action:

# An optional string that describes what users must do to mitigate the impact
# of a breaking change or known issue.

areas:

# An optional array of strings that denotes the parts/components/services of the
# product that are specifically affected.
# The list of valid values will vary by product.
# The docs for each release typically group the changes by type then by area.

description:

# An optional string that provides additional information about what has changed.
# Max 600 characters

feature-id:

# An optional string to associate a feature or enhancement with a unique feature flag

highlight:

# An optional boolean for items that should be included in release highlights
# or the UI to draw users' attention.

impact:

# An optional string that describes how the user's environment is/will be
# affected by a breaking change.

issues:

# An optional array of strings that contain URLs for issues that are relevant to the PR.
# They are externalized in the release docs so users can follow the links and
# understand the context.

prs:

# An optional array of product pull request identifiers (URLs or numbers).
# This field is used to map changelogs to the list of changes shipped in a product release.
# Each value is externalized in the release docs so users can follow the links and find more details (unless it is a private URL).

subtype:

# An optional string that applies only to breaking changes and further subdivides that type.
# For the acceptable values, refer to https://github.com/elastic/docs-builder/blob/main/src/Elastic.Documentation/ReleaseNotes/ChangelogEntrySubtype.cs
```
