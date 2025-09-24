Connection modes determine how a local {{es}} cluster establishes network access to a remote cluster. 


% need to think and decide the next paragraphs of the intro.

% is this too obvious?
If the destination cluster of a remote cluster connection doesn't have network security enabled, all traffic is allowed, hence there's no need to create this type of filter in such case.

% is this too obvious?
If you apply this type of filter to a deployment that didn't have network security enabled, all other traffic will be denied if you don't have other Network Security policies or filters applied to the deployment.

% This maybe to Remote clusters doc and not here we have already mentioned that this only applies to API key based.
::::{note}
When remote clusters are configured using the deprecated TLS certificate based authentication method, there's no need to create this type of filter to allow the connection, as the connection will already be accepted regardless of the destination cluster to have Network Security enabled.
::::

In remote filter creation doc

    % Not sure if we want any of this
    ::::{important}
    Network security filtering for remote cluster traffic from ECE to ECH is not supported. These filters apply only to {{ecloud}} resources, so the values must be {{ecloud}} IDs.

    If you require network security policies in the remote deployment for remote cluster connections coming from ECE, consider configuring the remote clusters with the deprecated [TLS certificate–based authentication model](/deploy-manage/remote-clusters/ece-remote-cluster-ece-ess.md). Traffic with this model is authenticated through mTLS and is not subject to network security filters.

    Refer to [Remote clusters and network security](/deploy-manage/remote-clusters.md#network-security) for more information.
    ::::    



---> Para Remote clusters and network security!!!

## Context

% Maybe better for remote clusters new introduction

With API key–based authentication, remote clusters functionality requires the local cluster (A) to trust the transport SSL certificate presented by the remote cluster server (B). However, when network security (traffic filtering) is enabled on the destination cluster (B), it's also necessary to ensure that traffic to B is allowed. This can be done using either IP-based traffic filters or remote cluster filters.

IP-based traffic filters are not ideal for orchestration systems when allowing traffic for remote cluster functionality, since tracking the source IP address of individual {{es}} instances can be complex.

Remote cluster filters provide a more reliable alternative: they inspect the client’s certificate to extract the `organization_id` and {{es}} `cluster_id` and decide whether to allow the traffic, adding an extra layer of security (mTLS).

% The replacement could simply be:
Traffic filtering for remote clusters incoming connections using API key authentication supports two methods:

* [Filtering by IP addresses and Classless Inter-Domain Routing (CIDR) masks](/deploy-manage/security/ip-filtering.md).
* Filtering by Organization or {{es}} cluster ID with a [Remote cluster type filter](/deploy-manage/security/remote-cluster-filtering.md).


NOT ADDED TO RCS PAGE:

::::{note}
When setting up traffic filters for a remote connection to an {{ece}} environment, you also need to upload the region’s TLS certificate of the local cluster to the {{ece}} environment’s proxy. You can find that region’s TLS certificate in the **Security** page of any deployment of the environment initiating the remote connection. This is regardless of whether you are using API key or TLS Certificates (deprecated) to authenticate remote connections.
::::


::::{important}
Because this type of filter operates at the proxy level, if the local deployments or organizations in the filter belong to a different ECE environment or to ECH, you must add the transport TLS CA certificate of the local environment to the ECE proxy:

* Find the TLS CA certificate in the **Security -> Remote Connections -> CA certificates** section of any deployment of the environment that initiates the remote connection. In {{ecloud}}, each provider and region has its own CA certificate, while in ECE a single CA certificate is used per installation.
    
* To add a CA certificate to the ECE proxy, go to **Platform -> Settings -> TLS certificates** in the UI and update the certificate chain used when configuring your ECE installation. Append the required CA certificates to the end of the chain. The final chain should look like this: `Proxy private key`, `Proxy SSL certificate`, `Proxy CA(s)`, followed by the remaining CAs. For more details, refer to [Add a proxy certificate](/deploy-manage/security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md#ece-tls-proxy).
::::

NOT ADDED FOR THE MOMENT
### Filter types and context

With API key–based authentication, remote clusters functionality requires the local cluster (A) to trust the transport SSL certificate presented by the remote cluster server (B). However, when network security (traffic filtering) is enabled on the destination cluster (B), it's also necessary to ensure that traffic to B is allowed. This can be done using either [IP-based traffic filters](/deploy-manage/security/ip-filtering.md) or [remote cluster filters](/deploy-manage/security/remote-cluster-filtering.md).

* IP-based traffic filters are not ideal for orchestration platforms when allowing traffic for remote clusters functionality, since tracking the source IP address of individual {{es}} instances can be complex.

* Remote cluster filters provide a more reliable alternative: they inspect the client’s certificate to extract the `organization_id` and {{es}} `cluster_id` and decide whether to allow the traffic, adding an extra layer of security (mTLS + API key authentication).


% this could replace the previous if we don't want to give any explanation
% Traffic filtering for remote clusters incoming connections using API key authentication supports two methods:
% 
% * [Filtering by IP addresses and Classless Inter-Domain Routing (CIDR) masks](/deploy-manage/security/ip-filtering.md).
% * Filtering by Organization or {{es}} cluster ID with a [Remote cluster type filter](/deploy-manage/security/remote-cluster-filtering.md).





NO AÑADIDO AUN:

(aqui hay que aclarar que si NO hay NS todo el trafico se permite, y si hay NS todo el trafico se deniega por lo que seria obligatorio añadir una regla.
tambien explicar que IP based is not feasible).

