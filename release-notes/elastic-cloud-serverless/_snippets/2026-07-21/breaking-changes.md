## July 21, 2026 [elastic-2026-07-21-breaking-changes]

* Limit exception list entry string lengths for endpoint artifacts.
  For more information, check [#274803](https://github.com/elastic/kibana/pull/274803).

  **Impact:** Creating or updating endpoint exception list items with string values longer than the new limits fails validation. Other exception list types are unaffected.

  **Action:** Shorten entry values that exceed the limits before saving. Typical limits are 4096 characters for entry values and 1024 characters for field names in advanced trusted apps and event filters.

