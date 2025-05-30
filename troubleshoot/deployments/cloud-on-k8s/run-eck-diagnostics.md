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

# Run eck-diagnostics [k8s-take-eck-dump]

`eck-diagnostics` is a stand-alone command line tool to create a diagnostic archive to help troubleshoot issues with ECK.


## Prepare [k8s_prepare] 

The tool is available at [https://github.com/elastic/eck-diagnostics/](https://github.com/elastic/eck-diagnostics/). You can find detailed installation instructions there.


## Run [k8s_run] 

The eck-diagnostics tool supports various command line flags. Run it with `-h` or `--help` to print all available options. The only required flag is `-r` or `--resources-namespace` which indicates the namespaces where your Elastic stack resources are deployed. There is also `-o` or `--operator-namespaces` that indicate where the ECK operator is deployed. If you don’t specify this flag the tool assumes the operator to be deployed in the `elastic-system` namespace.

```bash
eck-diagnostics -o <operator-namespaces> -r <resources-namespaces>
```

By default, the tool automatically runs [support diagnostics](https://github.com/elastic/support-diagnostics) for every Elasticsearch cluster and Kibana instance. This requires the temporary deployment of additional Pods into the Kubernetes cluster. If this is not what you want, you can turn off the feature by specifying the `--run-stack-diagnostics=false` flag.

The tool can also filter the Elastic resources that it runs diagnostics against by specifying the `-f` or `--filters` flag.  By specifying the type and name of resource, you can filter for any combination of Elastic stack components.

```bash
# Filter only for an elasticsearch cluster named 'mycluster', and a kibana instance named 'mykibana'.
eck-diagnostics -o <operator-namespaces> -r <resources-namespaces> -f "elasticsearch=mycluster" -f "kibana=mykibana"
```

Check [ECK Diagnostics in air-gapped environments](../../../deploy-manage/deploy/cloud-on-k8s/air-gapped-install.md#k8s-eck-diag-air-gapped) if you want to run support diagnostics in environments without access to the open internet.


## Example [k8s_example] 

Assuming the ECK operator is deployed in a namespace called `operators` and Elastic stack resources are deployed in the `security` and `monitoring` namespaces, you should run `eck-diagnostics` as follows:

```bash
eck-diagnostics -o=operators -r=security,monitoring
```

Sample output:

```bash
2021/10/06 20:34:20 ECK diagnostics with parameters: {DiagnosticImage:docker.elastic.co/eck-dev/support-diagnostics:8.1.4 ECKVersion: Kubeconfig: OperatorNamespaces:[operators] ResourcesNamespaces:[security monitoring] OutputDir:/tmp RunStackDiagnostics:true Verbose:false}
2021/10/06 20:34:22 Extracting Kubernetes diagnostics from operators
2021/10/06 20:34:23 ECK version is 1.8.0
2021/10/06 20:34:23 Extracting Kubernetes diagnostics from security
2021/10/06 20:34:23 Extracting Kubernetes diagnostics from monitoring
2021/10/06 20:34:24 ECK diagnostics written to /tmp/eck-diagnostic-2021-10-06T20-34-21.zip
```

