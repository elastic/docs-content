---
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
description: Link projects in the Cloud UI to enable cross-project search across multiple Serverless projects.
navigation_title: "Linking projects"
---

# Link projects for {{cps}} [link-projects-for-cps]

Before you can search across multiple projects, you must link them together. {{cps-cap}} only works between projects that are explicitly linked within your {{ecloud}} organization.

This guide explains how to link projects in the {{ecloud}} UI so you can run cross-project searches from an origin project. For an overview of {{cps}} concepts such as origin projects, linked projects, and search expressions, refer to [{{cps-cap}}](/explore-analyze/cross-project-search.md).

## Link projects using the Cloud UI

For prerequisites, project compatibility requirements, and technical preview restrictions, refer to [Configure {{cps}}](/deploy-manage/cross-project-search-config.md) in **Deploy and manage**.

::::{include} /deploy-manage/_snippets/cps-link-projects-procedure.md
::::

When your configuration is saved, a page with the list of linked projects opens.
