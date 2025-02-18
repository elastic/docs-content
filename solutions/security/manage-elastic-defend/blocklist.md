---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/blocklist.html
  - https://www.elastic.co/guide/en/serverless/current/security-blocklist.html
---

# Blocklist

% What needs to be done: Align serverless/stateful

% Use migrated content from existing pages that map to this page:

% - [x] ./raw-migrated-files/security-docs/security/blocklist.md
% - [ ] ./raw-migrated-files/docs-content/serverless/security-blocklist.md

The blocklist allows you to prevent specified applications from running on hosts, extending the list of processes that {{elastic-defend}} considers malicious. This helps ensure that known malicious processes aren’t accidentally executed by end users.

The blocklist is not intended to broadly block benign applications for non-security reasons; only use it to block potentially harmful applications. To compare the blocklist with other endpoint artifacts, refer to [*Optimize {{elastic-defend}}*](/solutions/security/manage-elastic-defend/optimize-elastic-defend.md).

::::{admonition} Requirements
* In addition to configuring specific entries on the **Blocklist** page, you must also ensure that the blocklist is enabled on the {{elastic-defend}} integration policy in the [Malware protection settings](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#malware-protection). This setting is enabled by default.
* You must have the **Blocklist** [privilege](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md) to access this feature.

::::


By default, a blocklist entry is recognized globally across all hosts running {{elastic-defend}}. If you have a [Platinum or Enterprise subscription](https://www.elastic.co/pricing), you can also assign a blocklist entry to specific {{elastic-defend}} integration policies, which blocks the process only on hosts assigned to that policy.

1. Find **Blocklist** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Add blocklist entry**. The **Add blocklist** flyout appears.
3. Fill in these fields in the **Details** section:

    1. `Name`: Enter a name to identify the application in the blocklist.
    2. `Description`: Enter a description to provide more information on the blocklist entry (optional).

4. In the **Conditions** section, enter the following information about the application you want to block:

    1. `Select operating system`: Select the appropriate operating system from the drop-down.
    2. `Field`: Select a field to identify the application being blocked:

        * `Hash`: The MD5, SHA-1, or SHA-256 hash value of the application’s executable.
        * `Path`: The full file path of the application’s executable.
        * `Signature`: (Windows only) The name of the application’s digital signer.

            ::::{tip}
            To find the signer’s name for an application, go to **Kibana** → **Discover** and query the process name of the application’s executable (for example, `process.name : "mctray.exe"` for a McAfee security binary). Then, search the results for the `process.code_signature.subject_name` field, which contains the signer’s name (for example, `McAfee, Inc.`).
            ::::

    3. `Operator`: For hash and path conditions, the operator is `is one of` and can’t be modified. For signature conditions, choose `is one of` to enter multiple values or `is` for one value.
    4. `Value`: Enter the hash value, file path, or signer name. To enter multiple values (such as a list of known malicious hash values), you can enter each value individually or paste a comma-delimited list, then press **Return**.

        ::::{note}
        Hash values must be valid to add them to the blocklist.
        ::::

5. Select an option in the **Assignment** section to assign the blocklist entry to a specific integration policy:

    * `Global`: Assign the blocklist entry to all {{elastic-defend}} integration policies.
    * `Per Policy`: Assign the blocklist entry to one or more specific {{elastic-defend}} integration policies. Select each policy where you want the blocklist entry to apply.

        ::::{note}
        You can also select the `Per Policy` option without immediately assigning a policy to the blocklist entry. For example, you could do this to create and review your blocklist configurations before putting them into action with a policy.
        ::::

6. Click **Add blocklist**. The new entry is added to the **Blocklist** page.
7. When you’re done adding entries to the blocklist, ensure that the blocklist is enabled for the {{elastic-defend}} integration policies that you just assigned:

    1. Go to the **Policies** page, then click on an integration policy.
    2. On the **Policy settings** tab, ensure that the **Malware protections** and **Blocklist** toggles are switched on. Both settings are enabled by default.



## View and manage the blocklist [manage-blocklist]

The **Blocklist** page displays all the blocklist entries that have been added to the {{security-app}}. To refine the list, use the search bar to search by name, description, or field value.

:::{image} ../../../images/security-blocklist.png
:alt: blocklist
:class: screenshot
:::


### Edit a blocklist entry [edit-blocklist-entry]

You can individually modify each blocklist entry. With a Platinum or Enterprise subscription, you can also change the policies that a blocklist entry is assigned to.

To edit a blocklist entry:

1. Click the actions menu (**…​**) for the blocklist entry you want to edit, then select **Edit blocklist**.
2. Modify details as needed.
3. Click **Save**.


### Delete a blocklist entry [delete-blocklist-entry]

You can delete a blocklist entry, which removes it entirely from all {{elastic-defend}} policies. This allows end users to access the application that was previously blocked.

To delete a blocklist entry:

1. Click the actions menu (**…​**) for the blocklist entry you want to delete, then select **Delete blocklist**.
2. On the dialog that opens, verify that you are removing the correct blocklist entry, then click **Delete**. A confirmation message displays.
