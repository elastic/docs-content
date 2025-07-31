---
navigation_title: "{{eck}}"
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-snapshots.html
applies_to:
  deployment:
    eck:
products:
  - id: cloud-kubernetes
---

# Manage snapshot repositories in {{eck}} [k8s-snapshots]

Snapshots allow you to back up and restore {{es}} indices, helping protect data from accidental deletion and enabling migration between clusters. In {{eck}} (ECK), you can register snapshot repositories and configure snapshot lifecycle policies to automate backups.

To set up automated snapshots for {{es}} on Kubernetes you have to:

1. Register the snapshot repository with the {{es}} API.
2. Set up a Snapshot Lifecycle Management Policy through [API](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-slm) or the [{{kib}} UI](/deploy-manage/tools/snapshot-and-restore.md)

::::{note}
Support for S3, GCS and Azure repositories is bundled in {{es}} by default from version 8.0. On older versions of {{es}}, or if another snapshot repository plugin should be used, you have to [Install a snapshot repository plugin](#k8s-install-plugin).
::::


For more information on {{es}} snapshots, check [Snapshot and Restore](/deploy-manage/tools/snapshot-and-restore.md) in the {{es}} documentation.

## Configuration examples [k8s_configuration_examples]

What follows is a non-exhaustive list of configuration examples. The first example might be worth reading even if you are targeting a Cloud provider other than GCP as it covers adding snapshot repository credentials to the {{es}} keystore and illustrates the basic workflow of setting up a snapshot repository:

* [Basic snapshot repository setup using GCS as an example](#k8s-basic-snapshot-gcs)

The following examples cover approaches that use Cloud-provider specific means to leverage Kubernetes service accounts to avoid having to configure snapshot repository credentials in {{es}}:

* [Use GKE Workload Identity](#k8s-gke-workload-identiy)
* [Use AWS IAM roles for service accounts (IRSA)](#k8s-iam-service-accounts)
* [Use Azure Workload Identity](#k8s-azure-workload-identity)

The final example illustrates how to configure secure and trusted communication when you

* [Use S3-compatible services](#k8s-s3-compatible)

### Basic snapshot repository setup using GCS as an example [k8s-basic-snapshot-gcs]

#### Configure GCS credentials through the {{es}} keystore [k8s-secure-settings]

The {{es}} GCS repository plugin requires a JSON file that contains service account credentials. These need to be added as secure settings to the {{es}} keystore. For more details, check [Google Cloud Storage Repository](/deploy-manage/tools/snapshot-and-restore/google-cloud-storage-repository.md).

Using ECK, you can automatically inject secure settings into a cluster node by providing them through a secret in the {{es}} Spec.

1. Create a file containing the GCS credentials. For this example, name it `gcs.client.default.credentials_file`. The file name is important as it is reflected in the secure setting.

    ```json
    {
      "type": "service_account",
      "project_id": "your-project-id",
      "private_key_id": "...",
      "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
      "client_email": "service-account-for-your-repository@your-project-id.iam.gserviceaccount.com",
      "client_id": "...",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://accounts.google.com/o/oauth2/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-bucket@your-project-id.iam.gserviceaccount.com"
    }
    ```

2. Create a Kubernetes secret from that file:

    ```sh
    kubectl create secret generic gcs-credentials --from-file=gcs.client.default.credentials_file
    ```

3. Edit the `secureSettings` section of the {{es}} resource:

    ```yaml
    apiVersion: elasticsearch.k8s.elastic.co/v1
    kind: Elasticsearch
    metadata:
      name: elasticsearch-sample
    spec:
      version: 8.16.1
      # Inject secure settings into Elasticsearch nodes from a k8s secret reference
      secureSettings:
      - secretName: gcs-credentials
    ```

    If you haven’t followed these instructions and named your GCS credentials file differently, you can still map it to the expected name now. Check [Secure Settings](../../security/secure-settings.md) for details.

4. Apply the modifications:

    ```bash
    kubectl apply -f elasticsearch.yml
    ```


GCS credentials are automatically propagated into each {{es}} node’s keystore. It can take up to a few minutes, depending on the number of secrets in the keystore. You don’t have to restart the nodes.


#### Register the repository in {{es}} [k8s-create-repository]

1. Create the GCS snapshot repository in {{es}}. You can either use the [Snapshot and Restore UI](/deploy-manage/tools/snapshot-and-restore.md) in {{kib}} version 7.4.0 or higher, or follow the procedure described in [Snapshot and Restore](/deploy-manage/tools/snapshot-and-restore.md):

    ```sh
    PUT /_snapshot/my_gcs_repository
    {
      "type": "gcs",
      "settings": {
        "bucket": "my_bucket",
        "client": "default"
      }
    }
    ```

2. Take a snapshot with the following HTTP request:

    ```sh
    PUT /_snapshot/my_gcs_repository/test-snapshot
    ```




### Use GKE Workload Identity [k8s-gke-workload-identiy]

GKE Workload Identity allows a Kubernetes service account to impersonate a Google Cloud IAM service account and therefore to configure a snapshot repository in {{es}} without storing Google Cloud credentials in {{es}} itself. This feature requires your Kubernetes cluster to run on GKE and your {{es}} cluster to run at least [version 7.13](https://github.com/elastic/elasticsearch/pull/71239) and [version 8.1](https://github.com/elastic/elasticsearch/pull/82974) when using searchable snapshots.

Follow the instructions in the [GKE documentation](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity) to configure workload identity, specifically:

1. Create or update your Kubernetes cluster with `--workload-pool=PROJECT_ID.svc.id.goog` enabled, where `PROJECT_ID` is your Google project ID
2. Create a namespace and a Kubernetes service account (`test-gcs` and `gcs-sa` in this example)
3. Create the bucket, the Google service account (`gcp-sa` in this example. Note that both Google and Kubernetes have the concept of a service account and this example is referring to the former) and set the relevant permissions through Google Cloud console or gcloud CLI
4. Allow the Kubernetes service account to impersonate the Google service account:

    ```sh
    gcloud iam service-accounts add-iam-policy-binding gcp-sa@PROJECT_ID.iam.gserviceaccount.com \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:PROJECT_ID.svc.id.goog[test-gcs/gcs-sa]"
    ```

5. Add the `iam.gke.io/gcp-service-account` annotation on the Kubernetes service account

    ```sh
    kubectl annotate serviceaccount gcs-sa \
        --namespace test-gcs \
        iam.gke.io/gcp-service-account=gcp-sa@PROJECT_ID.iam.gserviceaccount.com
    ```

6. Create an {{es}} cluster, referencing the Kubernetes service account

    ```yaml
    apiVersion: elasticsearch.k8s.elastic.co/v1
    kind: Elasticsearch
    metadata:
      name: elasticsearch-gcs-sample
      namespace: test-gcs
    spec:
      version: 8.16.1
      nodeSets:
      - name: default
        podTemplate:
          spec:
            automountServiceAccountToken: true
            serviceAccountName: gcs-sa
        count: 3
    ```

7. Create the snapshot repository as described in [Register the repository in Elasticsearch](#k8s-create-repository)


### Use AWS IAM roles for service accounts (IRSA) [k8s-iam-service-accounts]

The AWS IAM roles for service accounts feature allows you to give {{es}} restricted access to a S3 bucket without having to expose and store AWS credentials directly in {{es}}. This requires you to run the ECK operator on Amazon’s EKS offering and an [{{es}} cluster running at least version 8.1](https://www.elastic.co/guide/en/elasticsearch/reference/8.1/repository-s3.html#iam-kubernetes-service-accounts).

Follow [the AWS documentation](https://aws.amazon.com/premiumsupport/knowledge-center/eks-restrict-s3-bucket/) to set this feature up. Specifically you need to:

1. Define an IAM policy file, called `iam-policy.json` in this example, giving access to an S3 bucket called `my_bucket`

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "s3:ListBucketMultipartUploads",
                    "s3:ListBucketVersions",
                    "s3:ListBucket",
                    "s3:GetBucketLocation"
                ],
                "Resource": "arn:aws:s3:::my_bucket"
            },
            {
                "Sid": "VisualEditor1",
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject",
                    "s3:GetObject",
                    "s3:AbortMultipartUpload",
                    "s3:DeleteObject",
                    "s3:ListMultipartUploadParts"
                ],
                "Resource": "arn:aws:s3:::my_bucket/*"
            }
        ]
    }
    ```

2. Create the policy using AWS CLI tooling, using the name `eck-snapshots` in this example

    ```sh
    aws iam create-policy \
        --policy-name eck-snapshots \
        --policy-document file://iam-policy.json
    ```

3. Use `eksctl` to create an IAM role and create and annotate a Kubernetes service account with it. The service account is called `aws-sa` in the `default` namespace in this example.

    ```sh
    eksctl create iamserviceaccount \
      --name aws-sa \
      --namespace default \
      --cluster YOUR_CLUSTER \ <1>
      --attach-policy-arn arn:aws:iam::YOUR_IAM_ARN:policy/eck-snapshots \ <2>
      --approve
    ```

    1. Replace `YOUR_CLUSTER` with your actual EKS cluster name
    2. Replace with the actual AWS IAM ARN for the policy you just created

4. Create an {{es}} cluster referencing the service account

    ```yaml
    apiVersion: elasticsearch.k8s.elastic.co/v1
    kind: Elasticsearch
    metadata:
      name: es
    spec:
      version: 8.16.1
      nodeSets:
      - name: default
        count: 3
        podTemplate:
          spec:
            serviceAccountName: aws-sa
            containers:
            - name: elasticsearch
              env:
              - name: AWS_WEB_IDENTITY_TOKEN_FILE
                value: "/usr/share/elasticsearch/config/repository-s3/aws-web-identity-token-file" <1>
              - name: AWS_ROLE_ARN
                value: "arn:aws:iam::YOUR_ROLE_ARN_HERE" <2>
              volumeMounts:
              - name: aws-iam-token
                mountPath: /usr/share/elasticsearch/config/repository-s3
            volumes:
              - name: aws-iam-token
                projected:
                  sources:
                  - serviceAccountToken:
                      audience: sts.amazonaws.com
                      expirationSeconds: 86400
                      path: aws-web-identity-token-file
    ```

    1. {{es}} expects the service account token to be projected to exactly this path
    2. Replace with the actual `AWS_ROLE_ARN` for the IAM role you created in step 3

5. Create the snapshot repository as described in [Register the repository in Elasticsearch](#k8s-create-repository) but of type `s3`

    ```sh
    PUT /_snapshot/my_s3_repository
    {
      "type": "s3",
      "settings": {
        "bucket": "my_bucket"
      }
    }
    ```



### Use Azure Workload Identity [k8s-azure-workload-identity]

Starting with version 8.16 {{es}} supports Azure Workload identity which allows the use of Azure blob storage for {{es}} snapshots without exposing Azure credentials directly to {{es}}.

Follow the [Azure documentation](https://learn.microsoft.com/en-us/azure/aks/workload-identity-deploy-cluster) for setting up workload identity for the first five steps:

1. [Create a resource group](https://learn.microsoft.com/en-us/azure/aks/workload-identity-deploy-cluster#create-a-resource-group), if it does not exist yet.
2. [Create](https://learn.microsoft.com/en-us/azure/aks/workload-identity-deploy-cluster#create-an-aks-cluster) or [update](https://learn.microsoft.com/en-us/azure/aks/workload-identity-deploy-cluster#update-an-existing-aks-cluster) your AKS cluster to enable workload identity.
3. [Retrieve the OIDC issuer URL](https://learn.microsoft.com/en-us/azure/aks/workload-identity-deploy-cluster#retrieve-the-oidc-issuer-url).
4. [Create a managed identity](https://learn.microsoft.com/en-us/azure/aks/workload-identity-deploy-cluster#create-a-managed-identity) and [link it to a Kubernetes service account](https://learn.microsoft.com/en-us/azure/aks/workload-identity-deploy-cluster#create-a-kubernetes-service-account).
5. [Create the federated identity credential](https://learn.microsoft.com/en-us/azure/aks/workload-identity-deploy-cluster#create-the-federated-identity-credential).

    ::::{note}
    The following steps diverge from the tutorial in the Azure documentation. However, variables initialised as part of the Azure tutorial are still assumed to be present.
    ::::

6. Create an Azure storage account, if it does not exist yet.

    ```sh
    az storage account create \
          --name esstorage \
          --resource-group "${RESOURCE_GROUP}" \
          --location "${LOCATION}" \
          --encryption-services blob \
          --sku Standard_ZRS <1>
    ```

    1. This can be any of the supported storage account types `Standard_LRS`, `Standard_ZRS`, `Standard_GRS`, `Standard_RAGRS` but not `Premium_LRS` see [the {{es}} documentation](/deploy-manage/tools/snapshot-and-restore/azure-repository.md) for details.

7. Create a container in the storage account, for this example `es-snapshots`.

    ```sh
    az storage container create \
       --account-name "${STORAGE_ACCOUNT_NAME}" \
       --name es-snapshots --auth-mode login
    ```

8. Create a role assignment between the managed identity and the storage account.

    ```sh
    IDENTITY_PRINCIPAL_ID=$(az identity show \
        --name "${USER_ASSIGNED_IDENTITY_NAME}" \
        --resource-group "${RESOURCE_GROUP}" \
        --query principalId --o tsv)

    STORAGE_SCOPE=$(az storage account show \
      --resource-group "${RESOURCE_GROUP}" \
      --name "${STORAGE_ACCOUNT_NAME}" --query id -o tsv | sed 's#/##') <1>

    az role assignment create \
      --assignee-object-id "${IDENTITY_PRINCIPAL_ID}" \
      --role "Storage Blob Data Contributor" \
      --scope "${STORAGE_SCOPE}"
    ```

    1. The storage account ID needs to be specified as the scope for the role assignment without the leading slash returned by the `az storage account show` command.

9. Create a Kubernetes secret, called `keystore` in this example, with the storage account name. This is necessary to be able to specify the account name as a secure setting in {{es}} in the next step.

    ```sh
    kubectl create secret generic keystore \
      --from-literal=azure.client.default.account=${STORAGE_ACCOUNT_NAME}
    ```

10. Create an {{es}} cluster that uses the Kubernetes service account created earlier.

    ```yaml
    apiVersion: elasticsearch.k8s.elastic.co/v1
    kind: Elasticsearch
    metadata:
      name: az-workload-identity-sample
    spec:
      version: 8.16.0
      secureSettings:
      - secretName: keystore <1>
      nodeSets:
      - name: default
        count: 1
        podTemplate:
          metadata:
            labels:
              azure.workload.identity/use: "true"
          spec:
            serviceAccountName: workload-identity-sa <2>
            containers:
            - name: elasticsearch
              env:
              - name: AZURE_FEDERATED_TOKEN_FILE <3>
                value: /usr/share/elasticsearch/config/azure/tokens/azure-identity-token
              volumeMounts:
              - name: azure-identity-token
                mountPath: /usr/share/elasticsearch/config/azure/tokens <3>
    ```

    1. Specify the Kubernetes secret created in the previous step to configure the Azure storage account name as a secure setting.
    2. This is the service account created earlier in the steps from the [Azure Workload Identity](https://learn.microsoft.com/en-us/azure/aks/workload-identity-deploy-cluster#create-a-kubernetes-service-account) tutorial.
    3. The corresponding volume is injected by the [Azure Workload Identity Mutating Admission Webhook](https://azure.github.io/azure-workload-identity/docs/installation/mutating-admission-webhook.html). For {{es}} to be able to access the token, the mount needs to be in a sub-directory of the {{es}} config directory. The corresponding environment variable needs to be adjusted as well.

11. Create a snapshot repository of type `azure` through the {{es}} API, or through [*{{stack}} configuration policies*](../../deploy/cloud-on-k8s/elastic-stack-configuration-policies.md).

    ```sh
    POST _snapshot/my_azure_repository
    {
      "type": "azure",
      "settings": {
        "container": "es-snapshots"
      }
    }
    ```



### Use S3-compatible services [k8s-s3-compatible]

The following example assumes that you have deployed and configured a S3 compatible object store like [MinIO](https://min.io) that can be reached from the Kubernetes cluster, and also that you have created a bucket in said service, called `es-repo` in this example. The example also assumes an {{es}} cluster named `es` is deployed within the cluster. Most importantly the steps describing how to customize the JVM trust store are only necessary if your S3-compatible service is using TLS certificates that are not issued by a well known certificate authority.

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: es
spec:
  version: 8.16.1
  nodeSets:
  - name: mixed
    count: 3
```

1. Extract the cacerts JVM trust store from one of the running {{es}} nodes.

    ```sh
    kubectl cp es-es-mixed-0:/usr/share/elasticsearch/jdk/lib/security/cacerts cacerts
    ```

    ::::{note}
    You can skip this step if you want to create a new trust store that does not contain any well known CAs that {{es}} trusts by default. Be aware that this limits Elasticsearch’s ability to communicate with TLS secured endpoints to those for which you add CA certificates in the next steps.
    ::::

2. Obtain the CA certificate used to sign the certificate of your S3-compatible service. We assume it is called `tls.crt`
3. Add the certificate to the JVM trust store from step 1

    ```sh
    keytool -importcert -keystore cacerts -storepass changeit -file tls.crt -alias my-custom-s3-svc
    ```

    ::::{note}
    You need to have the Java Runtime environment with the `keytool` installed locally for this step. `changeit` is the default password used by the JVM, but it can be changed with `keytool` as well.
    ::::

4. Create a Kubernetes secret with the amended trust store

    ```sh
    kubectl create secret generic custom-truststore --from-file=cacerts
    ```

5. Create a Kubernetes secret with the credentials for your object store bucket

    ```sh
    kubectl create secret generic snapshot-settings \
       --from-literal=s3.client.default.access_key=$YOUR_ACCESS_KEY \
       --from-literal=s3.client.default.secret_key=$YOUR_SECRET_ACCESS_KEY
    ```

6. Update your {{es}} cluster to use the trust store and credentials from the Kubernetes secrets

    ```yaml
    apiVersion: elasticsearch.k8s.elastic.co/v1
    kind: Elasticsearch
    metadata:
      name: es
    spec:
      version: 8.16.1
      secureSettings:
      - secretName: snapshot-settings
      nodeSets:
      - name: mixed
        count: 3
        podTemplate:
          spec:
            volumes:
            - name: custom-truststore
              secret:
                secretName: custom-truststore
            containers:
            - name: elasticsearch
              volumeMounts:
              - name: custom-truststore
                mountPath: /usr/share/elasticsearch/config/custom-truststore
              env:
              - name: ES_JAVA_OPTS
                value: "-Djavax.net.ssl.trustStore=/usr/share/elasticsearch/config/custom-truststore/cacerts -Djavax.net.ssl.keyStorePassword=changeit"
    ```

7. Create the snapshot repository

    ```sh
    POST _snapshot/my_s3_repository
    {
      "type": "s3",
      "settings": {
        "bucket": "es-repo",
        "path_style_access": true,	<1>
        "endpoint": "<my-s3service-url>.default.svc.cluster.local/" <2>
      }
    }
    ```

    1. Whether or not you need to enable `path_style_access` depends on your choice of S3-compatible storage service and how it is deployed. If it is exposed through a standard Kubernetes service it is likely you need this option
    2. Replace this with the actual endpoint of your S3-compatible service



### Install a snapshot repository plugin [k8s-install-plugin]

If you are running a version of {{es}} before 8.0 or you need a snapshot repository plugin that is not already pre-installed you have to install the plugin yourself. To install the snapshot repository plugin, you can either use a [custom image](../../deploy/cloud-on-k8s/create-custom-images.md) or [add your own init container](../../deploy/cloud-on-k8s/init-containers-for-plugin-downloads.md) which installs the plugin when the Pod is created.

To use your own custom image with all necessary plugins pre-installed, use an {{es}} resource like the following:

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch-sample
spec:
  version: 8.16.1
  image: your/custom/image:tag
  nodeSets:
  - name: default
    count: 1
```

Alternatively, install the plugin when the Pod is created by using an init container:

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch-sample
spec:
  version: 8.16.1
  nodeSets:
  - name: default
    count: 1
    podTemplate:
      spec:
        initContainers:
        - name: install-plugins
          command:
          - sh
          - -c
          - |
            bin/elasticsearch-plugin remove --purge repository-gcs
            bin/elasticsearch-plugin install --batch repository-gcs
```

Assuming you stored this in a file called `elasticsearch.yaml` you can in both cases create the {{es}} cluster with:

```sh
kubectl apply -f elasticsearch.yaml
```



