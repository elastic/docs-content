---
navigation_title: CI/CD
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/ci-cd-observability.html
products:
  - id: observability
---



# CI/CD [ci-cd-observability]


To help administrators monitor and troubleshoot their CI/CD platform and help developers increase the speed and reliability of their CI/CD pipelines, Elastic {{observability}} provides visibility in Continuous Integration and Continuous Delivery (CI/CD) processes.

To provide monitoring dashboards, alerting, and root cause analysis on pipelines, Elastic works with the communities of the most popular CI/CD platforms to instrument tools with OpenTelemetry.


## CI/CD observability architectures [ci-cd-architecture]

Using the APM Server, connect all your OpenTelemetry native CI/CD tools directly to Elastic {{observability}}.

:::{image} /solutions/images/observability-simple-arch-observability.png
:alt: Simple architecture of CI/CD observability with Elastic
:title: Architecture of CI/CD observability with Elastic
:::

A more advanced CI/CD observability architecture includes an OpenTelemetry Collector deployed on the edge, next to the CI/CD tools. This architecture provides the following:

* Low latency between the CI/CD tools and the collector is particularly beneficial to ephemeral tools like the otel-cli.
* The ability to route the observability signals to multiple backends in addition to Elastic {{observability}}.

:::{image} /solutions/images/observability-advanced-arch-observability.png
:alt: Advanced architecture of CI/CD observability with Elastic
:title: Advanced architecture of CI/CD observability with Elastic
:::


## Observability for CI/CD administrators [ci-cd-administrators]

Elastic {{observability}} allows CI/CD administrators to monitor and troubleshoot CI/CD platforms and detect anomalies.


### CI/CD platform monitoring and alerting [ci-cd-monitoring]

Elastic {{observability}} helps CI/CD administrators monitor their platform by providing KPI dashboards of CI systems.

The Jenkins health dashboards provide insights on the build executions, the failures, the provisioning of build agents, the active and idle workers, or the JVM health.

:::{image} /solutions/images/observability-ci-cd-overview.png
:alt: CI/CD overview
:title: Jenkins KPIs in Elastic {{observability}}
:screenshot:
:::

:::{image} /solutions/images/observability-jenkins-kpis.png
:alt: Jenkins KPIs
:title: Jenkins Provisioning KPIs in Elastic {{observability}}
:screenshot:
:::

:::{image} /solutions/images/observability-jenkins-jvm-indicators.png
:alt: Jenkins JVM health indicators
:title: Jenkins JVM health indicators in Elastic {{observability}}
:screenshot:
:::


### CI/CD platform troubleshooting [ci-cd-troubleshooting]

CI/CD administrators need to assess the impact of anomalies when troubleshooting platform problems quickly, whether troubleshooting just one pipeline to much broader outages impacting many pipelines or the entire CI/CD platform.

Elastic {{observability}} enables troubleshooting CI platform outages by providing visualizations of pipeline executions as distributed traces, along with the capability to slice and dice pipeline executions in any dimension to assess the nature and the impact of the outage.

In the following image, a Jenkins CI build failed, and its exceptions are reported as errors. Select any of those errors to view the specific information. In this case, it’s errors relating to the CI agent that stopped.

:::{image} /solutions/images/observability-jenkins-pipeline-build.png
:alt: Jenkins pipeline builds
:title: Jenkins pipeline build error in Elastic {{observability}}
:screenshot:
:::

The Errors overview screen provides a high-level view of the exceptions that CI builds catch. Similar errors are grouped to quickly see which ones are affecting your services and allow you to take action to rectify them.

:::{image} /solutions/images/observability-jenkins-pipeline-errors.png
:alt: Jenkins pipeline build errors
:title: Jenkins jobs and pipelines errors in Elastic {{observability}}
:screenshot:
:::

:::{image} /solutions/images/observability-concourse-ci-traces.png
:alt: Concourse CI traces view
:title: Concourse CI pipeline execution as a trace in Elastic {{observability}}
:screenshot:
:::


## Observability for developers [ci-cd-developers]

Development teams need to continuously optimize their ever-changing CI/CD pipelines to improve their reliability while chasing faster pipelines. Visualizations of pipelines as distributed traces help to document what’s happening and improve performance and reliability (flaky tests and pipelines).

Integrating with many popular CI/CD and DevOps tools like Maven or Ansible using OpenTelemetry, Elastic {{observability}} solves these problems by providing deep insights into the execution of CI/CD pipelines.


### CI/CD pipeline visibility [ci-cd-visibility]

