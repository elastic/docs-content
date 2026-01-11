---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/response-actions-config.html
  - https://www.elastic.co/guide/en/serverless/current/security-response-actions-config.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Configure third-party response actions


You can direct third-party endpoint protection systems to perform response actions on enrolled hosts, such as isolating a suspicious endpoint from your network, without leaving the {{elastic-sec}} UI. This page explains the configuration steps needed to enable response actions for these third-party systems:

* CrowdStrike
* Microsoft Defender for Endpoint
* SentinelOne

Check out [](/solutions/security/endpoint-response-actions/third-party-response-actions.md) to learn which response actions are supported for each system.

::::{admonition} Prerequisites
* This feature requires the appropriate [subscription](https://www.elastic.co/pricing) in {{stack}} or [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md) in {{serverless-short}}.
* [{{kib}} feature privilege](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md): Under **Actions and Connectors**, turn on **Customize sub-feature privileges** and enable **Endpoint Security**.
* [{{elastic-sec}} feature privileges](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md): **All** for the response action features, such as **Host Isolation**, that you want to perform.
* (In {{serverless-short}}) [User roles](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles): **SOC manager** or **Endpoint operations analyst**
* Endpoints must have actively running third-party agents installed.
::::


Expand a section below for your endpoint security system:

::::{dropdown} Set up CrowdStrike response actions
1. **Enable API access in CrowdStrike.** Create an API client in CrowdStrike to allow access to the system. Refer to CrowdStrike’s docs for instructions.

    * Give the API client the minimum privilege required to read CrowdStrike data and perform actions on enrolled hosts. Consider creating separate API clients for reading data and performing actions, to limit privileges allowed by each API client.

        * To isolate and release hosts: `Read` access for `Alerts`, and `Read` and `Write` access for `Hosts`.

        * To run a script on a host: `Read` and `Write` access for `Real time response`; for elevated access, `Write` access for `Real time response (admin)` is also required.

    * Take note of the client ID, client secret, and base URL; you’ll need them in later steps when you configure {{elastic-sec}} components to access CrowdStrike.
    * The base URL varies depending on your CrowdStrike account type:

        * US-1:  `https://api.crowdstrike.com`
        * US-2: `https://api.us-2.crowdstrike.com`
        * EU-1: `https://api.eu-1.crowdstrike.com`
        * US-GOV-1: `https://api.laggar.gcw.crowdstrike.com`

2. **Install the CrowdStrike integration and {{agent}}.** Elastic’s [CrowdStrike integration](https://docs.elastic.co/en/integrations/crowdstrike) collects and ingests logs into {{elastic-sec}}.

    1. Find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), search for and select **CrowdStrike**, then select **Add CrowdStrike**.
    2. Configure the integration with an **Integration name** and optional **Description**.
    3. Select **Collect CrowdStrike logs via API**, and enter the required **Settings**:

        * **Client ID**: Client ID for the API client used to read CrowdStrike data.
        * **Client Secret**: Client secret allowing you access to CrowdStrike.
        * **URL**: The base URL of the CrowdStrike API.

    4. Select the **Falcon Alerts** and **Hosts** sub-options under **Collect CrowdStrike logs via API**.
    5. Scroll down and enter a name for the agent policy in **New agent policy name**. If other agent policies already exist, you can click the **Existing hosts** tab and select an existing policy instead. For more details on {{agent}} configuration settings, refer to [{{agent}} policies](/reference/fleet/agent-policy.md).
    6. Click **Save and continue**.
    7. Select **Add {{agent}} to your hosts** and continue with the [{{agent}} installation steps](/solutions/security/configure-elastic-defend/install-elastic-defend.md#enroll-agent) to install {{agent}} on a resource in your network (such as a server or VM). {{agent}} will act as a bridge collecting data from CrowdStrike and sending it back to {{elastic-sec}}.

3. **Create a CrowdStrike connector.** Elastic’s [CrowdStrike connector](kibana://reference/connectors-kibana/crowdstrike-action-type.md) enables {{elastic-sec}} to perform actions on CrowdStrike-enrolled hosts.

    ::::{important}
    Do not create more than one CrowdStrike connector.
    ::::


    1. Find **Connectors** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select **Create connector**.
    2. Select the CrowdStrike connector.
    3. Enter the configuration information:

        * **Connector name**: A name to identify the connector.
        * **CrowdStrike API URL**: The base URL of the CrowdStrike API.
        * **CrowdStrike Client ID**: Client ID for the API client used to perform actions in CrowdStrike.
        * **Client Secret**: Client secret allowing you access to CrowdStrike.

    4. Click **Save**.

4. **Create and enable detection rules to generate {{elastic-sec}} alerts.** (Optional) Create [detection rules](/solutions/security/detect-and-alert/create-detection-rule.md) to generate {{elastic-sec}} alerts based on CrowdStrike events and data. The [CrowdStrike integration docs](https://docs.elastic.co/en/integrations/crowdstrike) list the available ingested logs and fields you can use to build a rule query.

    This gives you visibility into CrowdStrike without needing to leave {{elastic-sec}}. You can perform supported endpoint response actions directly from alerts that a rule creates, by using the **Take action** menu in the alert details flyout.
::::


::::{dropdown} Set up Microsoft Defender for Endpoint response actions
1. **Create API access information in Microsoft Azure.** Create new applications in your Azure domain and grant them the following minimum API permissions:

    * To isolate and release hosts:

        * Microsoft Defender for Endpoint Fleet integration policy: Permission to read alert data (`Windows Defender ATP: Alert.Read.All`).
        * Microsoft Defender for Endpoint connector: Permission to read machine information as well as isolate and release a machine (`Windows Defender ATP: Machine.Read.All` and `Machine.Isolate`).

    * {applies_to}`stack: ga 9.1+` {applies_to}`serverless: ga` To run a script on a host:
    
        * Microsoft Defender for Endpoint connector: Permission to  manage live response library files as well as run live response on a specific machine (`Windows Defender ATP: Library.Manage` and `Machine.LiveResponse`)

    * {applies_to}`stack: ga 9.2+` {applies_to}`serverless: ga` To cancel an ongoing action on a host, you need the same permissions that are required for the action you're canceling.

    Refer to the [Microsoft Defender for Endpoint integration documentation](https://docs.elastic.co/en/integrations/microsoft_defender_endpoint) or [Microsoft’s documentation](https://learn.microsoft.com/en-us/defender-endpoint/api/exposed-apis-create-app-webapp) for details on creating a new Azure application.

    After you create the applications, take note of the client ID, client secret, and tenant ID for each one; you’ll need them in later steps when you configure Elastic Security components to access Microsoft Defender for Endpoint.

2. **Install the Microsoft Defender for Endpoint integration and {{agent}}.** Elastic’s [Microsoft Defender for Endpoint integration](https://docs.elastic.co/en/integrations/microsoft_defender_endpoint) collects and ingests logs into {{elastic-sec}}.

    ::::{note}
    You can also set up the [Microsoft M365 Defender integration](https://docs.elastic.co/en/integrations/m365_defender) as an alternative or additional data source.
    ::::


    1. Find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), search for and select **Microsoft Defender for Endpoint**, then select **Add Microsoft Defender for Endpoint**.
    2. Enter an **Integration name**. Entering a **Description** is optional.
    3. Ensure that **Microsoft Defender for Endpoint logs** is selected, and enter the required values for **Client ID**, **Client Secret**, and **Tenant ID**.
    4. Scroll down and enter a name for the agent policy in **New agent policy name**. If other agent policies already exist, you can click the **Existing hosts** tab and select an existing policy instead. For more details on {{agent}} configuration settings, refer to [{{agent}} policies](/reference/fleet/agent-policy.md).
    5. Click **Save and continue**.
    6. Select **Add {{agent}} to your hosts** and continue with the [{{agent}} installation steps](/solutions/security/configure-elastic-defend/install-elastic-defend.md#enroll-agent) to install {{agent}} on a resource in your network (such as a server or VM). {{agent}} will act as a bridge, collecting data from Microsoft Defender for Endpoint and sending it back to {{elastic-sec}}.

3. **Create a Microsoft Defender for Endpoint connector.** Elastic’s Microsoft Defender for Endpoint connector enables {{elastic-sec}} to perform actions on Microsoft Defender–enrolled hosts.

    ::::{important}
    Do not create more than one Microsoft Defender for Endpoint connector.
    ::::


    1. Find **Connectors** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select **Create connector**.
    2. Select the Microsoft Defender for Endpoint connector.
    3. Enter the configuration information:

        * **Connector name**: A name to identify the connector.
        * **Application client ID**: The client ID created in step 1.
        * **Tenant ID**: The tenant ID created in step 1.
        * **Client secret value**: The client secret created in step 1.

    4. (Optional) If necessary, adjust the default values populated for the other configuration parameters.
    5. Click **Save**.

4. **Create and enable detection rules to generate {{elastic-sec}} alerts.** Create [detection rules](/solutions/security/detect-and-alert/create-detection-rule.md) to generate {{elastic-sec}} alerts based on Microsoft Defender for Endpoint events and data.

    This gives you visibility into Microsoft Defender hosts without needing to leave {{elastic-sec}}. You can perform supported endpoint response actions directly from alerts that a rule creates, by using the **Take action** menu in the alert details flyout.

    When creating a rule, you can target any event containing a Microsoft Defender machine ID field. Use one or more of these index patterns:

    * `logs-microsoft_defender_endpoint.log-*`
    * `logs-m365_defender.alert-*`
    * `logs-m365_defender.incident-*`
    * `logs-m365_defender.log-*`
    * `logs-m365_defender.event-*`
::::


::::{dropdown} Set up SentinelOne response actions
1. **Generate API access tokens in SentinelOne.** You’ll need these tokens in later steps, and they allow {{elastic-sec}} to collect data and perform actions in SentinelOne.

    Create two API tokens in SentinelOne, and give them the minimum privilege required by the Elastic components that will use them:

    * SentinelOne integration: Permission to read SentinelOne data.
    * SentinelOne connector: Permission to read SentinelOne data and perform actions on enrolled hosts (for example, isolating and releasing an endpoint).

    Refer to the [SentinelOne integration docs](https://docs.elastic.co/en/integrations/sentinel_one) or SentinelOne’s docs for details on generating API tokens.

2. **Install the SentinelOne integration and {{agent}}.** Elastic’s [SentinelOne integration](https://docs.elastic.co/en/integrations/sentinel_one) collects and ingests logs into {{elastic-sec}}.

    1. Find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), search for and select **SentinelOne**, then select **Add SentinelOne**.
    2. Configure the integration with an **Integration name** and optional **Description**.
    3. Ensure that **Collect SentinelOne logs via API** is selected, and enter the required **Settings**:

        * **URL**: The SentinelOne console URL.
        * **API Token**: The SentinelOne API access token you generated previously, with permission to read SentinelOne data.

    4. Scroll down and enter a name for the agent policy in **New agent policy name**. If other agent policies already exist, you can click the **Existing hosts** tab and select an existing policy instead. For more details on {{agent}} configuration settings, refer to [{{agent}} policies](/reference/fleet/agent-policy.md).
    5. Click **Save and continue**.
    6. Select **Add {{agent}} to your hosts** and continue with the [{{agent}} installation steps](/solutions/security/configure-elastic-defend/install-elastic-defend.md#enroll-agent) to install {{agent}} on a resource in your network (such as a server or VM). {{agent}} will act as a bridge collecting data from SentinelOne and sending it to {{elastic-sec}}.

3. **Create a SentinelOne connector.** Elastic’s [SentinelOne connector](kibana://reference/connectors-kibana/sentinelone-action-type.md) enables {{elastic-sec}} to perform actions on SentinelOne-enrolled hosts.

    ::::{important}
    Do not create more than one SentinelOne connector.
    ::::


    1. Find **Connectors** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select **Create connector**.
    2. Select the **SentinelOne** connector.
    3. Enter the configuration information:

        * **Connector name**: A name to identify the connector.
        * **SentinelOne tenant URL**: The SentinelOne tenant URL.
        * **API token**: The SentinelOne API access token you generated previously, with permission to read SentinelOne data and perform actions on enrolled hosts.

    4. Click **Save**.

4. **Create and enable detection rules to generate {{elastic-sec}} alerts.** Create [detection rules](/solutions/security/detect-and-alert/create-detection-rule.md#create-custom-rule) to generate {{elastic-sec}} alerts based on SentinelOne events and data.

    This gives you visibility into SentinelOne without needing to leave {{elastic-sec}}. You can perform supported endpoint response actions directly from alerts that a rule creates, by using the **Take action** menu in the alert details flyout.

    When creating a rule, you can target any event containing a SentinelOne agent ID field. Use one or more of these index patterns:

    | Index pattern | SentinelOne agent ID field |
    | --- | --- |
    | `logs-sentinel_one.alert*` | `sentinel_one.alert.agent.id` |
    | `logs-sentinel_one.threat*` | `sentinel_one.threat.agent.id` |
    | `logs-sentinel_one.activity*` | `sentinel_one.activity.agent.id` |
    | `logs-sentinel_one.agent*` | `sentinel_one.agent.agent.id` |

    ::::{note}
    Do not include any other index patterns.
    ::::
::::
