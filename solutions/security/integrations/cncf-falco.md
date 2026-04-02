---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/ingest-falco.html
  - https://www.elastic.co/guide/en/serverless/current/ingest-falco.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# CNCF Falco

CNCF Falco is an open-source runtime security tool that detects anomalous activity in Linux hosts, containers, Kubernetes, and cloud environments. You can ingest Falco alerts into {{es}} to view them on {{elastic-sec}}'s Alerts page and incorporate them into your security workflows by using Falcosidekick, a proxy forwarder which can send alerts from your Falco deployments to {{es}}.

First, you’ll need to configure {{elastic-sec}} to receive data from Falco, then you’ll need to configure Falco and Falcosidekick to send data to {{es}}.


## Configure {{elastic-sec}} to receive Falco data [ingest-falco-setup-kibana]

In {{elastic-sec}}:

1. Click **Add integrations**.
2. Search the Integrations page for `Falco`, then select it.
3. Go to the Falco integration’s **Settings** tab.
4. Click **Install Falco**, then confirm by clicking **Install Falco** again. Installation should take less than a minute.

{{elastic-sec}} is now ready to receive data from Falco. The Falco integration page now has an **Assets** tab where you can inspect the newly installed assets that help to ingest Falco data.

Next, to make alerts from Falco appear on {{elastic-sec}}'s Alerts page:

1. Find the **Rules** page in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Detection rules (SIEM)**.
3. Search for a rule called `External Alerts`. Install it if necessary, and enable it.


## Configure Falco and Falcosidekick [ingest-falco-setup-falco]

You can either:

* [Send Falco data to {{es}} from virtual machines (VMs)](#ingest-falco-setup-falco-vm); or,
* [Send Falco data to {{es}} from Kubernetes](#ingest-falco-setup-falco-kubernetes).


### Configure Falco and Falcosidekick for VMs [ingest-falco-setup-falco-vm]

Multiple methods for configuring Falco to send data from VMs to {{es}} are available. This guide uses the [Falco sidekick on Docker using environment variables](https://github.com/falcosecurity/falcosidekick/blob/master/docs/outputs/elasticsearch.md) method.


### Configure Falco for VMs: [_configure_falco_for_vms]

1. Refer to Falco’s documentation to [install Falco on the Linux VMs you wish to monitor](https://falco.org/docs/setup/packages/).
2. Once Falco is installed, update `/etc/falco/falco.yaml` as follows:

    1. Enable JSON output: `json_output: true`
    2. Enable HTTP output: under `http_output`, for the `url` value, enter the `url:port` where Falcosidekick will listen. For example, if Falcosidekick is running on localhost:

        ```
        http_output:
          enabled: true
          url: "http://0.0.0.0:2801/"
        ```



### Configure Falcosidekick for VMs: [falco-config-falco-for-vms]

1. Refer to Falcosidekick’s documentation to [install Falcosidekick](https://github.com/falcosecurity/falcosidekick?tab=readme-ov-file#installation).
2. Use the [Falcosidekick on Docker using environment variables](https://github.com/falcosecurity/falcosidekick/blob/master/docs/outputs/elasticsearch.md) method and set your environment variables as follows:

    1. `ELASTICSEARCH_HOSTPORT`: Your {{es}} endpoint URL, which can be found under **Connection details** on the upper right of the **Integrations** page in {{kib}}.
    2. `ELASTICSEARCH_INDEX`: The {{es}} index where you want to store Falco logs.

       ::::{important}
       Your `ELASTICSEARCH_INDEX` value must match `logs-falco.alerts-*`.
       ::::

    3. `ELASTICSEARCH_SUFFIX`: The frequency with which you want the {{es}} index suffix to change. Either `daily`, `monthly`, `annually`, or `none`.
    4. `ELASTICSEARCH_APIKEY`: The recommended way to authenticate to {{es}}, by providing an [API key](/deploy-manage/api-keys/elasticsearch-api-keys.md). Note that support for this environment variable starts with Falcosidekick version 2.30. You can access the latest version on Falcosidekick’s [Docker Hub](https://hub.docker.com/r/falcosecurity/falcosidekick).
    5. `ELASTICSEARCH_USERNAME` and `ELASTICSEARCH_PASSWORD`: The username and password for an account on your {{es}} instance. Authentication using these environment variables is not supported on {{ecloud}} Serverless.
    6. `ELASTICSEARCH_MUTUALTLS` and `ELASTICSEARCH_CHECKCERT`: For security reasons, we recommend setting these to `true`.


For example:

```
docker run -d -p 2801:2801
           -e ELASTICSEARCH_HOSTPORT=https://test-falco.es.us-west2.gcp.elastic-cloud.com
           -e ELASTICSEARCH_INDEX=logs-falco.alerts-all
           -e ELASTICSEARCH_SUFFIX=none
           -e ELASTICSEARCH_APIKEY=XXXXXXXXXXXXX
           -e ELASTICSEARCH_MUTUALTLS=true
           -e ELASTICSEARCH_CHECKCERT=true falcosecurity/falcosidekick
```

::::{important}
The {{es}} account used to authenticate Falcosidekick only needs sufficient privileges to create and write to new indices. We recommend following the principle of least privilege when provisioning this account.
::::


After installing and configuring Falcosidekick, restart Falco with `sudo systemctl restart falco`. Falcosidekick should start sending alerts to {{es}}.


## Configure Falco and Falcosidekick for Kubernetes [ingest-falco-setup-falco-kubernetes]

1. Add the Falco [Helm charts](https://github.com/falcosecurity/charts/blob/master/README.md):

    ```bash
    helm repo add falcosecurity https://falcosecurity.github.io/charts
    helm repo update
    ```

2. Next, install Falco and Falcosidekick using the `falcosecurity/falco` Helm chart with [appropriate values](https://github.com/falcosecurity/falcosidekick/blob/master/docs/outputs/elasticsearch.md) for each of the `falcosidekick.config.elasticsearch.*` fields:

    ```
    helm install falco falcosecurity/falco \
            --set falcosidekick.enabled=true \
            --set tty=true \
            --set driver.kind=modern_ebpf \
            --set collectors.kubernetes.enabled=true \
            --set falcosidekick.config.elasticsearch.hostport="https://<ES host>" \
            --set falcosidekick.config.elasticsearch.username="<elastic>" \
            --set falcosidekick.config.elasticsearch.password="<password>" \
            --set falcosidekick.config.elasticsearch.index="logs-falco.alerts-all" \
            --set falcosidekick.config.elasticsearch.suffix="none"
    ```
