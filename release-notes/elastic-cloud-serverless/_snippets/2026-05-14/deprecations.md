## May 14, 2026 [elastic-2026-05-14-deprecations]

* Remove HTML converter/bridge from field formatters plugin and clean up.
  For more information, check [#267517](https://github.com/elastic/kibana/pull/267517) [#259295](https://github.com/elastic/kibana/issues/259295).

  **Impact:** Field formatters now return React elements instead of HTML strings, eliminating the use of dangerouslySetInnerHTML and removing a class of potential XSS vulnerabilities.

