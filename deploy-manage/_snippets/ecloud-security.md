{{ecloud}} has built-in security. For example, HTTPS communications between {{ecloud}} and the internet, as well as inter-node communications, are secured automatically, and cluster data is encrypted at rest.

In {{ech}}, you can augment these security features in the following ways:
* Configure [traffic filtering](/deploy-manage/security/traffic-filtering.md) to prevent unauthorized access to your deployments.
* Encrypt your deployment with a [customer-managed encryption key](/deploy-manage/security/encrypt-deployment-with-customer-managed-encryption-key.md).
* [Secure your settings](/deploy-manage/security/secure-settings.md) using {{es}} and {{kib}} keystores.
* Use the list of [{{ecloud}} static IPs](/deploy-manage/security/elastic-cloud-static-ips.md) to allow or restrict communications in your infrastructure.

{{ech}} doesn't support custom SSL certificates, which means that a custom CNAME for an {{ech}} endpoint such as *mycluster.mycompanyname.com* also is not supported.

Refer to [{{ecloud}} security](https://www.elastic.co/cloud/security) for more details about Elastic security and privacy programs.