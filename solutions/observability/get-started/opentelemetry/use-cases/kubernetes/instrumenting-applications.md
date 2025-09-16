---
navigation_title: Instrumenting Applications
description: Guidance on instrumenting applications with EDOT SDKs on Kubernetes using automatic or manual instrumentation.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_collector: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Instrument applications with EDOT SDKs on Kubernetes

The [Elastic Distributions of OpenTelemetry (EDOT) SDKs](opentelemetry://reference/edot-sdks/index.md) cover multiple languages. Read on to learn how to instrument applications for APM in a Kubernetes environment for all supported languages.

In Kubernetes environments with the OpenTelemetry Operator, [automatic or zero-code instrumentation](https://opentelemetry.io/docs/kubernetes/operator/automatic/) simplifies the instrumentation process by injecting and configuring instrumentation libraries into the targeted Pods.

On the other hand, manual instrumentation with OpenTelemetry allows you to customize trace spans, metrics, and logging directly in your application’s code. This approach provides more granular control over what and how data is captured.

## Prerequisites

Before starting with application auto-instrumentation, ensure the following prerequisites are in place for proper setup:

- Install the OpenTelemetry operator and EDOT collectors following the [quickstart guide]/solutions/observability/get-started/opentelemetry/quickstart/index.md).
- Ensure a valid `kind: Instrumentation` object exists in the cluster.

## Auto-instrumentation basics

Zero-code instrumentation is handled by the operator through `Instrumentation` objects, used to automatically inject the necessary SDKs and configuration into application workloads.

If you followed the [quickstart guide]/solutions/observability/get-started/opentelemetry/quickstart/index.md) to install the operator, there should be an `Instrumentation` object with name `elastic-instrumentation` in namespace `opentelemetry-operator-system`:

```bash
kubectl get instrumentation -A
NAMESPACE                       NAME                      AGE     ENDPOINT                                                                                                SAMPLER                    SAMPLER ARG
opentelemetry-operator-system   elastic-instrumentation   5d20h   http://opentelemetry-kube-stack-daemon-collector.opentelemetry-operator-system.svc.cluster.local:4318   parentbased_traceidratio   1.0
```

The `Instrumentation` object stores important parameters:

- The exporter endpoint represents the destination for the traces, in this case the HTTP receiver configured in the EDOT DaemonSet Collector. That endpoint has to be reachable by the Pods being instrumented.

   ```yaml
   exporter:
      endpoint: http://opentelemetry-kube-stack-daemon-collector.opentelemetry-operator-system.svc.cluster.local:4318
   ```

- Language-specific images used by the operator to inject the appropriate library into each Pod.

   ```yaml subs=true
   dotnet:
      image: docker.elastic.co/observability/elastic-otel-dotnet:{{version.edot_dotnet}}
   java:
      image: docker.elastic.co/observability/elastic-otel-javaagent:{{version.edot_java}}
   nodejs:
      image: docker.elastic.co/observability/elastic-otel-node:{{version.edot_node}}
   python:
      image: docker.elastic.co/observability/elastic-otel-python:{{version.edot_python}}
   ```

## Configure auto-instrumentation

To turn on auto-instrumentation, add the corresponding language annotation to the Pods template in your Deployment or relevant workload object, like StatefulSet, Job, CronJob, and so on.

For example, the template would contain the following under `spec.template.metadata.annotations`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  # ...
  template:
    metadata:
      annotations:
        instrumentation.opentelemetry.io/inject-<LANGUAGE>: "opentelemetry-operator-system/elastic-instrumentation"
      # ...
    spec:
      containers:
      - image: myapplication-image
        name: app
      # ...
