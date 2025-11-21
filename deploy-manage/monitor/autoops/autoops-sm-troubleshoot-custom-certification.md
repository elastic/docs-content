---
applies_to:
  deployment:
    self:
    ece:
    eck:
navigation_title: Elastic agent not recognizing SSL certificate
products:
  - id: cloud-kubernetes
  - id: cloud-enterprise
---

# Troubleshoot {{agent}} not recognizing custom SSL certificate 

If {{agent}} is failing to connect your self-managed cluster to AutoOps because it doesn't recognize your SSL certificate, this may be because your certificate is signed by a custom or internal Certificate Authority (CA). 

You may encounter an error like the following:

```sh
... x509: certificate signed by unknown authority ...
```

This error occurs because the machine where you have installed {{agent}} does not trust your custom or internal CA. To fix this error, you need to configure the agent with your custom certificate by providing its certificate file so that the machine trusts your CA.

This following section provides the steps to configure {{agent}} with a custom SSL certificate so that the agent can successfully connect your self-managed cluster to AutoOps.

## Configure AutoOps {{agent}} with a custom SSL certificate

To configure {{agent}} with your custom SSL certificate, you must edit the `elastic-agent.yml` file on the agent's host machine to add the path to your certificate. The host machine is the machine where you have installed the agent. 

Complete the following steps:

1. On the host machine, open the `elastic-agent.yml` file. \
  The default location is `/opt/Elastic/Agent/elastic-agent.yml`.
2. In the `elastic-agent.yml` file, locate the `receivers.metricbeatreceiver.metricbeat.modules` section. 
3. In this section, there will be two modules configured for `autoops_es`, one for metrics and one for templates. \
  Add the `ss.certificate_authorities` setting to both these modules using one of the following options:

    :::::{tab-set}
    :group: add-cert-auth-setting-to-module

    ::::{tab-item} Use environment variable (recommended)
    :sync: env-variable

    We recommend using this method because it's flexible and keeps sensitive paths out of your main configuration.

    Add the following line to both `autoops_es` modules:

    ```yaml
    ssl.certificate_authorities:
      - ${env:AUTOOPS_CA_CERT}
    ```
    After adding this line to both modules, make sure the` AUTOOPS_CA_CERT` environment variable is set on the host machine and contains the full path to your certificate file (for example: `/etc/ssl/certs/my_internal_ca.crt`).
    ::::

    ::::{tab-item} Hardcode file path
    :sync: hardcode-file-path

    Use this method to specify the path directly. This method is often simpler for fixed or test environments.

    ```yaml
    ssl.certificate_authorities:
      - "/path/to/your/ca.crt"
    ```

    ::::

    :::::

    $$$step-3-example$$$The following codeblock shows what your final configuration should look like. This example uses the second option, hardcoding the file path.

    ```yaml
    receivers:
      metricbeatreceiver:
        metricbeat:
          modules:
            # Metrics
            - module: autoops_es
              hosts: ${env:AUTOOPS_ES_URL}
              period: 10s
              metricsets:
                - cat_shards
                - cluster_health
                - cluster_settings
                - license
                - node_stats
                - tasks_management
              # --- ADD THIS LINE ---
              ssl.certificate_authorities:
                - "/path/to/your/ca.crt"

            # Templates
            - module: autoops_es
              hosts: ${env:AUTOOPS_ES_URL}
              period: 24h
              metricsets:
                - cat_template
                - component_template
                - index_template
              # --- ADD THIS LINE ---
              ssl.certificate_authorities:
                - "/path/to/your/ca.crt"
    ```
4. Save your changes to the `elastic-agent.yml` file.
5. Restart {{agent}} so that the new settings can take effect.\
    In most systemd-based Linux environments, you can use the following command to restart the agent:
    ```bash
    sudo systemctl restart elastic-agent
    ```
6. Check the agent logs again to confirm that the error is gone and that {{agent}} has successfully connected your self-managed cluster to AutoOps. 

    :::{note}
    If you encounter the following error in the agent logs, there may be a formatting issue in the `elastic-agent.yml` file.
    ```sh
    ... can not convert 'object' into 'string' ... ssl.certificate_authorities ...
    ```
    To fix this error, ensure your configuration matches the [example codeblock](#step-3-example) provided in step 3. The `ss.certificate_authorities` setting must be a list item (indicated by the `-`) containing one or more strings (the respective path to your certification files).
    :::