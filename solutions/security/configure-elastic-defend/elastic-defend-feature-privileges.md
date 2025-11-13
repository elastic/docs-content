---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/endpoint-management-req.html
  - https://www.elastic.co/guide/en/serverless/current/security-endpoint-management-req.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# {{elastic-defend}} feature privileges


You can create user roles and define privileges to manage feature access in {{elastic-sec}}. This allows you to use the principle of least privilege while managing access to {{elastic-defend}}'s features.

To configure roles and privileges, find **Roles** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). For more details on using this UI, refer to [](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for {{stack}}, or to [Custom roles](/deploy-manage/users-roles/cloud-organization/user-roles.md) for {{serverless-short}}.

::::{note}
{applies_to}`stack: ga 9.1` {{elastic-defend}}'s feature privileges can be assigned on a per-space basis. For more information, refer to [Spaces and Elastic Defend FAQ](/solutions/security/get-started/spaces-defend-faq.md).
::::

To grant access, select **All** for the **Security** feature in the **Assign role to space** configuration UI, then turn on the **Customize sub-feature privileges** switch.

::::{important}
Selecting **All** for the overall **Security** feature does NOT enable any sub-features. You must also enable the **Customize sub-feature privileges** switch, and then enable each sub-feature privilege individually.
::::


For each of the following sub-feature privileges, select the type of access you want to allow:

* **All**: Users have full access to the feature, which includes performing all available actions and managing configuration.
* **Read**: Users can view the feature, but can’t perform any actions or manage configuration (some features don’t have this privilege).
* **None**: Users can’t access or view the feature.

|     |     |
| --- | --- |
| **Endpoint List** | Access the [Endpoints](/solutions/security/manage-elastic-defend/endpoints.md) page, which lists all hosts running {{elastic-defend}}, and associated integration details. |
| **Automatic Troubleshooting** |Access [Automatic Troubleshooting](/solutions/security/manage-elastic-defend/automatic-troubleshooting.md) to check if your hosts have third-party AV software installed.<br><br>**Note:** In {{stack}} 9.0.0, this privilege is called **Endpoint Insights**. |
| **Global Artifact Management** {applies_to}`stack: ga 9.1` | Manage global assignment of endpoint artifacts (e.g., trusted applications, event filters) across all spaces and policies. This privilege controls global assignment rights only; privileges for each artifact type are required for full artifact management. |
| **Trusted Applications** | Access the [Trusted applications](/solutions/security/manage-elastic-defend/trusted-applications.md) page to remediate conflicts with other software, such as antivirus or endpoint security applications. |
| **Trusted Devices** {applies_to}`stack: ga 9.2` {applies_to}`serverless: ga`| Access the [Trusted devices](/solutions/security/manage-elastic-defend/trusted-devices.md) page to specify which trusted devices can connect to hosts with [Device Control](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#device-control) enabled.
| **Host Isolation Exceptions** | Access the [Host isolation exceptions](/solutions/security/manage-elastic-defend/host-isolation-exceptions.md) page to add specific IP addresses that isolated hosts can still communicate with. |
| **Blocklist** | Access the [Blocklist](/solutions/security/manage-elastic-defend/blocklist.md) page to prevent specified applications from running on hosts, extending the list of processes that {{elastic-defend}} considers malicious. |
| **Event Filters** | Access the [Event Filters](/solutions/security/manage-elastic-defend/event-filters.md) page to filter out endpoint events that you don’t want stored in {{es}}. |
| **Endpoint Exceptions** {applies_to}`stack: ga 9.2` {applies_to}`serverless: ga`| Add and use [endpoint exceptions](/solutions/security/detect-and-alert/add-manage-exceptions.md#endpoint-rule-exceptions).<br><br>**Note:** In {{stack}} 9.1.0 and earlier, this privilege is included within the **Security** privilege. |
| **{{elastic-defend}} Policy Management** | Access the [Policies](/solutions/security/manage-elastic-defend/policies.md) page and {{elastic-defend}} integration policies to configure protections, event collection, and advanced policy features. |
| **Response Actions History** | Access the [response actions history](/solutions/security/endpoint-response-actions/response-actions-history.md) for endpoints. |
| **Host Isolation** | Allow users to [isolate and release hosts](/solutions/security/endpoint-response-actions/isolate-host.md). |
| **Process Operations** | Perform host process-related [response actions](/solutions/security/endpoint-response-actions.md), including `processes`, `kill-process`, and `suspend-process`. |
| **File Operations** | Perform file-related [response actions](/solutions/security/endpoint-response-actions.md) in the response console. |
| **Execute Operations** | Perform shell commands and script-related [response actions](/solutions/security/endpoint-response-actions.md) in the response console.<br><br>The commands are run on the host using the same user account running the {{elastic-defend}} integration, which normally has full control over the system. Only grant this feature privilege to {{elastic-sec}} users who require this level of access. |
| **Scan Operations** | Perform folder scan [response actions](/solutions/security/endpoint-response-actions.md) in the response console. |

% The paragraph starting with "The commands are run ..." was in a warning admonition. Since admonitions inside tables aren't supported yet, converted this into plain text.

## Upgrade considerations [_upgrade_considerations]
```yaml {applies_to}
stack:
```

After upgrading from {{elastic-sec}} 8.6 or earlier, existing user roles will be assigned **None** by default for any new endpoint management feature privileges, and you’ll need to explicitly assign them. However, many features previously required the built-in `superuser` role, and users who previously had this role will still have it after upgrading.

You’ll probably want to replace the broadly permissive `superuser` role with more focused feature-based privileges to ensure that users have access to only the specific features that they need. Refer to [{{kib}} role management](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) for more details on assigning roles and privileges.
