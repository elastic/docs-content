---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/add-fleet-server-kubernetes.html
---

# Deploy Fleet Server on Kubernetes [add-fleet-server-kubernetes]

::::{note}
If your {{stack}} is orchestrated by [ECK](/deploy-manage/deploy/cloud-on-k8s.md), we recommend to deploy the {{fleet-server}} through the operator. That simplifies the process, as the operator automatically handles most of the resources configuration and setup steps.

Refer to [Run Fleet-managed {{agent}} on ECK](/deploy-manage/deploy/cloud-on-k8s/fleet-managed-elastic-agent.md) for more information.

::::


::::{important}
This guide assumes familiarity with Kubernetes concepts and resources, such as `Deployments`, `Pods`, `Secrets`, or `Services`, as well as configuring applications in Kubernetes environments.

::::


To use {{fleet}} for central management, a [{{fleet-server}}](/reference/ingestion-tools/fleet/fleet-server.md) must be running and accessible to your hosts.

You can deploy {{fleet-server}} on Kubernetes and manage it yourself. In this deployment model, you are responsible for high-availability, fault-tolerance, and lifecycle management of the {{fleet-server}}.

To deploy a {{fleet-server}} on Kubernetes and register it into {{fleet}} you will need the following details:

* The **Policy ID** of a {{fleet}} policy configured with the {{fleet-server}} integration.
* A **Service token**, used to authenticate {{fleet-server}} with Elasticsearch.
* For outgoing traffic:

    * The **{{es}} endpoint URL** where the {{fleet-server}} should connect to, configured also in the {{es}} output associated to the policy.
    * When a private or intermediate Certificate Authority (CA) is used to sign the {{es}} certificate, the **{{es}} CA file** or the **CA fingerprint**, configured also in the {{es}} output associated to the policy.

* For incoming connections:

    * A **TLS/SSL certificate and key** for the {{fleet-server}} HTTPS endpoint, used to encrypt the traffic from the {{agent}}s. This certificate has to be valid for the **{{fleet-server}} Host URL** that {{agent}}s use when connecting to the {{fleet-server}}.

* Extra TLS/SSL certificates and configuration parameters in case of requiring [mutual TLS](/reference/ingestion-tools/fleet/mutual-tls.md) (not covered in this document).

This document walks you through the complete setup process, organized into the following sections:

