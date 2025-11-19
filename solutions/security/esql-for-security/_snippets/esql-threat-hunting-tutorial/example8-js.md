% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```js
const response = await client.indices.create({
  index: "user-context",
  mappings: {
    properties: {
      "user.name": {
        type: "keyword",
      },
      "user.role": {
        type: "keyword",
      },
      "user.department": {
        type: "keyword",
      },
      "user.privileged": {
        type: "boolean",
      },
    },
  },
  settings: {
    "index.mode": "lookup",
  },
});
console.log(response);
```
