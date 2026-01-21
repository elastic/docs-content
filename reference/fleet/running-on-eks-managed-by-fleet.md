---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/running-on-eks-managed-by-fleet.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Configure Elastic Agent Add-On on Amazon EKS[configure-elastic-agent-on-eks]

Amazon EKS (Elastic Kubernetes Service) is a managed service that allows you to use Kubernetes on AWS without installing and operating your Kubernetes infrastructure.

Follow these steps to configure the Elastic Agent Add-On on Amazon EKS.

## What you need [_what_you_need]

* An existing Amazon EKS cluster. To deploy one, see [Create an Amazon EKS cluster](https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html).
* {{es}} for storing and searching your data, and {{kib}} for visualizing and managing it.

  ::::{tab-set}

  :::{tab-item} {{ech}}

  To get started quickly, spin up an [{{ech}}](https://www.elastic.co/cloud/elasticsearch-service) deployment. {{ech}} is available on AWS, GCP, and Azure. [Try it out for free](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
  :::

  :::{tab-item} Self-managed

  To install and run {{es}} and {{kib}}, see [Installing the {{stack}}](/deploy-manage/deploy/self-managed/installing-elasticsearch.md).
  :::

  ::::

### Step 1: Create the Node group

You can create a managed node group with either of the following:

*  [eksctl](https://docs.aws.amazon.com/eks/latest/userguide/create-managed-node-group.html#eksctl_create_managed_nodegroup)
*  [AWS Management Console](https://docs.aws.amazon.com/eks/latest/userguide/create-managed-node-group.html#console_create_managed_nodegroup)

### Step 2: Select the Elastic Agent Add-On

To see all available add-ons, check the [AWS Add-ons](https://docs.aws.amazon.com/eks/latest/userguide/workloads-add-ons-available-eks.html). You can also view the most current list of available add-ons using `eksctl`, the AWS Management Console, or the AWS CLI.

### Step 3: Configure Elastic Agent Add-On

1. Choose the version of Elastic Agent desired.
2. Get the URL and enrollment token from the cluster the Elastic Agent needs to register to.
3. From the Elastic Agent EKS add-on, go to **Configuration values** to enter the relevant URL and token values from your cluster.

```
agent:
	    fleet:
            enabled: true
            url: <insert url from onboarding>
            token: <insert enrollment token from onboarding>
```
Make sure  the configuration override is selected in case there are conflicts.

### Step 4: Review and create

Review the data and add the Elastic Agent EKS add-on to your cluster.

Once created, you can see the Elastic Agent Add-on is **Active** on the AWS EKS console.
Elastic Agent runs as a daemonset, so it is present on each node.

### Step 5: View your data in {{kib}} [_step_6_view_your_data_in_kib]

When the Elastic Agent is Active, it appears in Fleet and its configuration is downloaded.

1. Launch {{kib}}:

    ::::{tab-set}

    :::{tab-item} {{ech}}

    1. [Log in](https://cloud.elastic.co/) to your {{ecloud}} account.
    2. Navigate to the {{kib}} endpoint in your deployment.
    :::

    :::{tab-item} Self-managed

    Point your browser to [http://localhost:5601](http://localhost:5601), replacing `localhost` with the name of the {{kib}} host.

    :::

    ::::

2. To check if your {{agent}} is enrolled in {{fleet}}, go to **Management → {{fleet}} → Agents**.

:::{image} images/elastic-agent-fleet.png
:alt: {{agent}}s {{fleet}} page
:screenshot:
:::

## Important notes: [_important_notes_3]

On managed Kubernetes solutions like EKS, {{agent}} has no access to several data sources. Find below the list of the non available data:

1. Metrics from [Kubernetes control plane](https://kubernetes.io/docs/concepts/overview/components/#control-plane-components) components are not available. Consequently metrics are not available for `kube-scheduler` and `kube-controller-manager` components. In this regard, the respective **dashboards** will not be populated with data.
2. **Audit logs** are available only on Kubernetes master nodes as well, hence cannot be collected by {{agent}}.
3. Fields `orchestrator.cluster.name` and `orchestrator.cluster.url` are not populated. `orchestrator.cluster.name` field is used as a cluster selector for default Kubernetes dashboards, shipped with [Kubernetes integration](integration-docs://reference/kubernetes/index.md).

    In this regard, you can use [`add_fields` processor](beats://reference/filebeat/add-fields.md) to add `orchestrator.cluster.name` and `orchestrator.cluster.url` fields for each [Kubernetes integration](integration-docs://reference/kubernetes/index.md)'s component:

    ```yaml
    - add_fields:
        target: orchestrator.cluster
        fields:
          name: clusterName
          url: clusterURL
    ```
