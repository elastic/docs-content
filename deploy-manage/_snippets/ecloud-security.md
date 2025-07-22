{{ecloud}} has built-in security. For example, HTTPS communications between {{ecloud}} and the internet, as well as inter-node communications, are secured automatically, and cluster data is encrypted at rest.

In both {{ech}} and {{serverless-full}}, you can also configure [IP filters](/deploy-manage/security/ip-filtering-cloud.md) to prevent unauthorized access to your deployments and projects.

In {{ech}}, you can augment these security features in the following ways:
* [Configure private connectivity and apply VPC filtering](/deploy-manage/security/private-connectivity.md) to establish a secure connection for your {{ecloud}} deployments to communicate with other cloud services, and restrict traffic to deployments based on those private connections.
* Encrypt your deployment with a [customer-managed encryption key](/deploy-manage/security/encrypt-deployment-with-customer-managed-encryption-key.md).
* [Secure your settings](/deploy-manage/security/secure-settings.md) using {{es}} and {{kib}} keystores.
* Use the list of [{{ecloud}} static IPs](/deploy-manage/security/elastic-cloud-static-ips.md) to allow or restrict communications in your infrastructure.

{{ech}} doesn't support custom SSL certificates, which means that a custom CNAME for an {{ech}} endpoint such as *mycluster.mycompanyname.com* also is not supported.

Refer to [{{ecloud}} security](https://www.elastic.co/cloud/security) for more details about Elastic security and privacy programs.