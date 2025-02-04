# Rule exceptions [detections-ui-exceptions]

You can associate rule exceptions with detection and endpoint rules to prevent trusted processes and network activity from generating unnecessary alerts, therefore, reducing the number of false positives.

When creating exceptions, you can assign them to [individual rules](../../../solutions/security/detect-and-alert/rule-exceptions.md#rule-exceptions-intro) or to [multiple rules](../../../solutions/security/detect-and-alert/rule-exceptions.md#shared-exception-list-intro).


## Exceptions for individual rules [rule-exceptions-intro]

Exceptions, also referred to as *exception items*, contain the source event conditions that determine when alerts shouldn’t be generated.

You can create exceptions that apply exclusively to a single rule. These types of exceptions can’t be used by other rules, and you must manage them from the rule’s details page. To learn more about creating and managing single-rule exceptions, refer to [Add and manage exceptions](../../../solutions/security/detect-and-alert/add-manage-exceptions.md).

:::{image} ../../../images/security-exception-item-example.png
:alt: An exception item
:class: screenshot
:::

::::{note}
You can also use [value lists](../../../solutions/security/detect-and-alert/create-manage-value-lists.md) to define exceptions for detection rules. Value lists allow you to match an exception against a list of possible values.
::::



## Exceptions shared among multiple rules [shared-exception-list-intro]

If you want an exception to apply to multiple rules, you can add an exception to a shared exception list. Shared exception lists allow you to group exceptions together and then associate them with multiple rules. Refer to [Create and manage shared exception lists](../../../solutions/security/detect-and-alert/create-manage-shared-exception-lists.md) to learn more.

:::{image} ../../../images/security-rule-exceptions-page.png
:alt: Shared Exception Lists page
:class: screenshot
:::




