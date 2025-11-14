```js
const response = await client.indices.create({
  index: "threat-intel",
  mappings: {
    properties: {
      "indicator.value": {
        type: "keyword",
      },
      "indicator.type": {
        type: "keyword",
      },
      "threat.name": {
        type: "keyword",
      },
      "threat.severity": {
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