```

Where ``<LANGUAGE>`` is one of: `go` , `java`, `nodejs`, `python`, `dotnet`

::::{note}
Make sure you add the annotations at Pod level and not directly at the workload `spec` level.Annotation values must point to an existing `Instrumentation` object.
::::

You can also turn on auto-instrumentation by adding the annotation at namespace level. This approach automatically applies instrumentation to all Pods within the specified namespace.

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: mynamespace
  annotations:
    instrumentation.opentelemetry.io/inject-<LANGUAGE>: "opentelemetry-operator-system/elastic-instrumentation"
```

After adding annotations to Pods or Namespaces, restart the applications for the instrumentation injection to take effect:

```bash
kubectl rollout restart deployment/my-deployment
```

In case you have multiple Instrumentation objects with different settings or images, make sure you point your Pods to the desired `Instrumentation` objects in the annotations.

The possible values for the annotation are detailed in the [Operator documentation](https://opentelemetry.io/docs/kubernetes/operator/automatic/#add-annotations-to-existing-deployments). For reference purposes, the values are:

- `"true"`: to inject Instrumentation instance with `default` name from the current namespace.
- `"my-instrumentation"`: to inject Instrumentation instance with name `"my-instrumentation"` in the current namespace.
- `"my-other-namespace/my-instrumentation"`: to inject Instrumentation instance with name `"my-instrumentation"` from another namespace `"my-other-namespace"`.
- `"false"`: do not inject.

For details on instrumenting specific languages, refer to:

- [Instrumenting Java](elastic-otel-java://reference/edot-java/setup/k8s.md)
- [Instrumenting Python](elastic-otel-python://reference/edot-python/setup/index.md)
- [Instrumenting Node.js](elastic-otel-node://reference/edot-node/setup/index.md)

### Namespace based annotations example

The following example creates a namespace with an annotation to instrument all Pods of the namespace with `java` libraries.

```bash
kubectl create namespace java-apps

# Annotate app namespace
kubectl annotate namespace java-apps instrumentation.opentelemetry.io/inject-java="opentelemetry-operator-system/elastic-instrumentation"

# Run a java example application in the namespace
kubectl run otel-test -n java-apps --env OTEL_INSTRUMENTATION_METHODS_INCLUDE="test.Testing[methodB]" --image docker.elastic.co/demos/apm/k8s-webhook-test
```

## Verify auto-instrumentation

After adding the annotation and restarting the Pods, run `kubectl describe` on your application Pod to verify the SDK has been properly attached.

Make sure that the `init container`, `volume`, and `environment variables` described in [how auto-instrumentation works](#how-auto-instrumentation-works) have been successfully injected into the Pod.

## How auto-instrumentation works

The OpenTelemetry Operator automates the process of instrumenting applications by injecting the necessary libraries and configuration into the application Pods.

The process may vary slightly depending on the language, but it generally involves the following steps:

- Creating a shared volume: The operator declares an `emptyDir` shared volume within the Pod, and mounts it the app container and a new init container. This volume serves as the medium for sharing the instrumentation library between the new init container and the application container.

- Adding an init container: The operator adds an init container into the Pod. This container is responsible for copying the OpenTelemetry instrumentation library to the shared volume.

- Configuring the main container: The operator injects environment variables into the main application container to configure OpenTelemetry settings (for example, `OTEL_EXPORTER_OTLP_ENDPOINT` or `OTEL_TRACES_SAMPLER`). Additionally, it links the instrumentation library to the application using mechanisms specific to the language runtime, such as:

    - Java: The library is linked through the `javaagent` option using the JAVA_TOOL_OPTIONS environment variable.
    - Node.js: The library is linked through the `NODE_OPTIONS` environment variable.
    - Python: The operator uses the `PYTHONPATH` environment variable to load the library [sitecustomize](https://docs.python.org/es/dev/library/site.html#module-sitecustomize) module.

## Advanced configuration

You can apply OTel-specific configuration to your applications at two different levels:

- At Pod/container level, by using OTel-related environment variables.
- At `Instrumentation` object level, for example configuring different settings per language.

Use cases include the following:

- Change the library to be injected.
- Change the exporter endpoint.
- Apply certain logging level settings (`OTEL_LOG_LEVEL`).

### Additional Instrumentation objects

Consider the creation of different `Instrumentation` objects for different purposes, such as:

- Different configuration options for certain languages.
- Trying out different versions of the SDKs.

## Troubleshooting auto-instrumentation

When troubleshooting auto-instrumentation issues in a Kubernetes environment with the OpenTelemetry Operator, follow these steps:

1. Check that the operator is running. For example:

    ```bash
    $ kubectl get pods -n opentelemetry-operator-system
    NAME                                                              READY   STATUS             RESTARTS      AGE
    opentelemetry-kube-stack-opentelemetry-operator-7b8684cfbdbv4hj   2/2     Running            0             58s
    ...
    ```

2. Check that the `Instrumentation` object has been deployed. For example:

    ```bash
    $ kubectl describe Instrumentation -n opentelemetry-operator-system
    Name:         elastic-instrumentation
    Namespace:    opentelemetry-operator-system
    ...
    Kind:         Instrumentation
    Metadata:
    ...
    Spec:
    Dotnet:
        Image:  docker.elastic.co/observability/elastic-otel-dotnet:edge
    Go:
        Image:  ghcr.io/open-telemetry/opentelemetry-go-instrumentation/autoinstrumentation-go:v0.14.0-alpha
    Java:
        Image:  docker.elastic.co/observability/elastic-otel-javaagent:1.0.0
    Nodejs:
        Image:  docker.elastic.co/observability/elastic-otel-node:edge
    Python:
        Image:  docker.elastic.co/observability/elastic-otel-python:edge
    ...
    ```

3. Check that your pod is running. The following example checks the `banana` namespace:

    ```bash
    $ kubectl get pods -n banana
    NAME               READY   STATUS    RESTARTS   AGE
    example-otel-app   1/1     Running   0          104s
    ```

4. Check that the pod has the instrumentation `initcontainer` installed, or `container` for Go.The events must show that the Docker image was successfully pulled and containers started:

    ```bash
    $ kubectl describe pod/example-otel-app -n banana
    Name:             example-otel-app
    Namespace:        banana
    ...
    Annotations:      instrumentation.opentelemetry.io/inject-java: opentelemetry-operator-system/elastic-instrumentation
    Init Containers:
    opentelemetry-auto-instrumentation-java:
        Container ID:  docker://7ecdf3954263d591b994ed1c0519d16322479b1515b58c1fbbe51d3066210d99
        Image:         docker.elastic.co/observability/elastic-otel-javaagent:1.0.0
        Image ID:      docker-pullable://docker.elastic.co/observability/elastic-otel-javaagent@sha256:28d65d04a329c8d5545ed579d6c17f0d74800b7b1c5875e75e0efd29e210566a
        ...
    Containers:
    example-otel-app:
    ...
    Events:
    Type    Reason     Age   From               Message
    ----    ------     ----  ----               -------
    Normal  Scheduled  5m3s  default-scheduler  Successfully assigned banana/example-otel-app to docker-desktop
    Normal  Pulled     5m3s  kubelet            Container image "docker.elastic.co/observability/elastic-otel-javaagent:1.0.0" already present on machine
    Normal  Created    5m3s  kubelet            Created container opentelemetry-auto-instrumentation-java
    Normal  Started    5m3s  kubelet            Started container opentelemetry-auto-instrumentation-java
    Normal  Pulling    5m2s  kubelet            Pulling image "docker.elastic.co/demos/apm/k8s-webhook-test"
    Normal  Pulled     5m1s  kubelet            Successfully pulled image "docker.elastic.co/demos/apm/k8s-webhook-test" in 1.139s (1.139s including waiting). Image size: 406961626 bytes.
    Normal  Created    5m1s  kubelet            Created container example-otel-app
    Normal  Started    5m1s  kubelet            Started container example-otel-app
    ```

5. Check your pod log for agent output. For example:

    ```bash
    $ kubectl logs example-otel-app -n banana
    ...
    [otel.javaagent 2024-10-11 13:32:44:127 +0000] [main] INFO io.opentelemetry.javaagent.tooling.VersionLogger - opentelemetry-javaagent - version: 1.0.0
    ...
    ```

6. If there is no obvious agent log output, restart the pod with agent log level set to debug and look for agent debug output. Setting the agent to debug is different for the different language agents. Add or set the `OTEL_LOG_LEVEL` environment variable to `debug`. For example:

   ```yaml
      env:
      - name: OTEL_LOG_LEVEL
            value: "debug"
   ```

   For Java, you can set the `OTEL_JAVAAGENT_DEBUG` environment variable to `true`.

## Migrate from the Elastic APM Attacher for Kubernetes

While the Elastic APM Attacher for Kubernetes only supports the Elastic APM application agents, the OpenTelemetry operator can support both the Elastic APM application agents and the EDOT agents. The OpenTelemetry operator has more features and is being actively developed.

Migrating from the Elastic APM Attacher for Kubernetes consists of the following steps:

1. Install the OpenTelemetry operator.
2. Define and install Instrumentation CRDs which correspond to the currently defined values in the existing Elastic APM Attacher for Kubernetes deployment.
3. Change the annotations in deployment definitions from the `co.elastic.apm/attach: ...` to the `instrumentation.opentelemetry.io/inject-...` equivalents.
4. Deploy the new deployment definitions.

### Add instrumentation CRDs

For example, if you have Elastic APM Java agents version 1.53.0 and Elastic APM Nodejs agents version 4.11.2 defined for your values,
and additionally have set the `ELASTIC_APM_LOG_SENDING` environment variable to `true` for the Java agent by default, then the corresponding 
instrumentation would look as in the following snippet. Make sure to replace both `<ELASTIC_APM_SERVER_ENDPOINT>` and `<ELASTIC_API_KEY>`
with your credentials:

```yaml
#
# Filename: elastic-apm-instrumentation.yaml
#
apiVersion: opentelemetry.io/v1alpha1
kind: Instrumentation
metadata:
  name: elastic-apm-instrumentation
  namespace: opentelemetry-operator-system
spec:
  java:
    image: docker.elastic.co/observability/apm-agent-java:1.53.0
    env:
      - name: ELASTIC_APM_SERVER_URL
        value: "<ELASTIC_APM_SERVER_ENDPOINT>"
      - name: ELASTIC_APM_API_KEY
        value: "<ELASTIC_API_KEY>"
      - name: ELASTIC_APM_LOG_SENDING
        value: "true"
  nodejs:
    image: docker.elastic.co/observability/apm-agent-nodejs:4.11.2
    env:
      - name: ELASTIC_APM_SERVER_URL
        value: "<ELASTIC_APM_SERVER_ENDPOINT>"
      - name: ELASTIC_APM_API_KEY
        value: "<ELASTIC_API_KEY>"
```

To add the instrumentation to your cluster, run the following command:

```bash
kubectl apply -f elastic-apm-instrumentation.yaml
```

### Migrate your pods to the new Instrumentation

After you've defined the new instrumentations, migrate your pods by replacing the annotation that currently applies to them with the new annotation for the instrumentation. 

For example if you had a Java application deployment definition which specified the Elastic APM Attacher for Kubernetes annotation of `co.elastic.apm/attach: java`, you can replace that annotation with the equivalent annotation for the OpenTelemetry operator using the new instrumentation names you have defined. For the previous example Instrumentation, the annotation would be `instrumentation.opentelemetry.io/inject-java: "opentelemetry-operator-system/elastic-apm-instrumentation"`

Subsequent deployments will use the new instrumentation. The pods themselves will be auto-instrumented in the same way as they were already being instrumented. Any `ELASTIC_*` environment variables and configuration options will continue to apply.
