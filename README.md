## Azure Token Helper

1. `docker build -t azure-token-helper ./docker`
2. `docker volume create azure-token-helper-data`
2. `docker run -d -p 9999:9999 --name azure-token-helper --restart unless-stopped -v azure-token-helper-data:/root/.azure azure-token-helper`
3. `docker exec -it azure-token-helper az login --use-device-code`

Token endpoint is now available at http://localhost:9999/token
Bruno will call it automatically via the collection pre-request script.


## Bruno Collections

A starter collection is provided in the `Bruno/Collections` directory.

### Azure

Create a new environment file for the collection.
```yaml
name: Azure
variables:
  - name: AZURE_SUBSCRIPTION
    value: "{{azure_subscription}}"
  - name: AZURE_LOCATION
    value: "{{azure_location}}"
```

### Pre-request Collection Script

```javascript
const existingToken = bru.getVar("azure_token");
const expiresAt = bru.getVar("azure_token_expires_at");
const now = Date.now();

// Only fetch if missing or expired (with 60s buffer)
if (!existingToken || !expiresAt || now >= (parseInt(expiresAt) - 60000)) {
    const res = await axios.get("http://localhost:9999/token");
    bru.setVar("azure_token", res.data.token);
    bru.setVar("azure_token_expires_at", String(now + 3000000)); // 50 mins
}
```