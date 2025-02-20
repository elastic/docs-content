---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/saml-realm.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece_sign_outgoing_saml_message.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece_optional_settings.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-securing-clusters-SAML.html
  - https://www.elastic.co/guide/en/cloud/current/ec-securing-clusters-SAML.html
  - https://www.elastic.co/guide/en/cloud/current/ec-sign-outgoing-saml-message.html
  - https://www.elastic.co/guide/en/cloud/current/ec-securing-clusters-saml-azure.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-securing-clusters-SAML.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/echsign-outgoing-saml-message.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-saml-authentication.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/saml-guide-stack.html
---

# SAML

% What needs to be done: Refine

% GitHub issue: https://github.com/elastic/docs-projects/issues/347

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/saml-realm.md
% - [ ] ./raw-migrated-files/cloud/cloud-enterprise/ece_sign_outgoing_saml_message.md
% - [ ] ./raw-migrated-files/cloud/cloud-enterprise/ece_optional_settings.md
% - [ ] ./raw-migrated-files/cloud/cloud-enterprise/ece-securing-clusters-SAML.md
% - [ ] ./raw-migrated-files/cloud/cloud/ec-securing-clusters-SAML.md
% - [ ] ./raw-migrated-files/cloud/cloud/ec-sign-outgoing-saml-message.md
% - [ ] ./raw-migrated-files/cloud/cloud/ec-securing-clusters-saml-azure.md
% - [ ] ./raw-migrated-files/cloud/cloud-heroku/ech-securing-clusters-SAML.md
% - [ ] ./raw-migrated-files/cloud/cloud-heroku/echsign-outgoing-saml-message.md
% - [ ] ./raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-saml-authentication.md
% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/saml-guide-stack.md
%      Notes: some steps not needed for cloud / don't work needs clarification that there is an orch level

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):

$$$saml-create-realm$$$

$$$saml-attributes-mapping$$$

$$$saml-attribute-mapping-nameid$$$

$$$saml-kibana-basic$$$

$$$ec-securing-clusters-saml-azure-kibana$$$

$$$ec-securing-clusters-saml-azure-enterprise-search$$$

$$$saml-role-mapping$$$

$$$saml-configure-kibana$$$

$$$saml-logout$$$

$$$saml-enable-http$$$

$$$saml-enable-token$$$

$$$saml-es-user-properties$$$

$$$saml-enc-sign$$$

$$$saml-user-metadata$$$

$$$saml-elasticsearch-authentication$$$

$$$saml-no-kibana-sp-init-sso$$$

$$$req-authn-context$$$

**This page is a work in progress.** The documentation team is working to combine content pulled from the following pages:

* [/raw-migrated-files/elasticsearch/elasticsearch-reference/saml-realm.md](/raw-migrated-files/elasticsearch/elasticsearch-reference/saml-realm.md)
* [/raw-migrated-files/cloud/cloud-enterprise/ece_sign_outgoing_saml_message.md](/raw-migrated-files/cloud/cloud-enterprise/ece_sign_outgoing_saml_message.md)
* [/raw-migrated-files/cloud/cloud-enterprise/ece_optional_settings.md](/raw-migrated-files/cloud/cloud-enterprise/ece_optional_settings.md)
* [/raw-migrated-files/cloud/cloud-enterprise/ece-securing-clusters-SAML.md](/raw-migrated-files/cloud/cloud-enterprise/ece-securing-clusters-SAML.md)
* [/raw-migrated-files/cloud/cloud/ec-securing-clusters-SAML.md](/raw-migrated-files/cloud/cloud/ec-securing-clusters-SAML.md)
* [/raw-migrated-files/cloud/cloud/ec-sign-outgoing-saml-message.md](/raw-migrated-files/cloud/cloud/ec-sign-outgoing-saml-message.md)
* [/raw-migrated-files/cloud/cloud/ec-securing-clusters-saml-azure.md](/raw-migrated-files/cloud/cloud/ec-securing-clusters-saml-azure.md)
* [/raw-migrated-files/cloud/cloud-heroku/ech-securing-clusters-SAML.md](/raw-migrated-files/cloud/cloud-heroku/ech-securing-clusters-SAML.md)
* [/raw-migrated-files/cloud/cloud-heroku/echsign-outgoing-saml-message.md](/raw-migrated-files/cloud/cloud-heroku/echsign-outgoing-saml-message.md)
* [/raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-saml-authentication.md](/raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-saml-authentication.md)
* [/raw-migrated-files/elasticsearch/elasticsearch-reference/saml-guide-stack.md](/raw-migrated-files/elasticsearch/elasticsearch-reference/saml-guide-stack.md)