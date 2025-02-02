---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-connect.html
---

# Find your endpoint URL [ece-connect]

To connect to your Elasticsearch cluster, you need to look up the the cluster Endpoint URL:

1. [Log into the Cloud UI](log-into-cloud-ui.md), if you aren’t logged in already.
2. On the **Deployments** page, select one of your deployments.
3. Under **Endpoints**, the endpoint link for Elasticsearch is listed. If you already enabled Kibana, the endpoint where you can access Kibana is listed as well. Select the Elasticsearch endpoint to connect to the cluster in your browser. You should get the following standard message:

    ```json
    {
      "name" : "instance-0000000000",
      "cluster_name" : "85943ce00a934471cb971009e73d2d39",
      "cluster_uuid" : "0z2PsOX1TCGSk7PKgB9ajg",
      "version" : {
        "number" : "2.4.1",
        "build_hash" : "c67dc32e24162035d18d6fe1e952c4cbcbe79d16",
        "build_timestamp" : "2016-09-27T18:57:55Z",
        "build_snapshot" : false,
        "lucene_version" : "5.5.2"
      },
      "tagline" : "You Know, for Search"
    }
    ```

    If you are prompted for authentication credentials, you are trying to connect to a cluster that already has Shield enabled or that uses the X-Pack security features. Specify the credentials of a user, such as the default `elastic` user, to connect.


Currently, we support the following ways of connecting to an Elasticsearch cluster:

RESTful API with JSON over HTTP and HTTPS
:   Used by the `curl` command and most programming languages that aren’t Java. To interact with your cluster, use your Elasticsearch cluster endpoint information from the **Overview** page in the Cloud UI. Port 9200 is used for plain text, insecure HTTP connections while port 9243 is used for HTTPS. Using HTTPS is generally recommended, as it is more secure.

    If this is your first time using Elasticsearch, you can try out some `curl` commands to become familiar with the basics. If you’re on an operating system like macOS or Linux, you probably already have the `curl` command installed. For example, to connect to your cluster from the command line over HTTPS with the `curl` command:

    ```sh
    curl --cacert /path/to/elastic-ece-ca-cert.pem https://45e366dc3a4142e9a4d6bbe3c7eedee7.192.168.43.10.ip.es.io:9243
    {
      "name" : "instance-0000000000",
      "cluster_name" : "45e366dc3a4142e9a4d6bbe3c7eedee7",
      "version" : {
        "number" : "2.3.5",
        "build_hash" : "90f439ff60a3c0f497f91663701e64ccd01edbb4",
        "build_timestamp" : "2016-07-27T10:36:52Z",
        "build_snapshot" : false,
        "lucene_version" : "5.5.0"
      },
      "tagline" : "You Know, for Search"
    }
    ```

    To make this `curl` command work with your cluster, you need to replace the endpoint URL with your own.


::::{tip} 
If you created a cluster on Elasticsearch 5.0 or later or if you already enabled the security features, you must include authentication details with the -u parameter. For example: `curl -u elastic:W0UN0Rh9WX8eKeN69grVk3bX https://85943ce00a934471cb971009e73d2d39.us-east-1.aws.found.io:9243`. You can check [Get existing ECE security certificates](../../security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md) for how to get the CA certificate (`elastic-ece-ca-cert.pem` in this example) and use it to connect to the Elasticsearch cluster.
::::


Ingest methods
:   There are several ways to connect to Elasticsearch, perform searches, insert data, and more.  See the [ingesting data](https://www.elastic.co/guide/en/cloud-enterprise/current/ece-cloud-ingest-data.html) documentation.

