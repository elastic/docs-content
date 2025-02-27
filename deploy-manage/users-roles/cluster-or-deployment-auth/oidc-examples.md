---
mapped_urls:
  - https://www.elastic.co/guide/en/cloud/current/ec-securing-clusters-oidc-op.html
navigation_title: With Azure, Google, or Okta
applies_to:
  deployment:
    self:
    ess:
    ece:
    eck:
---

# Set up OpenID Connect with Azure, Google, or Okta [ec-securing-clusters-oidc-op]

This page explains how to implement OIDC, from the OAuth client credentials generation to the realm configuration for Elasticsearch and Kibana, with the following OpenID Connect Providers (OPs):

* [Azure](#ec-securing-oidc-azure)
* [Google](#ec-securing-oidc-google)
* [Okta](#ec-securing-oidc-okta)

For further detail about configuring OIDC, refer to [](/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md)

## Setting up OpenID Connect with Azure [ec-securing-oidc-azure]

Follow these steps to configure OpenID Connect single sign-on on in {{es}} with an Azure OP.

For more information about OpenID connect in Azure, refer to [Azure OAuth 2.0 and OpenID documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-v2-protocols).

1. Configure the OAuth client ID.

    1. Create a new application:

        1. Sign into the [Azure Portal](https://portal.azure.com/) and go to **Entra** (formerly Azure Active Directory). From there, select **App registrations** > **New registration** to register a new application.

            :::{image} ../../../images/cloud-ec-oidc-new-app-azure.png
            :alt: A screenshot of the Azure Owned Applications tab on the New Registration page
            :::

        2. Enter a **Name** for your application, for example `ec-oauth2`.
        3. Select a **Supported Account Type** according to your preferences.
        4. Set the **Redirect URI**. 
            
            It will typically be `<KIBANA_ENDPOINT_URL>/api/security/oidc/callback`, where `<KIBANA_ENDPOINT_URL>` is the base URL for your {{kib}} instance. 

            If you're using {{ech}}, then set this value to `<KIBANA_ENDPOINT_URL>/api/security/oidc/callback`.
        5. Select **Register**.
        6. Confirm that your new **Application (client) ID** appears in the app details.

    2. Create a client ID and secret:

        1. From the application that you created, go to **Certificates & secrets** and create a new secret under **Client secrets** > **New client secret**.

            :::{image} ../../../images/cloud-ec-oidc-oauth-create-credentials-azure.png
            :alt: A screenshot of the Azure Add a Client Secret dialog
            :::

        2. Provide a **Description**, for example `Kibana`.
        3. Select an expiration for the secret.
        4. Select **Add** and copy your newly created client secret for later use.

2. Add your client secret [to the {{es}} keystore](/deploy-manage/security/secure-settings.md).

    For OIDC, the client secret setting name in the keystore should be in the form `xpack.security.authc.realms.oidc.<oidc-realm-name>.rp.client_secret`.

3. Configure Elasticsearch with the OIDC realm.

    To learn more about the available endpoints provided by Microsoft Azure, refer to the **Endpoints** details in the application that you configured.

    :::{image} ../../../images/cloud-ec-oidc-endpoints-azure.png
    :alt: A screenshot of the Azure Endpoints dialog with fields for Display Name
    :::

    To configure Elasticsearch for OIDC, [update your Elasticsearch user settings](../../../deploy-manage/deploy/elastic-cloud/edit-stack-settings.md) with the following configuration:

    ```sh
    xpack:
        security:
        authc:
            realms:
            oidc:
                oidc1:
                order: 2
                rp.client_id: "<Application (client) ID>"
                rp.response_type: "code"
                rp.requested_scopes: ["openid", "email"]
                rp.redirect_uri: "KIBANA_ENDPOINT_URL/api/security/oidc/callback"
                op.issuer: "https://login.microsoftonline.com/<Directory (tenant) ID>/v2.0"
                op.authorization_endpoint: "https://login.microsoftonline.com/<Directory (tenant) ID>/oauth2/v2.0/authorize"
                op.token_endpoint: "https://login.microsoftonline.com/<Directory (tenant) ID>/oauth2/v2.0/token"
                op.userinfo_endpoint: "https://graph.microsoft.com/oidc/userinfo"
                op.endsession_endpoint: "https://login.microsoftonline.com/<Directory (tenant) ID>/oauth2/v2.0/logout"
                rp.post_logout_redirect_uri: "KIBANA_ENDPOINT_URL/logged_out"
                op.jwkset_path: "https://login.microsoftonline.com/<Directory (tenant) ID>/discovery/v2.0/keys"
                claims.principal: email
                claim_patterns.principal: "^([^@]+)@YOUR_DOMAIN\\.TLD$"
    ```

    Where:

    * `<Application (client) ID>` is your Client ID, available in the application details on Azure.
    * `<Directory (tenant) ID>` is your Directory ID, available in the application details on Azure.
    * `KIBANA_ENDPOINT_URL` is your Kibana endpoint.
    * `YOUR_DOMAIN` and `TLD` in the `claim_patterns.principal` regular expression are your organization email domain and top level domain.


    If you're using {{ece}} or {{ech}}, and you're using machine learning or a deployment with hot-warm architecture, you must include this configuration in the user settings section for each node type.

4. Create a role mapping.

    The following role mapping for OIDC restricts access to a specific user `(firstname.lastname)` based on the `claim_patterns.principal` email address. This prevents other users on the same domain from having access to your deployment. You can remove the rule or adjust it at your convenience.

    More details are available in our [Configuring role mappings documentation](/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md#oidc-role-mappings).

    ```json
    POST /_security/role_mapping/oidc_kibana
    {
        "enabled": true,
        "roles": [ "superuser" ],
        "rules" : {
          "all" : [
            {
              "field" : {
                "realm.name" : "oidc1"
              }
            },
            {
              "field" : {
                "username" : [
                  "<firstname.lastname>"
                ]
              }
            }
          ]
        },
        "metadata": { "version": 1 }
    }
    ```

    If you use an email in the `claim_patterns.principal`, you won’t need to add the domain in the role_mapping (for example, `firstname.lastname@your_domain.tld` should be `firstname.lastname`).

5. Configure Kibana with the OIDC realm. [Update your Kibana user settings](../../../deploy-manage/deploy/elastic-cloud/edit-stack-settings.md) with the following configuration:

    ```sh
    xpack.security.authc.providers:
        oidc.oidc1:
        order: 0
        realm: oidc1
        description: "Log in with Azure"
        basic.basic1:
        order: 1
    ```

## Setting up OpenID Connect with Google [ec-securing-oidc-google]

Follow these steps to configure OpenID Connect single sign-on on in {{es}} with a Google OP.

For more information about OpenID connect in Google, refer to [Google OpenID Connect documentation](https://developers.google.com/identity/protocols/oauth2/openid-connect).

1. Configure the OAuth client ID.

    1. Create a new project:

        1. Sign in to the Google Cloud and open the [New Project page](https://console.cloud.google.com/projectcreate). Create a new project.

    2. Create a client ID and secret:

        1. Navigate to the **APIs & Services** and open the [Credentials](https://console.cloud.google.com/apis/credentials) tab to create your OAuth client ID.

            :::{image} ../../../images/cloud-ec-oidc-oauth-create-credentials-google.png
            :alt: A screenshot of the Google  Cloud console Create Credentials dialog with the OAuth client ID field highlighted
            :::

        2. For **Application Type** choose `Web application`.
        3. Choose a **Name** for your OAuth 2 client, for example `ec-oauth2`.
        4. Add an **Authorized redirect URI**.
    
            It will typically be `<KIBANA_ENDPOINT_URL>/api/security/oidc/callback`, where `<KIBANA_ENDPOINT_URL>` is the base URL for your {{kib}} instance. 

            If you're using {{ech}}, then set this value to `<KIBANA_ENDPOINT_URL>/api/security/oidc/callback`.
        5. Select **Create** and copy your client ID and your client secret for later use.

2. Add your client secret [to the {{es}} keystore](/deploy-manage/security/secure-settings.md).

    For OIDC, the client secret setting name in the keystore should be in the form `xpack.security.authc.realms.oidc.<oidc-realm-name>.rp.client_secret`.

3. Configure Elasticsearch with the OIDC realm.

    To learn more about the endpoints provided by Google, refer to this [OpenID configuration](https://accounts.google.com/.well-known/openid-configuration).

    To configure Elasticsearch for OIDC, [update your Elasticsearch user settings](../../../deploy-manage/deploy/elastic-cloud/edit-stack-settings.md) with the following configuration:

    ```sh
    xpack:
        security:
        authc:
            realms:
            oidc:
                oidc1:
                order: 2
                rp.client_id: "YOUR_CLIENT_ID"
                rp.response_type: "code"
                rp.requested_scopes: ["openid", "email"]
                rp.redirect_uri: "<KIBANA_ENDPOINT_URL>/api/security/oidc/callback"
                op.issuer: "https://accounts.google.com"
                op.authorization_endpoint: "https://accounts.google.com/o/oauth2/v2/auth"
                op.token_endpoint: "https://oauth2.googleapis.com/token"
                op.userinfo_endpoint: "https://openidconnect.googleapis.com/v1/userinfo"
                op.jwkset_path: "https://www.googleapis.com/oauth2/v3/certs"
                claims.principal: email
                claim_patterns.principal: "^([^@]+)@YOUR_DOMAIN\\.TLD$"
    ```

    Where:

    * `YOUR_CLIENT_ID` is your Client ID.
    * `<KIBANA_ENDPOINT_URL>/api/security/oidc/callback` is your Kibana endpoint. 
  
        It will typically be `<KIBANA_ENDPOINT_URL>/api/security/oidc/callback`, where `<KIBANA_ENDPOINT_URL>` is the base URL for your {{kib}} instance. 

        If you're using {{ech}}, then set this value to `<KIBANA_ENDPOINT_URL>/api/security/oidc/callback`.
    * `YOUR_DOMAIN` and `TLD` in the `claim_patterns.principal` regular expression are your organization email domain and top level domain.


    If you're using {{ece}} or {{ech}}, and you're using machine learning or a deployment with hot-warm architecture, you must include this configuration in the user settings section for each node type.

1. Create a role mapping.

    The following role mapping for OIDC restricts access to a specific user `(firstname.lastname)` based on the `claim_patterns.principal` email address. This prevents other users on the same domain from having access to your deployment. You can remove the rule or adjust it at your convenience.

    More details are available in our [Configuring role mappings documentation](/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md#oidc-role-mappings).

    ```json
    POST /_security/role_mapping/oidc_kibana
    {
        "enabled": true,
        "roles": [ "superuser" ],
        "rules" : {
          "all" : [
            {
              "field" : {
                "realm.name" : "oidc1"
              }
            },
            {
              "field" : {
                "username" : [
                  "<firstname.lastname>"
                ]
              }
            }
          ]
        },
        "metadata": { "version": 1 }
    }
    ```

    If you use an email in the `claim_patterns.principal`, you won’t need to add the domain in the role_mapping (for example, `firstname.lastname@your_domain.tld` should be `firstname.lastname`).

2. Configure Kibana with the OIDC realm. [Update your Kibana user settings](../../../deploy-manage/deploy/elastic-cloud/edit-stack-settings.md) with the following configuration:

    ```sh
    xpack.security.authc.providers:
        oidc.oidc1:
        order: 0
        realm: oidc1
        description: "Log in with Google"
        basic.basic1:
        order: 1
    ```

## Setting up OpenID Connect with Okta [ec-securing-oidc-okta]

Follow these steps to configure OpenID Connect single sign-on on for {{es}} with an Okta OP.

For more information about OpenID connect in Okta, refer to [Okta OAuth 2.0 documentation](https://developer.okta.com/docs/guides/implement-oauth-for-okta/create-oauth-app/).

1. Configure the OAuth client ID.

    1. Create a new application:

        1. Go to **Applications** > **Add Application**.

            :::{image} ../../../images/cloud-ec-oidc-new-app-okta.png
            :alt: A screenshot of the Get Started tab on the Okta Create A New Application page
            :::

        2. For the **Platform** page settings, select **Web** then **Next**.
        3. In the **Application settings** choose a **Name** for your application, for example `Kibana OIDC`.
        4. Set the **Base URI** to `KIBANA_ENDPOINT_URL`. 
        5. Set the **Login redirect URI**.  
            
            It will typically be `<KIBANA_ENDPOINT_URL>/api/security/oidc/callback`.

            If you're using {{ech}}, then set this value to `<KIBANA_ENDPOINT_URL>/api/security/oidc/callback`.
        6. Set the **Logout redirect URI** as `KIBANA_ENDPOINT_URL/logged_out`.
        7. Choose **Done** and copy your client ID and client secret values for later use.

2. Add your client secret [to the {{es}} keystore](/deploy-manage/security/secure-settings.md).

    For OIDC, the client secret setting name in the keystore should be in the form `xpack.security.authc.realms.oidc.<oidc-realm-name>.rp.client_secret`.

3. Configure Elasticsearch with the OIDC realm.

    To learn more about the available endpoints provided by Okta, refer to the following OpenID configuration: `https://{{yourOktadomain}}/.well-known/openid-configuration`

    To configure Elasticsearch for OIDC, [update your Elasticsearch user settings](../../../deploy-manage/deploy/elastic-cloud/edit-stack-settings.md) with the following configuration:

    ```sh
    xpack:
        security:
        authc:
            realms:
            oidc:
                oidc1:
                order: 2
                rp.client_id: "YOUR_CLIENT_ID"
                rp.response_type: "code"
                rp.requested_scopes: ["openid", "email"]
                rp.redirect_uri: "KIBANA_ENDPOINT_URL/api/security/oidc/callback"
                op.issuer: "https://YOUR_OKTA_DOMAIN"
                op.authorization_endpoint: "https://YOUR_OKTA_DOMAIN/oauth2/v1/authorize"
                op.token_endpoint: "https://YOUR_OKTA_DOMAIN/oauth2/v1/token"
                op.userinfo_endpoint: "https://YOUR_OKTA_DOMAIN/oauth2/v1/userinfo"
                op.endsession_endpoint: "https://YOUR_OKTA_DOMAIN/oauth2/v1/logout"
                op.jwkset_path: "https://YOUR_OKTA_DOMAIN/oauth2/v1/keys"
                claims.principal: email
                claim_patterns.principal: "^([^@]+)@YOUR_DOMAIN\\.TLD$"
    ```

    Where:

    * `YOUR_CLIENT_ID` is the Client ID that you set up in the previous steps.
    * `KIBANA_ENDPOINT_URL` is your Kibana endpoint, available from the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
    * `YOUR_OKTA_DOMAIN` is the URL of your Okta domain shown on your Okta dashboard.
    * `YOUR_DOMAIN` and `TLD` in the `claim_patterns.principal` regular expression are your organization email domain and top level domain.


Remember to add this configuration for each node type in the [User settings](../../../deploy-manage/deploy/elastic-cloud/edit-stack-settings.md) if you use several node types based on your deployment architecture (Dedicated Master, High IO, and/or High Storage).

1. Create a role mapping.

    The following role mapping for OIDC restricts access to a specific user `(firstname.lastname)` based on the `claim_patterns.principal` email address. This prevents other users on the same domain from having access to your deployment. You can remove the rule or adjust it at your convenience.

    More details are available in our [Configuring role mappings documentation](/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md#oidc-role-mappings).

    ```json
    POST /_security/role_mapping/oidc_kibana
    {
        "enabled": true,
        "roles": [ "superuser" ],
        "rules" : {
          "all" : [
            {
              "field" : {
                "realm.name" : "oidc1"
              }
            },
            {
              "field" : {
                "username" : [
                  "<firstname.lastname>"
                ]
              }
            }
          ]
        },
        "metadata": { "version": 1 }
    }
    ```

    If you use an email in the `claim_patterns.principal`, you won’t need to add the domain in the role_mapping (for example, `firstname.lastname@your_domain.tld` should be `firstname.lastname`).

5. Configure {{kib}} with the OIDC realm. [Update your {{kib}} user settings](../../../deploy-manage/deploy/elastic-cloud/edit-stack-settings.md) with the following configuration:

    ```sh
    xpack.security.authc.providers:
        oidc.oidc1:
        order: 0
        realm: oidc1
        description: "Log in with Okta"
        basic.basic1:
        order: 1
    ```