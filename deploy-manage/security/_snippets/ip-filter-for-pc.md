When a private connection is applied to a deployment or project, you can't use SSO to log in to {{kib}} endpoints that are protected by private connections from the {{ecloud}} console. The connection to the {{kib}} public URL is still available.

As a workaround, you can add an IP filter for ingress traffic with the public IP address or addresses of the hosts that will use SSO through the {{ecloud}} console. You should scope your IP filter to the narrowest possible range: the egress IPs of your corporate VPN gateway, NAT gateway, or specific client machines.

If you don't create an IP filter, you might see an error like `Invalid SAML request` or `Forbidden due to traffic filtering`.

To add an IP filter:

:::{include} /deploy-manage/security/_snippets/network-security-page.md
:::
3. Select **Create policy** > **IP filter**.
4. Select the resource type that the IP filter will be applied to: either hosted deployments or serverless projects.
5. Select the cloud provider and region for the IP filter.
6. Add a meaningful name and description for the IP filter.
7. Under **Access control**, select **Ingress**.
8. Add the public IP address or addresses of the hosts that will use SSO through the {{ecloud}} console.
9. Under **Apply to resources**, associate the IP filter with one or more deployments or projects.
10. Click **Create**.