* [Compatibility requirements](#add-fleet-server-kubernetes-compatibility)
* [{{fleet-server}} and SSL/TLS certificates considerations](#add-fleet-server-kubernetes-cert-prereq)
* [{{fleet}} preparations](#add-fleet-server-kubernetes-add-server)
* [{{fleet-server}} installation](#add-fleet-server-kubernetes-install)
* [Troubleshoot {{fleet-server}}](#add-fleet-server-kubernetes-troubleshoot)
* [Next steps](#add-fleet-server-kubernetes-next)


## Compatibility [add-fleet-server-kubernetes-compatibility]

{{fleet-server}} is compatible with the following Elastic products:

* {{stack}} 7.13 or later.

    * For version compatibility, {{es}} must be at the same or a later version than {{fleet-server}}, and {{fleet-server}} needs to be at the same or a later version than {{agent}} (not including patch releases).
    * {{kib}} should be on the same minor version as {{es}}.



## Prerequisites [add-fleet-server-kubernetes-prereq]

Before deploying {{fleet-server}}, you need to:

* Prepare the SSL/TLS configuration, server certificate, [{{fleet-server}} host settings](/reference/ingestion-tools/fleet/fleet-settings.md#fleet-server-hosts-setting), and needed Certificate Authorities (CAs).
* Ensure components have access to the ports needed for communication.


### {{fleet-server}} and SSL/TLS certificates considerations [add-fleet-server-kubernetes-cert-prereq]

This section shows the minimum requirements in terms of Transport Layer Security (TLS) certificates for the {{fleet-server}}, assuming no mutual TLS (mTLS) is needed. Refer to [One-way and mutual TLS certifications flow](/reference/ingestion-tools/fleet/tls-overview.md) and [{{agent}} deployment models with mutual TLS](/reference/ingestion-tools/fleet/mutual-tls.md) for more information about the configuration needs of both approaches.

There are two main traffic flows for {{fleet-server}}, each with different TLS requirements:


#### [{{agent}} → {{fleet-server}}] inbound traffic flow [add-fleet-server-kubernetes-cert-inbound]

In this flow {{fleet-server}} acts as the server and {{agent}} acts as the client. Therefore, {{fleet-server}} requires a TLS certificate and key, and {{agent}} will need to trust the CA certificate used to sign the {{fleet-server}} certificate.

::::{note}
A {{fleet-server}} certificate is not required when installing the server using the **Quick start** mode, but should always be used for **production** deployments. In **Quick start** mode, the {{fleet-server}} uses a self-signed certificate and the {{agent}}s have to be enrolled with the `--insecure` option.

::::


If your organization already uses the {{stack}}, you may have a CA certificate that could be used to generate the new cert for the {{fleet-server}}. If you do not have a CA certificate, refer to [Generate a custom certificate and private key for {{fleet-server}}](/reference/ingestion-tools/fleet/secure-connections.md#generate-fleet-server-certs) for an example to generate a CA and a server certificate using the `elasticsearch-certutil` tool.

::::{important}
Before creating the certificate, you need to know and plan in advance the [hostname / URL](/reference/ingestion-tools/fleet/fleet-settings.md#fleet-server-hosts-setting) that the {{agent}} clients will use to access the {{fleet-server}}. This is important because the **hostname** part of the URL needs to be included in the server certificate as an `x.509 Subject Alternative Name (SAN)`. If you plan to make your {{fleet-server}} accessible through **multiple hostnames** or **FQDNs**, add all of them to the server certificate, and take in mind that the **{{fleet-server}} also needs to access the {{fleet}} URL during its bootstrap process**.

::::



#### [{{fleet-server}} → {{es}} output] outbound traffic flow [add-fleet-server-kubernetes-cert-outbound]

In this flow, {{fleet-server}} acts as the client and {{es}} acts as the HTTPS server. For the communication to succeed, {{fleet-server}} needs to trust the CA certificate used to sign the {{es}} certificate. If your {{es}} cluster uses certificates signed by a corporate CA or multiple intermediate CAs you will need to use them during the {{fleet-server}} setup.

::::{note}
If your {{es}} cluster is on Elastic Cloud or if it uses a certificate signed by a public and known CA, you won’t need the {{es}} CA during the setup.

::::


In summary, you need:

* A **server certificate and key**, valid for the {{fleet-server}} URL. The CA used to sign this certificate will be needed by the {{agent}} clients and the {{fleet-server}} itself.
* The **CA certificate** (or certificates) associated to your {{es}} cluster, except if you are sure your {{es}} certificate is fully trusted publicly.


### Default port assignments [default-port-assignments-kubernetes]

When {{es}} or {{fleet-server}} are deployed, components communicate over well-defined, pre-allocated ports. You may need to allow access to these ports. Refer to the following table for default port assignments:

|     |     |
| --- | --- |
| Component communication | Default port |
| {{agent}} → {{fleet-server}} | 8220 |
| {{fleet-server}} → {{es}} | 9200 |
| {{fleet-server}} → {{kib}} (optional, for {{fleet}} setup) | 5601 |
| {{agent}} → {{es}} | 9200 |
| {{agent}} → Logstash | 5044 |
| {{agent}} → {{kib}} (optional, for {{fleet}} setup) | 5601 |

In Kubernetes environments, you can adapt these ports without modifying the listening ports of the {{fleet-server}} or other applications, as traffic is managed by Kubernetes `Services`. This guide includes an example where {{agent}}s connect to the {{fleet-server}} through port `443` instead of the default `8220`.


## Add {{fleet-server}} [add-fleet-server-kubernetes-add-server]

A {{fleet-server}} is an {{agent}} that is enrolled in a {{fleet-server}} policy. The policy configures the agent to operate in a special mode to serve as a {{fleet-server}} in your deployment.


### {{fleet}} preparations [add-fleet-server-kubernetes-preparations]

::::{tip}
If you already have a {{fleet}} policy with the {{fleet-server}} integration, you know its ID, and you know how to generate an [{{es}} service token](elasticsearch://docs/reference/elasticsearch/command-line-tools/service-tokens-command.md) for the {{fleet-server}}, skip directly to [{{fleet-server}} installation](#add-fleet-server-kubernetes-install).

Also note that the `service token` required by the {{fleet-server}} is different from the `enrollment tokens` used by {{agent}}s to enroll to {{fleet}}.

::::


1. In {{kib}}, open **{{fleet}} → Settings** and ensure the **Elasticsearch output** that will be used by the {{fleet-server}} policy is correctly configured, paying special attention that:

    * The **hosts** field includes a valid URL that will be reachable by the {{fleet-server}} Pod(s).
    * If your {{es}} cluster uses certificates signed by private or intermediate CAs not publicly trusted, you have added the trust information in the **Elasticsearch CA trusted fingerprint** field or in the **advanced configuration** section through the `ssl.certificate_authorities` setting. For an example, refer to [Secure Connections](/reference/ingestion-tools/fleet/secure-connections.md#_encrypt_traffic_between_agents_fleet_server_and_es) documentation.

        ::::{important}
        This validation step is critical. The {{es}} host URL and CA information has to be added **in both the {{es}} output and the environment variables** provided to the {{fleet-server}}. It’s a common mistake to ignore the output settings believing that the environment variables will prevail, when the environment variables are only used during the bootstrap of the {{fleet-server}}.

        If the URL that {{fleet-server}} will use to access {{es}} is different from the {{es}} URL used by other clients, you may want to create a dedicated **{{es}} output** for {{fleet-server}}.

        ::::

2. Go to **{{fleet}} → Agent Policies** and select **Create agent policy** to create a policy for the {{fleet-server}}:

    * Set a **name** for the policy, for example `Fleet Server Policy Kubernetes`.
    * Do **not** select the option **Collect system logs and metrics**. This option adds the System integration to the {{agent}} policy. Because {{fleet-server}} will run as a Kubernetes Pod without any visibility to the Kubernetes node, there won’t be a system to monitor.
    * Select the **output** that the {{fleet-server}} needs to use to contact {{es}}. This should be the output that you verified in the previous step.
    * Optionally, you can set the **inactivity timeout** and **inactive agent unenrollment timeout** parameters to automatically unenroll and invalidate API keys after the {{fleet-server}} agents become inactive. This is especially useful in Kubernetes environments, where {{fleet-server}} Pods are ephemeral, and new {{agent}}s appear in {{fleet}} UI after Pod recreations.

3. Open the created policy, and from the **Integrations** tab select **Add integration**:

    * Search for and select the {{fleet-server}} integration.
    * Select **Add {{fleet-server}}** to add the integration to the {{agent}} policy.

        At this point you can configure the integration settings per [{{fleet-server}} scalability](/reference/ingestion-tools/fleet/fleet-server-scalability.md).

    * When done, select **Save and continue**. Do not add an {{agent}} at this stage.

4. Open the configured policy, which now includes the {{fleet-server}} integration, and select **Actions** → **Add {{fleet-server}}**. In the next dialog:

    * Confirm that the **policy for {{fleet-server}}** is properly selected.
    * **Choose a deployment mode for security**:

        * If you select **Quick start**, the {{fleet-server}} generates a self-signed TLS certificate, and subsequent agents should be enrolled using the `--insecure` flag.
        * If you select **Production**, you provide a TLS certificate, key and CA to the {{fleet-server}} during the deployment, and subsequent agents will need to trust the certificate’s CA.

    * Add your **{{fleet-server}} Host** information. This is the URL that clients ({{agent}}s) will use to connect to the {{fleet-server}}:

        * In **Production** mode, the {{fleet-server}} certificate must include the hostname part of the URL as an `x509 SAN`, and the {{fleet-server}} itself will need to access that URL during its bootstrap process.
        * On Kubernetes environments this could be the name of the `Kubernetes service` or reverse proxy that exposes the {{fleet-server}} Pods.
        * In the provided example we use `https://fleet-svc.<namespace>` as the URL, which corresponds to the Kubernetes service DNS resolution.

    * Select **generate service token** to create a token for the {{fleet-server}}.
    * From **Install {{fleet-server}} to a centralized host → Linux**, take note of the values of the following settings that will be needed for the {{fleet-server}} installation:

        * Service token(specified by `--fleet-server-service-token` parameter).
        * {{fleet}} policy ID (specified by `--fleet-server-policy` parameter).
        * {{es}} URL (specified by `--fleet-server-es` parameter).

5. Keep the {{kib}} browser window open and continue with the [{{fleet-server}} installation](#add-fleet-server-kubernetes-install).

    When the {{fleet-server}} installation has succeeded, the **Confirm Connection** UI will show a **Connected** status.



### {{fleet-server}} installation [add-fleet-server-kubernetes-install]


#### Installation overview [add-fleet-server-kubernetes-install-overview]

To deploy {{fleet-server}} on Kubernetes and enroll it into {{fleet}} you need the following details:

* **Policy ID** of the {{fleet}} policy configured with the {{fleet-server}} integration.
* **Service token**, that you can generate following the [{{fleet}} preparations](#add-fleet-server-kubernetes-preparations) or manually using the [{{es}}-service-tokens command](elasticsearch://docs/reference/elasticsearch/command-line-tools/service-tokens-command.md).
* **{{es}} endpoint URL**, configured in both the {{es}} output associated to the policy and in the Fleet Server as an environment variable.
* **{{es}} CA certificate file**, configured in both the {{es}} output associated to the policy and in the Fleet Server.
* {{fleet-server}} **certificate and key** (for **Production** deployment mode only).
* {{fleet-server}} **CA certificate file** (for **Production** deployment mode only).
* {{fleet-server}} URL (for **Production** deployment mode only).

If you followed the [{{fleet-server}} and SSL/TLS certificates considerations](#add-fleet-server-kubernetes-cert-prereq) and [{{fleet}} preparations](#add-fleet-server-kubernetes-preparations) you should have everything ready to proceed with the {{fleet-server}} installation.

The suggested deployment method for the {{fleet-server}} consists of:

* A Kubernetes Deployment manifest that relies on two Secrets for its configuration:

    * A Secret named `fleet-server-config` with the main configuration parameters, such as the service token, the {{es}} URL and the policy ID.
    * A Secret named `fleet-server-ssl` with all needed certificate files and the {{fleet-server}} URL.

* A Kubernetes ClusterIP Service named `fleet-svc` that exposes the {{fleet-server}} on port 443, making it available at URLs like `https://fleet-svc`, `https://fleet-svc.<namespace>` and `https://fleet-svc.<namespace>.svc`.

Adapt and change the suggested manifests and deployment strategy to your needs, ensuring you feed the {{fleet-server}} with the needed configuration and certificates. For example, you can customize:

* CPU and memory `requests` and `limits`. Refer to [{{fleet-server}} scalability](/reference/ingestion-tools/fleet/fleet-server-scalability.md) for more information about {{fleet-server}} resources utilization.
* Scheduling configuration, such as `affinity rules` or `tolerations`, if needed in your environment.
* Number of replicas, to scale the Fleet Server horizontally.
* Use an {{es}} CA fingerprint instead of a CA file.
* Configure other [Environment variables](/reference/ingestion-tools/fleet/agent-environment-variables.md).


#### Installation Steps [add-fleet-server-kubernetes-install-steps]

1. Create the Secret for the {{fleet-server}} configuration.

    ```shell
    kubectl create secret generic fleet-server-config \
    --from-literal=elastic_endpoint='<ELASTICSEARCH_HOST_URL>' \
    --from-literal=elastic_service_token='<SERVICE_TOKEN>' \
    --from-literal=fleet_policy_id='<POLICY_ID>'
    ```

    When running the command, substitute the following values:

    * `<ELASTICSEARCH_HOST_URL>`: Replace this with the URL of your {{es}} host, for example `'https://monitoring-es-http.default.svc:9200'`.
    * `<SERVICE_TOKEN>`: Use the service token provided by {{kib}} in the {{fleet}} UI.
    * `<POLICY_ID>`: Replace this with the ID of the created policy, for example `'dee949ac-403c-4c83-a489-0122281e4253'`.

    If you prefer to obtain a **yaml manifest** of the Secret to create, append `--dry-run=client -o=yaml` to the command and save the output to a file.

2. Create the Secret for the TLS/SSL configuration:

    ::::{tab-set}

    :::{tab-item} Quick start

    The following command assumes you have the {{es}} CA available as a local file.

    ```shell
    kubectl create secret generic fleet-server-ssl \
      --from-file=es-ca.crt=<PATH_TO_ES_CA_CERT_FILE>
    ```

    When running the command, substitute the following values:

    * `<PATH_TO_ES_CA_CERT_FILE>` with your local file containing the {{es}} CA(s).

    If you prefer to obtain a **yaml manifest** of the Secret to create, append `--dry-run=client -o=yaml` to the command and save the output to a file.
    :::

    :::{tab-item} Production
    The following command assumes you have the {{es}} CA and the {{fleet-server}} certificate, key and CA available as local files.

    ```shell
    kubectl create secret generic fleet-server-ssl \
      --from-file=es-ca.crt=<PATH_TO_ES_CA_CERT_FILE> \
      --from-file=fleet-ca.crt=<PATH_TO_FLEET_CA_CERT_FILE> \
      --from-file=fleet-server.crt=<PATH_TO_FLEET_SERVER_CERT> \
      --from-file=fleet-server.key=<PATH_TO_FLEET_SERVER_CERT_KEY> \
      --from-literal=fleet_url='<FLEET_URL>'
    ```

    When running the command, substitute the following values:

    * `<PATH_TO_ES_CA_CERT_FILE>` with your local file containing the {{es}} CA(s).
    * `<PATH_TO_FLEET_CA_CERT_FILE>` with your local file containing the {{fleet-server}} CA.
    * `<PATH_TO_FLEET_SERVER_CERT>` with your local file containing the server TLS certificate for the {{fleet-server}}.
    * `<PATH_TO_FLEET_SERVER_CERT_KEY>` with your local file containing the server TLS key for the {{fleet-server}}.
    * `<FLEET_URL>` with the URL that points to the {{fleet-server}}, for example `https://fleet-svc`. This URL will be used by the {{fleet-server}} during its bootstrap, and its hostname must be included in the server certificate’s x509 Subject Alternative Name (SAN) list.

    If you prefer to obtain a **yaml manifest** of the Secret to create, append `--dry-run=client -o=yaml` to the command and save the output to a file.
    :::

    ::::

    If your {{es}} cluster runs on Elastic Cloud or if it uses a publicly trusted CA, remove the `es-ca.crt` key from the proposed secret.

3. Save the proposed Deployment manifest locally, for example as `fleet-server-dep.yaml`, and adapt it to your needs:

    ::::{tab-set}

    :::{tab-item} Production

    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: fleet-svc
    spec:
      type: ClusterIP
      selector:
        app: fleet-server
      ports:
      - port: 443
        protocol: TCP
        targetPort: 8220
    ---
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: fleet-server
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: fleet-server
      template:
        metadata:
          labels:
            app: fleet-server
        spec:
          automountServiceAccountToken: false
          containers:
          - name: elastic-agent
            image: docker.elastic.co/beats/elastic-agent:9.0.0-beta1
            env:
              - name: FLEET_SERVER_ENABLE
                value: "true"
              - name: FLEET_SERVER_ELASTICSEARCH_HOST
                valueFrom:
                  secretKeyRef:
                    name: fleet-server-config
                    key: elastic_endpoint
              - name: FLEET_SERVER_SERVICE_TOKEN
                valueFrom:
                  secretKeyRef:
                    name: fleet-server-config
                    key: elastic_service_token
              - name: FLEET_SERVER_POLICY_ID
                valueFrom:
                  secretKeyRef:
                    name: fleet-server-config
                    key: fleet_policy_id
              - name: ELASTICSEARCH_CA
                value: /mnt/certs/es-ca.crt
              - name: FLEET_SERVER_CERT
                value: /mnt/certs/fleet-server.crt
              - name: FLEET_SERVER_CERT_KEY
                value: /mnt/certs/fleet-server.key
              - name: FLEET_CA
                value: /mnt/certs/fleet-ca.crt
              - name: FLEET_URL
                valueFrom:
                  secretKeyRef:
                    name: fleet-server-ssl
                    key: fleet_url
              - name: FLEET_SERVER_TIMEOUT
                value: '60s'
              - name: FLEET_SERVER_PORT
                value: '8220'
            ports:
            - containerPort: 8220
              protocol: TCP
            resources: {}
            volumeMounts:
            - name: certs
              mountPath: /mnt/certs
              readOnly: true
          volumes:
          - name: certs
            secret:
              defaultMode: 420
              optional: false
              secretName: fleet-server-ssl
    ```
    :::

    :::{tab-item} Quick start

    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: fleet-svc
    spec:
      type: ClusterIP
      selector:
        app: fleet-server
      ports:
      - port: 443
        protocol: TCP
        targetPort: 8220
    ---
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: fleet-server
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: fleet-server
      template:
        metadata:
          labels:
            app: fleet-server
        spec:
          automountServiceAccountToken: false
          containers:
          - name: elastic-agent
            image: docker.elastic.co/beats/elastic-agent:9.0.0-beta1
            env:
              - name: FLEET_SERVER_ENABLE
                value: "true"
              - name: FLEET_SERVER_ELASTICSEARCH_HOST
                valueFrom:
                  secretKeyRef:
                    name: fleet-server-config
                    key: elastic_endpoint
              - name: FLEET_SERVER_SERVICE_TOKEN
                valueFrom:
                  secretKeyRef:
                    name: fleet-server-config
                    key: elastic_service_token
              - name: FLEET_SERVER_POLICY_ID
                valueFrom:
                  secretKeyRef:
                    name: fleet-server-config
                    key: fleet_policy_id
              - name: ELASTICSEARCH_CA
                value: /mnt/certs/es-ca.crt
            ports:
            - containerPort: 8220
              protocol: TCP
            resources: {}
            volumeMounts:
            - name: certs
              mountPath: /mnt/certs
              readOnly: true
          volumes:
          - name: certs
            secret:
              defaultMode: 420
              optional: false
              secretName: fleet-server-ssl
    ```
    :::

    ::::

    Manifest considerations:

    * If your {{es}} cluster runs on Elastic Cloud or if it uses a publicly trusted CA, remove the `ELASTICSEARCH_CA` environment variable from the manifest.
    * Check the `image` version to ensure its aligned with the rest of your {{stack}}.
    * Keep `automountServiceAccountToken` set to `false` to disable the [Kubernetes Provider](/reference/ingestion-tools/fleet/kubernetes-provider.md).
    * Consider configuring requests and limits always as a best practice. Refer to [{{fleet-server}} scalability](/reference/ingestion-tools/fleet/fleet-server-scalability.md) for more information about resources utilization of the {{fleet-server}}.
    * You can change the listening `port` of the service to any port of your choice, but do not change the `targetPort`, as the {{fleet-server}} Pods will listen on port 8220.
    * If you want to expose the {{fleet-server}} externally, consider changing the service type to `LoadBalancer`.

4. Deploy the configured manifest to create the {{fleet-server}} and service:

    ```shell
    kubectl apply -f fleet-server-dep.yaml
    ```

    ::::{important}
    Ensure the `Service`, the `Deployment` and all the referenced `Secrets` are created in the **same Namespace**.

    ::::

5. Check the {{fleet-server}} Pod logs for errors and confirm in {{kib}} that the {{fleet-server}} agent appears as `Connected` and `Healthy` in **{{kib}} → {{fleet}}**.

    ```shell
    kubectl logs fleet-server-69499449c7-blwjg
    ```

    It can take a couple of minutes for {{fleet-server}} to fully start. If you left the {{kib}} browser window open during [{{fleet}} preparations](#add-fleet-server-kubernetes-preparations) it will show **Connected** when everything has gone well.

    ::::{note}
    In **Production mode**, during {{fleet-server}} bootstrap process, the {{fleet-server}} might be unable to access its own `FLEET_URL`. This is usually a temporary issue caused by the Kubernetes Service not forwarding traffic to the Pod(s).

    If the issue persists consider using `https://localhost:8220` as the `FLEET_URL` for the {{fleet-server}} configuration, and ensure that `localhost` is included in the certificate’s SAN.

    ::::


## Expose the {{fleet-server}} to {{agent}}s [add-fleet-server-kubernetes-expose]

This may include the creation of a Kubernetes `service`, an `ingress` resource, and / or DNS registers for FQDNs resolution. There are multiple ways to expose applications in Kubernetes.

Considerations when exposing {{fleet-server}}:

* If your environment requires the {{fleet-server}} to be reachable through multiple hostnames or URLs, you can create multiple **{{fleet-server}} Hosts** in **{{fleet}} → Settings**, and create different policies for different groups of agents.
* Remember that in **Production** mode, the **hostnames** used to access the {{fleet-server}} must be part of the {{fleet-server}} certificate as `x.509 Subject Alternative Names`.
* **Align always the service listening port to the URL**. If you configure the service to listen in port 8220 use a URL like `https://service-name:8220`, and if it listens in `443` use a URL like `https://service-name`.

Below is an end to end example of how to expose the server to external and internal clients using a LoadBalancer service. For this example we assume the following:

* The {{fleet-server}} runs in a namespace called `elastic`.
* External clients will access {{fleet-server}} using a URL like `https://fleet.example.com`, which will be resolved in DNS to the external IP of the Load Balancer.
* Internal clients will access {{fleet-server}} using the Kubernetes service directly `https://fleet-svc-lb.elastic`.
* The server certificate has both hostnames (`fleet.example.com` and `fleet-svc-lb.elastic`) in its SAN list.

1. Create the `LoadBalancer` Service

    ```shell
    kubectl expose deployment fleet-server --name fleet-svc-lb --type LoadBalancer --port 443 --target-port 8220
    ```

    That command creates a service named `fleet-svc-lb`, listening on port `443` and forwarding the traffic to the `fleet-server` deployment’s Pods on port `8220`. The listening `--port` (and the consequent URL) of the service can be customized, but the `--target-port` must remain on the default port (`8220`), because it’s the port used by the {{fleet-server}} application.

2. Add `https://fleet-server.example.com` and `https://fleet-svc-lb.elastic` as a new **{{fleet-server}} Hosts** in **{{fleet}} → Settings**. Align the port of the URLs if you configured something different from `443` in the Load Balancer.
3. Create a {{fleet}} policy for external clients using the `https://fleet-server.example.com` {{fleet-server}} URL.
4. Create a {{fleet}} policy for internal clients using the `https://fleet-svc-lb.elastic` {{fleet-server}} URL.
5. You are ready now to enroll external and internal agents to the relevant policies. Refer to [Next steps](#add-fleet-server-kubernetes-next) for more details.


## Troubleshoot {{fleet-server}} [add-fleet-server-kubernetes-troubleshoot]


### Common Problems [add-fleet-server-kubernetes-troubleshoot-common]

The following issues may occur when {{fleet-server}} settings are missing or configured incorrectly:

* {{fleet-server}} is trying to access {{es}} at `localhost:9200` even though the `FLEET_SERVER_ELASTICSEARCH_HOST` environment variable is properly set.

    This problem occurs when the `output` of the policy associated to the {{fleet-server}} is not correctly configured.

* TLS certificate trust issues occur even when the `ELASTICSEARCH_CA` environment variable is properly set during deployment.

    This problem occurs when the `output` of the policy associated to the {{fleet-server}} is not correctly configured. Add the **CA certificate** or **CA trusted fingerprint** to the {{es}} output associated to the {{fleet-server}} policy.

* In **Production mode**, {{fleet-server}} enrollment fails due to `FLEET_URL` not being accessible, showing something similar to:

    ```sh
    Starting enrollment to URL: https://fleet-svc/
    1st enrollment attempt failed, retrying enrolling to URL: https://fleet-svc/ with exponential backoff (init 1s, max 10s)
    Error: fail to enroll: fail to execute request to fleet-server: dial tcp 34.118.226.212:443: connect: connection refused
    Error: enrollment failed: exit status 1
    ```

    If the service and URL are correctly configured, this is usually a temporary issue caused by the Kubernetes Service not forwarding traffic to the Pod, and it should be cleared in a couple of restarts.

    As a workaround, consider using `https://localhost:8220` as the `FLEET_URL` for the {{fleet-server}} configuration, and ensure that `localhost` is included in the certificate’s SAN.



## Next steps [add-fleet-server-kubernetes-next]

Now you’re ready to add {{agent}}s to your host systems. To learn how, refer to [Install {{fleet}}-managed {{agent}}s](/reference/ingestion-tools/fleet/install-fleet-managed-elastic-agent.md), or [Run {{agent}} on Kubernetes managed by {{fleet}}](/reference/ingestion-tools/fleet/running-on-kubernetes-managed-by-fleet.md) if your {{agent}}s will also run on Kubernetes.

When you connect {{agent}}s to {{fleet-server}}, remember to use the `--insecure` flag if the **quick start** mode was used, or to provide to the {{agent}}s the CA certificate associated to the {{fleet-server}} certificate if **production** mode was used.
