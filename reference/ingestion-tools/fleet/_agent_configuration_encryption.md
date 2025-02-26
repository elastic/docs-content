---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/_elastic_agent_configuration_encryption.html
---

# {{agent}} configuration encryption [_agent_configuration_encryption]

It is important for you to understand the {{agent}} security model and how it handles sensitive values in integration configurations. At a high level, {{agent}} receives configuration data from {{fleet-server}} over an encrypted connection and persists the encrypted configuration on disk. This persistence allows agents to continue to operate even if they are unable to connect to the {{fleet-server}}.

The entire Fleet Agent Policy is encrypted at rest, but is recoverable if you have access to both the encrypted configuration data and the associated key. The key material is stored in an OS-dependent manner as described in the following sections.


## Darwin (macOS) [_darwin_macos]

Key material is stored in the system keychain. The value is stored as is without any additional transformations.


## Windows [_windows]

Configuration data is encrypted with [DPAPI](https://learn.microsoft.com/en-us/dotnet/standard/security/how-to-use-data-protection) `CryptProtectData` with `CRYPTPROTECT_LOCAL_MACHINE``. Additional entropy is derived from crypto/rand bytes stored in the `.seed` file. Configuration data is stored as separate files, where the name of the file is a SHA256 hash of the key, and the content of the file is encrypted with DPAPI data. The security of key data relies on file system permissions. Only the Administrator should be able to access the file.


## Linux [_linux]

The encryption key is derived from crypto/rand bytes stored in the `.seed` file after PBKDF2 transformation. Configuration data is stored as separate files, where the name of the file is a SHA256 hash of the key, and the content of the file is AES256-GSM encrypted. The security of the key material largely relies on file system permissions.

