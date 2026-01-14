% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```python
resp = client.bulk(
    refresh="wait_for",
    operations=[
        {
            "index": {
                "_index": "process-logs"
            }
        },
        {
            "@timestamp": "2025-05-20T08:20:00Z",
            "process": {
                "name": "powershell.exe",
                "command_line": "powershell.exe -enc JABzAD0ATgBlAHcALgBPAGIAagBlAGMAdAAgAFMAeQBzAHQAZQBtAC4ATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAA=",
                "parent": {
                    "name": "winword.exe"
                }
            },
            "user": {
                "name": "jsmith"
            },
            "host": {
                "name": "WS-001"
            }
        },
        {
            "index": {
                "_index": "process-logs"
            }
        },
        {
            "@timestamp": "2025-05-20T09:35:00Z",
            "process": {
                "name": "net.exe",
                "command_line": "net user /domain",
                "parent": {
                    "name": "cmd.exe"
                }
            },
            "user": {
                "name": "jsmith"
            },
            "host": {
                "name": "SRV-001"
            }
        },
        {
            "index": {
                "_index": "process-logs"
            }
        },
        {
            "@timestamp": "2025-05-20T10:50:00Z",
            "process": {
                "name": "sqlcmd.exe",
                "command_line": "sqlcmd -S localhost -Q \"SELECT * FROM customers\"",
                "parent": {
                    "name": "powershell.exe"
                }
            },
            "user": {
                "name": "jsmith"
            },
            "host": {
                "name": "DB-001"
            }
        },
        {
            "index": {
                "_index": "process-logs"
            }
        },
        {
            "@timestamp": "2025-05-20T02:35:00Z",
            "process": {
                "name": "ntdsutil.exe",
                "command_line": "ntdsutil \"ac i ntds\" \"ifm\" \"create full c:\temp\ntds\"",
                "parent": {
                    "name": "cmd.exe"
                }
            },
            "user": {
                "name": "admin"
            },
            "host": {
                "name": "DC-001"
            }
        },
        {
            "index": {
                "_index": "process-logs"
            }
        },
        {
            "@timestamp": "2025-05-20T12:15:00Z",
            "process": {
                "name": "schtasks.exe",
                "command_line": "schtasks.exe /create /tn UpdateCheck /tr c:\windows\temp\update.exe /sc daily",
                "parent": {
                    "name": "cmd.exe"
                }
            },
            "user": {
                "name": "jsmith"
            },
            "host": {
                "name": "WS-001"
            }
        },
        {
            "index": {
                "_index": "process-logs"
            }
        },
        {
            "@timestamp": "2025-05-20T12:30:00Z",
            "process": {
                "name": "schtasks.exe",
                "command_line": "schtasks.exe /create /tn SystemManager /tr powershell.exe -enc ZQBjAGgAbwAgACIASABlAGwAbABvACIA /sc minute /mo 5",
                "parent": {
                    "name": "powershell.exe"
                }
            },
            "user": {
                "name": "jsmith"
            },
            "host": {
                "name": "SRV-001"
            }
        },
        {
            "index": {
                "_index": "process-logs"
            }
        },
        {
            "@timestamp": "2025-05-20T13:15:00Z",
            "process": {
                "name": "sc.exe",
                "command_line": "sc.exe create RemoteService binPath= c:\windows\temp\remote.exe",
                "parent": {
                    "name": "cmd.exe"
                }
            },
            "user": {
                "name": "jsmith"
            },
            "host": {
                "name": "DB-001"
            }
        },
        {
            "index": {
                "_index": "process-logs"
            }
        },
        {
            "@timestamp": "2025-05-20T13:20:00Z",
            "process": {
                "name": "sc.exe",
                "command_line": "sc.exe create BackdoorService binPath= c:\programdata\svc.exe",
                "parent": {
                    "name": "powershell.exe"
                }
            },
            "user": {
                "name": "jsmith"
            },
            "host": {
                "name": "SRV-001"
            }
        },
        {
            "index": {
                "_index": "process-logs"
            }
        },
        {
            "@timestamp": "2025-05-20T13:25:00Z",
            "process": {
                "name": "sc.exe",
                "command_line": "sc.exe create PersistenceService binPath= c:\windows\system32\malicious.exe",
                "parent": {
                    "name": "cmd.exe"
                }
            },
            "user": {
                "name": "admin"
            },
            "host": {
                "name": "DC-001"
            }
        }
    ],
)
print(resp)

```
