---
navigation_title: Anonymization
description: Mask email addresses, IP addresses, host names, and other sensitive values before Kibana sends AI requests to a large language model, and restore them in the response.
type: how-to
applies_to:
  stack: preview 9.6+
  serverless: preview
products:
  - id: kibana
  - id: elasticsearch
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Anonymize data sent to LLMs [anonymize-ai-requests]

The **Anonymization** page lets you mask sensitive values, such as email addresses, IP addresses, and host names, before {{kib}} sends an AI request to a large language model (LLM). The model receives a token in place of each value, and {{kib}} restores the original values in the response.

Masking is configured separately for each [space](/deploy-manage/manage-spaces.md) and is off by default in new spaces.

## Requirements [anonymize-ai-requests-requirements]

- {applies_to}`stack: preview 9.6+` An [Enterprise license](https://www.elastic.co/subscriptions).
- {applies_to}`serverless: preview` An {{es}}, {{observability}}, {{elastic-sec}}, or [vector database](/solutions/vector-database.md) project with a [feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md) that includes connector access.
- The **All** privilege for **Advanced Settings**, and the **Read** or **All** privilege for **Actions and Connectors**. Refer to [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).

If you don't meet these requirements, the page doesn't appear in the navigation.

## What gets masked [anonymize-ai-requests-scope]

Masking applies to AI features in the space that use {{kib}}'s shared AI integration, with any connector. For example:

- [{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md) chat, including attached alerts and tool calls
- [AI steps](/explore-analyze/workflows/steps/ai-steps.md) in workflows
- [Automatic Migration](/solutions/security/get-started/automatic-migration.md) of detection rules

Requests sent directly to a connector aren't masked.

The {{elastic-sec}} AI Assistant also has separate [field-level anonymization settings](/solutions/security/ai/ai-assistant.md#ai-assistant-anonymization) that control which alert fields are sent to the LLM and which are obfuscated.

## How masking works [anonymize-ai-requests-how]

Each enabled pattern scans the request, including the system prompt, messages, and tool call arguments and responses. Every match is replaced with a token made of the entity type and a hash of the value, for example `EMAIL_ee4587b4…`. The same entity type and value always produce the same token, so the model can tell values apart and keep track of them without seeing them.

When the model responds, {{kib}} restores the original values before you see the response, including while it streams. Masked values in tool call arguments are also restored before the tool runs, so tools such as {{esql}} queries run against the real values. Stored conversations keep the original values.

:::{important}
Tokens are pseudonyms, not encryption. When a value comes from a small set, such as an IP address range or a list of user names, someone with access to the token can recover the value by guessing.
:::

## Turn on masking [anonymize-ai-requests-turn-on]

1. Find **Anonymization** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). In Classic view, it's under **Stack Management → AI**. In solution views and {{serverless-short}} projects, it's under **Management → AI**.
2. Review the **Built-in patterns** and **Custom patterns** tabs and turn on the patterns you want to apply.
3. Turn on **Masking enabled** in the page header. This switch is the same as **Mask PII in AI requests** on the **Settings** tab.

When masking is off, no patterns apply and requests are sent to the model unmasked.

## Built-in patterns [anonymize-ai-requests-built-in]

Elastic maintains the built-in patterns. You can turn each one on or off, but you can't edit them. In a new space, the following patterns are enabled when you turn on masking:

| Name | Entity type | Enabled in new spaces |
| --- | --- | --- |
| Email addresses | `EMAIL` | Yes |
| IPv4 addresses | `IP` | Yes |
| IPv6 addresses | `IP` | Yes |
| Host and machine names | `HOST_NAME` | Yes |
| Account and login names | `USER_NAME` | No |

The built-in patterns have the following limits:

- **Host and machine names** match only dot-separated names that end in a recognized suffix. Single-label names such as `server01`, and names such as `nas.local` that have only one label before an internal suffix, aren't masked.
- **Account and login names** match only the `DOMAIN\name` form, and mask only the `name` part. A user name that appears on its own, such as `jdoe`, isn't masked.
- **IPv4 addresses** also mask four-part version numbers, such as `3.11.4.2`, because they look the same as addresses.
- Some well-known public sites stay readable so that links in responses keep working:
  - These sites and all their subdomains: `github.com`, `githubusercontent.com`, `gitlab.com`, `stackoverflow.com`, `wikipedia.org`, `virustotal.com`, `owasp.org`, and `ss64.com`.
  - These exact hosts only: `attack.mitre.org`, `nvd.nist.gov`, `www.cisa.gov`, `learn.microsoft.com`, `docs.microsoft.com`, `www.microsoft.com`, `elastic.co`, `www.elastic.co`, and `docs.elastic.co`. Other hosts under these domains, such as `corp.mitre.org`, are masked.

To mask values that the built-in patterns miss, such as your own host naming convention, add a custom pattern.

## Add a custom pattern [anonymize-ai-requests-custom]

1. On the **Custom patterns** tab, add a new pattern.
2. Fill in the following fields:
   - **Name**: Shown in the pattern list and in audit records.
   - **Entity type**: Becomes the token prefix, so the model knows what kind of value it is. Choose one of `EMAIL`, `IP`, `URL`, `HOST_NAME`, `USER_NAME`, `CLOUD_ACCOUNT`, `ENTITY_NAME`, `RESOURCE_NAME`, or `RESOURCE_ID`.
   - **Pattern**: A regular expression in RE2 syntax, for example `EMP-\d+`.
   - **Enabled**: Whether the pattern applies when masking is on.
3. Click **Test pattern** to check the pattern against sample input.
4. Click **Save pattern**.

Patterns use [RE2 syntax](https://github.com/google/re2/wiki/Syntax), not JavaScript regular expressions:

- Lookahead, lookbehind, and backreferences aren't supported.
- `\uXXXX` escapes aren't supported. Use `\x{00e9}` instead.
- Matching is case-sensitive. Start the pattern with `(?i)` to ignore case.
- `\s` and `\w` match ASCII characters only. Use classes such as `\p{L}` to match letters in any script.

Custom patterns saved in an earlier version that aren't valid RE2 keep working. When you edit one, it shows an error until you rewrite it in RE2 syntax.

## Test your patterns [anonymize-ai-requests-test]

Use the **Pattern tester** tab to check what the model would receive before you turn on masking. Paste JSON or plain text as input, then click **Test pattern**. The output shows what the model receives, and a table lists each value that was masked and its token. The tester doesn't save the input or send it to a model.

The tab doesn't appear if `xpack.aiAnonymizationSettings.patternTester.enabled` is set to `false` in `kibana.yml`.

## Choose what happens when masking can't run [anonymize-ai-requests-on-failure]

A pattern might fail to run, for example because it doesn't compile or it times out. On the **Settings** tab, under **If masking cannot run**, select one of the following:

- **Block the request** (default): The request isn't sent to the model.
- **Allow the request through without the patterns that cannot run**: A pattern that doesn't compile is skipped, and the other patterns still apply. If the patterns fail while running, none of them apply, and the request is sent unmasked.

## Upgrade from an earlier version [anonymize-ai-requests-upgrade]

In earlier versions, anonymization rules were set in the `ai:anonymizationSettings` advanced setting. That setting no longer appears on the **Advanced Settings** page. Use the **Anonymization** page instead.

If a space had anonymization rules saved before the upgrade:

- Masking stays on if at least one rule was enabled.
- Built-in patterns are added turned off. Turn on the ones you want.
- Named entity recognition (NER) rules don't appear on the page.
