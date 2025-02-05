---
navigation_title: "ECE orchestrator"
applies:
  ece: all
---

# Elastic Cloud Enterprise orchestrator users

Control access to your {{ece}} [orchestrator](/deploy-manage/deploy/cloud-enterprise/deploy-an-orchestrator.md) and deployments. 

* [Manage passwords for default users](/deploy-manage/users-roles/cloud-enterprise-orchestrator/manage-system-passwords.html)
* [Manage orchestrator users and roles](/deploy-manage/users-roles/cloud-enterprise-orchestrator/manage-users-roles.html):
  * [Using native users](/deploy-manage/users-roles/cloud-enterprise-orchestrator/native-user-authentication.html)
  * By integrating with external authentication providers:
    * [Active Directory](/deploy-manage/users-roles/cloud-enterprise-orchestrator/active-directory.html)
    * [LDAP](/deploy-manage/users-roles/cloud-enterprise-orchestrator/ldap.html)
    * [SAML](/deploy-manage/users-roles/cloud-enterprise-orchestrator/saml.html)
* [Configure single sign-on to deployments](/deploy-manage/users-roles/cloud-enterprise-orchestrator/configure-sso-for-deployments.html) for orchestrator users

  ::::{tip}
  For {{ece}} deployments, you can configure SSO at the orchestrator level, the deployment level, or both.
  ::::

{{ece}} deployments can also use [cluster-level authentication and authorization](/deploy-manage/users-roles/cluster-or-deployment-auth.md).