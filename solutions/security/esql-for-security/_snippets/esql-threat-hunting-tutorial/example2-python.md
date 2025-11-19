% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```python
resp = client.bulk(
    refresh="wait_for",
    operations=[
        {
            "index": {
                "_index": "windows-security-logs"
            }
        },
        {
            "@timestamp": "2025-05-20T08:15:00Z",
            "event": {
                "code": "4625",
                "action": "logon_failed"
            },
            "user": {
                "name": "jsmith",
                "domain": "corp"
            },
            "host": {
                "name": "WS-001",
                "ip": "10.1.1.50"
            },
            "source": {
                "ip": "10.1.1.100"
            }
        },
        {
            "index": {
                "_index": "windows-security-logs"
            }
        },
        {
            "@timestamp": "2025-05-20T08:17:00Z",
            "event": {
                "code": "4624",
                "action": "logon_success"
            },
            "user": {
                "name": "jsmith",
                "domain": "corp"
            },
            "host": {
                "name": "WS-001",
                "ip": "10.1.1.50"
            },
            "source": {
                "ip": "10.1.1.100"
            },
            "logon": {
                "type": "3"
            }
        },
        {
            "index": {
                "_index": "windows-security-logs"
            }
        },
        {
            "@timestamp": "2025-05-20T09:30:00Z",
            "event": {
                "code": "4624",
                "action": "logon_success"
            },
            "user": {
                "name": "jsmith",
                "domain": "corp"
            },
            "host": {
                "name": "SRV-001",
                "ip": "10.1.2.10"
            },
            "source": {
                "ip": "10.1.1.50"
            },
            "logon": {
                "type": "3"
            }
        },
        {
            "index": {
                "_index": "windows-security-logs"
            }
        },
        {
            "@timestamp": "2025-05-20T10:45:00Z",
            "event": {
                "code": "4624",
                "action": "logon_success"
            },
            "user": {
                "name": "jsmith",
                "domain": "corp"
            },
            "host": {
                "name": "DB-001",
                "ip": "10.1.3.5"
            },
            "source": {
                "ip": "10.1.2.10"
            },
            "logon": {
                "type": "3"
            }
        },
        {
            "index": {
                "_index": "windows-security-logs"
            }
        },
        {
            "@timestamp": "2025-05-20T02:30:00Z",
            "event": {
                "code": "4624",
                "action": "logon_success"
            },
            "user": {
                "name": "admin",
                "domain": "corp"
            },
            "host": {
                "name": "DC-001",
                "ip": "10.1.4.10"
            },
            "source": {
                "ip": "10.1.3.5"
            },
            "logon": {
                "type": "3"
            }
        }
    ],
)
print(resp)

```
