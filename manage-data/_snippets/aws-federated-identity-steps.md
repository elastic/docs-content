- To create a new identity, on the **New Identity** tab:
  1. Enter a **Federated Identity Name**.
  2. Select **Launch CloudFormation**. The {{aws}} CloudFormation console opens with the stack parameters filled in. You can also expand **Steps to assume role** in {{kib}} for the same instructions.
  3. Sign in as an administrator to the {{aws}} account you want to onboard. Optionally, change the region you want to deploy the stack to.
  4. Enter a **Stack name**. Don't change the parameters that {{kib}} filled in.
  5. Select the checkbox for **I acknowledge that AWS CloudFormation might create IAM resources with custom names**, then select **Create stack**.
  6. When the stack status is `CREATE_COMPLETE`, open the **Outputs** tab.
  7. In {{kib}}, paste the `RoleArn` output value into **Role ARN**. Optionally, paste the `StackId` output value into **CloudFormation stack ARN** so {{kib}} can link directly to the stack.
  8. Select **Create Identity**.
- To reuse an identity, select the **Existing Identity** tab, then select the identity from the **Federated Identity Name** list. If the identity doesn't have the permissions the integrations you're setting up need, update its stack as described in [Update a federated identity's stack](/manage-data/ingest/managed-integrations/cloud-connector-deployment.md#federated-identity-aws-update).
