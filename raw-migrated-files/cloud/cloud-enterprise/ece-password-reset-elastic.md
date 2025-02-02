# Reset the password for the `elastic` user [ece-password-reset-elastic]

You might need to reset the password for the `elastic` superuser if you cannot authenticate with the `elastic` user ID and are effectively locked out from a cluster.

To reset the password:

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From your deployment menu, select **Security**.
4. Select **Reset password**.
5. Copy down the auto-generated password for the `elastic` user.

The password is hashed after you leave this pane, so if you lose it, you need to reset the password again.

