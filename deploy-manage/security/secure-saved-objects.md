---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/xpack-security-secure-saved-objects.html
applies_to:
  deployment:
    ece: ga
    eck: ga
    self: ga
products:
  - id: kibana
---

# Secure {{kib}} saved objects [xpack-security-secure-saved-objects]

{{kib}} stores entities such as dashboards, visualizations, alerts, actions, and advanced settings as saved objects, which are kept in a dedicated, internal {{es}} index. If such an object includes sensitive information, for example a PagerDuty integration key or email server credentials used by the alert action, {{kib}} encrypts it and makes sure it cannot be accidentally leaked or tampered with.

Encrypting sensitive information means that a malicious party with access to the {{kib}} internal indices won’t be able to extract that information without also knowing the encryption key.

Example [`kibana.yml`](/deploy-manage/stack-settings.md):

```yaml
xpack.encryptedSavedObjects:
  encryptionKey: "min-32-byte-long-strong-encryption-key"
```

::::{important}
If you don’t specify an encryption key, {{kib}} might disable features that rely on encrypted saved objects.

::::


::::{tip}
For help generating the encryption key, refer to the [`kibana-encryption-keys`](kibana://reference/commands/kibana-encryption-keys.md) script.

::::


## Encryption key rotation [encryption-key-rotation]

Many policies and best practices stipulate that encryption keys should be periodically rotated to decrease the amount of content encrypted with one key and therefore limit the potential damage if the key is compromised. {{kib}} allows you to rotate encryption keys whenever there is a need.

When you change an encryption key, be sure to keep the old one for some time. Although {{kib}} only uses a new encryption key to encrypt all new and updated data, it still may need the old one to decrypt data that was encrypted using the old key. It’s possible to have multiple old keys used only for decryption. {{kib}} doesn’t automatically re-encrypt existing saved objects with the new encryption key. Re-encryption only happens when you update existing object or use the [rotate encryption key API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-saved-objects).

Here is how your [`kibana.yml`](/deploy-manage/stack-settings.md) might look if you use key rotation functionality:

```yaml
xpack.encryptedSavedObjects:
  encryptionKey: "min-32-byte-long-NEW-encryption-key" <1>
  keyRotation:
    decryptionOnlyKeys: ["min-32-byte-long-OLD#1-encryption-key", "min-32-byte-long-OLD#2-encryption-key"] <2>
```

1. The encryption key {{kib}} will use to encrypt all new or updated saved objects. This is known as the primary encryption key.
2. A list of encryption keys {{kib}} will try to use to decrypt existing saved objects if decryption with the primary encryption key isn’t possible. These keys are known as the decryption-only or secondary encryption keys.


::::{note}
You might also leverage this functionality if multiple {{kib}} instances connected to the same {{es}} cluster use different encryption keys. In this case, you might have a mix of saved objects encrypted with different keys, and every {{kib}} instance can only deal with a specific subset of objects. To fix this, you must choose a single primary encryption key for `xpack.encryptedSavedObjects.encryptionKey`, move all other encryption keys to `xpack.encryptedSavedObjects.keyRotation.decryptionOnlyKeys`, and sync this configuration across all {{kib}} instances.

::::


At some point, you might want to dispose of old encryption keys completely. Make sure there are no saved objects that {{kib}} encrypted with these encryption keys. You can use the [rotate encryption key API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-saved-objects) to determine which existing saved objects require decryption-only keys and re-encrypt them with the primary key.


## Docker configuration [encryption-key-docker-configuration]

It’s also possible to configure the encryption keys using [Docker environment variables](../deploy/self-managed/install-kibana-with-docker.md#environment-variable-config).

Docker environment variable examples:

```sh
XPACK_ENCRYPTEDSAVEDOBJECTS_ENCRYPTIONKEY="min-32-byte-long-NEW-encryption-key"
XPACK_ENCRYPTEDSAVEDOBJECTS_KEYROTATION_DECRYPTIONONLYKEYS[0]="min-32-byte-long-OLD#1-encryption-key"
XPACK_ENCRYPTEDSAVEDOBJECTS_KEYROTATION_DECRYPTIONONLYKEYS[1]="min-32-byte-long-OLD#2-encryption-key"
```


