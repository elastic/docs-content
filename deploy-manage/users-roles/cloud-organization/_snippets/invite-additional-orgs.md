Because users are managed at the organization level, you must [invite users](/deploy-manage/users-roles/cloud-organization/manage-users.md#ec-invite-users) from within the organization that you want them to join. You can't invite users to join multiple organizations at once.

If a user already has an {{ecloud}} account, then they don't need to sign up again. Instead, they can log in with their selected login method. 

If your organization uses [SAML SSO](/deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md), then you don't need to invite users to join the organization. Users are added to the organization automatically when they log in to your identity provider SSO URL.

Organizations can have different authentication requirements. For example, one organization might enforce SAML SSO, while another organization might not enforce any specific login method. If your organization enforces a specific login method, then the user will need to use that method to log in, and might be prompted to re-authenticate. 