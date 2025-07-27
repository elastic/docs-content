---
applies_to:
  deployment:
    self:
navigation_title: Connect your self-managed cluster
---

# Connect your self-managed cluster to AutoOps

To use AutoOps with Cloud Connect, you first need to create an {{ecloud}} account or log in to your existing account. Once you choose to connect AutoOps to your self-managed cluster, an installation wizard will guide you through the steps of installing Elastic Agent to send metrics from your self-managed cluster to AutoOps in {{ecloud}}.  

Complete the steps in the following subsections to connect your cluster to AutoOps. The setup only takes about 10 minutes.

## Prerequisites

Ensure you meet the following requirements before proceeding:

* You have an [Enterprise self-managed license](https://www.elastic.co/subscriptions) or an active self-managed [free trial](https://cloud.elastic.co/registration).
* Your cluster is on a [supported {{es}} version](https://www.elastic.co/support/eol).
* The agent you install for the connection is allowed to send metrics outside your organization to {{ecloud}}.
* You have a dedicated user with following permissions to set up the Elastic Agent:

    | Type | Privilege |
    | --- | --- |
    | Cluster | `monitor`, `read_ilm`, and `read_slm` |
    | Index | `monitor`, `view_index_metadata`, and `*` indices <br> `allow_restricted_indices`: `true` |
    | Index | `read` and `.kibana*` indices <br> `allow_restricted_indices`: `true` |

## Connect to AutoOps

:::{note}
:::{include} /deploy-manage/monitor/_snippets/single-cloud-org.md
:::
:::

1. Go to your {{ecloud}} home page.
    * If you already have an {{ecloud}} account, log in to [{{ecloud}}](https://cloud.elastic.co?page=docs&placement=docs-body). 
    * If you don’t have an {{ecloud}} account, [sign up](/deploy-manage/deploy/elastic-cloud/create-an-organization) and create an organization.
2. In the **Connected clusters** section, select **Connect self-managed cluster**. 
3. On the **Cloud Connected Services** page, under **AutoOps**, select **Connect**.

### Select installation method

Your cluster ships metrics to AutoOps with the help of the Elastic Agent. 

:::{important} 
Using AutoOps for your self-managed cluster requires a new, dedicated Elastic Agent. You must install an agent even if you already have an existing one for other purposes.
:::

Select one of the following methods to install the Elastic Agent:

* Kubernetes
* Docker
* Linux
* Windows

### Configure agent

Depending on your selected installation method, you may have to provide the following information to create the installation command:

* **{{es}} endpoint URL**: The agent will use this URL to identify which cluster you want to connect to AutoOps.
* **Preferred authentication method**: Choose from the following:
    * **API key**: [Create an API key](/solutions/observability/apm/grant-access-using-api-keys) to grant access to the cluster.
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

Complete the following steps to run the command:

1. Copy the command. 
2. Paste it into a text editor and update the placeholder values in the following environment variables:

| Environment variable | Description |
| --- | --- |
| `AUTOOPS_OTEL_URL` | The {{ecloud}} URL to which the Elastic Agent ships data. The URL is generated based on the CSP and region you pick. <br> This URL shouldn't be edited. |
| `AUTOOPS_ES_URL` | The URL where the Elastic Agent communicates with {{es}}. |
| `ELASTICSEARCH_READ_API_KEY` | The API key for API key authentication to access the cluster. It combines the `${id}:${api_key}` values. <br> This variable shouldn't be used with `ELASTICSEARCH_READ_USERNAME` and `ELASTICSEARCH_READ_PASSWORD`. |
| `ELASTICSEARCH_READ_USERNAME` | The username for basic authentication to access the cluster. <br> This variable should be used with `ELASTICSEARCH_READ_PASSWORD`. |
| `ELASTICSEARCH_READ_PASSWORD` | The password for basic authentication to access the cluster. <br> This variable should be used with `ELASTICSEARCH_READ_USERNAME`. |
| `ELASTIC_CLOUD_CONNECTED_MODE_API_KEY` | The {{ecloud}} API Key used to register the cluster. <br> This key shouldn't be edited. |
| `AUTOOPS_TEMP_RESOURCE_ID` | The temporary ID for the current installation wizard. |

3. Ensure you meet the prerequisite for [permissions](#prerequisites) to run the command.
4. Run the command from the machine on which you want to install the agent. 

    :::{tip}
    For this step, we recommend using a machine different from the one on which your self-managed cluster is running.
    :::

5. Return to the wizard and select **I have run the command**.

It may take a few minutes for your cluster details to be validated and the first metrics to be shipped to AutoOps. For details on which metrics are collected by the agent, refer to [](/deploy-manage/monitor/autoops/cc-collected-metrics.md).

If the connection is unsuccessful, an error message will appear with a possible reason for the failure and recommended next steps. For a list of these errors, refer to [Potential errors](/deploy-manage/monitor/autoops/cc-cloud-connect-autoops-troubleshooting.md#potential-errors).

### Launch AutoOps

If the connection is successful, AutoOps will start analyzing your metrics and reporting on any issues found. Depending on the size of your cluster, this process can take up to 30 minutes. 

Once the account is ready, the **Open AutoOps** button will appear. Select it to launch AutoOps. 

Learn more about [AutoOps](/deploy-manage/monitor/autoops).

## Access AutoOps

Once you've completed the setup, you can access AutoOps for your self-managed cluster at any time.

1. Log in to [{{ecloud}}](https://cloud.elastic.co/home).
2. In the **Connected clusters** section, locate the cluster you want to work on.
3. In the **Services** column, select **AutoOps**.