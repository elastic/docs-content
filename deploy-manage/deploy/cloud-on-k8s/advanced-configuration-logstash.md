---
navigation_title: Advanced configuration
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-logstash-advanced-configuration.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Advanced configuration for {{ls}} on {{eck}} [k8s-logstash-advanced-configuration]

## Setting JVM options [k8s-logstash-jvm-options]

You can change JVM settings by using the `LS_JAVA_OPTS` environment variable to override default settings in `jvm.options`. This approach ensures that expected settings from `jvm.options` are set, and only options that explicitly need to be overridden are.

To do, this, set the  `LS_JAVA_OPTS` environment variable in the container definition of your Logstash resource:

```yaml
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: quickstart
spec:
  podTemplate:
    spec:
      containers:
        - name: logstash
          env:
            - name: LS_JAVA_OPTS   <1>
              value: "-Xmx2g -Xms2g"
```

1. This will change the maximum and minimum heap size of the JVM on each pod to 2GB



## Setting keystore [k8s-logstash-keystore]

You can specify sensitive settings with Kubernetes secrets. ECK automatically injects these settings into the keystore before it starts Logstash. The ECK operator continues to watch the secrets for changes and will restart Logstash Pods when it detects a change.

The Logstash Keystore can be password protected by setting an environment variable called `LOGSTASH_KEYSTORE_PASS`. Check out [Logstash Keystore](logstash://reference/keystore.md#keystore-password) documentation for details.

```yaml subs=true
apiVersion: v1
kind: Secret
metadata:
  name: logstash-keystore-pass
stringData:
  LOGSTASH_KEYSTORE_PASS: changed   <1>

apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: logstash-sample
spec:
  version: {{version.stack}}
  count: 1
  pipelines:
    - pipeline.id: main
      config.string: |-
        input { exec { command => 'uptime' interval => 10 } }
        filter {
          if ("${HELLO:}" != "") {   <2>
            mutate { add_tag => ["awesome"] }
          }
        }
  secureSettings:
    - secretName: logstash-secure-settings
  podTemplate:
    spec:
      containers:
        - name: logstash
          env:
            - name: LOGSTASH_KEYSTORE_PASS
              valueFrom:
                secretKeyRef:
                  name: logstash-keystore-pass
                  key: LOGSTASH_KEYSTORE_PASS
```

1. Value of password to protect the Logstash keystore
2. The syntax for referencing keys is identical to the syntax for environment variables



