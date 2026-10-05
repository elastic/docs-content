1. In the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), select **Serverless**.
2. Find your project and select **Manage**.
3. Under **Application endpoints, cluster and component IDs**, select **{{es}}**.
4. Copy the **Endpoint** value.

    :::{image} /solutions/images/cloud-console-serverless-endpoint.png
    :alt: The Elasticsearch panel on a Serverless project page in the Elastic Cloud Console, showing the Endpoint and AWS PrivateLink endpoint values with copy buttons
    :screenshot:
    :width: 50%
    :::

If your project runs on AWS, the panel also lists an **AWS PrivateLink endpoint**. Use it only when you connect through AWS PrivateLink. To learn more, refer to [](/deploy-manage/security/private-connectivity-aws.md).
