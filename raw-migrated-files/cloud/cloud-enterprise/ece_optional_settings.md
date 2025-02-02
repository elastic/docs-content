# Optional settings [ece_optional_settings]

The following optional realm settings are supported:

* `force_authn` Specifies whether to set the `ForceAuthn` attribute when requesting that the IdP authenticate the current user. If set to `true`, the IdP is required to verify the user’s identity, irrespective of any existing sessions they might have. Defaults to `false`.
* `idp.use_single_logout` Indicates whether to utilise the Identity Provider’s `<SingleLogoutService>` (if one exists in the IdP metadata file). Defaults to `true`.

After completing these steps, you can log in to Kibana by authenticating against your SAML IdP. If you encounter any issues with the configuration, refer to the [SAML troubleshooting page](https://www.elastic.co/guide/en/elasticsearch/reference/current/trb-security-saml.html) which contains information about common issues and suggestions for their resolution.

