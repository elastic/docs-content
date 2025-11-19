% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```js
const response = await client.indices.create({
  index: "asset-inventory",
  mappings: {
    properties: {
      "host.name": {
        type: "keyword",
      },
      "asset.criticality": {
        type: "keyword",
      },
      "asset.owner": {
        type: "keyword",
      },
      "asset.department": {
        type: "keyword",
      },
    },
  },
  settings: {
    "index.mode": "lookup",
  },
});
console.log(response);
```
