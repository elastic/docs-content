---
navigation_title: "{{agent}} release"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-agent-release.html
applies_to:
  stack: ga
products:
  - id: fleet
  - id: elastic-agent
---

# {{agent}} release process [fleet-agent-release]

{{agent}} follows a release process aligned with the broader Elastic Stack release schedule. Changes and fixes are documented in the [release notes](../../release-notes/fleet-elastic-agent/index.md).

## Independent Agent Release

Independent Agent Release (IAR) is a fast-track release process for {{agent}} and Endpoint, designed to deliver critical fixes and updates independently of the full stack release. The IAR version format appends a build identifier `+build{yyyymmddhhmm}` to the semantic version it is based on, where `{yyyymmddhhmm}` is the release timestamp of the build.
