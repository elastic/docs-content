---
applies_to:
  deployment:
    self:
    ece:
    eck:
navigation_title: Connect your cluster
products:
  - id: cloud-kubernetes
  - id: cloud-enterprise
---

# Connect your ECE, ECK, or self-managed cluster to AutoOps

To use AutoOps with your ECE, ECK, or self-managed {{es}} cluster, you first need to create an {{ecloud}} account or log in to your existing account. An installation wizard then guides you through the steps of installing {{agent}} to send metrics from your cluster to AutoOps in {{ecloud}}.  

The connection process takes about 10 minutes.

:::{note}
If you have an {{es}} cluster set up for local development or testing, you can connect it to AutoOps using Docker. Refer to [](/deploy-manage/monitor/autoops/cc-connect-local-dev-to-autoops.md).
:::

## Prerequisites

Ensure your system meets the following requirements before proceeding:

* Your cluster is on a [supported {{es}} version](https://www.elastic.co/support/eol) (7.17.x and above).
* Your cluster is on an [Enterprise self-managed license](https://www.elastic.co/subscriptions) or an [active self-managed trial](https://cloud.elastic.co/registration).
* The agent you install for the connection is allowed to send metrics to {{ecloud}}.
* {applies_to}`eck: ga 3.3` To install {{agent}} using ECK, your ECK operator is on version 3.3.0 and above.

## Connect to AutoOps [connect-to-autoops]

:::{note}
:::{include} /deploy-manage/monitor/_snippets/single-cloud-org.md
:::
:::

The following steps describe how to connect your cluster to AutoOps. 

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

:::{tip}
If you don't want {{agent}} to gather certain types of data from your cluster, you can disable the collection of related metrics before installing the agent. Learn more in [](../autoops/autoops-disable-metrics-collection.md).
:::

This is the first step of the installation wizard. Your cluster ships metrics to AutoOps with the help of {{agent}}. 

Select one of the following methods to install {{agent}}:

* **{{k8s}}**
* **Docker**
* **Linux**
* {applies_to}`eck: ga 3.3`  **{{eck}} (ECK)**

:::{note}
:applies_to: { eck: }
You can choose any installation method when connecting your ECK-managed cluster to AutoOps. However, for ECK version 3.3.0+, we recommend choosing **ECK** as your installation method for a more integrated experience.   
:::

:::{important} 
Each cluster that you want to connect requires a new, dedicated {{agent}}. You must install the agent even if you already have an existing one for other purposes.

You only need to install the agent once per cluster. 
:::

To learn more about how AutoOps securely gathers data from your cluster, refer to our [FAQ](/deploy-manage/monitor/autoops/ec-autoops-faq.md#data-gathering).

### Configure agent

Depending on your selected installation method, you might have to provide some or all of the following information to create the installation command:

* **{{es}} endpoint URL**: Enter the URL for the {{es}} cluster you want to monitor by connecting to AutoOps.
* **Preferred authentication method**: Choose one of the following:
  
  :::::{tab-set}
  :group: api-key-or-basic

  ::::{tab-item} API key
  :sync: api-key

  With this authentication method, you need to create an API key to grant access to your cluster. Complete the following steps:

  1. Go to {{kib}} in your {{es}} cluster.
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
  6. Select **Create API key**.
  7. Copy the key and save it for later. You will need it when you [install the agent](#install-agent).

  ::::

  ::::{tab-item} Basic
  :sync: basic

  With this authentication method, you need the username and password of a user with the necessary privileges to grant access to your cluster. There are two ways to set up a user with these privileges:

  * (Recommended) Go to {{kib}} in your cluster and then go to **Developer tools**. In **Console**, run the following command:
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

  :::{note}
  If you manually assign privileges, you won't be able to allow {{agent}} to access restricted indices.
  :::
  ::::

  :::::
* **System architecture**: Select the system architecture of the machine running the agent.
* $$$storage-location$$$**Storage location**: Select where to store your metrics data.\
In the **Cloud provider** field, select **Amazon Web Services**. In the **Region** field, select from the list of available AWS regions:
  
  :::{include} ../_snippets/autoops-cc-regions.md
  :::

$$$firewall-allowlist$$$
::::{note}
:::{include} ../_snippets/autoops-allowlist-port-and-urls.md
:::
::::

### Install agent

The wizard generates an installation command or a YAML manifest based on your configuration. Depending on your installation method, complete the following steps to install the agent:

:::::{tab-set}
:group: installation-eck-or-other

::::{tab-item} {{k8s}}, Docker, or Linux
:sync: installation-other
:::{tip}
For Docker or Linux-based installation, we recommend installing the agent on a different machine from the one where your cluster is running. This ensures optimum resource usage.
:::
1. Copy the command. 
2. Paste it into a text editor and update the placeholder values for the following environment variables:

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
::::

::::{tab-item} ECK
:sync: installation-ECK
```{applies_to}
eck: ga 3.3
```
1. Copy the YAML manifest. 
2. (Optional) Paste it into a text editor and change the values of the following variables:
    * Secret name
    * Policy name
    * `resourceSelector` label
3. Apply the manifest to your ECK environment.
4. Return to the wizard and select **Next**.

When you apply this manifest, the following things happen:
* An `AutoOpsAgentPolicy` resource is created.
* The ECK operator is configured to create an API key in each {{es}} cluster that matches your `resourceSelector` label.
* {{agent}} is deployed so that it's ready to send data from these clusters to AutoOps.

:::{tip}
After the `AutoOpsAgentPolicy` resource is created, you can check its status by running the following command:
```sh
kubectl describe autoopsagentpolicy <policy_name>
```
The status shows:
* Number of errors encountered when configuring {{agent}}.
* Number of clusters matched by the `resourceSelector`.
* Number of clusters that are connected and shipping data to AutoOps.
:::

::::

:::::

If the connection is unsuccessful, an error message is displayed with a possible reason for the failure and recommended next steps. For a list of these errors, refer to [Potential errors](/deploy-manage/monitor/autoops/cc-cloud-connect-autoops-troubleshooting.md#potential-errors). Sometimes, an exact reason for the failure cannot be determined. In this case, explore [additional resources](/troubleshoot/index.md#troubleshoot-additional-resources) or [contact us](/troubleshoot/index.md#contact-us).

To uninstall the agent, refer to [](/solutions/security/configure-elastic-defend/uninstall-elastic-agent.md).

### Launch AutoOps

If the connection is successful, AutoOps starts analyzing your metrics and reporting on any issues found. Depending on the size of your cluster, this process can take up to 30 minutes. 

:::::{tab-set}
:group: launch-eck-or-other

::::{tab-item} {{k8s}}, Docker, or Linux
:sync: launch-other
After your setup is complete, the **Open AutoOps** button is displayed in the wizard. Select it to launch [AutoOps](/deploy-manage/monitor/autoops.md). 
::::

::::{tab-item} ECK
:sync: launch-eck
```{applies_to}
eck: ga 3.3
```
The agent detects which {{es}} clusters to monitor based on the correct `resourceSelector` label. The `resourceSelector` uses standard {{k8s}} [label selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors) to match the clusters. 

Use the following command to apply the `resourceSelector` label to every cluster you want to connect. This code assumes your label is `autoops=enabled`.

```js
  kubectl -n {{namespace}} label elasticsearch <elasticsearch_cluster_name> autoops=enabled
```
:::{note}
The agent runs in the namespace chosen for the policy. However, the agent can detect {{es}} clusters throughout the {{k8s}} environment regardless of where they are installed. 
:::

After your setup is complete, the **View connected clusters** button is displayed in the wizard. Select it to view the clusters you have connected to [AutoOps](/deploy-manage/monitor/autoops.md).
::::
:::::

## Access AutoOps

After completing the setup, you can access AutoOps for your cluster at any time.

1. Log in to [{{ecloud}}](https://cloud.elastic.co/home).
2. In the **Connected clusters** section, locate the cluster you want to work on.
3. In the **Services** column, select **AutoOps**.

## Manage connected clusters

Perform the actions described in the following sections to manage your connected cluster(s). 

### Add an alias to a cluster

By default, each cluster has a name made up of a string of characters, but you can add a human-readable alias by completing the following steps. You need admin privileges to perform this action.

1. From the [{{ecloud}} home page](https://cloud.elastic.co/home), go to the **Connected clusters** section and select the cluster you want to work on.
2. On the cluster details page, select **Edit** in the **Cluster display name** field.
3. Enter the alias in the field that is displayed and then select the checkmark icon.

### Connect additional clusters

To connect more clusters, repeat the steps to [connect to AutoOps](#connect-to-autoops).

If you don't need to change any of your [configuration settings](#configure-agent) for the additional clusters, you can skip ahead and reuse the same installation command if you used the {{k8s}}, Docker, or Linux methods, or apply the same `resourceSelector` label if you used the ECK method.

Remember that you must install a separate, dedicated {{agent}} for each cluster. You only need to install the agent once per cluster. 

### Disconnect a cluster

Complete the following steps to disconnect your cluster from your Cloud organization. You need the **Organization owner** [role](/deploy-manage/monitor/autoops/cc-manage-users.md#assign-roles) to perform this action.

1. Based on your [installation method](#select-installation-method), complete the steps to stop {{agent}} from shipping metrics to {{ecloud}}.
2. Log in to [{{ecloud}}](https://cloud.elastic.co/home).
3. On the **Connected clusters** page or the **Connected clusters** section of the home page, locate the cluster you want to disconnect.
4. From that cluster’s actions menu, select **Disconnect cluster**.
5. Enter the cluster’s name in the field that is displayed and then select **Disconnect cluster**.

:::{tip}
:applies_to: { eck: ga 3.3 }
If your chosen installation method is ECK, you can also disconnect a cluster by removing your `resourceSelector` label from it. Run the following command:
```js
  kubectl -n {{namespace}} label elasticsearch <elasticsearch_cluster_name> autoops-
```
:::

:::{include} /deploy-manage/monitor/_snippets/disconnect-cluster.md
:::