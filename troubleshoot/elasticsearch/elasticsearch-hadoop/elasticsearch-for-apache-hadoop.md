---
navigation_title: Apache Hadoop
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/hadoop/current/troubleshooting.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Troubleshoot Elasticsearch for Apache Hadoop [troubleshooting]

Unfortunately, sometimes things do not go as expected and your elasticsearch-hadoop job execution might go awry: incorrect data might be read or written, the job might take significantly longer than expected or you might face some exception. This section tries to provide help and tips for doing your own diagnostics, identifying the problem and hopefully fixing it.


### `EsHadoopNoNodesLeftException` [_eshadoopnonodesleftexception]

Test that {{es}} is reacheable from the Spark/Hadoop cluster where the job is running. Your machine might reach it but that is not where the actual code will be running. If ES is accessible, minimize the number of tasks and their bulk size; if {{es}} is overloaded, it will keep falling behind, GC will kick in and eventually its nodes will become unresponsive causing clients to think the machines have died. See the [*Performance considerations*](elasticsearch-hadoop://reference/performance-considerations.md) section for more details.


### Test your network [_test_your_network]

Way too many times, folks use their local, development settings in a production environment. Double check that {{es}} is accessible from your production environments, check the host address and port and that the machines where the Hadoop/Spark job is running can access {{es}} (use `curl`, `telnet` or whatever tool you have available).

Using `localhost` (aka the default) in a production environment is simply a misconfiguration.


### Triple check the classpath [_triple_check_the_classpath]

Make sure to use only one version of elasticsearch-hadoop in your classpath. While it might not be obvious, the classpath in Hadoop/Spark is assembled from multiple folders; furthermore, there are no guarantees what version is going to be picked up first by the JVM. To avoid obscure issues, double check your classpath and make sure there is only one version of the library in there, the one you are interested in.


### Isolate the issue [_isolate_the_issue]

When encountering a problem, do your best to isolate it. This can be quite tricky and many times, it is the hardest part so take your time with it. Take baby steps and try to eliminate unnecessary code or settings in small chunks until you end up with a small, tiny example that exposes your problem.


### Use a speedy, local environment [_use_a_speedy_local_environment]

A lot of Hadoop jobs are batch in nature which means they take a long time to execute. To track down the issue faster, use whatever means possible to speed-up the feedback loop: use a small/tiny dataset (no need to load millions of records, some dozens will do) and use a local/pseudo-distributed Hadoop cluster alongside an Elasticsearch node running on your development machine.


### Check your settings [_check_your_settings]

Double check your settings and use constants or replicate configurations wherever possible. It is easy to make typos so try to reduce manual configuration by using properties files or constant interfaces/classes. If you are not sure what a setting is doing, remove it or change its value and see whether it affects your job output.


### Verify the input and output [_verify_the_input_and_output]

Take a close eye at your input and output; this is typically easier to do with Elasticsearch (the service out-lives the job/script, is real-time and can be accessed right away in a flexible meaner, including the command-line). If your data is not persisted (either in Hadoop or Elasticsearch), consider doing that temporarily to validate each step of your work-flow.


### Monitor [_monitor]

While logging helps with bugs and errors, for runtime behavior we strongly recommend doing proper monitoring of your Hadoop and {{es}} cluster. Both are outside the scope of this chapter however there are several popular, free solutions out there that are worth investigating. For {{es}}, we recommend [Marvel](https://www.elastic.co/products/marvel), a free monitoring tool (for development) created by the team behind {{es}}. Monitoring gives insight into how the cluster is actually behaving and helps you correlate behavior. If a monitoring solution is not possible, use the metrics provided by Hadoop, {{es}} and elasticsearch-hadoop to evaluate the runtime behavior.


### Increase logging [_increase_logging]

Logging gives you a lot of insight into what is going on. Hadoop, Spark and {{es}} have extensive logging mechanisms as [does](elasticsearch-hadoop://reference/logging.md) elasticsearch-hadoop however use that judiciously: too much logging can hide the actual issue so again, do it in small increments.


### Measure, do not assume [_measure_do_not_assume]

When encountering a performance issue, do some benchmarking first, in as much isolation as possible. Do not simply assume a certain component is slow; make sure/prove it actually is. Otherwise, more often than not, one might find herself fixing the wrong problem (and typically creating a new one).


### Find a baseline [_find_a_baseline]

Indexing performance depends *heavily* on the type of data being targeted and its mapping. Same goes for searching but add the query definition to the mix. As mentioned before, experiment and measure the various parts of your dataset to find the sweet-spot of your environment before importing/searching big amounts of data.

## Get help [help]

For more help, you can [contact us](/troubleshoot/index.md#contact-us). Use the tips in this section when emailing us or using the Elastic Support Portal.

### Provide details[_what_information_is_useful]

* OS & JVM version
* Hadoop / Spark version / distribution
* if using a certain library (Hive), the version used
* elasticsearch-hadoop version
* the job or script that is causing the issue
* Hadoop / Spark cluster size
* {{es}} cluster size
* the size of the dataset and a snippet of it in its raw format (CSV, TSV, etc.)

### Use a paste site [_where_do_i_post_my_information]

Don't paste long lines of code in emails or the Elastic Support Portal. Instead, use a sharing or pasting utility such as [GitHub Gist](https://gist.github.com/).

