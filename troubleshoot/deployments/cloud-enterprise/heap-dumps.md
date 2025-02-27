---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-capture-heap-dumps.html
---

# Heap dumps [ece-capture-heap-dumps]

From the Elastic Cloud Enterprise console you can capture JVM heap dumps from deployment instances. This can aid in debugging memory-related issues. Elastic Cloud Enterprise supports two kinds of heap dumps: out-of-memory and on-demand. Out-of-memory heap dumps are captured when the instance JVM runs out of memory and crashes. On-demand heap dumps can be captured from a running instance at any time.


## Viewing and downloading heap dumps [ece-view-heap-dumps] 

You can view and download captured heap dumps for a given deployment.

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From your deployment menu go to the **Heap dumps** page.

From this page, you can view all heap dumps that have been captured on your deployment and download a heap dump for analysis.

::::{note} 
Only one heap dump is retained per instance.
::::


::::{warning} 
Heap dumps contain the unsanitized contents of the instance’s heap. There are typically secrets and other sensitive data contained in heap dumps, and great care should be taken when handling and sharing them.
::::



## Capturing a new on-demand heap dump [ece-capture-on-demand-heap-dump] 

You can capture an on-demand heap dump from the deployment overview page.

::::{note} 
The JVM will be paused while the heap dump is being captured, so there may be a temporary performance or availability impact. Only one heap dump can be captured from a given instance at a time.
::::


1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From the deployment overview, find the instance you want to capture a heap dump from, select the instance context menu, and choose **Capture heap dump**

Alternatively, you can capture an on-demand heap dump directly from the **Heap dumps** page.

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From your deployment menu, go to the **Heap dumps** page.
4. From the dropdown, choose the instance you want to capture a heap dump from, and select **Start capture**

