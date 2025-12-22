---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/host-isolation-ov.html
  - https://www.elastic.co/guide/en/serverless/current/security-isolate-host.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Isolate a host


Host isolation allows you to isolate hosts from your network, blocking communication with other hosts on your network until you release the host. Isolating a host is useful for responding to malicious activity or preventing potential attacks, as it prevents lateral movement across other hosts.

Isolated hosts, however, can still send data to {{elastic-sec}}. You can also create [host isolation exceptions](/solutions/security/manage-elastic-defend/host-isolation-exceptions.md) for specific IP addresses that isolated hosts are still allowed to communicate with, even when blocked from the rest of your network.

::::{admonition} Requirements
* Host isolation requires the appropriate [subscription](https://www.elastic.co/pricing) in {{stack}} or [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md) in {{serverless-short}}.
* Hosts must have {{agent}} installed with the {{elastic-defend}} integration.
* For {{stack}} versions >= 7.15.0 and {{serverless-short}}, host isolation is supported for endpoints running Windows, macOS, and these Linux distributions:

    * CentOS/RHEL 8
    * Debian 11
    * Ubuntu 18.04, 20.04, and 22.04
    * AWS Linux 2

* To isolate and release hosts running any operating system, you must have the **Host Isolation** [privilege](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md) or the appropriate user role.
::::


:::{image} /solutions/images/security-isolated-host.png
:alt: Endpoint page highlighting a host that's been isolated
:screenshot:
:::

You can isolate a host from a detection alert’s details flyout, from the Endpoints page, or from the endpoint response console. Once a host is successfully isolated, an `Isolated` status displays next to the `Agent status` field, which you can view on the alert details flyout or Endpoints list table.

::::{tip}
If the request fails, verify that the {{agent}} and your endpoint are both online before trying again.
::::


All actions executed on a host are tracked in the host’s response actions history, which you can access from the Endpoints page. Refer to [](/solutions/security/endpoint-response-actions/isolate-host.md#view-host-isolation-details) for more information.


## Isolate a host [isolate-a-host]

::::{dropdown} Isolate a host from an event or a detection alert
1. Do one of the following:
    * {applies_to}`stack: ga 9.1` From the event analyzer view: Click an event. 
    * From the Alerts table or Timeline: Click **View details** (![View details icon](/solutions/images/security-view-details-icon.png "title =20x20")).
    * From a case with an attached alert: Click **Show alert details** (**>**).

2. Click **Take action → Isolate host**.
3. Enter a comment describing why you’re isolating the host (optional).
4. Click **Confirm**.
::::


::::{dropdown} Isolate a host from an endpoint
1. Find **Endpoints** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then either:

    * Select the appropriate endpoint in the **Endpoint** column, and click **Take action → Isolate host** in the endpoint details flyout.
    * Click the **Actions** menu (**…**) on the appropriate endpoint, then select **Isolate host**.

2. Enter a comment describing why you’re isolating the host (optional).
3. Click **Confirm**.
::::


:::::{dropdown} Isolate a host from the response console
::::{note}
The response console requires the appropriate [subscription](https://www.elastic.co/pricing) in {{stack}} or [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md) in {{serverless-short}}.
::::


1. Open the response console for the host (select the **Respond** button or actions menu option on the host, endpoint, or alert details view).
2. Enter the `isolate` command and an optional comment in the input area, for example:

    `isolate --comment "Isolate this host"`

3. Press **Return**.
:::::


:::::{dropdown} Automatically isolate a host using a rule’s endpoint response action
::::{note}
The host isolation endpoint response action requires the appropriate [subscription](https://www.elastic.co/pricing) in {{stack}} or [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md) in {{serverless-short}}.
::::


::::{important}
Be aware that automatic host isolation can result in unintended consequences, such as disrupting legitimate user activities or blocking critical business processes.
::::


1. Add an endpoint response action to a new or existing custom query rule. The endpoint response action will run whenever rule conditions are met:

    * **New rule**: On the last step of [custom query rule](/solutions/security/detect-and-alert/create-detection-rule.md#create-custom-rule) creation, go to the **Response Actions** section and select **{{elastic-defend}}**.
    * **Existing rule**: Edit the rule’s settings, then go to the **Actions** tab. In the tab, select **{{elastic-defend}}** under the **Response Actions** section.

2. In the **Response action** field, select **Isolate**.
3. Enter a comment describing why you’re isolating the host (optional).
4. To finish adding the response action, click **Create & enable rule** (for a new rule) or **Save changes** (for existing rules).
:::::


After the host is successfully isolated, an **Isolated** status is added to the endpoint. Active end users receive a notification that the computer has been isolated from the network:

:::{image} /solutions/images/security-host-isolated-notif.png
:alt: Host isolated notification message
:width: 50%
:screenshot:
:::


## Release a host [release-a-host]

::::{dropdown} Release a host from an event or detection alert
1. Do one of the following:
    * {applies_to}`stack: ga 9.1` From the event analyzer view: Click an event.
    * From the Alerts table or Timeline: Click **View details** (![View details icon](/solutions/images/security-view-details-icon.png "title =20x20")).
    * From a case with an attached alert: Click **Show alert details** (**>**).

2. From the alert details flyout, click **Take action → Release host**.
3. Enter a comment describing why you’re releasing the host (optional).
4. Click **Confirm**.
::::


::::{dropdown} Release a host from an endpoint
1. Find **Endpoints** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then either:

    * Select the appropriate endpoint in the **Endpoint** column, and click **Take action → Release host** in the endpoint details flyout.
    * Click the **Actions** menu (**…**) on the appropriate endpoint, then select **Release host**.

2. Enter a comment describing why you’re releasing the host (optional).
3. Click **Confirm**.
::::


:::::{dropdown} Release a host from the response console
::::{note}
The response console requires the appropriate [subscription](https://www.elastic.co/pricing) in {{stack}} or [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md) in {{serverless-short}}.
::::


1. Open the response console for the host (select the **Respond** button or actions menu option on the host, endpoint, or alert details view).
2. Enter the `release` command and an optional comment in the input area, for example:

    `release --comment "Release this host"`

3. Press **Return**.
:::::


After the host is successfully released, the **Isolated** status is removed from the endpoint. Active end users receive a notification that the computer has been reconnected to the network:

:::{image} /solutions/images/security-host-released-notif.png
:alt: Host released notification message
:width: 50%
:screenshot:
:::


## View host isolation history [view-host-isolation-details]

To confirm if a host has been successfully isolated or released, check the response actions history, which logs the response actions performed on a host.

Go to the **Endpoints** page, click an endpoint’s name, then click the **Response action history** tab. You can filter the information displayed in this view. Refer to [](/solutions/security/endpoint-response-actions/response-actions-history.md) for more details.

:::{image} /solutions/images/security-response-actions-history-endpoint-details.png
:alt: Response actions history page UI
:width: 90%
:screenshot:
:::
