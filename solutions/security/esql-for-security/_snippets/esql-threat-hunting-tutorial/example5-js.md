```js
const response = await client.indices.create({
  index: "network-logs",
  mappings: {
    properties: {
      "@timestamp": {
        type: "date",
      },
      source: {
        properties: {
          ip: {
            type: "ip",
          },
          port: {
            type: "integer",
          },
        },
      },
      destination: {
        properties: {
          ip: {
            type: "ip",
          },
          port: {
            type: "integer",
          },
        },
      },
      network: {
        properties: {
          bytes: {
            type: "long",
          },
          protocol: {
            type: "keyword",
          },
        },
      },
      host: {
        properties: {
          name: {
            type: "keyword",
          },
        },
      },
    },
  },
});
console.log(response);
```
