---
applies_to:
  deployment:
    self:
    ece:
    eck:
navigation_title: Connect your self-managed cluster
---

# Connect your self-managed cluster to AutoOps

To use AutoOps with your self-managed cluster, you first need to create an {{ecloud}} account or log in to your existing account. After you choose to connect AutoOps to your self-managed cluster, an installation wizard will guide you through the steps of installing {{agent}} to send metrics from your self-managed cluster to AutoOps in {{ecloud}}.  

Complete the steps in the following subsections to connect your cluster to AutoOps. The setup takes about 10 minutes.

## Prerequisites

Ensure your system meets the following requirements before proceeding:

* Your cluster is on a [supported {{es}} version](https://www.elastic.co/support/eol).
* You have an [Enterprise self-managed license](https://www.elastic.co/subscriptions) or an active self-managed [free trial](https://cloud.elastic.co/registration).
* The agent you install for the connection is allowed to send metrics outside your organization to {{ecloud}}.
* You have a dedicated user with the following permissions to set up {{agent}}:

    | Setting | Privileges |
    | --- | --- |
    | Cluster privileges | `monitor`, `read_ilm`, and `read_slm` |
    | Index privileges | `*` indices: `monitor`, `view_index_metadata`  |

<!-- Commenting out because I'm waiting for PM clarification
## Create a role for AutoOps

On your self-managed cluster, go to **Developer tools** from the navigation menu. In **Console**, run the following command:

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
-->
## Connect to AutoOps

:::{note}
:::{include} /deploy-manage/monitor/_snippets/single-cloud-org.md
:::
:::

1. Go to your {{ecloud}} home page.
    * If you already have an {{ecloud}} account, log in to [{{ecloud}}](https://cloud.elastic.co?page=docs&placement=docs-body). 
    * If you don’t have an {{ecloud}} account, [sign up](/deploy-manage/deploy/elastic-cloud/create-an-organization.md) and create an organization.
2. In the **Connected clusters** section, select **Connect self-managed cluster**. 
3. On the **Connected clusters** page, select **Accept and Continue**. This button only appears the first time you connect a cluster.
3. On the **Connect your self-managed cluster** page, in the **AutoOps** section, select **Connect**.

### Select installation method

Your cluster ships metrics to AutoOps with the help of {{agent}}. 

:::{important} 
Using AutoOps for your self-managed cluster requires a new, dedicated {{agent}}. You must install an agent even if you already have an existing one for other purposes.
:::

Select one of the following methods to install {{agent}}:

* Kubernetes
* Docker
* Linux
* Windows

### Configure agent

Depending on your selected installation method, you may have to provide the following information to create the installation command:

* **{{es}} endpoint URL**: The agent will use this URL to identify which cluster you want to connect to AutoOps.
* **Preferred authentication method**: Choose from the following:
    * **API key**: [Create an API key](/solutions/observability/apm/grant-access-using-api-keys.md) to grant access to the cluster.
    * **Basic**: Assign a username and password to a user with the required [permissions](#prerequisites).
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
If the machine where your self-managed cluster is running experiences technical issues, shipping metrics to AutoOps will be interrupted. We recommend installing the agent on a separate machine.
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

To connect more self-managed clusters, we recommend repeating the steps to [connect your self-managed cluster to AutoOps](#connect-your-self-managed-cluster-to-autoops).

You can use the same installation command to connect multiple clusters, but each cluster needs a separate, dedicated {{agent}}.

## Disconnect a cluster

Complete the following steps to disconnect your self-managed cluster from your Cloud organization. You need the **Organization owner** [role](/deploy-manage/monitor/autoops/cc-manage-users.md#assign-roles) to perform this action.

1. Log in to [{{ecloud}}](https://cloud.elastic.co/home).
2. In the **Connected clusters** section, locate the cluster you want to disconnect.
3. From that cluster’s actions menu, select **Disconnect cluster**.
4. Enter the cluster’s name in the field that appears and then select **Disconnect cluster**.

:::{include} /deploy-manage/monitor/_snippets/disconnect-cluster.md
:::