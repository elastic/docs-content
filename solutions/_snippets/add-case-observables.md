An observable is a piece of information about an investigation, for example, a suspicious URL or a file hash. Use observables to identify correlated events and better understand the severity and scope of a case. 

To view and manage observables, go to the **Observables** tab. You can find the tab in the following places:

- {applies_to}`stack: ga 9.3`: Go to the case's details page, then select the **Attachments** tab.
- {applies_to}`stack: ga 9.0`: Go to the case's details page.  

::::{important}
Each case can have a maximum of 50 observables.
::::

To create an observable:

1. Click **Add observable** from the **Observables** tab.
2. Provide the necessary details:

    * **Type**: Select a type for the observable. You can choose a preset type or a [custom one](/solutions/security/investigate/configure-case-settings.md#cases-observable-types).
    * **Value**: Enter a value for the observable. The value must align with the type you select.
    * **Description** (Optional): Provide additional information about the observable.

3. Click **Add observable**.

After adding an observable to a case, you can remove or edit it by using the **Actions** menu (**…**). 

::::{tip}
Go to the **Similar cases** tab to access other cases with the same observables.
::::