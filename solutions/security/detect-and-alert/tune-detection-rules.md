---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/tuning-detection-signals.html
  - https://www.elastic.co/guide/en/serverless/current/security-tune-detection-signals.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Tune detection rules [security-tune-detection-signals]

Using the {{security-app}}, you can tune prebuilt and custom detection rules to optimize alert generation. To reduce noise, you can:

* Add [exceptions](/solutions/security/detect-and-alert/add-manage-exceptions.md) to detection rules.

    ::::{tip}
    Using exceptions is recommended as this ensure excluded source event values persist even after prebuilt rules are updated.
    ::::

* Disable detection rules that rarely produce actionable alerts because they match expected local behavior, workflows, or policy exceptions.
* [Clone and modify](/solutions/security/detect-and-alert/manage-detection-rules.md#duplicate-rules) detection rule queries so they are aligned with local policy exceptions. This reduces noise while retaining actionable alerts.
* Clone and modify detection rule risk scores, and use branching logic to map higher risk scores to higher priority workflows.
* Enable [alert suppression](/solutions/security/detect-and-alert/suppress-detection-alerts.md) for custom query rules to reduce the number of repeated or duplicate alerts.

For details about tuning rules for specific categories:

* [Tune rules detecting authorized processes](/solutions/security/detect-and-alert/tune-detection-rules.md#tune-authorized-processes)
* [Tune Windows child process and PowerShell rules](/solutions/security/detect-and-alert/tune-detection-rules.md#tune-windows-rules)
* [Tune network rules](/solutions/security/detect-and-alert/tune-detection-rules.md#tune-network-rules)
* [Tune indicator match rules](/solutions/security/detect-and-alert/tune-detection-rules.md#tune-indicator-rules)


## Filter out uncommon application alerts [filter-rule-process]

Organizations frequently use uncommon and in-house applications. Occasionally, these can trigger unwanted alerts. To stop a rule matching on an application, add an exception for the required application.

For example, to prevent the [Unusual Process Execution Path - Alternate Data Stream](detection-rules://rules/windows/defense_evasion_unusual_dir_ads.md) rule from producing alerts for an in-house application named `myautomatedbuild`:

1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the Rules table, search for and then click on the **Unusual Process Execution Path - Alternate Data Stream** rule.

    The **Unusual Process Execution Path - Alternate Data Stream** rule details page is displayed.

    :::{image} /solutions/images/security-rule-details-page.png
    :alt: Rule details page
    :screenshot:
    :::

3. Select the **Rule exceptions** tab, then click **Add rule exception**.
4. Fill in these options:

    * **Field**: `process.name`
    * **Operator**: `is`
    * **Value**: `myautomatedbuild`

        :::{image} /solutions/images/security-process-exception.png
        :alt: Add Rule Exception UI
        :screenshot:
        :::

5. Click **Add rule exception**.


## Tune rules detecting authorized processes [tune-authorized-processes]

Authorized security testing, system tools, management frameworks, and administrative activity may trigger detection rules. These legitimate activities include:

* Authorized security research.
* System and software management processes running scripts, including scripts that start child processes.
* Administrative and management frameworks that create users, schedule tasks, make `psexec` connections, and run WMI commands.
* Legitimate scripts using the `whoami` command.
* Applications that work with file shares, such as backup programs, and use the server message block (SMB) protocol.

To reduce noise for authorized activity, you can do any of these:

* Add an exception to the rules that exclude specific servers, such as the relevant host names, agent names, or other common identifiers. For example, `host.name is <server-name>`.
* Add an exception to the rules that [exclude specific processes](/solutions/security/detect-and-alert/tune-detection-rules.md#filter-rule-process). For example, `process.name is <process-name>`.
* Add an exception to the rules that exclude a common user. For example, `user.name is <security-tester>`.

Another useful technique is to assign lower risk scores to rules triggered by authorized activity. This enables detections while keeping the resulting alerts out of high-priority workflows. Use these steps:

1. Before adding exceptions, duplicate the prebuilt rule.
2. Add an exception to the original prebuilt rule that excludes the relevant user or process name (`user.name is <user-name>` or `process.name is "process-name"`).
3. Edit the duplicated rule as follows:

    * Lower the `Risk score` (**Edit rule settings** → **About** tab).
    * Add an exception so the rule only matches the user or process name excluded in original prebuilt rules. (`user.name is not <user-name>` or `process.name is not <process-name>`).

        :::{image} /solutions/images/security-process-specific-exception.png
        :alt: Example of `is not` exception in the Add Rule Exception UI
        :screenshot:
        :::

4. Click **Add rule exception**.


## Tune Windows child process and PowerShell rules [tune-windows-rules]

Normal user activity may sometimes trigger one or more of these rules:

* [Suspicious MS Office Child Process](detection-rules://rules/windows/initial_access_suspicious_ms_office_child_process.md)
* [Suspicious MS Outlook Child Process](detection-rules://rules/windows/initial_access_suspicious_ms_outlook_child_process.md)
* [System Shells via Services](detection-rules://rules/windows/persistence_system_shells_via_services.md)
* [Unusual Parent-Child Relationship](detection-rules://rules/windows/privilege_escalation_unusual_parentchild_relationship.md)
* [Windows Script Executing PowerShell](detection-rules://rules/windows/initial_access_script_executing_powershell.md)

While all rules can be adjusted as needed, use care when adding exceptions to these rules. Exceptions could result in an undetected client-side execution, or a persistence or malware threat going unnoticed.

Examples of when these rules may create noise include:

* Receiving and opening email-attached Microsoft Office files, which include active content such as macros or scripts, from a trusted third-party source.
* Authorized technical support personnel who provide remote workers with scripts to gather troubleshooting information.

In these cases, exceptions can be added to the rules using the relevant `process.name`, `user.name`, and `host.name` conditions. Additionally, you can create duplicate rules with lower risk scores.


## Tune network rules [tune-network-rules]

The definition of normal network behavior varies widely across different organizations. Different networks conform to different security policies, standards, and regulations. When normal network activity triggers alerts, network rules can be disabled or modified. For example:

* To exclude a specific source, add a `source.ip` exception with the relevant IP address, and a `destination.port` exception with the relevant port number (`source.ip is 196.1.0.12` and `destination.port is 445`).
* To exclude source network traffic for an entire subnet, add a `source.ip` exception with the relevant CIDR notation (`source.ip is 192.168.0.0/16`).
* To exclude a destination IP for a specific destination port, add a `destination.ip` exception with the IP address, and a `destination.port` exception with the port number (`destination.ip is 38.160.150.31` and `destination.port is 445`)
* To exclude a destination subnet for a specific destination port, add a `destination.ip` exception using CIDR notation, and a ‘destination.port’ exception with the port number (`destination.ip is 172.16.0.0/12` and `destination.port is 445`).


## Tune indicator match rules [tune-indicator-rules]

Take the following steps to tune indicator match rules:

* Specify a detailed query as part of the indicator index query. Results of the indicator index query are used by the detection engine to query the indices specified in your rule definition’s index pattern. Using no query or the wildcard `***` query may result in your rule executing very large queries.
* Limit your rule’s additional look-back time to as short a duration as possible, and no more than 24 hours.
* Avoid cluster performance issues by scheduling your rule to run in one-hour intervals or longer. For example, avoid scheduling an indicator match rule to check for indicators every five minutes.

::::{note}
{{elastic-sec}} provides limited support for indicator match rules. Visit [support limitations](/solutions/security/detect-and-alert.md#support-indicator-rules) for more information.
::::



### Noise from common cloud-based network traffic [security-tune-detection-signals-noise-from-common-cloud-based-network-traffic]

In cloud-based organizations, remote workers sometimes access services over the internet. The security policies of home networks probably differ from the security policies of managed corporate networks, and these rules might need tuning to reduce noise from legitimate administrative activities:

* [RDP (Remote Desktop Protocol) from the Internet](detection-rules://rules/network/command_and_control_rdp_remote_desktop_protocol_from_the_internet.md)

::::{tip}
If your organization is widely distributed and the workforce travels a lot, use the `windows_anomalous_user_name_ecs`, `linux_anomalous_user_name_ecs`, and `suspicious_login_activity_ecs` [{{ml}}](/solutions/security/advanced-entity-analytics/anomaly-detection.md) jobs to detect suspicious authentication activity.
::::


