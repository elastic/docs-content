---
navigation_title: "{{agent}} release process"
applies_to:
  stack: ga
products:
  - id: fleet
  - id: elastic-agent
---

# {{agent}} release process [fleet-agent-release-process]

{{agent}} follows a release process aligned with the broader {{stack}} release schedule. The latest features, enhancements, and fixes are documented in the [release notes](../../release-notes/fleet-elastic-agent/index.md).

## Independent agent release

The independent agent release (IAR) is a hotfix release process for {{agent}} and {{elastic-defend}}, designed to deliver critical fixes and updates independently of the full stack release. The IAR process is more conservative than a typical patch release, and only modifies the specific {{agent}} components needed for a targeted fix. For example, an IAR hotfix release for {{elastic-defend}} would only change the endpoint-security executable, with the remaining executables being exactly those released in the previous patch.

The IAR version format appends a build identifier in the format `+build{yyyymmddhhmm}` to the semantic version it is based on, where `{yyyymmddhhmm}` is the release timestamp of the build.