The visualization of CI/CD pipelines as distributed traces in Elastic {{observability}} provides documentation and health indicators of all your pipelines.

The Applications Services view in Elastic {{observability}} provides a view of all your instrumented CI/CD servers with insights on their KPIs.

:::{image} /solutions/images/observability-jenkins-servers.png
:alt: Jenkins servers view
:title: Jenkins servers in Elastic {{observability}}
:screenshot:
:::

The Service page provides more granular insights into your CI/CD workflows by breaking down health and performance metrics by pipeline. To quickly view which pipelines experience the most errors, are the most frequently executed, or are the slowest, you can sort and filter the list.

:::{image} /solutions/images/observability-jenkins-server.png
:alt: Jenkins server view
:title: A Jenkins server in Elastic {{observability}}
:screenshot:
:::


### Individual pipeline visibility [ci-cd-pipelines]

Once you’ve identified the pipeline you want to troubleshoot, you can drill down to get more detailed information about its performance over time. The pipeline summary shows a breakdown of duration and failure rates across the pipeline’s individual builds and jobs to spot slowdowns or failures.

:::{image} /solutions/images/observability-jenkins-pipeline-overview.png
:alt: Jenkins pipeline overview
:title: Performance overview of a Jenkins pipeline in Elastic {{observability}}
:screenshot:
:::

The pipelines and traditional jobs are instrumented automatically. If you spot a slow or failing build and need to understand what’s happening, you can drill into the trace view of the build to look for the high duration jobs or jobs with errors. You can then dig into the details to understand the source of the error.

:::{image} /solutions/images/observability-jenkins-pipeline-trace.png
:alt: Trace of a Jenkins pipeline build
:title: A Jenkins pipeline build as a trace in Elastic {{observability}}
:screenshot:
:::

To investigate further, you can view the details of the build captured as labels.

:::{image} /solutions/images/observability-jenkins-pipeline-context.png
:alt: Attributes of a Jenkins pipeline execution
:title: Contextual attributes of a Jenkins pipeline execution in Elastic {{observability}}
:screenshot:
:::


## Store Jenkins pipeline logs in Elastic [ci-cd-store-jenkins-logs]

Jenkins pipeline logs can be sent through the OpenTelemetry Protocol (OTLP) to be stored in an observability backend alongside the traces of the pipeline builds and Jenkins health metrics. Storing logs in an observability backend provides several benefits including:

* Better observability, monitoring, alerting, and troubleshooting of the Jenkins instance thanks to the unification of all the signals in the observability backend.
* Better traceability and long term storage for builds so you can more easily audit the Software Delivery Lifecycle.
* Better scalability and reliability of Jenkins by greatly reducing the quantity of data stored in Jenkins and limiting the well known file system performance challenges of Jenkins when storing a large history of builds.


### Requirements and configuration [ci-cd-store-jenkins-logs-requirements-configuration]

Storing Jenkins pipeline logs in Elastic requires:

