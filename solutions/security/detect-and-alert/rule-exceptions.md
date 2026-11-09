---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/detections-ui-exceptions.html
  - https://www.elastic.co/guide/en/serverless/current/security-rule-exceptions.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
description: Associate rule exceptions with detection rules to prevent trusted activity from generating unnecessary alerts.
---

# Rule exceptions [detections-ui-exceptions]

You can associate rule exceptions with detection and endpoint rules to prevent trusted processes and network activity from generating unnecessary alerts, therefore, reducing the number of false positives.

When creating exceptions, you can assign them to [individual rules](#rule-exceptions-intro) or to [multiple rules](#shared-exception-list-intro). If a rule fires on activity that's normal in any environment, [tune the rule](/solutions/security/detect-and-alert/tune-detection-rules.md) instead.

## Exceptions for authorized activity [exceptions-authorized-activity]

Authorized activity often triggers detection rules because it looks like what attackers do. When a rule correctly detects a behavior that your organization performs on purpose, add an exception so the rule ignores that specific source. Common examples include the following activity.

* Authorized security testing and research
* System and software management tools that run scripts, including scripts that start child processes
* Administration frameworks that create users, schedule tasks, make `psexec` connections, or run WMI commands
* Backup programs and other applications that use file shares over the server message block (SMB) protocol
* Microsoft Office files with macros or scripts that users receive from a trusted third party
* Scripts that support staff give remote workers to collect troubleshooting information

Match the exception to what identifies the authorized source, such as the host (`host.name is <server-name>`), the process (`process.name is <process-name>`), or the user (`user.name is <security-tester>`). Combine conditions where you can. An exception that matches only a process name also hides that process when an attacker runs it.

Take extra care with exceptions on rules that detect initial access or persistence, such as [Suspicious MS Office Child Process](detection-rules://rules/windows/initial_access_suspicious_ms_office_child_process.md). A broad exception on these rules can let a malicious document or a persistence mechanism go unnoticed.

If you still want alerts for the activity, but at a lower priority, [lower the rule's severity or risk score](/solutions/security/detect-and-alert/tune-detection-rules.md#change-rule-logic) instead of adding an exception.


## Exceptions for individual rules [rule-exceptions-intro]

Exceptions, also referred to as **exception items**, contain the source event conditions that determine when alerts shouldn’t be generated.

You can create exceptions that apply exclusively to a single rule. These types of exceptions can’t be used by other rules, and you must manage them from the rule’s details page. To learn more about creating and managing single-rule exceptions, refer to [Add and manage exceptions](add-manage-exceptions.md).

:::{image} /solutions/images/security-exception-item-example.png
:alt: An exception item
:screenshot:
:::

::::{note}
You can also use [value lists](create-manage-value-lists.md) to define exceptions for detection rules. Value lists allow you to match an exception against a list of possible values.
::::



## Exceptions shared among multiple rules [shared-exception-list-intro]

If you want an exception to apply to multiple rules, you can add an exception to a shared exception list. Shared exception lists allow you to group exceptions together and then associate them with multiple rules. Refer to [Create and manage shared exception lists](create-manage-shared-exception-lists.md) to learn more.

:::{image} /solutions/images/security-rule-exceptions-page.png
:alt: Shared Exception Lists page
:screenshot:
:::




