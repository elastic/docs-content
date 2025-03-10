---
navigation_title: Watcher
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-troubleshooting.html
---

# Troubleshoot Watcher [watcher-troubleshooting]


## Dynamic mapping error when trying to add a watch [_dynamic_mapping_error_when_trying_to_add_a_watch] 

If you get the *Dynamic Mapping is Disabled* error when you try to add a watch, verify that the index mappings for the `.watches` index are available. You can do that by submitting the following request:

```console
GET .watches/_mapping
```
%  TEST[skip:deprecation warning]

If the index mappings are missing, follow these steps to restore the correct mappings:

1. Stop the Elasticsearch node.
2. Add `xpack.watcher.index.rest.direct_access : true` to `elasticsearch.yml`.
3. Restart the Elasticsearch node.
4. Delete the `.watches` index:

    ```console
    DELETE .watches
    ```
    %  TEST[skip:index deletion and deprecation warning]

5. Disable direct access to the `.watches` index:

    1. Stop the Elasticsearch node.
    2. Remove `xpack.watcher.index.rest.direct_access : true` from `elasticsearch.yml`.
    3. Restart the Elasticsearch node.



## Unable to send email [_unable_to_send_email] 

If you get an authentication error indicating that you need to continue the sign-in process from a web browser when Watcher attempts to send email, you need to configure Gmail to [Allow Less Secure Apps to access your account](https://support.google.com/accounts/answer/6010255?hl=en).

If you have two-step verification enabled for your email account, you must generate and use an App Specific password to send email from {{watcher}}. For more information, see:

* Gmail: [Sign in using App Passwords](https://support.google.com/accounts/answer/185833?hl=en)
* Outlook.com: [App passwords and two-step verification](http://windows.microsoft.com/en-us/windows/app-passwords-two-step-verification)


## {{watcher}} not responsive [_watcher_not_responsive] 

Keep in mind that there’s no built-in validation of scripts that you add to a watch. Buggy or deliberately malicious scripts can negatively impact {{watcher}} performance. For example, if you add multiple watches with buggy script conditions in a short period of time, {{watcher}} might be temporarily unable to process watches until the bad watches time out.

