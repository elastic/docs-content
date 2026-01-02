---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/trusted-apps-ov.html
  - https://www.elastic.co/guide/en/serverless/current/security-trusted-applications.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Trusted applications

::::{note}
If you use {{elastic-defend}} along with other antivirus (AV) software, you might need to configure the other system to trust {{elastic-endpoint}}. Refer to [](/solutions/security/manage-elastic-defend/allowlist-elastic-endpoint-in-third-party-antivirus-apps.md) for more information.
::::


You can add Windows, macOS, and Linux applications that should be trusted, such as other antivirus or endpoint security applications. Trusted applications are designed to help mitigate performance issues and incompatibilities with other endpoint software installed on your hosts. Trusted applications apply only to hosts running the {{elastic-defend}} integration.

::::{tip}
To ensure you're using the right feature for your use case, we recommend reviewing [](/solutions/security/manage-elastic-defend/optimize-elastic-defend.md) to understand the differences between trusted applications and alert exceptions.
::::

::::{admonition} Requirements
You must have the **Trusted Applications** [privilege](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md) or the appropriate user role to access this feature.
::::


Trusted applications create blindspots for {{elastic-defend}}, because the applications are no longer monitored for threats. One avenue attackers use to exploit these blindspots is by DLL (Dynamic Link Library) side-loading, where they leverage processes signed by trusted vendors — such as antivirus software — to execute their malicious DLLs. Such activity appears to originate from the trusted application’s process.

Trusted applications might still generate alerts in some cases, such as if the application’s process events indicate malicious behavior. To reduce false positive alerts, add an [Endpoint alert exception](/solutions/security/detect-and-alert/add-manage-exceptions.md#endpoint-rule-exceptions), which prevents {{elastic-defend}} from generating alerts. To compare trusted applications with other endpoint artifacts, refer to [](/solutions/security/manage-elastic-defend/optimize-elastic-defend.md).

Additionally, trusted applications still generate process events for visualizations and other internal use by the {{stack}}. To prevent process events from being written to {{es}}, use an [event filter](/solutions/security/manage-elastic-defend/event-filters.md) to filter out the specific events that you don’t want stored in {{es}}, but be aware that features that depend on these process events may not function correctly.

By default, a trusted application is recognized globally across all hosts running {{elastic-defend}}. You can also assign a trusted application to a specific {{elastic-defend}} integration policy, enabling the application to be trusted by only the hosts assigned to that policy.

To add a trusted application:

1. Find **Trusted applications** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Add trusted application**.
3. Fill in these fields in the **Details** section:

    1. `Name`: Enter a name for the trusted application.
    2. `Description` (Optional): Enter a description for the trusted application.
4. Select an option in the **Conditions** section:

   :::::{tab-set}

   ::::{tab-item} Basic

   Define conditions based on the application's hash, executable path, or signer.

    1. `Select operating system`: Select the appropriate operating system from the drop-down.
    2. `Field`: Select a field to identify the trusted application:

        * `Hash`: The MD5, SHA-1, or SHA-256 hash value of the application’s executable.
        * `Path`: The full file path of the application’s executable.
        * `Signature`: (Windows and macOS only) The name of the application’s digital signer.

            ::::{tip}
            To find the signer’s name for an application, go to **Discover** and query the process name of the application’s executable (for example, `process.name : "mctray.exe"` for a McAfee security binary). Then, search the results for the `process.code_signature.subject_name` field, which contains the signer’s name (for example, `McAfee, Inc.`).
            ::::

    3. `Operator`: Select an operator to define the condition:

        * `is`: Must be *exactly* equal to `Value`; wildcards are not supported. This operator is required for the `Hash` and `Signature` field types.
        * `matches`: Can include wildcards in `Value`, such as `C:\path\*\app.exe`. This option is only available for the `Path` field type. Available wildcards are `?` (match one character) and `*` (match zero or more characters).

          ::::{note}
          Unlike detection rule exceptions, trusted applications do not require escaping special characters.
          ::::

    4. `Value`: Enter the hash value, file path, or signer name. To add an additional value, click **AND**.

        ::::{note}
        You can only add a single field type value per trusted application. For example, if you try to add two `Path` values, you’ll get an error message. Also, an application’s hash value must be valid to add it as a trusted application. In addition, to minimize visibility gaps in the {{security-app}}, be as specific as possible in your entries. For example, combine `Signature` information with a known `Path`.
        ::::

   ::::

   ::::{tab-item} Advanced

   {applies_to}`stack: ga 9.2`

   Define more complex conditions, such as trusting specific file paths or remote IP addresses.

    1. `Select operating system`: Select the appropriate operating system from the drop-down.
    2. `Field`: Select a field to identify the trusted application.
    3. `Operator`: Select an operator to define the condition:
       * `is`
       * `is not`
       * `is one of`
       * `is not one of`
       * `matches` | `does not match`:  Allows you to use wildcards in `Value`, such as `C:\path\*\app.exe`.  Available wildcards are `?` (match one character) and `*` (match zero or more characters).

          ::::{note}
          Unlike detection rule exceptions, trusted applications do not require escaping special characters.
          ::::

          ::::{important}
          Using wildcards can impact performance. To create a more efficient trusted application using wildcards, use multiple conditions and make them as specific as possible. For example, adding conditions using `process.name` or `file.name` can help limit the scope of wildcard matching.
          ::::

    4. `Value`: Enter the value associated with the `Field`. To enter multiple values (when using `is one of` or `is not one of`), enter each value, then press **Return**. 
    5. To define multiple conditions, click `AND` and configure a new condition. You can also add nested conditions by selecting `Add nested condition`.

   :::::

4. Select an option in the **Assignment** section to assign the trusted application to a specific integration policy:

    * `Global`: Assign the trusted application to all integration policies for {{elastic-defend}}.
    * `Per Policy`: Assign the trusted application to one or more specific {{elastic-defend}} integration policies. Select each policy in which you want the application to be trusted.

        ::::{note}
        You can also select the `Per Policy` option without immediately assigning a policy to the trusted application. For example, you could do this to create and review your trusted application configurations before putting them into action with a policy.
        ::::

5. Click **Add trusted application**. The application is added to the **Trusted applications** list.


## View and manage trusted applications [trusted-apps-list]

The **Trusted applications** page displays all the trusted applications that have been added to the {{security-app}}. To refine the list, use the search bar to search by name, description, or field value.

:::{image} /solutions/images/security-trusted-apps-list.png
:alt: trusted apps list
:screenshot:
:::


### Edit a trusted application [edit-trusted-app]

You can individually modify each trusted application. You can also change the policies that a trusted application is assigned to.

To edit a trusted application:

1. Click the actions menu (**…**) on the trusted application you want to edit, then select **Edit trusted application**.
2. Modify details as needed.
3. Click **Save**.


### Delete a trusted application [delete-trusted-app]

You can delete a trusted application, which removes it entirely from all {{elastic-defend}} integration policies.

To delete a trusted application:

1. Click the actions menu (**…**) on the trusted application you want to delete, then select **Delete trusted application**.
2. On the dialog that opens, verify that you are removing the correct application, then click **Delete**. A confirmation message appears.
