---
navigation_title: Manage quarantined files
description: Find, restore, and retrieve files that Elastic Defend quarantines when malware protection is set to Prevent.
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Manage quarantined files [manage-quarantined-files]

When **Prevent** is enabled for malware protection, {{elastic-defend}} will quarantine any malicious file it finds (this includes files defined in the [blocklist](/solutions/security/manage-elastic-defend/blocklist.md)). Specifically, {{elastic-defend}} will remove the file from its current location, apply a rolling XOR with the key `ELASTIC`, move it to a different folder, and rename it as a GUID string, such as `318e70c2-af9b-4c3a-939d-11410b9a112c`.

The quarantine folder location varies by operating system:

* macOS: `/System/Volumes/Data/.equarantine`
* Linux: `.equarantine` at the root of the mount point of the file being quarantined
* Windows:
    * Quarantined file: `[DriveLetter:]\.equarantine` on the same volume as the original file (for example, `C:\.equarantine`)
    * Quarantine metadata (`.mdata`): `C:\Program Files\Elastic\Endpoint\state` for files from every volume

To restore a quarantined file to its original state and location, [add an exception](/solutions/security/detect-and-alert/add-manage-exceptions.md) to the rule that identified the file as malicious. If the exception would’ve stopped the rule from identifying the file as malicious, {{elastic-defend}} restores the file.

You can access a quarantined file by using the `get-file` [response action command](/solutions/security/endpoint-response-actions.md#response-action-commands) in the response console. To do this, copy the path from the alert’s **Quarantined file path** field (`file.Ext.quarantine_path`), which appears under **Highlighted fields** in the alert details flyout. Then paste the value into the `--path` parameter. This action doesn’t restore the file to its original location, so you will need to do this manually.

::::{important}
When you retrieve a quarantined file using `get-file`, the XOR obfuscation is automatically reversed, and the original malicious file is retrieved.
::::

::::{note}
* In {{stack}}, response actions and the response console UI are [Enterprise subscription](https://www.elastic.co/pricing) features.
* In {{serverless-short}}, response actions and the response console UI are Endpoint Protection Complete [project features](/deploy-manage/deploy/elastic-cloud/project-settings.md).
::::
