---
navigation_title: Diagnostics
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-take-eck-dump.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Capture ECK diagnostics [k8s-take-eck-dump]

{{eck}} (ECK) diagnostics is a stand-alone command line tool that you can run on hosts where the ECK operator is installed. It collects logs, metrics, and configuration details, and stores everything into an archive file that can be provided to [Elastic support](/troubleshoot/index.md#troubleshoot-work-with-support) for troubleshooting and investigation purposes.

::::{note}
:::{include} /troubleshoot/_snippets/diagnostics-privacy.md
:::
::::

## Prepare [k8s_prepare] 

To install the [eck-diagnostics](https://github.com/elastic/eck-diagnostics/) tool:

1. Locate the [latest release](https://github.com/elastic/eck-diagnostics/releases/latest).
2. Download the `*.tar.gz` asset associated with your hardware profile.
3. Unpack the gzip'ed tar archive to access the diagnostic binary `eck-diagnostics`.

## Run [k8s_run] 

You must know the Kubernetes namespaces of your operator and stack resources to run this diagnostic. The most common usage of this `eck-diagnostics` binary is:

```bash
eck-diagnostics -o <operator-namespaces> -r <resources-namespaces>
```

This tool supports various command line flags. The most common command line flags are:

* (Optional) `-h` or `--help` to print all available options. 

    ```bash
    eck-diagnostics --help
    ```

* (Required) `-r` or `--resources-namespaces` to indicate the namespaces where your Elastic stack resources are deployed. 

* (Optional) `-o` or `--operator-namespaces` to specify the namespace where the ECK operator is installed. Defaults to `elastic-system`.

* (Optional) `--stack-diagnostics-timeout` to designate the maximum waiting time to pull the {{es}} and {{kib}} diagnostics. Defaults to `5m0s`.

* (Optional) `--run-stack-diagnostics=false` to deactivate collecting [{{es}} diagnostics](/troubleshoot/elasticsearch/diagnostic.md) and [{{kib}} diagnostics](/troubleshoot/kibana/capturing-diagnostics.md) from the resources namespace. This is enabled by default and is recommended, but requires the temporary deployment of additional Pods into the Kubernetes cluster.

* (Optional) `-f` or `--filters` to filter the Elastic stack resources to run diagnostics against. By specifying the type and name of resource, you can filter for any combination of Elastic stack components.

    ```bash
    # Filter only for an elasticsearch cluster named 'mycluster', and a kibana instance named 'mykibana'.
    eck-diagnostics -o <operator-namespaces> -r <resources-namespaces> -f "elasticsearch=mycluster" -f "kibana=mykibana"
    ```

Check [ECK Diagnostics in air-gapped environments](/deploy-manage/deploy/cloud-on-k8s/air-gapped-install.md#k8s-eck-diag-air-gapped) for command line flags to run support diagnostics in environments without access to the open internet.

## Example [k8s_example] 

Assuming the ECK operator is deployed in a namespace called `operators` and Elastic stack resources are deployed in the `security` and `monitoring` namespaces, you should run `eck-diagnostics` as follows:

```bash
eck-diagnostics -o=operators -r=security,monitoring
```

Sample output:

```bash
2026/01/01 20:34:20 ECK diagnostics with parameters: {DiagnosticImage:docker.elastic.co/eck-dev/support-diagnostics:9.3.1 ECKVersion: Kubeconfig: OperatorNamespaces:[operators] ResourcesNamespaces:[security monitoring] OutputDir:/tmp RunStackDiagnostics:true Verbose:false}
2026/01/01 20:34:22 Extracting Kubernetes diagnostics from operators
2026/01/01 20:34:23 ECK version is 3.1.0
2026/01/01 20:34:23 Extracting Kubernetes diagnostics from security
2026/01/01 20:34:23 Extracting Kubernetes diagnostics from monitoring
2026/01/01 20:34:24 ECK diagnostics written to /tmp/eck-diagnostic-2026-01-01T20-34-21.zip
```
