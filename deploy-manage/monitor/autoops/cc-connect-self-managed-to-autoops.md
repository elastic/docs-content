---
applies_to:
  deployment:
    self:
    ece:
    eck:
navigation_title: Connect your self-managed cluster
products:
  - id: cloud-kubernetes
  - id: cloud-enterprise
---

# Connect your self-managed cluster to AutoOps

To use AutoOps with your ECE, ECK, or self-managed cluster, you first need to create an {{ecloud}} account or log in to your existing account. An installation wizard will then guide you through the steps of installing {{agent}} to send metrics from your cluster to AutoOps in {{ecloud}}.  

Complete the steps in the following subsections to connect your cluster to AutoOps. The connection process takes about 10 minutes.

:::{note}
If you have an {{es}} cluster set up for local development or testing, you can connect it to AutoOps using Docker. Refer to [](/deploy-manage/monitor/autoops/cc-connect-local-dev-to-autoops.md).
:::

## Prerequisites

Ensure your system meets the following requirements before proceeding:

* Your cluster is on a [supported {{es}} version](https://www.elastic.co/support/eol) (7.17.x and above).
* Your cluster is on an [Enterprise self-managed license](https://www.elastic.co/subscriptions) or an active self-managed [trial](https://cloud.elastic.co/registration).
* The agent you install for the connection is allowed to send metrics to {{ecloud}}.

## Connect to AutoOps [connect-to-autoops]

:::{note}
:::{include} /deploy-manage/monitor/_snippets/single-cloud-org.md
:::
:::

The following steps describe how to connect your ECE, ECK, or self-managed cluster to AutoOps. 

<!-- Private preview instructions:
:::::{tab-set}
:group: existing-or-new-cloud-account

::::{tab-item} Existing account
:sync: existing

If you already have an {{ecloud}} account:
1. Go to the [Cloud Connected Services](https://cloud.elastic.co/connect-cluster-services) page for private preview.
2. Log in to your account.
3. On the **Cloud Connected Services** page, in the **AutoOps** section, select **Connect**.
4. Go through the installation wizard as detailed in the following sections.
::::

::::{tab-item} New account
:sync: new

If you don’t have an existing {{ecloud}} account: 
1. Go to the [Cloud Connected Services sign up](https://cloud.elastic.co/registration?onboarding_service_type=ccm) page for private preview. 
2. Follow the prompts on your screen to sign up for an account and create an organization.
3. Go through the installation wizard as detailed in the following sections.
::::

:::::
-->

:::::{tab-set}
:group: existing-or-new-cloud-account

::::{tab-item} Existing account
:sync: existing

If you already have an {{ecloud}} account:
1. Log in to [{{ecloud}}](https://cloud.elastic.co/login?redirectTo=%2Fconnect-cluster-services).
    - The link provided should take you directly to the **Connect your self-managed cluster** page
2. On your home page, in the **Connected clusters** section, select **Connect self-managed cluster**. 
3. On the **Connect your self-managed cluster** page, in the **AutoOps** section, select **Connect**.
4. Go through the installation wizard as detailed in the following sections.
::::

::::{tab-item} New account
:sync: new

If you don’t have an existing {{ecloud}} account: 
1. Go to the [Cloud Connected Services sign up](https://cloud.elastic.co/registration?onboarding_service_type=ccm) page. 
2. Follow the prompts on your screen to sign up for {{ecloud}} and create an organization.
3. Go through the installation wizard as detailed in the following sections.
::::

:::::


### Select installation method

This is the first step of the installation wizard. Your cluster ships metrics to AutoOps with the help of {{agent}}. 

Select one of the following methods to install {{agent}}:

* **Kubernetes**
* **Docker**
* **Linux**
<!-- Not applicable for private preview
* **Windows**
-->

:::{important} 
Using AutoOps for your ECE, ECK, and self-managed clusters requires a new, dedicated {{agent}}. You must install an agent even if you already have an existing one for other purposes.
:::

To learn more about how AutoOps securely gathers data from your cluster, refer to our [FAQ](/deploy-manage/monitor/autoops/ec-autoops-faq.md#data-gathering).

### Configure agent

Depending on your selected installation method, you may have to provide the following information to create the installation command:

* **{{es}} endpoint URL**: Enter the URL for the {{es}} cluster you want to monitor by connecting to AutoOps.
* **Preferred authentication method**: Choose one of the following:
:::::{tab-set}
:group: api-key-or-basic

::::{tab-item} API key
:sync: api-key

With this authentication method, you need to create an API key to grant access to your cluster. Complete the following steps:

1. Go to {{kib}} in your self-managed cluster.
2. Go to the **API keys** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
3. Select **Create API key**.
4. In the flyout, enter a name for your key and select **User API key**.
5. Enable **Control security privileges** and enter the following script:
```json
{
 "autoops": {
   "cluster": [
     "monitor",
     "read_ilm",
     "read_slm"
   ],
   "indices": [
     {
       "names": [
         "*"
       ],
       "privileges": [
         "monitor",
         "view_index_metadata"
       ],
       "allow_restricted_indices": true
     }
   ],
   "applications": [],
   "run_as": [],
   "metadata": {},
   "transient_metadata": {
     "enabled": true
   }
 }
}

```
5. Select **Create API key**.
6. Copy the key and save it for later. You will need it when you [install the agent](#install-agent).

::::

::::{tab-item} Basic
:sync: basic

With this authentication method, you need the username and password of a user with the necessary privileges to grant access to your cluster. There are two ways to set up a user with the these privileges:

* (Recommended) Go to {{kib}} in your self-managed cluster and then go to **Developer tools**. In **Console**, run the following command:
```js
POST /_security/role/autoops
{
  "cluster": [
    "monitor",
    "read_ilm",
    "read_slm"
  ],
  "indices": [
    {
      "names": [
        "*"
      ],
      "privileges": [
        "monitor",
        "view_index_metadata"
      ],
      "allow_restricted_indices": true
    }
  ],
  "applications": [],
  "run_as": [],
  "metadata": {
    "description": "Allows Elastic agent to pull cluster metrics for AutoOps."
  },
  "transient_metadata": {
    "enabled": true
  }
}
```
* Alternatively, manually assign the following privileges in your account:

    | Setting | Privileges |
    | --- | --- |
    | Cluster privileges | `monitor`, `read_ilm`, and `read_slm` |
    | Index privileges | Indices: `*` <br> `monitor`, `view_index_metadata`  |
:::{{note}}
If you manually assign privileges, you won't be able to allow {{agent}} to access restricted indices.
:::
::::

:::::
* **System architecture**: Select the system architecture of the machine running the agent.
* **Metrics storage location**: Select where to store your metrics data from the list of available AWS regions:
  
  :::{include} ../_snippets/autoops-cc-regions.md
  :::

### Install agent

The wizard will generate an installation command based on your configuration. Depending on your installation method, the following command formats are available:

* Kubernetes
    * YAML
    <!-- Not applicable for private preview 
    * Helm Chart -->
* Docker
    * Docker
    * Docker compose
* Linux
<!-- Not applicable for private preview
* Windows
-->

:::{tip}
To ensure optimum resource usage, we recommend installing the agent on a different machine from the one where your cluster is running.
:::

Complete the following steps to run the command:

1. Copy the command. 
2. Paste it into a text editor and update the placeholder values in the following environment variables:

    | Environment variable | Description |
    | --- | --- |
    | `AUTOOPS_OTEL_URL` | The {{ecloud}} URL to which {{agent}} ships data. The URL is generated based on the CSP and region you pick. <br> This URL shouldn't be edited. |
    | `AUTOOPS_ES_URL` | The URL {{agent}} uses to communicate with {{es}}. |
    | `AUTOOPS_ES_API_KEY` | The API key for API key authentication to access the cluster. It combines the `${id}:${api_key}` values. <br> This variable shouldn't be used with `AUTOOPS_ES_USERNAME` and `AUTOOPS_ES_PASSWORD`. |
    | `AUTOOPS_ES_USERNAME` | The username for basic authentication to access the cluster. <br> This variable should be used with `AUTOOPS_ES_PASSWORD`. |
    | `AUTOOPS_ES_PASSWORD` | The password for basic authentication to access the cluster. <br> This variable should be used with `AUTOOPS_ES_USERNAME`. |
    | `ELASTIC_CLOUD_CONNECTED_MODE_API_KEY` | The {{ecloud}} API Key used to register the cluster. <br> This key shouldn't be edited. |
    | `AUTOOPS_TEMP_RESOURCE_ID` | The temporary ID for the current installation wizard. |

3. Run the command from the machine where you want to install the agent. 
4. Return to the wizard and select **I have run the command**.

It might take a few minutes for your cluster details to be validated and the first metrics to be shipped to AutoOps.

If the connection is unsuccessful, an error message will appear with a possible reason for the failure and recommended next steps. For a list of these errors, refer to [Potential errors](/deploy-manage/monitor/autoops/cc-cloud-connect-autoops-troubleshooting.md#potential-errors).

Sometimes, an exact reason for the failure cannot be determined. In this case, explore [additional resources](/troubleshoot/index.md#troubleshoot-additional-resources) or [contact us](/troubleshoot/index.md#contact-us).

To uninstall the agent, refer to [](/solutions/security/configure-elastic-defend/uninstall-elastic-agent.md).

### Launch AutoOps

If the connection is successful, AutoOps will start analyzing your metrics and reporting on any issues found. Depending on the size of your cluster, this process can take up to 30 minutes. 

After the account is ready, the **Open AutoOps** button will appear in the wizard. Select it to launch AutoOps. 

Learn more about [AutoOps](/deploy-manage/monitor/autoops.md).

## Access AutoOps

After you've completed the setup, you can access AutoOps for your cluster at any time.

1. Log in to [{{ecloud}}](https://cloud.elastic.co/home).
2. In the **Connected clusters** section, locate the cluster you want to work on.
3. In the **Services** column, select **AutoOps**.

Learn more about [what you can do with AutoOps in your cluster](/deploy-manage/monitor/autoops/use-autoops-in-sm-cluster.md).

## Connect additional clusters

To connect more clusters, we recommend repeating the steps to [connect to AutoOps](#connect-to-autoops).

You can use the same installation command to connect multiple clusters, but each cluster needs a separate, dedicated {{agent}}.

## Disconnect a cluster

Complete the following steps to disconnect your cluster from your Cloud organization. You need the **Organization owner** [role](/deploy-manage/monitor/autoops/cc-manage-users.md#assign-roles) to perform this action.

1. Based on your [installation method](#select-installation-method), complete the steps to stop {{agent}} from shipping metrics to {{ecloud}}.
2. Log in to [{{ecloud}}](https://cloud.elastic.co/home).
3. On the **Connected clusters** page or the **Connected clusters** section of the home page, locate the cluster you want to disconnect.
4. From that cluster’s actions menu, select **Disconnect cluster**.
5. Enter the cluster’s name in the field that appears and then select **Disconnect cluster**.

:::{include} /deploy-manage/monitor/_snippets/disconnect-cluster.md
:::
