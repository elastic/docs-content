---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/package-signatures.html
---

# Package signatures [package-signatures]

All integration packages published by Elastic have package signatures that prevent malicious attackers from tampering with package content. When you install an Elastic integration, {{kib}} downloads the package and verifies the package signature against a public key. If the package is unverified, you can choose to force install it. However, it’s strongly recommended that you avoid installing unverified packages.

::::{important}
By installing an unverified package, you acknowledge that you assume any risk involved.
::::


To force installation of an unverified package:

* When using the {{integrations}} UI, you’ll be prompted to confirm that you want to install the unverified integration. Click **Install anyway** to force installation.
* When using the {{fleet}} API, if you attempt to install an unverified package, you’ll see a 400 response code with a verification failed message. To force installation, set the URL parameter `ignoreUnverified=true`. For more information, refer to [{{kib}} {{fleet}} APIs](/reference/ingestion-tools/fleet/fleet-api-docs.md).

After installation, unverified {{integrations}} are flagged on the **Installed integrations** tab of the {{integrations}} UI.


## Why is package verification necessary? [why-verify-packages]

Integration packages contain instructions, such as ILM policies, transforms, and mappings, that can significantly modify the structure of your {{es}} indices. Relying solely on HTTPS DNS name validation to prove provenance of the package is not a safe practice. A determined attacker could forge a certificate and serve up packages intended to disrupt the target.

Installing verified packages ensures that your integration software has not been corrupted or otherwise tampered with.


## What does it mean for a package to be unverified? [what-does-unverified-mean]

Here are some situations where an integration package will fail verification during installation:

* The package zip file on the Elastic server has been tampered with.
* The user has been maliciously redirected to a fake Elastic package registry.
* The public Elastic key has been compromised, and Elastic has signed packages with an updated key.

Here are some reasons why an integration might be flagged as unverified after installation:

* The integration package failed verification, but was force installed.
* The integration package was installed before {{fleet}} added support for package signature verification.


## What if the Elastic key changes in the future? [what-if-key-changes]

In the unlikely event that the Elastic signing key changes in the future, any verified integration packages will continue to show as verified until new packages are installed or existing ones are upgraded. If this happens, you can set the `xpack.fleet.packageVerification.gpgKeyPath` setting in the `kibana.yml` configuration file to use the new key.
