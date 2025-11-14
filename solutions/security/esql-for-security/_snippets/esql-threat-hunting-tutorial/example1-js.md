```js
const { Client } = require("@elastic/elasticsearch");

const client = new Client({
  nodes: [process.env["ELASTICSEARCH_URL"]],
  auth: {
    apiKey: process.env["ELASTIC_API_KEY"],
  },
});

async function run() {
  const response = await client.indices.create({
    index: "windows-security-logs",
    mappings: {
      properties: {
        "@timestamp": {
          type: "date",
        },
        event: {
          properties: {
            code: {
              type: "keyword",
            },
            action: {
              type: "keyword",
            },
          },
        },
        user: {
          properties: {
            name: {
              type: "keyword",
            },
            domain: {
              type: "keyword",
            },
          },
        },
        host: {
          properties: {
            name: {
              type: "keyword",
            },
            ip: {
              type: "ip",
            },
          },
        },
        source: {
          properties: {
            ip: {
              type: "ip",
            },
          },
        },
        logon: {
          properties: {
            type: {
              type: "keyword",
            },
          },
        },
      },
    },
  });
  console.log(response);
}

run();
```