* Elastic {{observability}} version 8.1 or higher.
* The OpenTelemetry Protocol endpoint configured on the Jenkins OpenTelemetry Plugin to be reachable from the Jenkins Agents (i.e. don’t specify a localhost OTLP endpoint unless OpenTelemetry collectors are also deployed on the Jenkins Agents).
* When using OpenTelemetry Collectors, to set up a [logs pipeline](https://opentelemetry.io/docs/collector/configuration/#service) in addition to the traces and metrics pipelines.

To store pipeline logs in Elastic:

1. Navigate to the *OpenTelemetry* section of the Jenkins configuration screen.
2. Set the *OTLP Endpoint*.
3. Use the *Add Visualisation Observability Backend* drop-down to select the **Elastic {{observability}}** option.
4. Set the *{{kib}} base URL*.
5. Click the *Advanced* button to choose a storage integration strategy. There are two options for storing pipeline logs in Elastic {{observability}}:

    * **Store pipeline logs in Elastic and visualize logs both in Elastic and through Jenkins**, which means you can view logs stored in Elastic on demand in the Jenkins UI. Read more in [Visualize logs in both {{kib}} and Jenkins](#ci-cd-visualize-logs-kibana-and-jenkins) below.
    * **Store pipeline logs in Elastic and visualize logs exclusively in Elastic**, which means logs will no longer be visible through the Jenkins UI. Read more in [Visualize logs exclusively in {{kib}}](#ci-cd-visualize-logs-kibana) below.


Visualizing logs both in Elastic and through Jenkins is recommended because it provides a more seamless user experience by continuing to render the logs in the Jenkins UI while allowing you to verify the {{es}} setup.


### Visualize logs in both {{kib}} and Jenkins [ci-cd-visualize-logs-kibana-and-jenkins]

The Jenkins OpenTelemetry Plugin provides pipeline log storage in {{es}} while enabling you to visualize the logs in {{kib}} and continue to display them through the Jenkins pipeline build console.

:::{image} /solutions/images/observability-ci-cd-visualize-logs-kibana-and-jenkins-console.png
:alt: Jenkins Console Output page displaying both log contents and a link to view logs in Elastic {{observability}}
:screenshot:
:::

This more advanced setup requires connecting the Jenkins Controller to {{es}} with read permissions on the `logs-apm.app` and preferably on the Metadata of the {{ilm-init}} policy of this index template (by default it’s the `logs-apm.app_logs-default_policy` policy). Use "Validate {{es}} configuration" to verify the setup.

:::{image} /solutions/images/observability-ci-cd-visualize-logs-kibana-and-jenkins-architecture.png
:alt: Architecture diagram for storing pipeline logs in Elastic and visualizing logs in both Elastic and Jenkins
:title: Architecture for storing pipeline logs in Elastic and visualizing logs in both Elastic and Jenkins
:::


### Visualize logs exclusively in {{kib}} [ci-cd-visualize-logs-kibana]

Visualizing logs exclusively in {{kib}} involves a simpler setup that doesn’t require access to {{es}} from the Jenkins Controller. This is because the Jenkins pipeline build console displays a hyperlink to the {{kib}} logs visualization screen instead of displaying the logs in the Jenkins UI.

:::{image} /solutions/images/observability-ci-cd-visualize-logs-kibana-console.png
:alt: Jenkins Console Output page with link to view logs in Elastic {{observability}}
:screenshot:
:::

:::{image} /solutions/images/observability-ci-cd-visualize-logs-kibana-architecture.png
:alt: Architecture diagram for storing pipeline logs in Elastic and visualizing logs exclusively in Elastic
:title: Architecture for storing pipeline logs in Elastic and visualizing logs exclusively in Elastic
:::


## Instrument CI/CD pipelines [ci-cd-instrumentation]

Observing CI/CD pipelines is achieved by instrumenting the different CI/CD and DevOps tools. Elastic works with the Open Source communities leveraging OpenTelemetry to provide the best coverage.


### Jenkins [ci-cd-jenkins]


#### Install the OpenTelemetry plugin [ci-cd-install-jenkins]

1. On the Jenkins UI, go to **Manage Jenkins** > **Manage Plugins**.

    :::{image} /solutions/images/observability-jenkins-plugin-manager.png
    :alt: Jenkins Plugin Manager
    :screenshot:
    :::

2. Click the **Available** tab, and search for **OpenTelemetry**.
3. Select the **OpenTelemetry** checkbox and then click **Download now and install after restart**.

    To verify that the plugin is installed, click the **Installed** tab, and search for **OpenTelemetry Plugin**.



#### Configure the OpenTelemetry plugin [ci-cd-configure-jenkins]

The OpenTelemetry plugin needs to be configured to report data to an OpenTelemetry service. In addition, you will need the endpoint of the OpenTelemetry service, the type of authentication, and the access credentials.

1. On the Jenkins UI, go to **Manage Jenkins** > **Configure System**.
2. Go to the OpenTelemetry Plugin section.
3. Configure your OpenTelemetry endpoint and authentication using the Elastic APM Server URL and the APM Server authentication:

    * If using the Elastic APM secret token authorization, select a **Bearer Authentication Token**, and add the token as a Jenkins secret text credential.

        :::{image} /solutions/images/observability-configure-otel-plugin.png
        :alt: Configure OTEL plugin
        :screenshot:
        :::

    * If using the Elastic API Key authorization, define the **Header Authentications**:

        * Header name: `"Authorization"`
        * Header value: a secret text credential with the value of `"ApiKey an_api_key"` (`an_api_key` is the value of the secret key)


1. Go to **Add Visualisation Observability Backend** and define the URL for your {{kib}} server.

    :::{image} /solutions/images/observability-kibana-url.png
    :alt: Define {{kib}} URL
    :screenshot:
    :::

2. Finally, there are additional settings to configure:

    * Endpoint certificates to use in communications.
    * The service name and service namespace sent to the OpenTelemetry service.
    * Timeouts and batch process times.
    * Any steps you may want to omit from the data you send.

        ::::{warning}
        You can export the OpenTelemetry configuration as environment variables to use them with other tools like otel-cli, Ansible Otel plugin, and so on. If you enable this option, consider that you can potentially expose the credentials in the console output.
        ::::


To learn more about the integration of Jenkins with Elastic {{observability}}, see [OpenTelemetry](https://plugins.jenkins.io/opentelemetry/).


#### Install Jenkins dashboards in {{kib}} [ci-cd-jenkins-dashbaords]

There are out of the box {{kib}} dashboards that help visualize some metrics for the CI/CD platform.

Using the [Import saved objects API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-saved-objects-import) or the {{kib}} UI, you can [install dashboards](https://github.com/jenkinsci/opentelemetry-plugin/blob/master/docs/DASHBOARDS.md#elastic) that are compatible with version 7.12 or higher.

For instance, you can follow the below steps:

* Import the dashboard in the {{kib}} UI

:::{image} /solutions/images/observability-jenkins-dashboard-import.png
:alt: Import {{kib}} dashboard
:title: Import dashboard in {{kib}}
:screenshot:
:::

* The new dashboard is now ready to be used:

:::{image} /solutions/images/observability-jenkins-dashboard-ready.png
:alt: Jenkins dashboard in {{kib}}
:title: Jenkins dashboard in {{kib}} is ready
:screenshot:
:::

:::{image} /solutions/images/observability-jenkins-dashboard.png
:alt: Jenkins dashboard
:title: Jenkins dashboard in {{kib}}
:screenshot:
:::


### Maven [ci-cd-maven]

The Maven OpenTelemetry extension integration provides comprehensive visibility into all of your Maven builds. The extension generates traces for each build and performance metrics to help you understand which Maven goals or Maven submodules are run the most, how often they fail, and how long they take to complete.

The context propagation from CI pipelines (Jenkins job or pipeline) is passed to the Maven build through the `TRACEPARENT` and `TRACESTATE` environment variables that match the [W3C Trace Context specification](https://www.w3.org/TR/trace-context/). Therefore, everything that happens in the CI platform is also shown in the traces.

You can configure your Maven project with the [Maven OpenTelemetry extension](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/maven-extension). For example, you can add the following snippet to your pom.xml file:

```bash
<project>
  ...
  <build>
    <extensions>
      <extension>
          <groupId>io.opentelemetry.contrib</groupId>
          <artifactId>opentelemetry-maven-extension</artifactId>
          <version>1.12.0-alpha</version>
      </extension>
    </extensions>
  </build>
</project>
```

You can now trigger to send the Maven build reporting performance data to Elastic {{observability}} by passing the configuration details as environment variables:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="https://elastic-apm-server.example.com:8200"
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer an_apm_secret_token"
export OTEL_TRACES_EXPORTER="otlp"

mvn verify
```

You can instrument Maven builds without modifying the pom.xml file using the Maven command line argument “-Dmaven.ext.class.path=…”

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="https://elastic-apm-server.example.com:8200"
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer an_apm_secret_token"
export OTEL_TRACES_EXPORTER="otlp"

mvn -Dmaven.ext.class.path=path/to/opentelemetry-maven-extension.jar verify
```

You can also trigger your Maven builds from the CI platform and visualize the end-to-end pipeline execution in Elastic {{observability}}, including the detailed steps of your CI pipeline and the Maven build.

When invoking Maven builds with Jenkins, it’s unnecessary to use environment variables to configure the Maven build (`OTEL_EXPORTER_OTLP_ENDPOINT…`) to rely on the Jenkins capability to inject OpenTelemetry configuration as environment variables. For more details, refer to [Install the OpenTelemetry plugin](#ci-cd-install-jenkins).

:::{image} /solutions/images/observability-jenkins-maven-pipeline.png
:alt: Maven builds in Jenkins
:title: A Jenkins pipeline executing Maven builds
:screenshot:
:::

To learn more, see the [integration of Maven builds with Elastic {{observability}}](https://github.com/open-telemetry/opentelemetry-java-contrib/tree/main/maven-extension).


### Ansible [ci-cd-ansible]

The Ansible OpenTelemetry plugin integration provides visibility into all your Ansible playbooks. The plugin generates traces for each run and performance metrics to help you understand which Ansible tasks or roles are run the most, how often they fail, and how long they take to complete.

You can configure your Ansible playbooks with the [Ansible OpenTelemetry callback plugin](https://docs.ansible.com/ansible/latest/collections/community/general/opentelemetry_callback.html). It’s required to install the OpenTelemetry python libraries and configure the callback as stated in the [examples](https://docs.ansible.com/ansible/latest/collections/community/general/opentelemetry_callback.html#examples) section.

The context propagation from the Jenkins job or pipeline is passed to the Ansible run. Therefore, everything that happens in the CI is also shown in the traces.

:::{image} /solutions/images/observability-jenkins-ansible-pipeline.png
:alt: Ansible playbooks in Jenkins
:title: Visibility into your Ansible playbooks
:screenshot:
:::

This integration feeds, out of the box, the Service Map with all the services that are connected to the Ansible Playbook. All of these features can help you quickly and visually assess your services used in your provisioning and Continuous Deployment.

:::{image} /solutions/images/observability-ansible-service-map.png
:alt: Ansible service map view
:title: ServiceMap view of a Jenkins pipeline execution instrumented with the Ansible plugin
:screenshot:
:::


### Ansible AWX/Tower [ci-cd-ansible-tower]

The Ansible OpenTelemetry plugin integration supports Ansible AWX/Tower. To enable it, follow these steps.

AWX requires an Execution Environment with the Ansible and Python packages installed. You can use the [Ansible Builder CLI tool](https://www.ansible.com/blog/introduction-to-ansible-builder) to create the container definition. Then upload the container to an image repository accessible by AWX and define an Execution Environment using the container you created.

To inject the environment variables and service details, use custom credential types and assign the credentials to the Playbook template. This gives you the flexibility to reuse the endpoint details for Elastic APM and also standardize on custom fields for reporting purposes.

:::{image} /solutions/images/observability-ansible-automation-apm-endpoint.png
:alt: Applications Services Endpoint in Ansible Tower
:title: An Applications Services Endpoint in Ansible AWX/Tower
:screenshot:
:::

:::{image} /solutions/images/observability-ansible-automation-apm-service-details.png
:alt: Custom fields in Ansible Tower
:title: Custom fileds in Ansible AWX/Tower
:screenshot:
:::

Want to learn more? This [blog post](https://www.elastic.co/blog/5-questions-about-ansible-that-elastic-observability-can-answer) provides a great overview of how all of these pieces work together.


### Otel CLI [ci-cd-otel-cli]

[otel-cli](https://github.com/equinix-labs/otel-cli) is a command-line tool for sending OpenTelemetry traces, which is useful if instrumenting your scripts explicitly when no other implicit integration is in place.

Using the otel-cli wrapper, you can configure your build scripts implemented in shell, make, or another scripting language. For example, instrumenting the Makefile below with otel-cli helps visualize every command in each goal as spans.

```bash
# see https://blog.container-solutions.com/tagging-docker-images-the-right-way

NAME   := acmecorp/foo
TAG    := $$(git log -1 --pretty=%!H(MISSING))
IMG    := ${NAME}:${TAG}
LATEST := ${NAME}:latest

build:
  @otel-cli exec \
    --name 'docker build' \
    docker build -t ${IMG} .
  @otel-cli exec \
    --name 'docker tag' \
    docker tag ${IMG} ${LATEST}

push:
  @otel-cli exec \
    --name 'docker push' \
    --attrs "http.url=https://docker.elastic.dev" \
    docker push ${NAME}

login:
  @otel-cli exec \
    --name 'docker login' \
    --attrs 'rpc.system=grpc' \
    docker login -u ${DOCKER_USER} -p ${DOCKER_PASS}
```

To invoke shell scripts that use otel-cli for tracing:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="elastic-apm-server.example.com:8200"
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer an_apm_secret_token"
export OTEL_TRACES_EXPORTER="otlp"

make login build push
```

:::{image} /solutions/images/observability-jenkins-makefile.png
:alt: Jenkins build executing an instrumented Makefile
:title: A Jenkins build executing a Makefile instrumented with the otel-cli in Elastic {{observability}}
:screenshot:
:::

:::{image} /solutions/images/observability-jenkins-service-map.png
:alt: Jenkins service map view
:title: ServiceMap view of a Jenkins pipeline execution instrumented with the otel-cli
:screenshot:
:::


### Pytest-otel [ci-cd-pytest-otel]

[pytest-otel](https://pypi.org/project/pytest-otel/) is a pytest plugin for sending Python test results as OpenTelemetry traces. The test traces help you understand test execution, detect bottlenecks, and compare test executions across time to detect misbehavior and issues.

The context propagation from CI pipelines (Jenkins job or pipeline) is passed to the Maven build through the `TRACEPARENT`.

```bash
OTEL_EXPORTER_OTLP_ENDPOINT=https://elastic-apm-server.example.com:8200 \
OTEL_EXPORTER_OTLP_HEADERS="authorization=Bearer an_apm_secret_token" \
OTEL_SERVICE_NAME=pytest_otel \
pytest --otel-session-name='My_Test_cases'
```

:::{image} /solutions/images/observability-pytest-otel-pipeline.png
:alt: Pytest tests
:title: Visibility into your Pytest tests
:screenshot:
:::


### Concourse CI [ci-cd-concourse-ci]

To configure Concourse CI to send traces, refer to the [tracing](https://concourse-ci.org/tracing.html) docs. In the Concourse configuration, you just need to define `CONCOURSE_TRACING_OTLP_ADDRESS` and `CONCOURSE_TRACING_OTLP_HEADERS`.

```bash
CONCOURSE_TRACING_OTLP_ADDRESS=elastic-apm-server.example.com:8200
CONCOURSE_TRACING_OTLP_HEADERS=Authorization=Bearer your-secret-token
```

Context propagation is supported; therefore, you can benefit from the integrations described above.

Once Concourse CI tracing is configured, Concourse CI pipeline executions are reported in Elastic {{observability}}.

:::{image} /solutions/images/observability-jenkins-concourse.png
:alt: Concourse CI pipeline execution
:title: A Concourse CI pipeline execution in Elastic {{observability}}
:screenshot:
:::

The Concourse CI doesn’t report health metrics through OpenTelemetry. However, you can use the [OpenTelemetry Collector Span Metrics Processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/spanmetricsprocessor#span-metrics-processor) to derive pipeline execution traces into KPI metrics like throughput and the error rate of pipelines.


## Check service health from deployment pipelines [check-service-health-from-cd-pipelines]

Integrating automated service health checks in deployment pipelines is critical for end-to-end deployment automation, which crucially enables deployment frequency to be increased.

Elastic {{observability}} exposes HTTP APIs to check the health of services. You can integrate these APIs in deployment pipelines to verify the behavior of newly deployed instances, and either automatically continue the deployments or roll back according to the health status.

The following example shows a canary deployment pipeline that leverages Elastic health check HTTP APIs to automate the quality check before rolling out the deployment from the canary to the entire set of instances:

:::{image} /solutions/images/observability-ci-cd-canary-deployment-pipeline.png
:alt: Canary Deployment Pipeline
:::

Perform the health check by invoking the `KIBANA_URL/internal/apm/services` API to compare the transaction error rate of the service on the newly deployed instances with a threshold value. Pass the following parameters to the invocation:

* `start` and `end`: time interval using the [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format (e.g. "2021-09-01T13:24:12Z" which is a UTC time)
* `kuery`: used to filter on the service name and, for example, the new version being deployed to narrow down to the canary instances. Example `service.name:"MY_SERVICE_NAME" AND service.version:"1.2.3"`
* `environment`: the environment on which the canary instances are deployed. Example: `production`.

To define the time range, use the `start` and `end` parameters. These parameters are dates in ISO-8601 format. To query only one service, compose a filter in the parameter `kuery`, then filter by the service name using the expression `service.name:MY_SERVICE_NAME and service.version: SERVICE_VERSION`. Finally apply an `environment` filter by passing the `environment` parameter. To select all environments, use `ENVIRONMENT_ALL`.

The API call requires authentication. We recommend to use an API Token to authenticate.

The API is subject to changes and a stable API optimized for Continuous Delivery use cases will soon be published.

```python
def check_service_health(service_name, service_version, error_rate_threshold, kibana_url, api_token):
    now = datetime.now()
    five_minutes_ago = now - timedelta(minutes=5)
    params = {
        "start": five_minutes_ago.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "kuery": "service.name:{} and service.version:{}".format(service_name, service_version),
        "environment": "ENVIRONMENT_ALL"
    }
    url = "{}/internal/apm/services?{}".format(kibana_url, urllib.parse.urlencode(params))
    req = urllib.request.Request(url=url, headers={"Authorization": "Bearer {}".format(api_token)})
    with urllib.request.urlopen(req) as response:
     body = response.read().decode("utf8")
     obj = json.loads(body)
     if len(obj['items']) > 0 and obj['items'][0].transactionErrorRate > error_rate_threshold:
            raise Exception("Error rate for service {} is higher than threshold {}, current value is {}".format(service_name, error_rate_threshold, obj['items'][0].transactionErrorRate))
```

