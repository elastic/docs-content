% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```js
const response = await client.indices.create({
  index: "process-logs",
  mappings: {
    properties: {
      "@timestamp": {
        type: "date",
      },
      process: {
        properties: {
          name: {
            type: "keyword",
          },
          command_line: {
            type: "text",
          },
          parent: {
            properties: {
              name: {
                type: "keyword",
              },
            },
          },
        },
      },
      user: {
        properties: {
          name: {
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
