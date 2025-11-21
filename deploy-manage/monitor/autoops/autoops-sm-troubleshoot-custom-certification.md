---
applies_to:
  deployment:
    self:
    ece:
    eck:
navigation_title: Troubleshooting
products:
  - id: cloud-kubernetes
  - id: cloud-enterprise
---

# AutoOps for self-managed clusters troubleshooting

If {{agent}} is failing to connect to your self-managed cluster because it doesn't recognize your SSL certificate, this may be because your certificate is signed by a custom or internal Certificate Authority (CA). You may encounter an error similar to the following:

```sh
... x509: certificate signed by unknown authority ...
```

{{agent}} fails to connect to your self-managed cluster because the agent's host machine, the machine where you have installed the agent, does not natively trust your custom or internal CA. To fix this problem,  