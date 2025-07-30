---
applies_to:
  deployment:
    self:
    ece:
    eck:
navigation_title: Connect your self-managed cluster
---

# Connect your self-managed cluster to AutoOps

To use AutoOps with your self-managed cluster, you first need to create an {{ecloud}} account or log in to your existing account. An installation wizard will then guide you through the steps of installing {{agent}} to send metrics from your self-managed cluster to AutoOps in {{ecloud}}.  

Complete the steps in the following subsections to connect your cluster to AutoOps. The connection process takes about 10 minutes.

## Prerequisites

Ensure your system meets the following requirements before proceeding:

* Your cluster is on a [supported {{es}} version](https://www.elastic.co/support/eol).
* You have an [Enterprise self-managed license](https://www.elastic.co/subscriptions) or an active self-managed [free trial](https://cloud.elastic.co/registration).
* The agent you install for the connection is allowed to send metrics outside your organization to {{ecloud}}.

## Connect to AutoOps

:::{note}
:::{include} /deploy-manage/monitor/_snippets/single-cloud-org.md
:::
:::

:::::{tab-set}
:group: existing-or-new-cloud-account

::::{tab-item} Existing account
:sync: existing

If you already have an {{ecloud}} account:
1. Log in to [{{ecloud}}](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On your home page, in the **Connected clusters** section, select **Connect self-managed cluster**. 
3. On the **Connected clusters** page, select **Accept and continue**. This button only appears the first time you connect a cluster.
4. On the **Connect your self-managed cluster** page, in the **AutoOps** section, select **Connect**.
::::

::::{tab-item} New account
:sync: new

If you don’t have an existing {{ecloud}} account: 
1. Sign up for an account. 
<!-- 
Add cloud-connected marketing link to sign up when available
 -->
2. Follow the prompts on your screen to create an organization.
3. Go through the installation wizard as detailed in the following sections.
::::

:::::

### Select installation method

This is the first step of the installation wizard. Your cluster ships metrics to AutoOps with the help of {{agent}}. 

Select one of the following methods to install {{agent}}:

* Kubernetes
* Docker
* Linux
* Windows

:::{important} 
Using AutoOps for your self-managed cluster requires a new, dedicated {{agent}}. You must install an agent even if you already have an existing one for other purposes.
:::

### Configure agent

Depending on your selected installation method, you may have to provide the following information to create the installation command:

* **{{es}} endpoint URL**: The agent will use this URL to identify which cluster you want to connect to AutoOps.
* **Preferred authentication method**: Choose one of the following:
:::::{tab-set}
:group: api-key-or-basic

::::{tab-item} API key
:sync: api-key

With this authentication method, you need to [create an API key](/solutions/observability/apm/grant-access-using-api-keys.md) with the following privileges to grant access to your cluster:

| Setting | Privileges |
    | --- | --- |
    | Cluster privileges | `monitor`, `read_ilm`, and `read_slm` |
    | Index privileges | Indices: `*` <br> `monitor`, `view_index_metadata`, `allow_restricted_indices: true`  |

::::

::::{tab-item} Basic
:sync: basic

With this authentication method, you need the username and password of a user with the necessary privileges to grant access to your cluster. There are two ways to set up a user with the these privileges:

* (Recommended) On your self-managed cluster, go to **Developer tools** from the navigation menu. In **Console**, run the following command:
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
* **Metrics storage location**: Select where to store your metrics data from the list of available cloud service providers and regions.

### Install agent

The wizard will generate an installation command based on your configuration. Depending on your installation method, the following command formats are available:

* Kubernetes
    * YAML
    * Helm Chart
* Docker
    * Docker
    * Docker compose
* Linux
* Windows

:::{tip}
We recommend installing the agent on a separate machine from the one where your self-managed cluster is running.
:::

Complete the following steps to run the command:

1. Copy the command. 
2. Paste it into a text editor and update the placeholder values in the following environment variables:

| Environment variable | Description |
| --- | --- |
| `AUTOOPS_OTEL_URL` | The {{ecloud}} URL to which {{agent}} ships data. The URL is generated based on the CSP and region you pick. <br> This URL shouldn't be edited. |
| `AUTOOPS_ES_URL` | The URL {{agent}} uses to communicate with {{es}}. |
| `ELASTICSEARCH_READ_API_KEY` | The API key for API key authentication to access the cluster. It combines the `${id}:${api_key}` values. <br> This variable shouldn't be used with `ELASTICSEARCH_READ_USERNAME` and `ELASTICSEARCH_READ_PASSWORD`. |
| `ELASTICSEARCH_READ_USERNAME` | The username for basic authentication to access the cluster. <br> This variable should be used with `ELASTICSEARCH_READ_PASSWORD`. |
| `ELASTICSEARCH_READ_PASSWORD` | The password for basic authentication to access the cluster. <br> This variable should be used with `ELASTICSEARCH_READ_USERNAME`. |
| `ELASTIC_CLOUD_CONNECTED_MODE_API_KEY` | The {{ecloud}} API Key used to register the cluster. <br> This key shouldn't be edited. |
| `AUTOOPS_TEMP_RESOURCE_ID` | The temporary ID for the current installation wizard. |

4. Run the command from the machine where you want to install the agent. 
5. Return to the wizard and select **I have run the command**.

It might take a few minutes for your cluster details to be validated and the first metrics to be shipped to AutoOps.

If the connection is unsuccessful, an error message will appear with a possible reason for the failure and recommended next steps. For a list of these errors, refer to [Potential errors](/deploy-manage/monitor/autoops/cc-cloud-connect-autoops-troubleshooting.md#potential-errors).

Sometimes, an exact reason for the failure cannot be determined. In this case, explore [additional resources](/troubleshoot/index.md#troubleshoot-additional-resources) or [contact us](/troubleshoot/index.md#contact-us).

### Launch AutoOps

If the connection is successful, AutoOps will start analyzing your metrics and reporting on any issues found. Depending on the size of your cluster, this process can take up to 30 minutes. 

After the account is ready, the **Open AutoOps** button will appear in the wizard. Select it to launch AutoOps. 

Learn more about [AutoOps](/deploy-manage/monitor/autoops.md).

## Access AutoOps

After you've completed the setup, you can access AutoOps for your self-managed cluster at any time.

1. Log in to [{{ecloud}}](https://cloud.elastic.co/home).
2. In the **Connected clusters** section, locate the cluster you want to work on.
3. In the **Services** column, select **AutoOps**.

## Connect additional clusters

To connect more self-managed clusters, we recommend repeating the steps to [connect to AutoOps](#connect-to-autoops).

You can use the same installation command to connect multiple clusters, but each cluster needs a separate, dedicated {{agent}}.

## Disconnect a cluster

Complete the following steps to disconnect your self-managed cluster from your Cloud organization. You need the **Organization owner** [role](/deploy-manage/monitor/autoops/cc-manage-users.md#assign-roles) to perform this action.

1. Log in to [{{ecloud}}](https://cloud.elastic.co/home).
2. In the **Connected clusters** section, locate the cluster you want to disconnect.
3. From that cluster’s actions menu, select **Disconnect cluster**.
4. Enter the cluster’s name in the field that appears and then select **Disconnect cluster**.

:::{include} /deploy-manage/monitor/_snippets/disconnect-cluster.md
:::