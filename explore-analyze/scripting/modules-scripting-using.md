---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-using.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# How to write Painless scripts [modules-scripting-using]

:::{tip}   
This guide provides a beginner-friendly introduction to Painless scripting with step-by-step tutorials and practical examples. If you're new to scripting or Painless, this is the recommended starting point.

For users with Java or Painless experience looking for technical specifications and advanced features, refer to [A Brief Painless walkthrough](elasticsearch://reference/scripting-languages/painless/brief-painless-walkthrough.md) in the Reference section.
:::

Wherever scripting is supported in the {{es}} APIs, the syntax follows the same pattern; you specify the language of your script, provide the script logic (or source), and add parameters that are passed into the script:

```js
  "script": {
    "lang":   "...",
    "source" | "id": "...",
    "params": { ... }
  }
```

`lang`
:   Specifies the language the script is written in. Defaults to `painless`.

`source`, `id`
:   The script itself, which you specify as `source` for an inline script or `id` for a stored script. Use the [stored script APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-script) to create and manage stored scripts.

`params`
:   Specifies any named parameters that are passed into the script as variables. [Use parameters](/explore-analyze/scripting/modules-scripting-use-parameters.md) instead of hard-coded values to decrease compile time.

Get started with Painless scripting:

* [](/explore-analyze/scripting/modules-scripting-write-first-script.md)
* [](/explore-analyze/scripting/modules-scripting-use-parameters.md)
* [](/explore-analyze/scripting/modules-scripting-shorten-script.md)
* [](/explore-analyze/scripting/modules-scripting-store-and-retrieve.md)
* [](/explore-analyze/scripting/modules-scripting-update-documents.md)
