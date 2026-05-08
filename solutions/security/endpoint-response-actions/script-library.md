---
applies_to:
  stack: ga 9.4+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Script library

The script library provides a centralized location to upload, manage, and organize scripts for use with the [`runscript`](/solutions/security/endpoint-response-actions.md#runscript) response action on endpoints protected by {{elastic-defend}}. From the script library, you can upload new scripts, view script details and metadata, edit or delete existing scripts, and download scripts for offline review.

::::{admonition} Requirements
* The script library requires the appropriate [subscription](https://www.elastic.co/pricing) in {{stack}} or the appropriate [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md) in {{serverless-short}}.
* You must have the **{{elastic-defend}} Scripts Management** [privilege](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md) to access this feature.
::::

To access the script library, find **Script library** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

## Upload a script [upload-script]

1. From the **Script Library** page, click **Upload script**.
2. In the **Upload script** flyout, configure the following:

    **Required fields:**

    * **File**: Select or drag and drop a script file. You can upload individual script files (such as `.sh`, `.ps1`, or `.py`) or ZIP archive files that contain the script to run. Scripts are run on Windows machines using `CMD` and on Linux and MacOS machines using `Bash`.
    
      The default file size maximum is 25 MB, configurable in [`kibana.yml`](/deploy-manage/stack-settings.md) with the `xpack.securitySolution.maxEndpointScriptFileSize` setting. 

        ::::{note}
        Duplicate files are not allowed. If you upload a file with the same SHA256 hash as an existing script, the upload is rejected and an error message identifies the existing script.
        ::::

    * **File type**: Select the type of uploaded file — **Script file** or **Archive**. If you select **Archive**, you must also provide the **Path to executable file**, which is the relative path to the main script inside the archive (for example, `./scripts/cleanup_logs.sh`).
    * **Name**: Enter a display name for the script.
    * **Operating systems**: Select all the platforms that the script is compatible with (Linux, macOS, Windows).

    **Optional fields:**

    * **This script requires user input**: Select this option if the script prompts for or requires additional input parameters when executed.
    * **Categories**: Classify the script using one or more predefined categories, such as Data Collection, Remediation Action, or System Inventory.
    * **Description**: Enter a brief summary of what the script does.
    * **Instructions**: Provide step-by-step guidance on how to run or configure the script.
    * **Examples**: Provide one or more examples of how to use the script.

3. Click **Upload**.

## View and manage scripts [manage-scripts]

The **Script Library** page displays all uploaded scripts. You can search by script name, description, created by, updated by, file name or file SHA256 hash, and filter by **File type**, **Operating systems**, or **Categories**.

:::{image} /solutions/images/security-script-library.png
:alt: Script library showing a list of uploaded scripts
:screenshot:
:::

### View script details [view-script-details]

Click a script's name or select **View details** from the row's actions menu ({icon}`boxes_vertical`) to open a flyout with the script's full metadata, including its description, instructions, examples, file name, path to executable file (for archives), file size, and SHA256 hash.

### Edit a script [edit-script]

1. Click the actions menu ({icon}`boxes_vertical`) on the script you want to edit, then select **Edit script**.
2. Modify the metadata or replace the script file as needed.
3. Click **Save**.

::::{note}
You cannot remove an operating system from a script if a detection rule's `runscript` response action currently references the script for that operating system.
::::

### Download a script [download-script]

Click the actions menu ({icon}`boxes_vertical`) on the script you want to download, then select **Download script**.

### Delete a script [delete-script]

1. Click the actions menu ({icon}`boxes_vertical`) on the script you want to delete, then select **Delete script**.
2. On the confirmation dialog, click **Delete**.

::::{note}
If you delete a script that is currently referenced by a detection rule's `runscript` response action, the `runscript` action will fail when the rule runs.
::::
