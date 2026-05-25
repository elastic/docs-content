---
navigation_title: Document deployment types
description: "How to write and review Elastic documentation that spans multiple deployment types. Covers the different deployment types, how to classify the impact of deployment context on your content, and where to apply each documentation strategy."
---

# Documenting deployment types

Elastic ships the same products across very different operational models. The same task, such as changing a setting, configuring a feature, or creating a snapshot of a cluster, can require completely different workflows depending on how the user deployed Elastic.

This page is the entry point for writing and reviewing documentation that spans deployment types. It covers what the deployment types are, how to recognize when content is deployment-sensitive, and where to find the patterns we use to handle that variation.

:::{note}
If you have questions about deployment types or how to document them, reach out to **@elastic/docs**.
:::

## In this section

- [Signals: how to recognize deployment context](signals.md) — signs that a doc, PR, or procedure is about a specific deployment type
- [Strategies for deployment-type variation](strategies.md) — choose an editorial approach based on how much content varies
- [Review checklist](review-checklist.md) — symptoms to look for in PRs and audits

## See also

- [Write cumulative documentation](/contribute-docs/how-to/cumulative-docs/index.md) — how to tag content with `applies_to`
- [Deployment options](/get-started/deployment-options.md) — reader-facing overview
- [Deploy and manage](/deploy-manage/index.md) — full reader-facing deployment documentation

---

## Available deployment types

Deployment types differ mainly in who operates the platform and how much of the stack lifecycle is automated. For cues that signal a piece of content is rooted in a specific deployment type, refer to [](signals.md).

| Deployment type | One-line summary |
|---|---|
| **Self-managed** | You own everything. |
| **{{eck}} (ECK)** | Kubernetes-native orchestration; you run the operator. |
| **{{ece}} (ECE)** | Same software as ECH — but you run the platform. |
| **{{ech}} (ECH)** | Elastic operates the platform; you configure and maintain the deployment. |
| **{{serverless-full}}** | Elastic operates and configures; you use it. |

ECH, ECE, ECK, and self-managed run the **versioned** flavor of the {{stack}} — they share the same versioning and compatibility model, though each orchestrator exposes a different subset of stack configuration and features. {{serverless-full}} runs the **serverless** flavor — unversioned and continuously delivered. For how flavors map to `applies_to` tags, refer to [Dimensions](/contribute-docs/how-to/cumulative-docs/guidelines.md#dimensions).

Not every component is available on every deployment type. For the component matrix, refer to [Deployment options](/get-started/deployment-options.md).

### Naming deployment types in published docs

Sometimes, people refer to everything not hosted on {{ecloud}} as "self-managed" (meaning self-managed, ECE, and ECK together). **Don't use this in published documentation.** Self-managed, ECE, and ECK differ in meaningful ways that the grouping obscures. Always name the specific deployment type.

### Serverless is both a flavor and a deployment type

`serverless` appears in both the Stack/Serverless and Deployment dimensions of `applies_to`. This is because Serverless acts as both:

- A **flavor** of the {{stack}} — unversioned, continuously delivered, behaves differently from the versioned {{stack}}
- A **deployment type** — projects are created, scaled, and managed differently from any other deployment type

When tagging, use `serverless` in whichever dimension matches your page's primary focus. For more on dimension choice, refer to [Dimensions](/contribute-docs/how-to/cumulative-docs/guidelines.md#dimensions).

---

## Same task, different steps

The most common writer mistake is assuming a task that's universal in concept is also universal in procedure. It usually isn't.

| Task | Same or different steps? |
|---|---|
| Configure an `elasticsearch.yml` setting | Different — the file isn't directly accessible on orchestrated deployments |
| Configure something in the {{kib}} UI | Same across deployment types (exceptions for {{serverless-short}}) |
| Configure an {{es}} cluster-level / dynamic setting | Same across deployment types — done through the {{es}} API (exceptions for {{serverless-short}}) |
| Add a config file to your {{es}} instance | Different — depends on deployment type |
| Install {{agent}} to send data to {{es}} | Same — action is performed on the client |
| Integrate a custom application using client libraries | Same — action is performed in client code |
| Configure {{ilm-init}} policies | Same across versioned deployment types; unavailable in {{serverless-short}} |

:::{tip}
Usage of a feature is usually the same across deployment types. Admin and orchestration tasks are usually different. When in doubt, separate "how to use" from "how to install or configure."
:::

---

## Classify content by deployment-sensitivity

When writing or reviewing a page, ask one question: **how deployment-sensitive is this content?**

| Sensitivity | What it looks like | Examples |
|---|---|---|
| **Not sensitive** | Independent of deployment type | Feature usage, query behavior, client code, {{kib}} UI workflows |
| **Somewhat sensitive** | Same task, different surface | Editing a setting, adding a secure setting, accessing logs |
| **Very sensitive** | Different steps, blockers, or unavailable in some types | Setting up monitoring, installing the operator, configuring snapshots |

The sensitivity level determines which [strategy](strategies.md) to apply. The classification itself is the most important review skill: if you can't name the sensitivity, you can't choose the right approach.
