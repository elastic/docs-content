---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/host-isolation-exceptions.html
  - https://www.elastic.co/guide/en/serverless/current/security-host-isolation-exceptions.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Host isolation exceptions


You can configure host isolation exceptions for specific IP addresses that [isolated hosts](/solutions/security/endpoint-response-actions/isolate-host.md) are still allowed to communicate with, even when blocked from the rest of your network. Isolated hosts can still send data to {{elastic-sec}}, so you don’t need to set up host isolation exceptions for them.

Host isolation exceptions support IPv4 addresses, with optional classless inter-domain routing (CIDR) notation.

::::{admonition} Requirements
* You must have the **Host Isolation Exceptions** [privilege](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md) or the appropriate user role to access this feature.
* Host isolation requires the appropriate [subscription](https://www.elastic.co/pricing) in {{stack}} or [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md) in {{serverless-short}}.
::::


::::{important}
* Each host isolation exception IP address should be a highly trusted and secure location since you’re allowing it to communicate with hosts that have been isolated to prevent a potential threat from spreading.
* If your hosts depend on VPNs for network communication, you should also set up host isolation exceptions for those VPN servers' IP addresses.

::::

By default, a host isolation exception is recognized globally across all hosts running {{elastic-defend}}. You can also assign a host isolation exception to a specific {{elastic-defend}} integration policy, affecting only the hosts assigned to that policy.

1. Find **Host isolation exceptions** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Add Host isolation exception**.
3. Fill in these fields in the **Add Host isolation exception** flyout:

    1. `Name your host isolation exceptions`: Enter a name to identify the host isolation exception.
    2. `Description`: Enter a description to provide more information on the host isolation exception (optional).
    3. `Enter IP Address`: Enter the IP address for which you want to allow communication with an isolated host. This must be an IPv4 address, with optional CIDR notation (for example, `0.0.0.0` or `1.0.0.0/24`, respectively).

4. Select an option in the **Assignment** section to assign the host isolation exception to a specific integration policy:

    * `Global`: Assign the host isolation exception to all integration policies for {{elastic-defend}}.
    * `Per Policy`: Assign the host isolation exception to one or more specific {{elastic-defend}} integration policies. Select each policy where you want the host isolation exception to apply.

        ::::{note}
        You can also select the `Per Policy` option without immediately assigning a policy to the host isolation exception. For example, you could do this to create and review your host isolation exception configurations before putting them into action with a policy.
        ::::

5. Click **Add Host isolation exception**. The new exception is added to the **Host isolation exceptions** list.


## View and manage host isolation exceptions [manage-host-isolation-exceptions]

The **Host isolation exceptions** page displays all the host isolation exceptions that have been configured for {{elastic-sec}}. To refine the list, use the search bar to search by name, description, or IP address.

:::{image} /solutions/images/security-host-isolation-exceptions-ui.png
:alt: List of host isolation exceptions
:screenshot:
:::


### Edit a host isolation exception [edit-host-isolation-exception]

You can individually modify each host isolation exception and change the policies that a host isolation exception is assigned to.

To edit a host isolation exception:

1. Click the actions menu (**…**) for the exception you want to edit, then select **Edit Exception**.
2. Modify details as needed.
3. Click **Save**. The newly modified exception appears at the top of the list.


### Delete a host isolation exception [delete-host-isolation-exception]

You can delete a host isolation exception, which removes it entirely from all {{elastic-defend}} integration policies.

To delete a host isolation exception:

1. Click the actions menu (**…**) on the exception you want to delete, then select **Delete Exception**.
2. On the dialog that opens, verify that you are removing the correct host isolation exception, then click **Delete**. A confirmation message is displayed.
