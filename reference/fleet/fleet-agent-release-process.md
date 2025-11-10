---
navigation_title: "{{agent}} release process"
applies_to:
  stack: ga
products:
  - id: fleet
  - id: elastic-agent
---

# {{agent}} release process [fleet-agent-release-process]

## Scheduled releases

{{agent}} follows a release process aligned with the broader {{stack}} release schedule. The latest features, enhancements, and fixes are documented in the [release notes](elastic-agent://release-notes/index.md).

## Independent {{agent}} releases [independent-agent-releases]

Independent {{agent}} releases deliver critical fixes and updates for {{agent}} and {{elastic-defend}}, independently of the full stack release. This is a more conservative process than a typical patch release, and only modifies the specific {{agent}} components needed for a targeted fix. For example, an independent {{agent}} hotfix release for {{elastic-defend}} would only change the endpoint-security executable, with the remaining executables being exactly those released in the previous patch.

In independent {{agent}} releases, a build identifier is appended to the semantic version of the base release in the format `+build{yyyymmddhhmm}`, where `{yyyymmddhhmm}` is the release timestamp of the build.
