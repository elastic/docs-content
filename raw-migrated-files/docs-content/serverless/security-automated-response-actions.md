# Automated response actions [security-automated-response-actions]

Add {{elastic-defend}}'s [response actions](../../../solutions/security/endpoint-response-actions.md) to detection rules to automatically perform actions on an affected host when an event meets the rule’s criteria. Use these actions to support your response to detected threats and suspicious events.

::::{admonition} Requirements
:class: note

* Automated response actions require the Endpoint Protection Complete [project feature](../../../deploy-manage/deploy/elastic-cloud/project-settings.md).
* Hosts must have {{agent}} installed with the {{elastic-defend}} integration.
* Your user role must have the ability to create detection rules and the privilege to perform [specific response actions](../../../solutions/security/endpoint-response-actions.md#response-action-commands) (for example, custom roles require the **Host Isolation** privilege to isolate hosts).

::::


To add automated response actions to a new or existing rule:

1. Do one of the following:

    * **New rule**: On the last step of rule creation, go to the **Response Actions** section and select **{{elastic-defend}}**.
    * **Existing rule**: Edit the rule’s settings, then go to the **Actions*** tab. In the tab, select ***{{elastic-defend}}** under the **Response Actions** section.

2. Select an option in the **Response action** field:

    * **Isolate**: [Isolate the host](../../../solutions/security/endpoint-response-actions/isolate-host.md), blocking communication with other hosts on the network.
    * **Kill process**: Terminate a process on the host.
    * **Suspend process**: Temporarily suspend a process on the host.

        ::::{important}
        Be aware that automatic host isolation can result in unintended consequences, such as disrupting legitimate user activities or blocking critical business processes.

        ::::

3. For process actions, specify how to identify the process you want to terminate or suspend:

    * Turn on the toggle to use the alert’s **process.pid** value as the identifier.
    * To use a different alert field value to identify the process, turn off the toggle and enter the **Custom field name**.

4. Enter a comment describing why you’re performing the action on the host (optional).
5. To finish adding the response action, click **Create & enable rule** (for a new rule) or **Save changes** (for existing rules).
