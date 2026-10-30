---
description: Add your own YARA rules to Elastic Defend to detect threats that are specific to your environment, and learn the rules and meta fields that Elastic Defend enforces.
applies_to:
  stack: ga 9.6+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Custom YARA signatures

[YARA](https://virustotal.github.io/yara/) is a rule-based language for identifying malware and other threats by the patterns they contain. Custom YARA signatures let you add your own YARA rules to {{elastic-defend}}, so that it can detect threats that are specific to your environment, such as malware that targets your organization or indicators from a threat report that you're tracking.

{{elastic-endpoint}} evaluates your YARA rules against the memory of running processes on protected hosts. When a rule matches, {{elastic-defend}} generates an alert. To see these alerts on the **Alerts** page, the Endpoint Security ({{elastic-defend}}) rule, or the Memory Threat - Detected - {{elastic-defend}} rule, must be turned on. Refer to [Identify alerts from custom YARA signatures](#identify-custom-yara-signature-alerts) for details.

::::{important}
Custom YARA signatures only detect threats. They never block a process or stop a thread, even when [memory threat protection](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#memory-protection) is set to **Prevent**.
::::

A custom YARA signature has a name, one or more operating systems, and a definition. The definition is YARA code that can contain one or more rules, like the contents of a `.yar` file. By default, a custom YARA signature applies globally to all hosts running {{elastic-defend}}. You can also assign it to specific {{elastic-defend}} integration policies, so that it only applies to the hosts assigned to those policies.

::::{admonition} Requirements
* Custom YARA signatures require the appropriate [subscription](https://www.elastic.co/pricing) in {{stack}} or [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md) in {{serverless-short}}.
* You must have the **Custom YARA Signatures** [privilege](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md) or the appropriate user role to access this feature.
::::

## Add a custom YARA signature

1. Go to the **Artifacts** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select the **Custom YARA signatures** tab.
2. Click **Add YARA signature**. The Add YARA signature flyout opens.
3. In the **Details** section, do the following:
    * Enter a **Name** for your signature.
    * In the **Operating system** field, select one or more operating systems: Windows, Linux, or macOS. {{elastic-defend}} only applies the signature to hosts running the selected operating systems.
    * Optionally, enter a **Description**.
4. In the **Definition** section, write or paste your YARA code. The editor suggests YARA keywords as you type, and checks your code as you work, showing errors and warnings with their line numbers. Refer to [YARA rule requirements](#yara-rule-requirements) and [Meta fields that {{elastic-defend}} uses](#yara-meta-fields) for details on what is allowed.
5. Select an option in the **Assignment** section:
    * **Global**: Assign the signature to all {{elastic-defend}} integration policies.
    * **Per Policy**: Assign the signature to one or more specific {{elastic-defend}} integration policies.
6. Click one of the following:
    * **Create & enable signature**: Saves the signature and starts applying it to hosts.
    * **Create signature without enabling**: Saves the signature, but doesn't apply it to hosts until you [turn it on](#enable-disable-custom-yara-signatures).

::::{tip}
To add multiple signatures at once, you can import an NDJSON file instead. Refer to [Import and export custom YARA signatures](#import-export-custom-yara-signatures).
::::

::::{note}
You can't save a signature that has errors. Warnings don't prevent you from saving.
::::

After you add a signature, make sure the policies that it's assigned to [apply custom YARA signatures](#apply-custom-yara-signatures-policy).

### YARA rule requirements [yara-rule-requirements]

{{elastic-defend}} checks the definition of each custom YARA signature when you save it. Your definition must meet the following requirements:

* It must contain at least one valid YARA rule, and can contain up to 256 rules.
* It must not exceed 32,766 bytes. This limit applies to the whole definition, not to each rule.
* Rule names can be up to 128 characters long.
* It can't use the `include` directive. Each signature must be self-contained.
* It can only import the following YARA modules: `pe`, `elf`, `math`, `time`, `string`, and `console`. Importing any other module, such as `hash`, `macho`, `dotnet`, `dex`, `magic`, or `cuckoo`, causes an error.

Syntax errors and other YARA compiler errors prevent you from saving the signature. YARA compiler warnings appear in the editor, but don't prevent you from saving the signature.

### Meta fields that {{elastic-defend}} uses [yara-meta-fields]

In YARA, the `meta` section of a rule is optional, and you can add any metadata to it that you want. {{elastic-defend}} reads three meta fields, `os`, `arch`, and `scan_type`, and uses them to limit where a rule applies. {{elastic-defend}} validates their values when you save the signature, but it doesn't validate any other meta fields that you add.

| Meta field | Allowed values | If you omit it |
| --- | --- | --- |
| `os` | A comma-separated list of one or more of `Windows`, `Linux`, and `MacOS`. The list must match the operating systems selected in the **Operating system** field of the signature. | The operating systems selected in the **Operating system** field apply. |
| `arch` | `x86`, `arm64`, or both in a comma-separated list. | The rule applies to both `x86` and `arm64`. |
| `scan_type` | `Memory`. | The rule scans memory. Memory is currently the only supported scan type. |

The following rules apply to these meta fields:

* Values are case-sensitive. For example, use `MacOS`, not `macos`, and `Memory`, not `memory`.
* Separate multiple values with a comma, optionally followed by a space (for example, `"Windows, Linux"` or `"x86,arm64"`). Don't repeat a value in the same list.
* Each field can appear only once in each rule.
* The `os` value must list exactly the same operating systems as the **Operating system** field of the signature, in any order. If they differ, {{elastic-defend}} rejects the signature. If you don't want to keep them in sync, omit `os` from your rules.
* When a signature contains more than one rule, `arch` and `scan_type` must be consistent across all its rules. Either omit the field from every rule, or use the same value in every rule.

## Apply custom YARA signatures to hosts [apply-custom-yara-signatures-policy]

For a signature to take effect on a host, all the following must be true:

* The signature is enabled.
* The signature is global, or it's assigned to the {{elastic-defend}} integration policy that the host uses.
* In that policy, [memory threat protection](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#memory-protection) is turned on, and the **Apply custom YARA signatures in detection mode** setting is turned on. This setting is turned on by default in new {{elastic-defend}} integration policies. In existing policies, you must turn it on yourself.

To check or change the policy setting:

1. Go to **Assets** → **Endpoints** → **Policies**, then select the policy.
2. On the **Policy settings** tab, find the **Memory threat** section.
3. Turn **Apply custom YARA signatures in detection mode** on or off. This setting is only available when memory threat protection is turned on.
4. Click **Save**.

To see which custom YARA signatures are assigned to a policy, assign more signatures, or remove them, open the policy and select its **Custom YARA signatures** tab.

{{elastic-endpoint}} scans each running process with your signatures about 5 minutes after the process starts, and then again every 24 hours by default. Processes that are already running when the policy takes effect are scanned too. To change how often processes are re-scanned, refer to the `user_yara_rescan_interval_seconds` settings in [{{elastic-defend}} advanced settings](/reference/security/defend-advanced-settings.md).

[Trusted applications](/solutions/security/manage-elastic-defend/trusted-applications.md) and [{{elastic-endpoint}} exceptions](/solutions/security/manage-elastic-defend/elastic-endpoint-exceptions.md) apply to these scans: {{elastic-endpoint}} skips processes that are trusted, and doesn't generate alerts that match an exception.

## View and manage custom YARA signatures

The **Custom YARA signatures** tab on the **Artifacts** page lists all custom YARA signatures. To refine the list, use the search bar to search by name, description, or YARA code. To view the YARA code and other details of a signature, click its name.

### Turn a custom YARA signature on or off [enable-disable-custom-yara-signatures]

Use the **Enabled** toggle in the list to turn a signature on or off. A signature that is turned off stays in your list, but {{elastic-defend}} doesn't apply it to hosts.

### Import and export custom YARA signatures [import-export-custom-yara-signatures]

::::{admonition} Requirements
* To export custom YARA signatures, you need the **Custom YARA Signatures: Read** [privilege](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md).
* To import per-policy items, you need the **Custom YARA Signatures: All** privilege.
* To import global items, you need the **Custom YARA Signatures: All** and the **Global artifact management: All** privilege.
* To import items to a different space, you need the **Global artifact management: All** privilege.
::::

You can import and export custom YARA signatures as NDJSON files:

- **When the list is empty**: Click **Import YARA signatures**.
- **When the list has entries**: Click the actions menu {icon}`boxes_vertical`, then select **Import YARA signatures** or **Export YARA signatures**.

::::{note}
The imported file must be an NDJSON file exported from {{kib}}. Files exported from third-party software, including `.yar` files, are not supported. To add rules from a `.yar` file, paste them into the **Definition** field of a new signature instead.
::::

When you import an NDJSON file, the imported signatures are appended to your existing entries — existing entries are not removed or overwritten. If a signature that you import already exists, {{elastic-defend}} keeps the existing version and skips the imported one.

Items are processed individually on import — items that fail validation, and per-policy items that are not visible in the current space, are skipped, while the remaining items are imported. Imported YARA code must meet the same [requirements](#yara-rule-requirements) as code that you enter in the editor.

If an imported per-policy item is assigned to a policy that doesn't exist in the current environment, the item is imported with the policy assignment removed.

### Edit a custom YARA signature

You can individually modify each custom YARA signature.

To edit a custom YARA signature:

1. Click the actions menu (**…**) on the signature you want to edit, then select **Edit YARA signature**.
2. Modify details as needed.
3. Click **Save**.

### Delete a custom YARA signature

You can delete a custom YARA signature, which removes it entirely from all {{elastic-defend}} integration policies.

To delete a custom YARA signature:

1. Click the actions menu (**…**) on the signature you want to delete, then select **Remove from YARA signatures list**.
2. On the dialog that opens, verify that you are removing the correct signature, then click **Delete**.

## Identify alerts from custom YARA signatures [identify-custom-yara-signature-alerts]

When a custom YARA signature matches the memory of a running process, {{elastic-defend}} generates a memory threat detection alert. It appears on the **Alerts** page only if one of the following [endpoint protection rules](/solutions/security/manage-elastic-defend/endpoint-protection-rules.md) is turned on:

* The [Endpoint Security ({{elastic-defend}})](detection-rules://rules/integrations/endpoint/elastic_endpoint_security.md) rule, which is turned on by default when you install Elastic prebuilt rules.
* If you use the feature-specific protection rules instead, [Memory Threat - Detected - {{elastic-defend}}](detection-rules://rules/integrations/endpoint/defense_evasion_elastic_memory_threat_detected.md).

The [Memory Threat - Prevented - {{elastic-defend}}](detection-rules://rules/integrations/endpoint/defense_evasion_elastic_memory_threat_prevented.md) rule doesn't create alerts for custom YARA signatures, because they only detect threats.

The alert includes the following fields:

* `rule.custom_yara_signature.entry_name`: The name of the custom YARA signature that contains the matching rule.
* `rule.custom_yara_signature.rule_identifier`: The name of the YARA rule that matched.
* `rule.custom_yara_signature.entry_id`: The ID of the custom YARA signature that contains the matching rule.

The `entry_name` and `rule_identifier` fields appear in the **Highlighted fields** section of the alert details flyout. If you have the **Custom YARA Signatures: Read** privilege and the signature exists in the current space, the value links to the signature. If the signature doesn't exist in the current space, an information icon appears next to the value instead of a link.

::::{note}
The signature name is stored in the alert when it's generated, so it might not match the current name if you rename the signature later.
::::
