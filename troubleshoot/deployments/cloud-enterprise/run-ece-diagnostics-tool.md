---
navigation_title: Diagnostics
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-run-ece-diagnostics.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Run ECE diagnostics tool [ece-run-ece-diagnostics]

ECE diagnostics is a command line tool that you can run on hosts where the ECE instance is installed. It collects logs and metrics, and stores everything into an archive file that can be provided to [Elastic support](/troubleshoot/index.md#troubleshoot-work-with-support) for troubleshooting and investigation purposes.

::::{note}
:::{include} /troubleshoot/_snippets/diagnostics-privacy.md
:::
::::

## Prepare [ece_prepare] 

::::{warning} 
Don’t use the diagnostics tool that comes bundled in ECE images. Always download the latest binary to avoid any known vulnerabilities in the diagnostics acquisition and shipping flow.
::::

Download the bundled diagnostic binary.

* For x86_64 CPU architectures: [https://download.elasticsearch.org/cloud/amd64/ece-diagnostics](https://download.elasticsearch.org/cloud/amd64/ece-diagnostics)
* For ARM CPU architectures: [https://download.elasticsearch.org/cloud/arm64/ece-diagnostics](https://download.elasticsearch.org/cloud/arm64/ece-diagnostics)

Make it executable.

```sh
chmod +x ./ece-diagnostics
```


## How to use [ece_how_to_use] 

To run the default diagnostic

```sh
./ece-diagnostics run
```

This tool supports various command line flags. You can also run it with `-h` or `--help` to print all available subcommands and options:

```sh
./ece-diagnostics --help
```

For example, Elastic Support frequently requests pulling the ECE diagnostic along with certain deployment diagnostics. You can pull these together via:

```sh
./ece-diagnostics run --deployments MY_DEPLOYMENT_ID_1,MY_DEPLOYMENT_ID_2
```

::::{note} 
<<<<<<< anniegale9538-patch-1
ECE deployment diagnostics are not the same as [stack diagnostics](https://github.com/elastic/support-diagnostics#usage-examples), which Elastic support may also request. You can get stack diagnostics from {{ece}} > Deployment > Operations > Generate Bundle.
=======
ECE deployment diagnostics are not the same as [stack diagnostics](https://github.com/elastic/support-diagnostics#usage-examples), which Elastic support may also request. You can get the [{{es}} diagnostic](/troubleshoot/elasticsearch/diagnostic.md) and [{{kib}} diagnostic](/troubleshoot/kibana/capturing-diagnostics.md) from {{ece}} > Deployment > Operations > Prepare Bundle.
>>>>>>> main
::::

## Example output [ece_example_output] 

When you run the ECE diagnostics tool on the host you want to troubleshoot, you might get an output similar to this one:

```sh
[...]
✓ collected information on certificates (took: 104ms)
✓ collected information on client-forwarder connectivity (took: 369ms)
✓ collected API information for ECE and Elasticsearch (took: 9.117s)
✓ collected ZooKeeper stats (took: 9.146s)
✓ collected ECE metricbeat data (took: 12.534s)
✓ collected system information (took: 12.992s)
✓ collected host logs for ECE (took: 29.222s)
✓ collected Docker info and logs (took: 29.246s)
Finished creating file: /tmp/ecediag-192.168.44.10-20220506-084902.tar.gz (total: 48.937s)
```

At that point, you’re ready to upload the `.tar.gz` file to Elastic Support.

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::
